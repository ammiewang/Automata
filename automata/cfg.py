import string

class CFG:
    def __init__(self, rules):
        self.start = None
        self.rules = rules #{nonterminal:productions}
        self.terminals = set()
        self.nonterminals = set()
        self.new_syms = list(string.ascii_uppercase) # TODO: need backup alphabet in case we run out
        self.other_terminals = set(['+', '-', '*', '/', '%', '^', '(', ')', '[', ']', '{', '}', '!', '=', '~'])
        self.firsts_found = False
        self.follows_found = False
        self.predicts_found = False
        #self.new_syms = ['α', 'β', 'ξ', 'δ', 'φ', 'γ', 'η', 'ι', 'ς', 'κ', 'λ', 'μ', 'ν', 'π', 'θ', 'ρ', 'σ', 'τ', 'υ', 'ω', 'χ', 'ψ', 'ζ']
        #all letters in ^ are lowercase

    def find_terms_nonterms(self):
        self.terminals = set()
        self.nonterminals = set()
        for nt, prods in self.rules.items():
            for str in prods:
                for char in str:
                    term = self.is_terminal(char)
                    if term and char not in self.terminals:
                        self.terminals.add(char)
                    elif not term and char not in self.nonterminals:
                        self.nonterminals.add(char)

        if self.start not in self.nonterminals:
            self.nonterminals.add(self.start)

        for c in self.nonterminals:
            if c in self.new_syms:
                self.new_syms.remove(c)

    def is_terminal(self, str):
        try:
            return str.islower() or str == 'ε' or str in self.other_terminals
        except:
            for s in str:
                if not (s.islower() or s == 'ε' or str in self.other_terminals):
                    return False
            return True

    def nts_for_terms(self):
        new_nonterms = set()
        for nt, prod in self.rules.items():
            for str in prod:
                if self.is_terminal(str) and nt not in new_nonterms:
                    new_nonterms.add(nt)
        return new_nonterms

    def reachable_from_nt(self, ch):
        cont = True
        visited = set()
        curr = set([ch])
        while cont:
            cont = False
            next = set()
            for nt in curr:
                if nt in self.rules:
                    prods = self.rules[nt]
                    for str in prods:
                        for char in str:
                            if not self.is_terminal(char) and char not in visited:
                                next.add(char)
                                visited.add(char)
                                cont = True
            curr = next

        return visited

    def elim_nonterminating(self):
        new_rules = {}
        new_nonterms = self.nts_for_terms()
        self.find_terms_nonterms()
        reaches = {}
        nonexistent = set()

        curr = self.rules.copy()
        cont = True
        while cont:
            cont = False
            for nt, prods in curr.items():
                new_rules[nt] = []
                for str in prods:
                    include = True
                    for char in str:
                        x = self.reachable_from_nt(nt)
                        if (not self.is_terminal(char) and char not in self.rules) or \
                        (not self.is_terminal(char) and \
                        len(x.intersection(new_nonterms)) == 0 \
                        and char not in new_nonterms):
                            include = False
                            break
                    if include:
                        new_rules[nt].append(str)
                    else:
                        cont = True
                if len(new_rules[nt]) == 0:
                    del new_rules[nt]
            curr = new_rules.copy()
            self.rules = new_rules.copy()

        self.rules = new_rules

    def elim_unreachable(self):
        #new_rules = {self.start: self.rules[self.start]}
        new_rules = {}
        curr_nonterms = set([self.start])
        #visited = set()
        cont = True
        while cont:
            add_nonterms = set()
            cont = False
            for nt in curr_nonterms:
                #if nt not in new_rules: shouldn't need this check
                new_rules[nt] = self.rules[nt]
                for str in self.rules[nt]:
                    if not self.is_terminal(str):
                        for char in str:
                            if char not in add_nonterms and not \
                            self.is_terminal(char) and char not in new_rules:
                            #and char not in visited (same as char not in new_rules):
                                #visited.add(char)
                                add_nonterms.add(char)
                                cont = True
            curr_nonterms = add_nonterms

        self.rules = new_rules

    def unit_prods(self):
        unit_prods = {}
        not_unit_prods = {}
        for nt, prod in self.rules.items():
            for str in prod:
                if len(str) == 1 and not self.is_terminal(str): #change isupper in case of list
                    if nt in unit_prods:
                        unit_prods[nt].append(str)
                    else:
                        unit_prods[nt] = [str]
                else:
                    if nt in not_unit_prods:
                        not_unit_prods[nt].append(str)
                    else:
                        not_unit_prods[nt] = [str]

        return unit_prods, not_unit_prods

    def find_unit_prod_pairs(self):
        unit_productions, not_unit_prods = self.unit_prods()

        new_unit_prod = {}
        for nt,prods in unit_productions.items():
            new_prods = set()
            curr_prods = prods[:]
            while len(curr_prods) > 0:
                add_to_prods = set()
                for nt2 in curr_prods:
                    if nt2 not in new_prods:
                        new_prods.add(nt2)
                        if nt2 in unit_productions:
                            add_to_prods = add_to_prods.union(unit_productions[nt2])
                curr_prods = add_to_prods
            new_unit_prod[nt] = new_prods

        return new_unit_prod, not_unit_prods

    def elim_unit(self):
        new_no_unit_prod = {}
        unit_prods, not_unit_prods = self.find_unit_prod_pairs()
        for nt,prods in unit_prods.items():
            try:
                new_prods = not_unit_prods[nt][:]
            except:
                new_prods = []
            for nt2 in prods:
                if nt != nt2:
                    if nt2 in not_unit_prods:
                        new_prods += not_unit_prods[nt2][:]
            new_no_unit_prod[nt] = new_prods

        for nt, prods in self.rules.items():
            if nt not in new_no_unit_prod:
                new_no_unit_prod[nt] = prods

        for nt, prods in new_no_unit_prod.items():
            new_no_unit_prod[nt] = self.unique(prods)

        self.rules = new_no_unit_prod
        self.reduce()

    def find_null_prod(self, grammar):
        nts_to_replace = set()
        for nt, prods in grammar.items():
            if 'ε' in prods:
                nts_to_replace.add(nt)
        return nts_to_replace

    def enum_strs(self, str, all_letters, null_prods):
        if len(all_letters) == 0:
            if str == '':
                return ['ε']
            else:
                return [str]
        else:
            if all_letters[0] not in null_prods:
                return self.enum_strs(str+all_letters[0], all_letters[1:], null_prods)
            else:
                return self.enum_strs(str+all_letters[0], all_letters[1:], null_prods) + \
                self.enum_strs(str, all_letters[1:], null_prods)

    def unique(self, lst):
        new_lst = []
        for x in lst:
            if x not in new_lst:
                new_lst.append(x)
        return new_lst

    def elim_null(self):
        new_grammar = self.rules
        nts_to_replace = self.find_null_prod(new_grammar)
        cont = True if len(nts_to_replace) > 0 else False
        all_nts_to_replace = nts_to_replace.copy()

        while cont:
            cont = False
            start_ep = True if self.start in nts_to_replace else False
            strs = {}
            for nt, prods in new_grammar.items():
                for str in prods:
                    for char in str:
                        if char in nts_to_replace:
                            if nt not in strs:
                                strs[nt] = [str]
                            else:
                                strs[nt].append(str)
                            break

            for nt, prods in strs.items():
                for str in prods:
                    new_prods = self.enum_strs('', str, nts_to_replace) #take self.unique() of this?
                    new_grammar[nt].remove(str)
                    new_grammar[nt] += new_prods

            for nt, prods in new_grammar.items():
                if 'ε' in prods and nt in all_nts_to_replace and nt != self.start:
                    new_grammar[nt].remove('ε')

            nts_to_replace = self.find_null_prod(new_grammar)#.difference(all_nts_to_replace)
            all_nts_to_replace = all_nts_to_replace.union(nts_to_replace)
            #print(self.find_null_prod(new_grammar), nts_to_replace, all_nts_to_replace)

            if len(nts_to_replace) > 0:
                cont = False if nts_to_replace == set([self.start]) and start_ep else True
            else:
                cont = False

        for nt, prods in new_grammar.items():
            new_grammar[nt] = self.unique(prods)

        new_grammar = {k:v for k,v in new_grammar.items() if len(v) > 0}
        self.rules = new_grammar
        self.reduce()

    def reduce(self):
        self.elim_nonterminating()
        self.elim_unreachable()
        #make sure all productions of a nonterminal are unique?

    def reduce_no_units_or_nulls(self):
        self.reduce()
        self.elim_null()
        self.elim_unit()
        #make sure all productions of a nonterminal are unique?

    def new_ss(self):
        while self.new_syms[0] in self.rules:
            self.new_syms.pop(0)
        new_start = self.new_syms.pop(0)
        self.rules[new_start] = [self.start]
        self.start = new_start

    def replace_terms(self):
        self.find_terms_nonterms()
        new_nt = {}
        new_nt_rev = {}
        already_exists = set()
        for nt, prods in self.rules.items():
            if len(prods) == 1 and self.is_terminal(prods[0]):
                already_exists.add(prods[0])
                new_nt_rev[prods[0]] = nt

        for t in self.terminals:
            if t not in already_exists:
                if t != 'ε' and t.upper() not in self.nonterminals:
                    new_nt[t.upper()] = [t]
                    new_nt_rev[t] = t.upper()
                    if t.upper() in self.new_syms:
                        self.new_syms.remove(t.upper())
                    self.nonterminals.add(t.upper())
                else:
                    new_nt[self.new_syms[0]] = [t]
                    new_nt_rev[t] = self.new_syms[0]
                    self.nonterminals.add(self.new_syms.pop(0))

        new_rules = {}
        for nt, prods in self.rules.items():
            new_prods = []
            for str in prods:
                new_str = str
                for char in str:
                    if self.is_terminal(char) and len(str) != 1:
                        new_str = new_str.replace(char, new_nt_rev[char])
                new_prods.append(new_str)
            new_rules[nt] = new_prods

        new_rules.update(new_nt)
        self.rules = new_rules

    def replace_long_seqs(self):
        new_rules = {}
        new_nt = {}
        new_nt_rev = {}
        for nt, prods in self.rules.items():
            new_prods = []
            for str in prods:
                new_str = str
                while len(new_str) > 2:
                    nt2 = new_str[-2:]
                    if nt2 not in new_nt_rev:
                        new_nt[self.new_syms[0]] = [nt2]
                        new_nt_rev[nt2] = self.new_syms[0]
                        sym = self.new_syms.pop(0)
                    else:
                        sym = new_nt_rev[nt2]
                    new_str = new_str[:-2] + sym
                new_prods.append(new_str)
            new_rules[nt] = new_prods

        new_rules.update(new_nt)
        self.rules = new_rules

    def determine_ordering(self):
        ordering = [self.start]
        cont = True
        nts = set(self.start)
        while cont:
            cont = False
            new_nts = set()
            for nt in nts:
                prods = self.rules[nt]
                for str in prods:
                    for char in str:
                        if not self.is_terminal(char) and char not in ordering:
                            ordering.append(char)
                            new_nts.add(char)
                            cont = True
            nts = new_nts
        self.ordering = ordering

    def substitute(self, str):
        new_prod = []
        char = str[0]
        postfix = str[1:]
        for prod in self.rules[char]:
            new_prod.append(prod + postfix)
        return new_prod

    def check(self, prods, i):
        rep = set()
        new_nt = set()
        for prod in prods:
            char = prod[0]
            if not self.is_terminal(char):
                j = self.ordering.index(char)
                if i > j:
                    rep.add(prod)
                elif i == j:
                    new_nt.add(prod)

        return new_nt, rep

    def subs(self, i):
        new_prod = []
        nt = self.ordering[i]
        new_nt, rep = self.check(self.rules[nt], i)
        to_rm = new_nt.union(rep)
        all_left_recs = set(new_nt.copy())
        cont = True if len(rep) > 0 else False
        new_prods = []

        while cont:
            cont = False
            new_prods = []
            nt2 = set()

            for prod in rep:
                x = self.substitute(prod)
                eq, gt = self.check(x, i)
                nt2 = nt2.union(gt)
                all_left_recs = all_left_recs.union(eq)
                if len(gt) > 0:
                    cont = True
                new_prods += x

            rep = nt2

        new_nts = {}
        postfixes = {}
        new_nt_sym = None

        if len(all_left_recs) > 0:
            new_nt_sym = self.new_syms.pop(0)
            dict = self.elim_left_rec(all_left_recs, new_nt_sym)
            new_nts.update(dict)
            new_prods.append(nt+new_nt_sym)
            for lr in all_left_recs:
                try:
                    new_prods.remove(lr)
                except:
                    continue

        for exp in to_rm:
            self.rules[nt].remove(exp)
        self.rules[nt] += new_prods

        return new_nts, new_nt_sym

    def check_ij_form(self):
        new_nts = {}
        left_rec = {}
        for i in range(len(self.ordering)):
            nnts, sym = self.subs(i)
            if len(nnts) > 0:
                new_nts.update(nnts)
                left_rec[self.ordering[i]] = self.ordering[i] + sym

        new_nts.update(self.rules)
        self.rules = new_nts
        self.left_rec = left_rec


    def elim_left_rec(self, strs, new_nt):
        dict = {new_nt: []}
        for str in strs:
            postfix = str[1:]
            dict[new_nt] += [postfix + new_nt, postfix]
        return dict

    def fix_gnform(self):
        original = set()
        for i in range(len(self.ordering)-1, -1, -1): #
            nt = self.ordering[i]
            if nt in self.left_rec:
                lr = self.left_rec[nt]
                self.rules[nt].remove(lr)
                new_prods = []
                for prod in self.rules[nt]:
                    new_prods.append(prod + lr[1:])
                self.rules[nt] += new_prods

            new_prods = []
            for str in self.rules[nt]:
                first_char = str[0]
                if not self.is_terminal(first_char):
                    new_prods += self.substitute(str)
                else:
                    new_prods += [str]
            self.rules[nt] = new_prods
            original.add(nt)

        new_rules = {}
        for nt, prods in self.rules.items():
            if nt not in original:
                new_prods = []
                for str in prods:
                    first_char = str[0]
                    if not self.is_terminal(first_char):
                        new_prods += self.substitute(str)
                    else:
                        new_prods += [str]
                new_rules[nt] = new_prods
            else:
                new_rules[nt] = prods

        self.rules = new_rules

    def convert_to_cnf(self):
        self.new_ss()
        self.elim_null()
        self.elim_unit()
        self.replace_terms()
        self.replace_long_seqs()
        self.reduce()

    def convert_to_gnf(self):
        #self.find_terms_nonterms()
        self.convert_to_cnf()
        self.determine_ordering()
        self.check_ij_form()
        self.fix_gnform()
        self.reduce()

    def convert_to_pda(self):
        self.convert_to_gnf()

        s = state(0)
        p = PDA(set([s]), self.start)
        self.find_terms_nonterms()
        p.alphabet = self.terminals.difference(set(['ε']))
        p.stack_symbols = self.nonterminals.union(p.alphabet)
        terms = self.terminals.difference(set(['ε']))

        for t in terms:
            s.outpaths[(t, t)] = set([(s, 'ε')])

        for nt in self.nonterminals:
            prods = self.rules[nt]
            for str in prods:
                if ('ε', nt) in s.outpaths:
                    s.outpaths[('ε', nt)].add((s, str))
                else:
                    s.outpaths[('ε', nt)] = set([(s, str)])

        self.my_pda = p
        self.my_pda.start_state = s

    def elim_left_rec_with_ep(self):
        new_rules = {}
        for nt, prods in self.rules.items():
            new_nt_made = False
            new_rules[nt] = []
            nonrecursing = set()
            for prod in prods:
                if prod[0] == nt:
                    if not new_nt_made:
                        while self.new_syms[0] in self.rules:
                            self.new_syms.pop(0)
                        new_nt = self.new_syms.pop(0)
                        new_rules[new_nt] = ['ε']
                        new_nt_made = True
                    new_rules[new_nt].append(prod[1:] + new_nt)
                else:
                    nonrecursing.add(prod)
            if not new_nt_made:
                new_rules[nt] = prods
            else:
                for prod in nonrecursing:
                    if prod != 'ε':
                        new_rules[nt].append(prod + new_nt)
                    else:
                        new_rules[nt].append(prod)
        self.rules = new_rules

    def check_repeats(self, nt, prods):
        firsts = {}
        for prod in prods:
            try:
                if prod[0] not in firsts:
                    firsts[prod[0]] = [prod]
                else:
                    firsts[prod[0]].append(prod)
            except:
                pass
        return firsts

    def elim_common_subexpr_round(self):
        new_rules = {}
        new_round = False
        for nt, prods in self.rules.items():
            firsts = self.check_repeats(nt, prods)
            new_rules[nt] = []
            #prods_temp = prods[:]
            if len(firsts) == len(prods):
                new_rules[nt] = prods
            else:
                new_round = True
                for key, val in firsts.items():
                    if len(val) == 1:
                        new_rules[nt].append(val[0])
                    else:
                        while self.new_syms[0] in self.rules:
                            self.new_syms.pop(0)
                        new_nt = self.new_syms.pop(0)
                        new_rules[new_nt] = []
                        for prod2 in val:
                            if len(prod2[1:]) >= 1:
                                new_rules[new_nt].append(prod2[1:])
                            else:
                                new_rules[new_nt].append('ε')
                        new_rules[nt].append(key + new_nt)
        self.rules = new_rules
        return new_round

    def elim_common_subexpression(self):
        cont = True
        while cont:
            cont = self.elim_common_subexpr_round()

    def find_all_null_possible(self):
        cont = True
        eps = self.find_null_prod(self.rules)
        while cont:
            cont = False
            new_eps = set()
            for nt, prods in self.rules.items():
                for prod in prods:
                    is_ep = True
                    for char in prod:
                        if char not in eps:
                            is_ep = False
                            break
                    if is_ep:
                        new_eps.add(nt)
                        cont = True
            eps = eps.union(new_eps)
        return eps

    def prod_first_set(self, prod):
        if not self.firsts_found:
            self.first_sets()
        first = set()

        if self.is_terminal(prod[0]):
            return set([prod[0]])
        else:
            while len(prod) > 0 and not self.is_terminal(prod[0]) and 'ε' in self.firsts[prod[0]]:
                first = first.union(fs[prod[0]]).difference('ε')
                prod = prod[1:]
            if len(prod) == 0:
                first.add('ε')
            elif self.is_terminal(prod[0]):
                first.add(prod[0])
            else:
                first = first.union(self.firsts[prod[0]])
            return first


    def first_sets(self):
        first_sets_dict = {}
        also_inherits_from = {}
        eps = self.find_all_null_possible()
        self.eps = eps

        for nt, prods in self.rules.items():
            first_sets_dict[nt] = set()
            also_inherits_from[nt] = set()
            for prod in prods:
                if self.is_terminal(prod[0]):
                    first_sets_dict[nt].add(prod[0])
                else:
                    also_inherits_from[nt].add(prod[0])
                    str = prod
                    while str[0] in eps:
                        str = str[1:]
                        if len(str) > 0:
                            also_inherits_from[nt] = also_inherits_from[nt].union(set([str[0]]))
                        else:
                            break

        for nt in first_sets_dict:
            if nt in eps and 'ε' not in first_sets_dict[nt]:
                first_sets_dict[nt].add('ε')

        for nt, other_nts in also_inherits_from.items():
            cont = True
            temp = other_nts
            visited = set([nt])
            while cont:
                cont = False
                for prod in temp:
                    if prod not in visited:
                        temp = temp.union(also_inherits_from[prod]).difference(set([nt])) #difference part optional
                        visited.add(prod)
                        cont = True
            also_inherits_from[nt] = temp

        for nt, other_nts in also_inherits_from.items():
            for prod in other_nts:
                first_wo_ep = first_sets_dict[prod].difference('ε')
                first_sets_dict[nt] = first_sets_dict[nt].union(first_wo_ep)

        self.firsts = first_sets_dict
        self.firsts_found = True
        return first_sets_dict

    def follow_sets(self):
        if not self.firsts_found:
            self.first_sets()
        eps = self.find_all_null_possible()

        also_inherits_from_follow = {}
        follow_sets = {self.start: set(['$'])}

        for nt in self.rules:
            if nt != self.start:
                follow_sets[nt] = set()

            also_inherits_from_follow[nt] = set()

            for nt2, prods in self.rules.items():
                for prod in prods:
                    if nt in prod:
                        ind_of_nt = prod.index(nt)
                        if ind_of_nt == len(prod)-1:
                            also_inherits_from_follow[nt].add(nt2)
                        elif self.is_terminal(prod[ind_of_nt+1]): #should never be epsilon
                            follow_sets[nt].add(prod[ind_of_nt+1])
                        else:
                            first_prod_set = self.prod_first_set(prod[ind_of_nt+1:])
                            follow_sets[nt] = follow_sets[nt].union(first_prod_set).difference('ε')

        for nt, other_nts in also_inherits_from_follow.items():
            cont = True
            temp = other_nts
            visited = set([nt])
            while cont:
                cont = False
                for prod in temp:
                    if prod not in visited:
                        temp = temp.union(also_inherits_from_follow[prod]).difference(set([nt])) #difference part optional
                        visited.add(prod)
                        cont = True
            also_inherits_from_follow[nt] = temp

        for nt, other_nts in also_inherits_from_follow.items():
            for prod in other_nts:
                follow_sets[nt] = follow_sets[nt].union(follow_sets[prod])

        self.follows = follow_sets
        self.follows_found = True
        return follow_sets

    def predict_sets(self):
        if not self.firsts_found:
            self.first_sets()
        if not self.follows_found:
            self.follow_sets()
        predict = {}
        for nt, prods in self.rules.items():
            for prod in prods:
                pfs = self.prod_first_set(prod)
                if 'ε' not in pfs:
                    predict[(nt,prod)] = pfs
                else:
                    predict[(nt,prod)] = pfs.difference('ε').union(self.follows[nt])
        self.predicts = predict
        return predict

    def make_parse_table(self):
        if not self.predicts_found:
            self.predict_sets()
        table = {}
        for key, vals in self.predicts.items():
            nt, prod = key
            for val in vals:
                if (nt, val) not in table:
                    table[(nt, val)] = set([prod])
                else:
                    table[(nt, val)].add(prod)
        self.parse_table = table


    def print_cfg(self):
        for nt, prods in self.rules.items():
            s = ''
            for str in prods:
                s += str + ' | '
            s = s[:-3]
            if nt != self.start:
                print(nt + ' --> ' + s)
            else:
                print(nt + '*' + ' --> ' + s)

    def print_converted_cfg(self):
        for nt, prods in self.rules.items():
            s = ''
            for str in prods:
                s2 = ' '.join(str)
                s += s2 + '  |  '
            s = s[:-5]
            if nt != self.start:
                print(nt + ' --> ' + s)
            else:
                print(nt + '*' + ' --> ' + s)
