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
    d.print_dfa(True)

    """
    Correct Output

    States:  [7, 8, 6, 5]
    Start State:  7
    Accept States:  [6]
    Outpaths:
    State: 7 , Outpaths:  [('a', 7), ('b', 8)]
    State: 8 , Outpaths:  [('a', 7), ('b', 6)]
    State: 6 , Outpaths:  [('a', 7), ('b', 5)]
    State: 5 , Outpaths:  [('a', 7), ('b', 5)]
    State Collapses:
    [(5, [0, 2]), (6, [4]), (7, [1]), (8, [3])]
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
    d.print_dfa(True)

    """
    Correct Output

    States:  [4, 6, 5]
    Start State:  5
    Accept States:  [4]
    Outpaths:
    State: 4 , Outpaths:  [('a', 6), ('b', 6)]
    State: 6 , Outpaths:  [('a', 6), ('b', 6)]
    State: 5 , Outpaths:  [('a', 4), ('b', 4)]
    State Collapses:
    [(4, [3, 1]), (5, [0]), (6, [2])]
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
    d.print_dfa(True)

    """
    Correct Output

    States:  [7, 8, 6]
    Start State:  6
    Accept States:  [7]
    Outpaths:
    State: 7 , Outpaths:  [('0', 7), ('1', 8)]
    State: 8 , Outpaths:  [('0', 8), ('1', 8)]
    State: 6 , Outpaths:  [('0', 6), ('1', 7)]
    State Collapses:
    [(6, [0, 3]), (7, [4, 2, 1]), (8, [5])]
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
    d.print_dfa(True)

    """
    Correct Output

    States:  [7, 9, 8, 6]
    Start State:  9
    Accept States:  [6, 8]
    Outpaths:
    State: 7 , Outpaths:  [('a', 8), ('b', 8)]
    State: 9 , Outpaths:  [('a', 6), ('b', 6)]
    State: 8 , Outpaths:  [('a', 8), ('b', 8)]
    State: 6 , Outpaths:  [('a', 7), ('b', 7)]
    State Collapses:
    [(6, [2, 1]), (7, [3, 4]), (8, [5]), (9, [0])]
    """
#test4()
