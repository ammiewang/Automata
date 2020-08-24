# Automata
  performs various conversions on DFAs, NFAs, and regular expressions

### Requirements
- Python 3
- pgi/PyGObject

### Operations

#### DFAs
- DFA to regex conversion
  - Recursively utilizes formula 9.19 from Lecture 9 of Dexter Kozen's *Automata and Computability*
  - Since various (correct) regular expressions can be derived for the same language, the user must select whether they want to receive a random or particular one. If the user chooses to randomly receive any regular expression for their DFA, the program will make a random choice for which states are removed when simplifying the automaton. Otherwise, the user must specify which state they would like to remove at each recursive step of the algorithm.

- DFA minimization
  - Uses DFA minimization algorithm in Lecture 14 of *Automata and Computability*, also described [here](https://www.geeksforgeeks.org/minimization-of-dfa/)

#### NFAs
- NFA to DFA conversion
  - Uses the subset construction technique, described [here](https://en.wikipedia.org/wiki/Powerset_construction)

#### Regexes
- Regex to DFA conversion
  - Parses the regex, converts the regex to an NFA, converts the NFA to a DFA, and minimizes the DFA
- Regex Complementation
  - Converts the regex to a DFA, takes the complement of the DFA, and converts this complement into a new regex


### Running the Program
- To input your own DFA/NFA/regex, run main.py
- To run one of the test functions, navigate to the Automata directory, uncomment the call to the specific test function in your chosen test file, and run the command 'python -m tests/test_file_name.py'
