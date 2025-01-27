from turing_machine import SimplifiedTuringMachine, TuringMachine, TuringMachineError
from typing import Generator
from os import get_terminal_size, startfile
import re

STRING_INDICATOR = "'"
COMMENT_INDICATOR = "//"

MACHINE_NAME_KEYWORD = "name"
BLANK_SYMBOL_KEYWORD = "blank"
INITIAL_STATE_KEYWORD = "initial"
FINAL_STATES_KEYWORD = "final"

START_TRANSITION_FUNCTION_KEYWORD = "startprogr"
END_TRANSITION_FUNCTION_KEYWORD = "endprogr"

GET_FORMAL_DEFINITION_COMMAND = "#printdef"
RUN_WITH_ALL_STEPS_COMMAND = "#runsteps"
RUN_FINAL_STATE_ONLY_COMMAND = "#run"
RENDER_GRAPHICAL_TRANSITION_DIAGRAM_COMMAND = "#renderdiagram"

STATE_DIAGRAM_FORMAT = "pdf"


def get_separator() -> str:
    # returns a separator with the same width as the terminal window
    return "\n" + "\n" + "─" * get_terminal_size().columns + "\n" + "\n"


class TMLangSyntaxError(Exception):
    pass


class TMLangValueError(Exception):
    pass


def evaluate_str(code: str) -> str:  # evaluates a string in TMLang
    # ex n°1: str_from_str("'test'") = 'test'
    # ex n°2: str_from_str("test") = 'test'
    code = code.strip()
    if code.startswith(STRING_INDICATOR) and code.endswith(STRING_INDICATOR):
        return code[1:-1]
    return code


def evaluate_set(set_str: str) -> tuple:
    # takes a str written with set notation and returns a tuple listing the elements given
    # ex : evaluate_set("{test, test1, 'test 2'}") gives ('test', 'test1', 'test 2')
    # if the function returns None, the input is invalid
    set_str = set_str.strip()
    if not (set_str.startswith("{") and set_str.endswith("}")):
        return None
    elements = set_str[1:-1].split(",")
    output_list = []
    for element in elements:
        output_list.append(evaluate_str(element))
    if output_list == [""]:
        return ()

    return tuple(output_list)


def is_blank(line: str) -> bool:
    # returns True if the line can be ignored by the interpreter (i.e. it is blank)
    return line.strip() == ""


def remove_comments_and_blanks(line: str) -> str:
    # removes the comment contained in the line (if there is one)
    # it also removes all the blanks at the start and the end of the line
    return re.sub(f"{COMMENT_INDICATOR}.*", "", line).strip()


