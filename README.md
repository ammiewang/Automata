# dfas
converts DFAs to regular expressions

Requirements:
- Python 3
- pgi/PyGObject

Description:
  This program converts deterministic finite automata into regular expressions by recursively utilizing the formula in Dexter Kozen's Automata and Computability (pg. 53). Various (correct) regular expressions can be derived for the same language, so the user must select whether they want to receive a random or particular one. If the user chooses to randomly receive any regular expression for their DFA, the program will make a random choice for which states are removed when simplifying the automaton. Otherwise, the user must specify which state they would like to remove at each recursive step of the algorithm.

Instructions:
  - run main.py
  - input the number of states, the start state, the accept states, and the alphabet for your DFA
    - example:
      - Input the number of states: 4
      - Input the start state: 0
      - Input the accept states: 1 2
      - Inut the alphabet: a b c
  - input the correct paths in the popup window and press the 'Enter' button (on the window)
    - example:
      - if 0 -- (a) --> 1, write 1 under row '0' column 'a'
  - return to the terminal and choose whether the regular expression will be randomized (y) or not (n)
    - if not (n), choose which states to remove at each step
  - a regular expression for the given DFA will output to the terminal
