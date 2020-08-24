from automata.state import state
from automata.nfa import NFA

def test1():
    s0 = state(0)
    s1 = state(1)
    s0.outpaths = {'b': [s0, s1]}
    s1.outpaths = {'a': [s1], 'b': [s0]}
    n = NFA([s0,s1])
    n.start_states = [s0]
    n.accept_states = [s1]
    n.alphabet = ['a','b']
    n.nfa_to_dfa()
    n.my_dfa.print_dfa()

    """
    Correct Output

    States:  [{0}, '∅', {0, 1}, {1}]
    Start State:  {0}
    Accept States:  [{0, 1}, {1}]
    Outpaths:
    State: {0} , Outpaths:  [('a', '∅'), ('b', {0, 1})]
    State: ∅ , Outpaths:  [('a', '∅'), ('b', '∅')]
    State: {0, 1} , Outpaths:  [('a', {1}), ('b', {0, 1})]
    State: {1} , Outpaths:  [('a', {1}), ('b', {0})]
    """

test1()
