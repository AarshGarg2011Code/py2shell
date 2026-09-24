import ast
import os
import subprocess
import sys
import json
from .base import commands, base


class terminal(base):
    def __init__(self, shell_bin: str = "/bin/bash", map_path: str = "command_map.json"):
        super().__init__(map_path=map_path)
        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f: self.command_map = json.load(f)
        self.shell_bin = shell_bin
        self.env_state = os.environ.copy()
        self.commands = commands()
    def transpile_single(self, py_line: str) -> str:
        self.reset()
        tree = ast.parse(py_line)
        self.visit(tree)
        return " && ".join(self.output_lines) if self.output_lines else ":"
    def start_repl(self):
        print("py2shell terminal")
        print("type python code or commands like cd('..'), ls('.') to run")
        print("type 'exit' or 'quit' to close\n")
        while True:
            try:
                current_dir = os.getcwd()
                prompt_str = f"py2shell {current_dir}>>> "
                user_input = input(prompt_str)
                if user_input.strip() in ("exit", "quit"): break
                if user_input.strip() == "cmdlist": print(self.command_map)
                if not user_input.strip(): continue
                tree = ast.parse(user_input)
                executed_locally = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        func_name = node.func.id
                        if hasattr(self.commands, func_name):
                            method = getattr(self.commands, func_name)
                            args = [self._eval_node_val(arg).strip('"') for arg in node.args]
                            method(*args)
                            executed_locally = True
                            break
                if not executed_locally:
                    bash_cmd = self.transpile_single(user_input)
                    print(f"  [bash]  {bash_cmd}")
                    self._run_bash(bash_cmd)
            except KeyboardInterrupt:
                print("\nKeyboardInterrupt")
                break
            except Exception as e: print(f"Error: {e}", file=sys.stderr)

    def _run_bash(self, bash_cmd: str):
        proc = subprocess.run(
            [self.shell_bin, "-c", f"{bash_cmd} && env"],
            capture_output=True,
            text=True,
            env=self.env_state,
        )
        if proc.stdout:
            output_lines = proc.stdout.splitlines()
            env_vars = {}
            cmd_output = []
            for line in output_lines:
                if "=" in line and not line.startswith(" "):
                    k, v = line.split("=", 1)
                    env_vars[k] = v
                else: cmd_output.append(line)
            if cmd_output: print("\n".join(cmd_output))
            self.env_state.update(env_vars)
            if "PWD" in env_vars and os.path.exists(env_vars["PWD"]): os.chdir(env_vars["PWD"])
        if proc.stderr: print(f"Shell error: {proc.stderr.strip()}", file=sys.stderr)
