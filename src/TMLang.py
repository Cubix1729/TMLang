from turing_machine import TuringMachineError
from TMLang_interpreter import interpret_from_code, TMLangSyntaxError, TMLangValueError
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="A small language for designing and programming Turing machines",
    )

    parser.add_argument("filename", help="the path to the file containing the code to interpret")

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="the file to write the generated output (default: stdout)",
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
        help="when rendering a transition diagram, the program will automatically open the generated image",
    )

    args = parser.parse_args()

    with open(args.filename, "r") as file:
        code = file.read()

    if args.output is not None:
        sys.stdout = open(args.output, "w", encoding="utf-8")

    try:
        for i in interpret_from_code(
            code, render_image=(not args.verify), automatically_open_image_generated=args.auto_open
        ):
            if not args.verify:
                print(i)

    except TMLangSyntaxError as error:
        print(f"TMLangSyntaxError: {error}")
    except TMLangValueError as error:
        print(f"TMLangValueError: {error}")
    except TuringMachineError as error:
        print(f"TuringMachineError: {error}")


if __name__ == "__main__":
    main()
