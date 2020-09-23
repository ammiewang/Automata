from automata.pda import PDA
from automata.state import state

def test1():
    #strings in the language {a^n b^n | n >= 1}
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s0.outpaths = {('a', 'A'): {(s0, 'AA')}, ('a', '$'): {(s0, 'A$')}, ('b', 'A'): {(s1, 'ε')}}
    s1.outpaths = {('b', 'A'): {(s1, 'ε')}, ('ε', '$'): {(s2, 'ε')}}
    p = PDA({s0,s1,s2})
    p.input_alphabet = {'a', 'b'}
    p.stack_symbols = {'$', 'A', 'B'}
    p.start_state = s0
    p.accept_states = {s2}
    p.to_cfg()
    p.my_cfg.print_converted_cfg()
#test1()

def test2():
    #strings in the language {a^m b^m c^n d^n | m,n >= 1}
    #https://scanftree.com/automata/dpda-for-a-to-power-n-b-to-power-n-c-to-power-m-d-to-power-m
    s0 = state(0)
    s1 = state(1)
    s2 = state(2)
    s3 = state(3)
    s4 = state(4)
    s0.outpaths = {('a', 'A'): {(s0, 'AA')}, ('a', '$'): {(s0, 'A$')}, ('b', 'A'): {(s1, 'ε')}}
    s1.outpaths = {('b', 'A'): {(s1, 'ε')}, ('c', '$'): {(s2, 'C$')}}
    s2.outpaths = {('c', 'C'): {(s2, 'CC')}, ('d', 'C'): {(s3, 'ε')}}
    s3.outpaths = {('d', 'C'): {(s3, 'ε')}, ('ε', '$'): {(s4, 'ε')}}
    p = PDA({s0,s1,s2,s3,s4})
    p.input_alphabet = {'a', 'b'}
    p.stack_symbols = {'$', 'A', 'B'}
    p.start_state = s0
    p.accept_states = {s4}
    p.to_cfg()
    p.my_cfg.print_converted_cfg()
#test2()
