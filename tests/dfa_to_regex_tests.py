from automata.dfa import state, path, DFA
import random


def test1():
    #even number of 0s
    s0 = state(0)
    s1 = state(1)
    s0.outpaths = {'0': s1, '1': s0}
    s1.outpaths = {'0': s0, '1': s1}
    d = DFA([s0, s1])
    d.start_state = s0
    d.accept_states = [s0]
    d.alphabet = ['0', '1']
    print(d.all_regex(False) + '\n')

#test1()

def test2():
    #odd number of 0s
    s0 = state(0)
    s1 = state(1)
    s0.outpaths = {'0': s1, '1': s0}
    s1.outpaths = {'0': s0, '1': s1}
    d = DFA([s0, s1])
    d.start_state = s0
    d.accept_states = [s1]
    d.alphabet = ['0', '1']
    print(d.all_regex() + '\n')

#test2()

def test3():
    #pg 17 Example 3.2 from Automata & Computability
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s0.outpaths = {'a': s1, 'b': s0}
    s1.outpaths = {'a': s2, 'b': s0}
    s2.outpaths = {'a': s3, 'b': s0}
    s3.outpaths = {'a': s3, 'b': s3}
    d = DFA([s0, s1, s2, s3])
    d.start_state = s0
    d.accept_states = [s3]
    d.alphabet = ['a', 'b']
    print(d.all_regex() + '\n')

#test3()

def test4():
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s0.outpaths = {'a': s1}
    s1.outpaths = {'a': s2, 'b': s0}
    d = DFA([s0, s1, s2])
    d.start_state = s0
    d.accept_states = [s2]
    d.alphabet = ['a', 'b']
    print(d.all_regex(False))

#test4()
