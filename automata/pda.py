from collections import deque
from random import choice
from automata.state import state

class PDA:
    def __init__(self, states, init_stack_sym=None):
        self.states = states #for each state in states,
        #state.outpaths would have the form {(inp_letter, on_stack): ([(resuling_state, replace_stack_top)]}
        self.start_state = None
        self.accept_states = set()#[]
        self.input_alphabet = set()#[]
        self.stack_symbols = set()#[]
        if init_stack_sym is None:
            self.init_stack_symbol = '$'
            self.stack_symbols.add('$')
        else:
            self.init_stack_symbol = init_stack_sym
            self.stack_symbols.add(init_stack_sym)
        self.stack = deque(self.init_stack_symbol)

    def to_cfg(self):
        from automata.cfg import CFG
        self.my_cfg = CFG({})

        self.count = 0
        self.state_names = {}
        new_rules = {'S': []}
        self.flatten_transitions()

        #1. all start state combos
        for st in self.states:
            n = self.namify(self.start_state, self.init_stack_symbol, st)
            self.state_names[n] = 'A' + str(self.count)
            new_rules['S'].append(['A' + str(self.count)])
            self.count += 1
        #2. look at all transitions
        for s1, inp, sym1, s2, sym2 in self.transitions:
            if sym2 == 'ε':
                n = self.namify(s1, sym1, s2)
                if n not in self.state_names:
                    self.state_names[n] = 'A' + str(self.count)
                    self.count += 1
                nt = self.state_names[n]
                if nt not in new_rules:
                    new_rules[nt] = []
                new_rules[nt].append([inp])
            else:
                for s3 in self.states:
                    n = self.namify(s1, sym1, s3)
                    if n not in self.state_names:
                        self.state_names[n] = 'A' + str(self.count)
                        self.count += 1
                    nt = self.state_names[n]
                    if nt not in new_rules:
                        new_rules[nt] = []
                    #get all combos for one [pXq]
                    lst = self.enumerate_nts(s2, sym2, s3)
                    if inp != 'ε':
                        lst = [[inp] + seq for seq in lst]
                    new_rules[nt] += lst

        self.my_cfg.rules = new_rules
        self.my_cfg.start = 'S'
        self.my_cfg.reduce()

    def enumerate_nts(self, s1, sym, sf):
        if len(sym) == 1:
            n = self.namify(s1, sym, sf)
            if n not in self.state_names:
                self.state_names[n] = 'A' + str(self.count)
                self.count += 1
            return [[self.state_names[n]]]
        else:
            lst = []
            for s in self.states:
                n = self.namify(s1, sym[0], s)
                if n not in self.state_names:
                    self.state_names[n] = 'A' + str(self.count)
                    self.count += 1
                prefix = [self.state_names[n]]
                postfixes = self.enumerate_nts(s, sym[1:], sf)
                for pf in postfixes:
                    lst.append(prefix + pf)
            return lst


    def namify(self, st1, sym, st2):
        return 'Q' + str(st1.id) + ' ' + sym + ' ' + 'Q' + str(st2.id)#

    def flatten_transitions(self):
        transitions = set()
        for s in self.states:
            for key, val in s.outpaths.items():
                for s2, sym in val:
                    transitions.add((s, key[0], key[1], s2, sym))
        self.transitions = transitions

    def print_pda(self):
        self.flatten_transitions()
        print('Start State:', self.start_state.id)
        print('Accept State(s):', [s.id for s in self.accept_states])
        print('Transitions:')
        for s1, inp, sym1, s2, sym2 in self.transitions:
            print('δ(', s1.id, ',', inp, ',', sym1, ')', '-->', '(', s2.id, ',', sym2, ')')
