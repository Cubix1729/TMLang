from TMLang_interpreter import interpret_from_code
import argparse
import sys

parser = argparse.ArgumentParser(
    prog="TMLang",
    description="A small language for programming Turing machines",
)

parser.add_argument("filename", help="the path to the file containing the code you want to interpret")

parser.add_argument(
    "-o",
    "--output",
    default=None,
    help="the file you want to write the generated output (default: stdout)",
)

parser.add_argument(
    "-v",
    "--verify",
    action="store_true",
    help="if used, the output is printed only in case of error in the program given",
)

parser.add_argument(
    "-a",
    "--auto-open",
    action="store_true",
    help="when rendering a transition diagram, the program will automatically the generated image",
)

args = parser.parse_args()

with open(args.filename, "r") as file:
    code = file.read()

if args.output is not None:
    sys.stdout = open(args.output, "w", encoding="utf-8")

for i in interpret_from_code(code, automatically_open_image_generated=args.auto_open):
    if not args.verify:
        print(i)
