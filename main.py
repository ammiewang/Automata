from automata.state import state, path
from automata.dfa import DFA
from automata.nfa import NFA
from automata.regex import Regex
from display.dnfa_window import dnfa_window
from display.rand_window import rand_window
from display.selection_window import select_window
from display.automaton_window import inp_window

if __name__ == '__main__':
    option = select_window()

    if option == 1 or option == 2:
        automaton = DFA([])
        opt = 'dfa'
        inp_window(automaton, opt)
        if option == 1:
            dnfa_window(automaton, opt)
            rand_window(automaton)
        elif option == 2:
            dnfa_window(automaton, opt)
            automaton.minimize()
            dnfa_window(automaton, opt, inp=True)

    elif option == 3:
        automaton = NFA([])
        opt = 'nfa'
        inp_window(automaton, opt)
        dnfa_window(automaton, opt)
        automaton.nfa_to_dfa()
        my_dfa = automaton.my_dfa
        opt = 'dfa'
        print(my_dfa.alphabet)
        for st in my_dfa.states:
            print('id:', st.id, ', outpaths: ', [(k, v.id) for k,v in st.outpaths.items()])
        dnfa_window(my_dfa, opt, inp=True)

    elif option == 4:
        automaton = Regex('')
        opt = 'regex'
        inp_window(automaton, opt)
        automaton.dfa_maker()
        my_dfa = automaton.my_dfa
        opt = 'dfa'
        dnfa_window(my_dfa, opt, inp=True)
