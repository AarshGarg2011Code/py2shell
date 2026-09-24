import ast
import os
from .base import base
class transpiler(base):
    def __init__(self, map_path: str = "command_map.json"): super().__init__(map_path=map_path)
    def transpile_code(self, py_code: str) -> str:
        self.reset()
        tree = ast.parse(py_code)
        self.visit(tree)
        header = [
            "#!/usr/bin/env bash",
            "# py2shell v0.1.0",
            "",
        ]
        return "\n".join(header + self.output_lines)
    def transpile_file(self, input_filepath: str, output_filepath: str = None) -> str:
        if not os.path.exists(input_filepath): raise FileNotFoundError(f"Source file not found: {input_filepath}")
        with open(input_filepath, "r", encoding="utf-8") as f: py_code = f.read()
        bash_script = self.transpile_code(py_code)
        if output_filepath:
            with open(output_filepath, "w", encoding="utf-8") as f: f.write(bash_script)
            os.chmod(output_filepath, 0o755)
        return bash_script
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            args = []
            for arg in node.args:
                val = self._eval_node_val(arg)
                if val: args.append(val)
            for kw in node.keywords:
                val = self._eval_node_val(kw.value)
                if kw.arg in ["human_readable", "h"] and val == "true": args.append("-h")
                elif kw.arg in ["long_format", "l"] and val == "true": args.append("-l")
                elif kw.arg in ["show_hidden", "a"] and val == "true": args.append("-a")
                elif kw.arg in ["recursive", "r"] and val == "true": args.append("-r")
                elif kw.arg in ["count", "c"]: args.extend(["-c", val])
                elif kw.arg in ["lines", "n"]: args.extend(["-n", val])
                elif kw.arg in ["unit", "u"]: args.extend(["-u", val])
                elif kw.arg in ["output", "o"]: args.extend(["-O", val])
                else: args.extend([f"--{kw.arg}", val])
            full_cmd = f"{func_name} {' '.join(args)}".strip()
            self.output_lines.append(full_cmd)
