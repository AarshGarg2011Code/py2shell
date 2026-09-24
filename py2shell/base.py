import ast
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import platform
from pathlib import Path
from typing import Optional, Union, List
class commands:
    @staticmethod
    def cd(path: str = "~"):
        target = Path(path).expanduser()
        try:
            os.chdir(target)
            print(f"Directory changed to: {os.getcwd()}")
        except FileNotFoundError: print(f"cd: no such file or directory: {path}", file=sys.stderr)
    @staticmethod
    def ls(path: str = ".", long_format: bool = False, show_hidden: bool = False):
        target = Path(path).expanduser()
        if not target.exists():
            print(f"ls: cannot access '{path}': No such file or directory", file=sys.stderr)
            return
        entries = sorted(os.scandir(target), key=lambda e: e.name.lower())
        for entry in entries:
            if not show_hidden and entry.name.startswith("."): continue
            if long_format:
                stat = entry.stat()
                mode = oct(stat.st_mode)[-3:]
                size = stat.st_size
                print(f"{mode}\t{size} B\t{entry.name}")
            else: print(entry.name, end="  ")
        if not long_format: print()
    @staticmethod
    def pacman(action_flag: str, package_name: str = ""):
        if not shutil.which("pacman"):
            print("pacman: command not found", file=sys.stderr)
            return
        cmd = ["sudo", "pacman", action_flag]
        if package_name: cmd.append(package_name)
        subprocess.run(cmd)
    @staticmethod
    def systemctl(action: str, service_name: str):
        cmd = ["systemctl", action, service_name]
        subprocess.run(cmd)
    @staticmethod
    def journalctl(unit: str = None, follow: bool = False, lines: int = None):
        cmd = ["journalctl"]
        if unit: cmd.extend(["-u", unit])
        if follow: cmd.append("-f")
        if lines: cmd.extend(["-n", str(lines)])
        subprocess.run(cmd)
    @staticmethod
    def ld(object_files: list, output_binary: str = "a.out"):
        if not shutil.which("ld"):
            print("ld: command not found", file=sys.stderr)
            return
        cmd = ["ld", "-o", output_binary] + object_files
        subprocess.run(cmd)
    @staticmethod
    def mkdir(path: str, parents: bool = True):
        try:
            Path(path).mkdir(parents=parents, exist_ok=True)
            print(f"Directory created: {path}")
        except Exception as e: print(f"mkdir error: {e}", file=sys.stderr)
    @staticmethod
    def cat(filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f: print(f.read(), end="")
        except Exception as e: print(f"cat error: {e}", file=sys.stderr)
    @staticmethod
    def touch(filepath: str):
        try: Path(filepath).touch(exist_ok=True)
        except Exception as e: print(f"touch: {e}", file=sys.stderr)
    @staticmethod
    def rm(path: str, recursive: bool = False):
        target = Path(path)
        try:
            if target.is_dir():
                if recursive: shutil.rmtree(target)
                else: print(f"rm: cannot remove '{path}': Is a directory", file=sys.stderr)
            elif target.is_file(): target.unlink()
        except Exception as e: print(f"rm: {e}", file=sys.stderr)
    @staticmethod
    def cp(src: str, dst: str):
        try:
            src_path = Path(src)
            if src_path.is_dir(): shutil.copytree(src, dst, dirs_exist_ok=True)
            else: shutil.copy2(src, dst)
        except Exception as e: print(f"cp: {e}", file=sys.stderr)
    @staticmethod
    def mv(src: str, dst: str):
        try: shutil.move(src, dst)
        except Exception as e: print(f"mv: {e}", file=sys.stderr)
    @staticmethod
    def pwd(): print(os.getcwd())
    @staticmethod
    def curl(url: str, output: str = None):
        try:
            if not url.startswith(("http://", "https://")): url = "https://" + url
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
            )
            if output:
                with urllib.request.urlopen(req) as response, open(output, "wb") as f: f.write(response.read())
                print(f"Downloaded: {url} -> {output}")
            else:
                with urllib.request.urlopen(req) as response: print(response.read().decode("utf-8", errors="ignore"), end="")
        except Exception as e: print(f"curl: {e}", file=sys.stderr)
    @staticmethod
    def ping(host: str, count: int = 4):
        flag = "-n" if platform.system().lower() == "windows" else "-c"
        subprocess.run(["ping", flag, str(count), host])
    @staticmethod
    def uname():
        info = platform.uname()
        print(f"{info.system} {info.node} {info.release} {info.version} {info.machine}")
    @staticmethod
    def kill(pid: int, signal_num: int = 15):
        try: os.kill(int(pid), int(signal_num))
        except Exception as e: print(f"kill: {e}", file=sys.stderr)
    @staticmethod
    def git(action: str, *args):
        if not shutil.which("git"):
            print("git: command not found", file=sys.stderr)
            return
        subprocess.run(["git", action] + list(args))
    @staticmethod
    def grep(pattern: str, filepath: str, ignore_case: bool = False):
        import re
        try:
            flags = re.IGNORECASE if ignore_case else 0
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if re.search(pattern, line, flags): print(line, end="")
        except Exception as e: print(f"grep: {e}", file=sys.stderr)
    @staticmethod
    def head(filepath: str, lines: int = 10):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for _ in range(lines):
                    line = f.readline()
                    if not line: break
                    print(line, end="")
        except Exception as e: print(f"head: {e}", file=sys.stderr)
    @staticmethod
    def tail(filepath: str, lines: int = 10):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.readlines()
                for line in content[-lines:]: print(line, end="")
        except Exception as e: print(f"tail: {e}", file=sys.stderr)
    @staticmethod
    def wc(filepath: str):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.count("\n")
                words = len(content.split())
                bytes_count = len(content.encode("utf-8"))
                print(f"  {lines}  {words}  {bytes_count} {filepath}")
        except Exception as e: print(f"wc: {e}", file=sys.stderr)
    @staticmethod
    def find(directory: str = ".", name: str = None):
        try:
            target = Path(directory)
            pattern = f"*{name}*" if name else "*"
            for path in target.rglob(pattern): print(path)
        except Exception as e: print(f"find: {e}", file=sys.stderr)
    @staticmethod
    def echo(*args): print(" ".join(str(arg) for arg in args))
    @staticmethod
    def clear(): os.system("cls" if platform.system().lower() == "windows" else "clear")
    @staticmethod
    def export(key: str, value: str): os.environ[key] = str(value)
    @staticmethod
    def env():
        for key, value in os.environ.items(): print(f"{key}={value}")
    @staticmethod
    def sh(var_name: str) -> str:
        val = os.environ.get(var_name, "")
        print(val)
        return val
    @staticmethod
    def ps(flags: str = "aux"): subprocess.run(["ps", flags])
    @staticmethod
    def top(): subprocess.run(["top"])
    @staticmethod
    def htop(): subprocess.run(["htop"])
    @staticmethod
    def df(human_readable: bool = True):
        cmd = ["df", "-h"] if human_readable else ["df"]
        subprocess.run(cmd)
    @staticmethod
    def du(path: str = ".", human_readable: bool = True):
        cmd = ["du", "-sh", path] if human_readable else ["du", "-s", path]
        subprocess.run(cmd)
    @staticmethod
    def free(human_readable: bool = True):
        cmd = ["free", "-m"] if human_readable else ["free"]
        subprocess.run(cmd)
    @staticmethod
    def uptime(): subprocess.run(["uptime"])
    @staticmethod
    def wget(url: str, output: Optional[str] = None):
        cmd = ["wget"]
        if output: cmd.extend(["-O", output])
        cmd.append(url)
        subprocess.run(cmd)
    @staticmethod
    def netstat(flags: str = "-tulpn"): subprocess.run(["netstat", flags])
    @staticmethod
    def ss(flags: str = "-tulpn"): subprocess.run(["ss", flags])
    @staticmethod
    def dig(domain: str): subprocess.run(["dig", domain])
    @staticmethod
    def nslookup(domain: str): subprocess.run(["nslookup", domain])
    @staticmethod
    def ip(option: str = "addr"): subprocess.run(["ip", option])
    @staticmethod
    def ifconfig(): subprocess.run(["ifconfig"])
    @staticmethod
    def ssh(user_host: str, command: Optional[str] = None):
        cmd = ["ssh", user_host]
        if command: cmd.append(command)
        subprocess.run(cmd)
    @staticmethod
    def tar(flags: str, archive_name: str, target: str): subprocess.run(["tar", flags, archive_name, target])
    @staticmethod
    def zip(output_zip: str, target: str, recursive: bool = True):
        cmd = ["zip", "-r", output_zip, target] if recursive else ["zip", output_zip, target]
        subprocess.run(cmd)
    @staticmethod
    def unzip(archive: str, destination: Optional[str] = None):
        cmd = ["unzip", archive]
        if destination: cmd.extend(["-d", destination])
        subprocess.run(cmd)
    @staticmethod
    def gzip(filepath: str): subprocess.run(["gzip", filepath])
    @staticmethod
    def chmod(mode: str, filepath: str): subprocess.run(["chmod", mode, filepath])
    @staticmethod
    def chown(owner_group: str, filepath: str): subprocess.run(["chown", owner_group, filepath])
    @staticmethod
    def sudo(command: str, *args): subprocess.run(["sudo", command] + list(args))
class base(ast.NodeVisitor):
    def __init__(self, map_path: str = "command_map.json"):
        self.output_lines = []
        self.command_map = {}
        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f: self.command_map = json.load(f)
    def reset(self): self.output_lines = []
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                val = self._eval_node_val(node.value)
                self.output_lines.append(f"{var_name}={val}")
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name == "print":
                args = [self._eval_node_val(arg) for arg in node.args]
                self.output_lines.append(f'echo {" ".join(args)}')
            elif func_name in self.command_map.values():
                sh_cmd = [k for k, v in self.command_map.items() if v == func_name][0]
                args = [self._eval_node_val(arg).strip('"') for arg in node.args]
                self.output_lines.append(f'{sh_cmd} {" ".join(args)}'.strip())
    def _eval_node_val(self, node) -> str:
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "sh":
                if node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str): return f"${arg.value}"
                    elif isinstance(arg, ast.Name): return f"${arg.id}"
        if isinstance(node, ast.Constant):
            if isinstance(node.value, str): return f'"{node.value}"'
            return str(node.value)
        elif isinstance(node, ast.Name): return f'"${node.id}"'
        return '""'
