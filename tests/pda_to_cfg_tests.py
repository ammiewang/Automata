from automata.pda import PDA
from automata.state import state

def test1():
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
test1()
