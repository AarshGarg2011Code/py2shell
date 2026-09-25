# py2shell

##### Transpile Python code into native shell statements and run an interactive Python-driven shell.
##### py2shell is a Python-to-Bash transpiler and interactive REPL designed to bridge high-level Python syntax with native shell executions.
##### Write operations in Python-like function calls or raw scripts, and let py2shell compile and execute them down to shell statements.

## Features:

##### Interactive REPL (py2shell): A live terminal session that dynamically transpiles Python expressions to subshell commands or executes built-in system abstractions.
##### Python CLI Launcher: Support for running as an executable (py2shell) or directly as a Python module (python -m py2shell).
##### AST-Based Transpilation: Parses Python code via ast to generate safe, chained Bash statements.
##### Environment & Path State Syncing: Maintains shell environment variables (ENV) and working directory (PWD) updates across execution blocks.
##### Built-in System Utilities: Cross-platform abstractions for file and process operations like mkdir, rm, cp, mv, chmod, df, ps, and tar.

### Installation: Install py2shell directly from PyPI: pip install py2shell

### Quick Start:

##### 1. Interactive Terminal (REPL): Launch the interactive REPL using:    `python -m py2shell` or just `py2shell`
##### Inside the interactive terminal:
##### py2shell /your/current/dir>>> mkdir('my_folder')
##### 2. Using Programmatically
##### You can also import Py2Shell Base or Terminal into your own Python projects: from py2shell import terminal
##### Instantiate terminal engine
##### term = terminal(shell_bin="/bin/bash")

### Transpile a single Python line into chained Bash output, using:
##### python -m py2shell your_script.py -o bash_script.sh
#### or
##### py2shell your_script.py -o bash_script.sh

## Project Structure

##### py2shell/
##### ├── command_map.json      # Mapping definitions between Python calls & shell commands
##### ├── pyproject.toml        # Build system metadata & dependencies
##### ├── README.md             # Documentation
##### └── py2shell/
##### ───────├── **init**.py       # Package initialization
##### ───────├── **main**.py       # Module entry point (python -m py2shell)
##### ───────├── base.py           # Core AST parser and built-in command handlers
##### ───────├── cli.py            # CLI entry point logic
##### ───────├── terminal.py       # Live Interactive REPL engine
##### ───────└── transpiler.py     # Subshell execution pipeline

## How It Works:

##### AST Parsing: When Python code is supplied, py2shell parses the string into an Abstract Syntax Tree using Python's native ast module.
##### Command Resolution: Built-in methods defined in Commands are executed natively inside Python's process.Non-native or mapped commands are converted into equivalent Bash command flags.
##### Subshell Execution and State Syncing: Shell statements execute through a subshell process. Upon completion, updated environment variables and path states (PWD) are synced back to the parent REPL.
##### Built-In Commands: py2shell includes built-in wrappers for common system tools.

## Making valid Py2Shell scripts
### It is important to note that (as of v0.1.0) Py2Shell Transpiler can only work flawlessly if the python file to be transpiled, is written according to Py2Shell rules.
#### These rules include:
##### 1. Keeping the syntax Python-Based in the `.py` script.
##### 2. Not using standard Python built-in functions, and instead, writing Bash standard functions in Python syntax.
###### This basically means, that instead of `print()`, there will be `echo()`. Python standard functions won't get transpiled properly.
##### 3. Not trying to test Py2Shell `.py` files using Python.
###### Do not run the `.py` files meant for Py2Shell transpilation, in Python. Otherwise, it WILL result in long tracebacks of undefined functions.
##### 4. Being aware of what you program in the Py2Shell scripts.
###### Carelessly writing Py2Shell code may result in unwanted commands getting run after transpilation. So be careful or else the bash script will go haywire. Do not use `sudo()` a lot of the time, excessive `sudo` commands are already harmful, and some 'accidental' `sudo` commands can damage your Linux/WSL
##### 5. Knowing that v0.1.0 is the first version of Py2Shell and doesn't have many features *yet*.
###### There are many things missing in Py2Shell v0.1.0, like control flow and pipeline features in transpiler. These features will be added in later versions. So, for the time being until Py2Shell v0.1.x comes out and give newer features, try not to use conditionals, assignments, loops, and all that in the Py2Shell scripts. For v0.1.0, stick to raw functions executions only.
##### 6. Py2Shell is open source. You can take reference of the source files to learn how to use Py2Shell like a pro. You can also have copies of the sources, and make Py2Shell distros of your own.
##### 7. Take reference of the test scripts provided in this GitHub repo.
##### 8. Apart from using the Py2Shell Transpiler, you can also import Py2Shell modules in your Python scripts.
#### For any queries, email me at *aarshg.13@gmail.com*
#### Also, view `command_map.json` to see in-built py2shell functions which definetely wont error on transpilation, unless you use them wrong. All other bash commands you want to write in py2shell python scripts, are to be written on your own (as of v0.1.0).
## License

This project is licensed under the MIT License.

#### Warning - Py2Shell v0.1.0 has only been tested on ArchLinux. For BEST performance and to make all commands work, use Py2Shell in ArchLinux/ArchLinuxWSL

