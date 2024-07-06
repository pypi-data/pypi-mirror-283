# quyk

An uncomplicated tool to test decorated functions directly from your terminal.

## Installation

Install quyk into you project directory.
```sh
pip install quyk
```
or
```sh
poetry add quyk
```

## Usage
Import one decorator and apply it to any functions you want to test from the command line:
```python
from quyk import cli_test

@cli_test(test_args=("foo", "bar"))
def stitch_together(*args):
	return f"stitched {'-'.join(args)}"
# ...
```

Scan all `.py` files in your project for decorated functions:
```sh
$ quyk scan							# default to entire current directory
> ⠙ Scanning directory
> ✔ Found 4 decorated functions 
```
... or hone into a specific folder:
```sh
$ quyk scan ./tricky_feature		# optionally provide [dir_path]
> ⠙ Scanning directory
> ✔ Found 2 decorated functions 
```

Interactively run your scanned tests:
```sh
$ quyk test							# use Arrows, Enter, and Escape to pick a test 
> [?] Select a function to test: 
   > stitch_together
     do_something
     do_something_else
> stitch_together: stitched foo-bar
```
... or directly test a specific function
```sh
$ quyk test do_something			# optionally provide [func_name]
> do_something: This thing!
```

Or export the runnable test files and edit them to your liking:
```sh
$ quyk export						# optionally pass [dir_path] to place test files there
> ⠋ Exporting tests
> ✔ Test files exported to /path/to/project/quyk_tests
```

----
#### That's it!