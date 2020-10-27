class Regex:
    def __init__(self, ex):
        new_ex = ex.replace(' ', '')
        self.regex = new_ex
        self.syms = {'+', '*', '(', ')'}

    def get_alph(self):
        self.alphabet = set()
        for char in self.regex:
            if char not in self.syms and char not in self.alphabet and char != 'ε':
                self.alphabet.add(char)

    def make_nfa_part(self, part, num):
        if '*' not in part:
            states = [state(i) for i in range(num, num + len(part) + 1)]
            for i in range(len(states)-1):
                states[i].outpaths[part[i]] = [states[i+1]]
            return states, num + len(part) + 1
        else:
            starred_letters_index = set()
            for i in range(len(part)):
                if part[i] == '*':
                    starred_letters_index.add(i-1)

            states = [state(num)]
            num += 1
            i = 0
            while i < len(part):
                if i not in starred_letters_index:
                    new_state = state(num)
                    if part[i] in states[-1].outpaths:
                        states[-1].outpaths.append(new_state)
                    else:
                        states[-1].outpaths[part[i]] = [new_state]
                    states.append(new_state)
                    num += 1
                    i += 1
                else:
                    if part[i] in states[-1].outpaths:
                        states[-1].outpaths.append(states[-1])
                    else:
                        states[-1].outpaths[part[i]] = [states[-1]]
                    if i < len(part)-2 and i+2 in starred_letters_index:
                        new_state = state(num)
                        if 'ε' in states[-1].outpaths: #check not necessary unless 'ε' in alphabet?
                            states[-1].outpaths['ε'].append(new_state)
                        else:
                            states[-1].outpaths['ε'] = [new_state]
                        states.append(new_state)
                        num += 1
                    i += 2
            return states, num

    def get_parts(self):
        strs = []
        str = ''
        for i in range(len(self.regex)):
            if self.regex[i] not in self.syms:
                str += self.regex[i]
            elif self.regex[i] == '*':
                if self.regex[i-1] not in self.syms:
                    str += self.regex[i]
            else:
                if len(str) != 0:
                    strs.append(str)
                    str = ''
        if len(str) != 0:
            strs.append(str)

        num = 0
        parts_dict = {}
        for str in strs:
            states, num = self.make_nfa_part(str, num)
            if str in parts_dict:
                parts_dict[str].append(states)
            else:
                parts_dict[str] = [states]

        self.parts_dict = parts_dict
        #print([(key, len(parts_dict[key])) for key in parts_dict])
        self.count_dict = {k: 0 for k in self.parts_dict}
        self.num = num

    def plus(self, nfa_parts, finalize=False):
        if len(nfa_parts) == 1:
            if finalize:
                self.my_nfa.start_states = [nfa_parts[0][0]]
                self.my_nfa.accept_states = [nfa_parts[0][-1]]
            return nfa_parts[0]
        else:
            new_state = state(self.num)
            self.num += 1
            new_state.outpaths = {'ε': [states[0] for states in nfa_parts]}
            new_state2 = state(self.num)
            self.num += 1
            new_states = [new_state]
            for states in nfa_parts:
                if 'ε' not in states[-1].outpaths:
                    states[-1].outpaths['ε'] = [new_state2]
                else:
                    states[-1].outpaths['ε'].append(new_state2)
                new_states += states
            new_states += [new_state2]
            if finalize:
                self.my_nfa.start_states = [new_states[0]]
                self.my_nfa.accept_states = [new_states[-1]]
            return new_states

    def kleene_star(self, states):
        if 'ε' not in states[-1].outpaths:
            states[-1].outpaths['ε'] = [states[0]]
        else:
            states[-1].outpaths['ε'].append(states[0])
        if 'ε' not in states[0].outpaths:
            states[0].outpaths['ε'] = [states[-1]]
        else:
            states[0].outpaths['ε'].append(states[-1])
        return states

    def concat(self, nfa_parts):
        if len(nfa_parts) == 1:
            return nfa_parts[0]

        for i in range(len(nfa_parts)-1):
            if 'ε' not in nfa_parts[i][-1].outpaths:
                nfa_parts[i][-1].outpaths['ε'] = [nfa_parts[i+1][0]] #check for epsilon?
            else:
                nfa_parts[i][-1].outpaths['ε'].append(nfa_parts[i+1][0])

        new_nfa_parts = []
        for part in nfa_parts:
            new_nfa_parts += part

        return new_nfa_parts

    def exp_parts(self, part, round):

        if part in self.parts_dict:
            idx = self.count_dict[part]
            self.count_dict[part] += 1
            if round == 0:
                self.my_nfa.start_states = [self.parts_dict[part][idx][0]]
                self.my_nfa.accept_states = [self.parts_dict[part][idx][-1]]
            return self.parts_dict[part][idx]

        elif '(' not in part:
            parts = part.split('+')
            lst = []
            for key in parts:
                idx = self.count_dict[key]
                self.count_dict[key] += 1
                lst.append(self.parts_dict[key][idx])
            if round == 0:
                return plus(lst, finalize=True)
            return self.plus(lst)

        else:
            pluses = []
            paren_count = 0
            for i in range(len(part)):
                if part[i] == '(':
                    paren_count += 1
                elif part[i] == ')':
                    paren_count -= 1
                elif paren_count == 0 and part[i] == '+':
                    pluses.append(i)

            prev = 0
            plus_parts = []
            for idx in pluses:
                plus_parts.append(part[prev:idx])
                prev = idx + 1
            plus_parts.append(part[prev:])

            if len(plus_parts) == 0:
                plus_parts = [part]

            #concat_parts = [[] for p in plus_parts]
            concat_parts = []
            for pp in plus_parts:
                if '(' not in pp:
                    concat_parts.append([(pp, False)])
                else:
                    paren_count = 0
                    pairs = []
                    str = ''
                    for i in range(len(pp)):
                        if pp[i] == '(':
                            if paren_count == 0:
                                if len(str) > 0:
                                    pairs.append((str, False),)
                                    str = ''
                                opening = i
                            else:
                                str += pp[i]
                            paren_count += 1
                        elif pp[i] == ')':
                            paren_count -= 1
                            if paren_count == 0:
                                if i < len(pp)-1 and pp[i+1] == '*':
                                    pairs.append((str, True,),)
                                else:
                                    pairs.append((str, False),)
                                str = ''
                            else:
                                str += pp[i]
                        elif paren_count != 0 or (paren_count == 0 and pp[i] != '*') \
                        or (i > 0 and pp[i-1] != ')' and paren_count == 0 and pp[i] == '*'):
                            str += pp[i]

                    if len(str) != 0:
                        pairs.append((str, False),)

                    concat_parts.append(pairs)

            new_plus = []
            for cp in concat_parts:
                new_concat = []
                for str, klst in cp:
                    #print(str)
                    nfa_part = self.exp_parts(str, round+1)
                    if klst:
                        nfa_part = self.kleene_star(nfa_part)
                    new_concat.append(nfa_part)
                new_plus.append(new_concat)

            final_plus = []
            for cc in new_plus:
                final_plus.append(self.concat(cc))

            if round == 0:
                return self.plus(final_plus, finalize=True)

            return self.plus(final_plus)

    def nfa_maker(self):
        self.get_alph()
        self.my_nfa = NFA([])
        self.get_parts()
        states = self.exp_parts(self.regex, 0)
        self.my_nfa.states = states
        self.my_nfa.alphabet = list(self.alphabet)

    def dfa_maker(self):
        self.nfa_maker()
        self.my_nfa.nfa_to_dfa()
        self.my_dfa = self.my_nfa.my_dfa
        self.my_dfa.alphabet = list(self.alphabet)
        self.my_dfa.minimize()

    def complement_maker(self, rand=True):
        self.dfa_maker()
        self.my_dfa.take_dfa_complement()
        self.complement = self.my_dfa.complement.all_regex(rand)
