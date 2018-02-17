# intelligent Tutoring System (iTS)

[![Build Status](https://travis-ci.org/pallavagarwal07/iTS.svg?branch=master)](https://travis-ci.org/pallavagarwal07/iTS)

## Installation :

First do a shallow clone of the repository :
```
git clone --depth 1 http://www.github.com/pallavagarwal07/iTS
```
If you want the executable to run from any directory (recommended) put a symlink to the executable in your path.

```
cd /usr/local/bin
sudo ln -s <PATH TO CLONED DIR>/its its
```

## Usage :

The executable **its** is run to start the program.

The following Flags are supported:

```
-i Specify the input file (default is stdin)
-o Specify the output file (default is stderr)
-c Specify the file with the code to be run (Default is assets/code.c)
-v Verbosity level (verbosity level is compounded)
-vv
-vvv
```

## Test Suite:
In case you feel that something is wrong with the program, or if it not working,
run the test_suite in its directory.