def interpret_from_code(code: str, render_image=True, automatically_open_image_generated=False) -> Generator[str]:
    code_lines = code.splitlines()
    blank_symbol = None
    initial_state = None
    final_states = None
    machine_name = None
    line_number = 0  # line_number is a 0-based index

    # We first of all interpret the values defined with the keywords: name, initial, final, and blank
    for line_number in range(len(code_lines)):
        if all(x is not None for x in [blank_symbol, initial_state, final_states, machine_name]):
            break

        code_line = remove_comments_and_blanks(code_lines[line_number])
        if not is_blank(code_line):
            if code_line.startswith(MACHINE_NAME_KEYWORD):
                argument = code_line[len(MACHINE_NAME_KEYWORD) :].strip()
                machine_name = evaluate_str(argument)

            elif code_line.startswith(BLANK_SYMBOL_KEYWORD):
                argument = code_line[len(BLANK_SYMBOL_KEYWORD) :].strip()
                blank_symbol = evaluate_str(argument)

            elif code_line.startswith(INITIAL_STATE_KEYWORD):
                argument = code_line[len(INITIAL_STATE_KEYWORD) :].strip()
                initial_state = evaluate_str(argument)

            elif code_line.startswith(FINAL_STATES_KEYWORD):
                argument = code_line[len(FINAL_STATES_KEYWORD) :].strip()
                final_states = evaluate_set(argument)
                if final_states is None:
                    raise TMLangSyntaxError(f"line {line_number + 1}: invalid set syntax '{argument}'")

            else:
                raise TMLangSyntaxError(f"line {line_number + 1}: invalid syntax")

    if any(x is None for x in [blank_symbol, initial_state, final_states, machine_name]):
        raise TMLangValueError("Not all necessary values were precised (blank, initial, final, name)")

    code_line = remove_comments_and_blanks(code_lines[line_number])
    while not code_line == START_TRANSITION_FUNCTION_KEYWORD:
        if not is_blank(code_line):
            raise TMLangSyntaxError(f"line {line_number}: expected {START_TRANSITION_FUNCTION_KEYWORD}")
        line_number += 1
        code_line = remove_comments_and_blanks(code_lines[line_number])

    line_number += 1
    code_line = remove_comments_and_blanks(code_lines[line_number])

    transition_function = {}

    while not code_line == END_TRANSITION_FUNCTION_KEYWORD:
        if not is_blank(code_line):
            if re.fullmatch(".+,.+:.+,.+,.+", code_line):
                key = tuple(x.strip() for x in code_line.split(":")[0].split(","))

                value = tuple(x.strip() for x in code_line.split(":")[1].split(","))
                transition_function[key] = value

            else:
                raise TMLangSyntaxError(f"line {line_number + 1}: expected {END_TRANSITION_FUNCTION_KEYWORD}")
        line_number += 1
        try:
            code_line = remove_comments_and_blanks(code_lines[line_number])
        except IndexError:
            raise TMLangSyntaxError(f"line {line_number}: expected {END_TRANSITION_FUNCTION_KEYWORD}")

    turing_machine_described = SimplifiedTuringMachine(
        name=machine_name,
        transition_function=transition_function,
        blank_symbol=blank_symbol,
        initial_state=initial_state,
        final_states=final_states,
    )

    # We then execute eventual commands
    is_first_action = True  # used for printing the separator correctly
    for line_number in range(line_number + 1, len(code_lines)):
        code_line = remove_comments_and_blanks(code_lines[line_number])

        if not is_blank(code_line):

            if not is_first_action:
                yield get_separator()

            if code_line == GET_FORMAL_DEFINITION_COMMAND:
                yield turing_machine_described.get_formal_definition()

            elif code_line.startswith(RENDER_GRAPHICAL_TRANSITION_DIAGRAM_COMMAND):
                transition_diagram_graph = turing_machine_described.get_transition_diagram()
                argument = code_line[len(RENDER_GRAPHICAL_TRANSITION_DIAGRAM_COMMAND) :].strip()
                if argument:
                    image_format = argument
                else:
                    image_format = STATE_DIAGRAM_FORMAT
                if render_image:  # don't render images in verifying mode
                    file_name = transition_diagram_graph.render(format=image_format)
                    yield f"Transition diagram rendered as {image_format} to file '{file_name}'"
                if automatically_open_image_generated:
                    startfile(file_name)

            elif code_line.startswith(RUN_WITH_ALL_STEPS_COMMAND):
                argument = code_line[len(RUN_WITH_ALL_STEPS_COMMAND) :].strip()
                starting_tape = evaluate_str(argument)
                for step in turing_machine_described.perform_computation_from_tape(
                    starting_tape=starting_tape, all_steps=True
                ):
                    yield step

            elif code_line.startswith(RUN_FINAL_STATE_ONLY_COMMAND):
                argument = code_line[len(RUN_FINAL_STATE_ONLY_COMMAND) :].strip()
                starting_tape = evaluate_str(argument)
                for step in turing_machine_described.perform_computation_from_tape(
                    starting_tape=starting_tape, all_steps=False
                ):
                    yield step

            else:
                raise TMLangSyntaxError(f"line {line_number + 1}: unknown action")

            is_first_action = False
