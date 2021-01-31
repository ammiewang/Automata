from automata.state import state
from automata.dfa import DFA

class NFA():
    def __init__(self, states):
        self.start_states = []
        self.accept_states = []
        self.states = states
        self.alphabet = []

    def e_transitions(self):
        for state in self.states:
            state.only_eps = set()
            if 'ε' in state.outpaths:
                original_states = set(state.outpaths['ε'])
                ep_states = set(state.outpaths['ε'])
                while len(ep_states) > 0:
                    possible_ep_states = set()
                    for state2 in ep_states:
                        if 'ε' in state2.outpaths:
                            for st in state2.outpaths['ε']:
                                if st not in possible_ep_states and st not in original_states:
                                    original_states.add(st)
                                    possible_ep_states.add(st)
                    ep_states = possible_ep_states
                state.only_eps = original_states

        #print([st.id for st in self.states])
        for state in self.states:
            state.ep_outpaths = {}
            for char in self.alphabet:
                if char in state.outpaths:
                    state.ep_outpaths[char] = set(state.outpaths[char])
                    for state2 in state.outpaths[char]:
                        if 'ε' in state2.outpaths:
                            state.ep_outpaths[char] = state.ep_outpaths[char].union(state2.only_eps)
                elif 'ε' in state.outpaths:
                    ep_states = set(state.outpaths['ε'])
                    acc_states = set(self.accept_states)

                    if state not in acc_states and \
                    len(state.only_eps.intersection(acc_states)) != 0 \
                    and type(state.id) != set:
                        self.accept_states.append(state)

                    visited = set()
                    while len(ep_states) > 0:
                        possible_ep_states = set()
                        for st in ep_states:
                            if 'ε' in st.outpaths:
                                for st2 in st.outpaths['ε']:
                                    if st2 not in possible_ep_states and st2 not in visited:
                                        possible_ep_states.add(st2)
                                        visited.add(st2)
                                        #print('inhere')
                            if char in st.outpaths:
                                #print(char)
                                #print(st.outpaths[char][0].id)
                                for st2 in st.outpaths[char]:
                                    if char not in state.ep_outpaths: #and st2 not in found:
                                        state.ep_outpaths[char] = set([st2])
                                        state.ep_outpaths[char] = state.ep_outpaths[char].union(st2.only_eps)
                                    elif st2 not in state.ep_outpaths[char]: #and st2 not in found:
                                        state.ep_outpaths[char].add(st2)
                                        state.ep_outpaths[char] = state.ep_outpaths[char].union(st2.only_eps)
                        ep_states = possible_ep_states



    def nfa_to_dfa(self):
        try: self.alphabet.remove('ε')
        except: pass

        self.new_ss = state({s.id for s in self.start_states})
        temp_op = {key: set() for key in self.alphabet + ['ε']}
        for ss in self.start_states:
            for k,v in ss.outpaths.items():
                set_v = set(v)
                temp_op[k] = temp_op[k].union(set_v)
        self.new_ss.outpaths = {k:list(v) for k,v in temp_op.items()}
        self.new_ss.made_of = set(self.start_states)
        self.states.append(self.new_ss)

        self.e_transitions()
        if 'ε' in self.new_ss.outpaths:
            del self.new_ss.outpaths['ε']

        existing_states = [self.new_ss.made_of]
        new_states = [self.new_ss]
        dfa_states = [self.new_ss]

        while len(new_states) > 0:
            next_round = []
            for es in new_states:
                new_dict = {key: set() for key in self.alphabet}
                for sub_state in es.made_of:
                    for char, states in sub_state.ep_outpaths.items():
                        new_dict[char] = new_dict[char].union(states)
                for char,states in new_dict.items():
                    if states not in existing_states:
                        id = set([s.id for s in states])
                        if id == set():
                            id = '∅'
                        new_state = state(id)
                        new_state.made_of = states
                        es.outpaths[char] = new_state
                        dfa_states.append(new_state)
                        existing_states.append(states)
                        next_round.append(new_state)
                    else:
                        for x in dfa_states:
                            if x.made_of == states:
                                es.outpaths[char] = x
                                break
            new_states = next_round

        self.my_dfa = DFA(dfa_states)
        self.my_dfa.alphabet = self.alphabet
        self.my_dfa.start_state = self.new_ss

        acc_ids = {st.id for st in self.accept_states}
        for st in self.my_dfa.states:
            for s in st.made_of:
                if s.id in acc_ids:
                    self.my_dfa.accept_states.append(st)
                    break
