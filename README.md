# py2shell

Transpile Python code into native shell statements and run an interactive Python-driven shell.
py2shell is a Python-to-Bash transpiler and interactive REPL designed to bridge high-level Python syntax with native shell executions.
Write operations in Python-like function calls or raw scripts, and let py2shell compile and execute them down to shell statements.

## Features:

Interactive REPL (py2shell): A live terminal session that dynamically transpiles Python expressions to subshell commands or executes built-in system abstractions.
Python CLI Launcher: Support for running as an executable (py2shell) or directly as a Python module (python -m py2shell).
AST-Based Transpilation: Parses Python code via ast to generate safe, chained Bash statements.
Environment & Path State Syncing: Maintains shell environment variables (ENV) and working directory (PWD) updates across execution blocks.
Built-in System Utilities: Cross-platform abstractions for file and process operations like mkdir, rm, cp, mv, chmod, df, ps, and tar.

### Installation: Install py2shell directly from PyPI:pip install py2shell

### Quick Start:

1. Interactive Terminal (REPL): Launch the interactive REPL using: `python -m py2shell` or just `py2shell`
Inside the interactive terminal:
py2shell /your/current/dir>>> mkdir('my_folder')
2. Using Programmatically
You can also import Py2Shell Base or Terminal into your own Python projects: from py2shell import terminal

Instantiate transpiler engine

term = terminal(shell_bin="/bin/bash")

### Transpile a single Python line into chained Bash output, using:

python -m py2shell your_script.py -o bash_script.sh

## Project Structure

py2shell/
├── command_map.json      # Mapping definitions between Python calls & shell commands
├── pyproject.toml        # Build system metadata & dependencies
├── README.md             # Documentation
└── py2shell/
├── **init**.py       # Package initialization
├── **main**.py       # Module entry point (python -m py2shell)
├── base.py           # Core AST parser and built-in command handlers
├── cli.py            # CLI entry point logic
├── terminal.py       # Live Interactive REPL engine
└── transpiler.py     # Subshell execution pipeline

## How It Works:

AST Parsing: When Python code is supplied, py2shell parses the string into an Abstract Syntax Tree using Python's native ast module.
Command Resolution: Built-in methods defined in Commands are executed natively inside Python's process.Non-native or mapped commands are converted into equivalent Bash command flags.
Subshell Execution and State Syncing: Shell statements execute through a subshell process. Upon completion, updated environment variables and path states (PWD) are synced back to the parent REPL.
Built-In Commands: py2shell includes built-in wrappers for common system tools.

## License

This project is licensed under the MIT License.

