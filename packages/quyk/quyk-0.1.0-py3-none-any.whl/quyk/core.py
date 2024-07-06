import sys
import os
import ast
import shutil
import logging
import inquirer
from halo import Halo
from .cli_test import registered_functions

logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)

def get_data_dir():
    xdg_data_home = os.getenv('XDG_DATA_HOME', os.path.join(os.path.expanduser("~"), '.local', 'share'))
    data_dir = os.path.join(xdg_data_home, 'quyk')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def get_test_script_dir(dir_path):
    data_dir = get_data_dir()
    script_dir = os.path.join(data_dir, os.path.basename(os.path.abspath(dir_path)))
    os.makedirs(script_dir, exist_ok=True)
    return script_dir

def extract_decorated_functions(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read(), filename=file_path)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id == 'cli_test':
                    test_args = None
                    for keyword in decorator.keywords:
                        if keyword.arg == 'test_args':
                            if isinstance(keyword.value, ast.List):
                                test_args = [ast.literal_eval(elt) if isinstance(elt, ast.Constant) else elt for elt in keyword.value.elts]
                            elif isinstance(keyword.value, ast.Tuple):
                                test_args = tuple(ast.literal_eval(elt) if isinstance(elt, ast.Constant) else elt for elt in keyword.value.elts)
                            else:
                                test_args = ast.literal_eval(keyword.value)
                    is_async = isinstance(node, ast.AsyncFunctionDef)
                    functions.append((node.name, test_args, is_async))
    return functions

def get_module_path(base_dir, file_path):
    rel_path = os.path.relpath(file_path, base_dir)
    module_path = os.path.splitext(rel_path)[0].replace(os.path.sep, '.')
    return module_path

def scan_directory(dir_path):
    global registered_functions
    old_registered_functions = set(registered_functions.keys())
    registered_functions.clear()
    excluded_dirs = {'build', 'dist', '__pycache__'}
    base_dir = os.path.abspath(dir_path)
    sys.path.insert(0, base_dir)
    
    spinner = Halo(text='Scanning directory', spinner='dots')
    spinner.start()
    
    try:
        files_to_scan = [
            os.path.join(root, file)
            for root, dirs, files in os.walk(base_dir)
            for file in files
            if file.endswith(".py") and not any(d in root.split(os.sep) for d in excluded_dirs)
        ]
        
        for file_path in files_to_scan:
            spinner.text = f"Checking: {os.path.basename(file_path)}"
            functions = extract_decorated_functions(file_path)
            for func_name, test_args, is_async in functions:
                registered_functions[func_name] = (file_path, test_args, is_async)
        
        spinner.succeed(f"Found {len(registered_functions)} decorated functions")
    except Exception as e:
        spinner.fail(str(e))
        return
    finally:
        spinner.stop()
    
    script_dir = get_test_script_dir(dir_path)
    
    # Remove old test files
    for func_name in old_registered_functions:
        if func_name not in registered_functions:
            old_script_path = os.path.join(script_dir, f"quyk_test_{func_name}.py")
            if os.path.exists(old_script_path):
                os.remove(old_script_path)
                logger.info(f"Removed old test script: {old_script_path}")
    
    # Create new test files
    for func_name, (file_path, test_args, is_async) in registered_functions.items():
        script_path = os.path.join(script_dir, f"quyk_test_{func_name}.py")
        module_path = get_module_path(base_dir, file_path)
        with open(script_path, 'w') as f:
            f.write(f"import asyncio\n")
            f.write(f"from {module_path} import {func_name}\n\n")
            if is_async:
                f.write("async def main():\n")
                f.write(f"    await {func_name}(*{test_args})\n\n")
                f.write("asyncio.run(main())\n")
            else:
                f.write(f"{func_name}(*{test_args})\n")
        logger.info(f"Created/Updated test script: {script_path}")

def test_function(func_name):
    script_dir = get_test_script_dir(".")
    script_path = os.path.join(script_dir, f"quyk_test_{func_name}.py")
    if not os.path.exists(script_path):
        logger.error(f"Test script for function {func_name} not found. Run `quyk scan` first.")
        return
    # Create a temporary copy of the test script in the same directory as the original function
    with open(script_path, 'r') as src_file:
        content = src_file.read()
    temp_script_path = f".temp.{os.path.basename(script_path)}"
    with open(temp_script_path, 'w') as temp_file:
        temp_file.write(content)
    try:
        logger.info(f"Running test for {func_name}")
        os.system(f"python {temp_script_path}")
    finally:
        os.remove(temp_script_path)

def list_registered_functions():
    script_dir = get_test_script_dir(".")
    if not os.path.exists(script_dir) or not os.listdir(script_dir):
        logger.error("No functions registered. Run `quyk scan` first.")
        return
    logger.info("Registered functions:")
    for file in os.listdir(script_dir):
        if file.startswith("quyk_test_") and file.endswith(".py"):
            func_name = file[len("quyk_test_"):-len(".py")]
            logger.info(f" - {func_name}")

def export_tests(export_dir=None):
    if export_dir is None:
        export_dir = os.path.join(os.getcwd(), 'quyk_tests')
    os.makedirs(export_dir, exist_ok=True)
    
    script_dir = get_test_script_dir(".")
    if not os.path.exists(script_dir):
        logger.error("No test scripts found. Run 'quyk scan' first.")
        return
    
    files_to_export = [
        f for f in os.listdir(script_dir)
        if f.startswith("quyk_test_") and f.endswith(".py")
    ]
    
    spinner = Halo(text='Exporting tests', spinner='dots')
    spinner.start()
    
    try:
        for file in files_to_export:
            spinner.text = f"Exporting: {file}"
            shutil.copy2(os.path.join(script_dir, file), export_dir)
        spinner.succeed(f"Test files exported to {export_dir}")
    except Exception as e:
        spinner.fail(str(e))
    finally:
        spinner.stop()

def main():
    if len(sys.argv) < 2:
        print("Usage: quyk <command> [args]")
        print("Commands:")
        print("  scan [directory]  Scan for decorated functions and update test scripts")
        print("  test [function]   Run tests for all or a specific function")
        print("  export [directory] Export test scripts to a directory")
        return
    command = sys.argv[1]
    if command == "scan":
        dir_path = sys.argv[2] if len(sys.argv) > 2 else "."
        scan_directory(os.path.abspath(dir_path))
    elif command == "test":
        if len(sys.argv) > 2:
            func_name = sys.argv[2]
            test_function(func_name)
        else:
            script_dir = get_test_script_dir(".")
            choices = [f[len("quyk_test_"):-len(".py")] for f in os.listdir(script_dir) 
                       if f.startswith("quyk_test_") and f.endswith(".py")]
            if not choices:
                logger.error("No registered functions found. Run 'quyk scan' first.")
                return
            questions = [
                inquirer.List('function',
                              message="Select a function to test",
                              choices=choices,
                              ),
            ]
            answers = inquirer.prompt(questions)
            if answers:
                test_function(answers['function'])
    elif command == "export":
        export_dir = sys.argv[2] if len(sys.argv) > 2 else None
        export_tests(export_dir)
    else:
        logger.error(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
