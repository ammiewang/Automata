from automata.dfa import DFA
from automata.state import state, path

def test1():
    #from https://www.gatevidyalay.com/minimization-of-dfa-minimize-dfa-example/
    print('Test 1')
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s4 = state(4)
    s0.outpaths = {'a': s1, 'b': s2}
    s1.outpaths = {'a': s1, 'b': s3}
    s2.outpaths = {'a': s1, 'b': s2}
    s3.outpaths = {'a': s1, 'b': s4}
    s4.outpaths = {'a': s1, 'b': s2}
    d = DFA([s0,s1,s2,s3,s4])
    d.start_state = s1
    d.accept_states = [s4]
    d.alphabet = ['a', 'b']
    d.minimize()
    print('states: ', [s.id for s in d.states])
    print('outpaths: ', [('state: ' + str(s.id), [(key, val.id) for key,val in s.outpaths.items()]) for s in d.states])
    print('start state: ', d.start_state.id)
    print('accept states: ', [s.id for s in d.accept_states])
    print('new state to old states:', [(key.id, [v.id for v in val]) for key, val in d.new_states.items()])

    """
    Correct Output

    states:  [3, 4, 1, 5]
    outpaths:  [('state: 3', [('a', 1), ('b', 4)]), ('state: 4', [('a', 1), ('b', 5)]), ('state: 1', [('a', 1), ('b', 3)]), ('state: 5', [('a', 1), ('b', 5)])]
    start state:  1
    accept states:  [4]
    new state to old states: [(5, [0, 2]), (4, [4]), (3, [3]), (1, [1])]
    """

#test1()

def test2():
    #Example 13.1 from Automata & Computability
    print('Test 2')
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s0.outpaths = {'a': s1, 'b': s3}
    s1.outpaths = {'a': s2, 'b': s2}
    s2.outpaths = {'a': s2, 'b': s2}
    s3.outpaths = {'a': s2, 'b': s2}
    d = DFA([s0,s1,s2,s3])
    d.start_state = s0
    d.accept_states = [s1, s3]
    d.alphabet = ['a', 'b']
    d.minimize()
    print('states: ', [s.id for s in d.states])
    print('outpaths: ', [('state: ' + str(s.id), [(key, val.id) for key,val in s.outpaths.items()]) for s in d.states])
    print('start state: ', d.start_state.id)
    print('accept states: ', [s.id for s in d.accept_states])
    print('new state to old states:', [(key.id, [v.id for v in val]) for key, val in d.new_states.items()])

    """
    Correct Output

    states:  [2, 4, 0]
    outpaths:  [('state: 2', [('a', 2), ('b', 2)]), ('state: 4', [('a', 2), ('b', 2)]), ('state: 0', [('a', 4), ('b', 4)])]
    start state:  0
    accept states:  [4]
    new state to old states: [(4, [1, 3]), (2, [2]), (0, [0])]
    """

#test2()

def test3():
    #from https://www.geeksforgeeks.org/minimization-of-dfa/
    print('Test 3')
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s4 = state(4)
    s5 = state(5)
    s0.outpaths = {'0': s3, '1': s1}
    s1.outpaths = {'0': s2, '1': s5}
    s2.outpaths = {'0': s2, '1': s5}
    s3.outpaths = {'0': s0, '1': s4}
    s4.outpaths = {'0': s2, '1': s5}
    s5.outpaths = {'0': s5, '1': s5}
    d = DFA([s0,s1,s2,s3,s4,s5])
    d.start_state = s0
    d.accept_states = [s1, s2, s4]
    d.alphabet = ['0', '1']
    d.minimize()
    print('states: ', [s.id for s in d.states])
    print('outpaths: ', [('state: ' + str(s.id), [(key, val.id) for key,val in s.outpaths.items()]) for s in d.states])
    print('start state: ', d.start_state.id)
    print('accept states: ', [s.id for s in d.accept_states])
    print('new state to old states:', [(key.id, [v.id for v in val]) for key, val in d.new_states.items()])

    """
    Correct Output

    states:  [6, 5, 7]
    outpaths:  [('state: 6', [('0', 6), ('1', 7)]), ('state: 5', [('0', 5), ('1', 5)]), ('state: 7', [('0', 7), ('1', 5)])]
    start state:  6
    accept states:  [7]
    new state to old states: [(6, [3, 0]), (7, [1, 4, 2]), (5, [5])]
    """
#test3()

def test4():
    #Example 13.2 from Automata & Computability
    print('Test 4')
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s4 = state(4)
    s5 = state(5)
    s0.outpaths = {'a': s1, 'b': s2}
    s1.outpaths = {'a': s3, 'b': s4}
    s2.outpaths = {'a': s4, 'b': s3}
    s3.outpaths = {'a': s5, 'b': s5}
    s4.outpaths = {'a': s5, 'b': s5}
    s5.outpaths = {'a': s5, 'b': s5}
    d = DFA([s0,s1,s2,s3,s4,s5])
    d.start_state = s0
    d.accept_states = [s1, s2, s5]
    d.alphabet = ['a', 'b']
    d.minimize()
    print('states: ', [s.id for s in d.states])
    print('outpaths: ', [('state: ' + str(s.id), [(key, val.id) for key,val in s.outpaths.items()]) for s in d.states])
    print('start state: ', d.start_state.id)
    print('accept states: ', [s.id for s in d.accept_states])
    print('new state to old states:', [(key.id, [v.id for v in val]) for key, val in d.new_states.items()])

    """
    Correct Output

    states:  [0, 5, 7, 6]
    outpaths:  [('state: 0', [('a', 6), ('b', 6)]), ('state: 5', [('a', 5), ('b', 5)]), ('state: 7', [('a', 5), ('b', 5)]), ('state: 6', [('a', 7), ('b', 7)])]
    start state:  0
    accept states:  [6, 5]
    new state to old states: [(6, [1, 2]), (7, [3, 4]), (0, [0]), (5, [5])]
    """
#test4()
