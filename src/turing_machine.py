from prettytable import PrettyTable
from typing import Generator
import graphviz

# Symbol defnitions
GO_LEFT_SYMBOL = "L"
GO_RIGHT_SYMBOL = "R"
STAY_IN_PLACE_SYMBOL = "N"

MAX_NUMBER_OF_STEPS = 2000


class TuringMachineError(Exception):  # A custom error for Turing machines
    pass


class Tape:
    """A class for the Turing machine's tape"""

    def __init__(self, starting_configuration: str, blank_symbol: str):
        self.blank_symbol = blank_symbol
        self._tape: dict = {}
        for i in range(len(starting_configuration)):
            self._tape[i] = starting_configuration[i]

    def __getitem__(self, index: int):
        if index in self._tape:
            return self._tape[index]
        else:
            return self.blank_symbol

    def __setitem__(self, index: int, char: str):
        self._tape[index] = char

    def __str__(self):
        output = ""
        if self._tape == {}:  # if self._tape is empty, there will be a ValueError when calling min and max
            return ""
        min_used_index = min(self._tape.keys())
        max_used_index = max(self._tape.keys())
        for i in range(min_used_index, max_used_index + 1):
            if i in self._tape:
                output += self._tape[i]
            else:
                output += self.blank_symbol

        return output

    def render_with_pos_indicator(self, head_position: int):
        output = ""
        if self._tape == {}:  # if self._tape is empty, there will be a ValueError when calling min and max
            return ""
        min_used_index = min(self._tape.keys())
        max_used_index = max(self._tape.keys())
        for i in range(min_used_index, max_used_index + 1):
            if i in self._tape:
                output += self._tape[i]
            else:
                output += self.blank_symbol

        output += "\n" + " " * (head_position - min_used_index - 1) + "^"  # adds a position pointer
        return output


class TransitionFunction:
    def __init__(self, transition_function: dict):
        self.transition_function = transition_function
        # The right format for transition_function is:
        # {(current state, symbol scanned): (next state, new symbol, moving direction), etc...}

    def transition_table(self):
        # outputs the transition table as a str
        table = PrettyTable(
            [
                "Current state",
                "Scanned symbol",
                "Next state",
                "Print symbol",
                "Moving direction",
            ]
        )

        for key, value in self.transition_function.items():
            table.add_row([key[0], key[1], value[0], value[1], value[2]])

        return table.get_string()

    def __str__(self):
        return self.transition_table()

    def __getitem__(self, index):
        return self.transition_function[index]

    def as_dict(self):
        return self.transition_function

    def verify_validity(
        self,
        possible_states: tuple | list,
        alphabet: tuple | list,
        final_states: tuple | list,
    ):
        """Raises a TuringMachineError if the transition function isn't in the right format - doesn't return anything"""
        for key, value in self.transition_function.items():
            if not len(key) == 2:
                raise TuringMachineError(
                    f"Transition function not valid: expected 2 inputs for each transition function defnintion, got {len(key)}"
                )

            if not len(value) == 3:
                raise TuringMachineError(
                    f"Transition function not valid: expected 3 outputs for each transition function defnintion, got {len(value)}"
                )

            start_state = key[0]
            symbol_read = key[1]
            new_state = value[0]
            new_symbol = value[1]
            direction = value[2]

            if start_state in final_states:
                raise TuringMachineError(f"Transition function not valid: state '{key[0]}' is a final state")

            if start_state not in possible_states:
                raise TuringMachineError(f"Transition function not valid: '{key[0]}' not in possible states")

            if new_state not in possible_states:
                raise TuringMachineError(f"Transition function not valid: '{value[0]}' is not in possible states")

            if symbol_read not in alphabet:
                raise TuringMachineError(f"Transition function not valid: '{key[1]}' is not in alphabet")

            if new_symbol not in alphabet:
                raise TuringMachineError(f"Transition function not valid: '{value[1]}' is not in alphabet")

            if direction not in (GO_LEFT_SYMBOL, GO_RIGHT_SYMBOL, STAY_IN_PLACE_SYMBOL):
                raise TuringMachineError(f"Transition function not valid: direction indicator '{value[2]}' is invalid")


