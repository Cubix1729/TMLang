# TMLang
TMLang, which stands for Turing Machine Language, is a small language for programming Turing machines.
It can, from a given machine:
 - Give the formal mathematical definition and the render the transition function as a table
 - Perform a computation from a given starting tape
 - Render the transition table as a state diagram, using `graphviz`

## Usage

### TMLang Syntax

Comments are written with `//`, and they must be in a separate line.
TMLang interprets the code line by line, so statements cannot be separated into several lines.
In TMLang, you write strings in two different ways: either with no quotation marks, or by using `''` to make it more clear.
You write sets by using curly brackets.

To create a Turing machine in TMLang, you first have to precise:
 - The machine's name, with the keyword `name`
 - The alphabet's blank (default) symbol with `blank`
 - The initial state, using `initial`
 - The set of final states (possibly empty), with `final`

Then, you write the transition function in this way:
 - You first you the keyword `startprog` to indicate you are starting the transition function
 - Then, the transition function is written line by line, ideally with some identation at the start of each line. The syntax is the following:
    - `old state, symbol read: new state, symbol to write, direction`
 - To end the transition function definition, use the keyword `endprogr`

When the Turing machine is completely defined, you can use it with the following commands:
 - `#printdef` to print the complete mathematical definition
 - `#run` to run the Turing machine from the starting tape precised, and print the final result of the computation
 - `#runsteps`: does the same thing except it prints all intermediate steps as well
 - `#renderdiagram` renders the transition diagram to a pdf file

### Example

Here is an example TMLang program (you can find it in examples/one_third_machine.tmlang):
```
// Computes the sequence 0101010101010101..., which is 1/3 in binary

name 'One Third Machine'
initial a
final {}
blank 0


startprogr
    a, 0: b, 0, R
    b, 0: a, 1, R
endprogr



#printdef
#run ''
#renderdiagram
```