import argparse
import sys
from .terminal import terminal
from .transpiler import transpiler
def main():
    parser = argparse.ArgumentParser(
        description="py2shell - a bridge between python and bash"
    )
    parser.add_argument("input_file", nargs="?", help="path to input python (.py) file")
    parser.add_argument(
        "-o", "--output", help="path for output bash (.sh) script file"
    )
    parser.add_argument(
        "-m", "--map", default="command_map.json", help="path to command mapping json file"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="start the live interactive repl terminal",
    )
    args = parser.parse_args()
    if args.interactive or not args.input_file:
        term = terminal(map_path=args.map)
        term.start_repl()
    else:
        trans = transpiler(map_path=args.map)
        try:
            output = trans.transpile_file(args.input_file, args.output)
            if not args.output: print(output)
            else: print(f"generated executable script: {args.output}")
        except Exception as e:
            print(f"error: {e}", file=sys.stderr)
            sys.exit(1)
#if __name__ == "__main__":
#    main()