class TuringMachine:
    """
    Implements a Turing machine with an infinite tape on both sides :

    possible_states: a list of the turing machine's possible states (must be strings)
    initial_state: the state in which the machine starts
    final_states: a list of the states in which the program terminates
    alphabet: a list/tuple of the symbols that can appear on the tape
    blank_symbol: a string containing the default symbol
    transition_function: the transition function

    """

    def __init__(
        self,
        name: str,
        transition_function: dict,
        possible_states: tuple | list,
        initial_state: str,
        final_states: tuple | list,
        alphabet: tuple | list,
        blank_symbol: str,
    ):

        # We test the given values to see if they're correct/valid

        if not blank_symbol in alphabet:  # we verify blank_symbol is valid
            raise TuringMachineError(f"Blank symbol chosen '{blank_symbol}' isn't in alphabet")

        if not initial_state in possible_states:  # we verify initial_state in valid
            raise TuringMachineError(f"Initial state '{initial_state}' isn't in possible states")

        for state in final_states:  # we verify final_states is valid
            if not state in possible_states:
                raise TuringMachineError(f"Invalid final state: '{state}' not in possible states")

        self.transition_function = TransitionFunction(transition_function)
        self.transition_function.verify_validity(
            possible_states=possible_states,
            alphabet=alphabet,
            final_states=final_states,
        )

        # Set the values for the alphabet, the possible states, etc...
        self.name = name
        self.alphabet = alphabet
        self.blank_symbol = blank_symbol
        self.possible_states = possible_states
        self.final_states = final_states
        self.initial_state = initial_state

        # Initialise the Turing machine
        self.state = initial_state
        self.head_position = 0
        self.tape = Tape(
            starting_configuration="", blank_symbol=blank_symbol
        )  # We don't precise the starting tape; it will be initialised later on

    def get_formal_definition(
        self,
    ) -> str:  # returns a string representation of the machine's definition
        output = ""
        output += f"Turing machine '{self.name}' defined with:\n"
        output += f"* Set of states 𝙌 = {set(self.possible_states)}\n"
        output += f"* Initial state 𝙦₀ = '{self.initial_state}'\n"
        output += f"* Set of final/accepting states 𝙁 = {set(self.final_states) if self.final_states else "∅"}\n"  # we represent set() as ∅
        output += f"* Alphabet 𝜞 = {set(self.alphabet)} with blank symbol 𝑩 = '{self.blank_symbol}'\n"
        output += "* Transition function 𝛿 : (𝙌 ∖ 𝙁) × 𝙁 → 𝙌 × 𝙁 × {L, R, N}, represented as the following table:\n\n"
        output += self.transition_function.transition_table()
        return output

    def get_transition_diagram(self) -> graphviz.Digraph:
        """Returns the Turing machine's definition as a transition diagram"""
        transition_diagram_output = graphviz.Digraph(
            filename=f"transition_diagram_{self.name.replace(" ", "_")}",
            graph_attr={
                "labelloc": "t",
                "label": f"Transition diagram for Turing machine '{self.name}'",
                "fontname": "Liberation Sans italic bold",
            },
        )

        transition_diagram_output.node("start", shape="plaintext")
        transition_diagram_output.edge("start", self.initial_state)

        for key, value in self.transition_function.as_dict().items():
            start_state = key[0]
            symbol_read = key[1]
            new_state = value[0]
            new_symbol = value[1]
            direction = value[2]

            if new_state in self.final_states:
                transition_diagram_output.node(new_state, shape="doublecircle")

            transition_diagram_output.edge(
                start_state,
                new_state,
                label=f"{symbol_read}, {new_symbol}, {direction}",
            )

        return transition_diagram_output

    def initialise_computation(self, starting_tape: str):
        for char in starting_tape:  # we verify starting_tape is valid
            if not char in self.alphabet:
                raise TuringMachineError(f"Invalid starting tape: symbol '{char}' not in alphabet")

        self.tape = Tape(starting_tape, blank_symbol=self.blank_symbol)
        self.head_position = 0
        self.state = self.initial_state

    def get_tape(self) -> str:
        return self.tape.render_with_pos_indicator(head_position=self.head_position)

    def step(self):
        current_state = self.state
        symbol_under_head = self.tape[self.head_position]
        try:
            next_state, symbol_to_write, direction_to_move_head = self.transition_function[
                (current_state, symbol_under_head)
            ]
        except KeyError:
            raise TuringMachineError(
                f"Turing machine entered a state undefined by the transition function,"
                f"in state '{current_state} with symbol {symbol_under_head}"
            )

        self.state = next_state
        self.tape[self.head_position] = symbol_to_write
        if direction_to_move_head == GO_LEFT_SYMBOL:
            self.head_position -= 1
        elif direction_to_move_head == GO_RIGHT_SYMBOL:
            self.head_position += 1

    def in_final_state(self):
        return self.state in self.final_states

    def perform_computation_from_tape(self, starting_tape: str, all_steps: bool = False) -> Generator[str]:
        # return a generator that yields formatted string for each step of the computation
        # if all_steps is set to False, the ouput only contains the final result
        # after MAX_NUMBER_OF_STEPS steps, the program will assume the machine is caught in an infinite loop
        self.initialise_computation(starting_tape=starting_tape)
        num_step = 1
        infinite_loop = False
        while not self.in_final_state():
            if num_step >= MAX_NUMBER_OF_STEPS:
                infinite_loop = True
                yield f"The Turing machine seems to be caught in an infinite loop. After {num_step} steps, the tape is:\n{self.get_tape()}"
                break
            if all_steps:
                yield f"Step {num_step}, with state '{self.state}':\n{self.get_tape()}\n"
            self.step()
            num_step += 1

        if not infinite_loop:
            yield f"Turing machine '{self.name}' ended on state '{self.state}' from input '{starting_tape}' after {num_step} steps, with final tape:\n{self.get_tape()}"


class SimplifiedTuringMachine(TuringMachine):
    """
    Same as TuringMachine, except you don't have to precise alphabet and possible_states,
    as they will be deduced from the transition function given
    """

    def __init__(self, name, transition_function, initial_state, final_states, blank_symbol):
        alphabet = []
        possible_states = []

        for key, value in transition_function.items():
            start_state = key[0]
            symbol_read = key[1]
            new_state = value[0]
            new_symbol = value[1]
            direction = value[2]

            alphabet.append(symbol_read)
            alphabet.append(new_symbol)

            possible_states.append(start_state)
            possible_states.append(new_state)

        # we then remove duplicates
        alphabet = sorted(list(set(alphabet)))
        possible_states = sorted(list(set(possible_states)))

        super().__init__(
            name=name,
            transition_function=transition_function,
            possible_states=possible_states,
            initial_state=initial_state,
            final_states=final_states,
            alphabet=alphabet,
            blank_symbol=blank_symbol,
        )
