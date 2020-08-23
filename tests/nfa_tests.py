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
    for st in n.my_dfa.states:
        print('state id:', st.id, ', outpaths: ', [(k, v.id) for k,v in st.outpaths.items()])
    print('accept states:', [s.id for s in n.my_dfa.accept_states])
    print('start state: ', n.my_dfa.start_state.id)

    """
    Correct Output

    state id: {0} , outpaths:  [('a', '∅'), ('b', {0, 1})]
    state id: ∅ , outpaths:  [('a', '∅'), ('b', '∅')]
    state id: {0, 1} , outpaths:  [('a', {1}), ('b', {0, 1})]
    state id: {1} , outpaths:  [('a', {1}), ('b', {0})]
    accept states: [{0, 1}, {1}]
    start state:  {0}
    """

test1()
