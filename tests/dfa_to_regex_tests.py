from automata.dfa import state, path, DFA
import random


def test1():
    #1a in HW3 in Automata & Computability
    print('Test 1')
    s0 = state(0)
    s1 = state(1)
    s0.outpaths = {'a': s1, 'b': s0}
    s1.outpaths = {'a': s0, 'b': s1}
    d = DFA([s0, s1])
    d.start_state = s0
    d.accept_states = [s0]
    d.alphabet = ['a', 'b']
    print(d.all_regex(False) + '\n')

#test1()

def test2():
    #1b in HW3 in Automata & Computability
    print('Test 2')
    s0 = state(0)
    s1 = state(1)
    s0.outpaths = {'a': s0, 'b': s1}
    s1.outpaths = {'a': s1, 'b': s0}
    d = DFA([s0, s1])
    d.start_state = s0
    d.accept_states = [s1]
    d.alphabet = ['a', 'b']
    print(d.all_regex() +'\n')

#test2()

def test3():
    #1d in HW3 in Automata & Computability
    print('Test 3')
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s0.outpaths = {'a': s2, 'b': s1}
    s1.outpaths = {'a': s3, 'b': s0}
    s2.outpaths = {'a': s0, 'b': s3}
    s3.outpaths = {'a': s1, 'b': s2}
    d = DFA([s0, s1, s2, s3])
    d.start_state = s0
    d.accept_states = [s1]
    d.alphabet = ['a', 'b']
    print(d.all_regex() + '\n')

test3()

def test4():
    #pg 17 Example 3.2 from Automata & Computability
    #accepts strings w/ 3 consecutive a's
    print('Test 4')
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

#test4()

def test5():
    #accepts any variant of a(ba)*a
    print('Test 5')
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

#test5()

def test6():
    #Example 13.2 from Automata & Computability
    #accepts {a,b} and any strings with 3+ characters
    print('Test 6')
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
    print(d.all_regex())

#test6()
