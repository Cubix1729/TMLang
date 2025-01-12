from TMLang_interpreter import interpret_from_code
import argparse
import sys

parser = argparse.ArgumentParser(
    prog="TMLang",
    description="A minimal language for programming Turing machines",
)


parser.add_argument(
    "filename", help="the path to the file containing the code you want to interpret"
)

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

args = parser.parse_args()


with open(args.filename, "r") as file:
    code = file.read()

if args.output is not None:
    sys.stdout = open(args.output, "w", encoding="utf-8")

for i in interpret_from_code(code):
    if not args.verify:
        print(i)
