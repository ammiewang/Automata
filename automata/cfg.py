import string

class CFG:
    def __init__(self, rules):
        self.start = None
        self.rules = rules #{nonterminal:productions}
        self.terminals = set()
        self.nonterminals = set()
        self.new_syms = list(string.ascii_uppercase) # TODO: need backup alphabet in case we run out
        #self.new_syms = ['α', 'β', 'ξ', 'δ', 'φ', 'γ', 'η', 'ι', 'ς', 'κ', 'λ', 'μ', 'ν', 'π', 'θ', 'ρ', 'σ', 'τ', 'υ', 'ω', 'χ', 'ψ', 'ζ']
        #all letters in ^ are lowercase

    def find_terms_nonterms(self):
        for nt, prods in self.rules.items():
            for str in prods:
                for char in str:
                    term = self.is_terminal(char)
                    if term and char not in self.terminals:
                        self.terminals.add(char)
                    elif not term and char not in self.nonterminals:
                        self.nonterminals.add(char)

        for c in self.nonterminals:
            self.new_syms.remove(c)

    def is_terminal(self, str):
        return str.islower() or str == 'ε'

    def elim_nonterminating(self):
        new_nonterms = set()
        for nt, prod in self.rules.items():
            for str in prod:
                if self.is_terminal(str) and nt not in new_nonterms:
                    new_nonterms.add(nt)

        visited = set()
        curr_nt = {nt for nt in new_nonterms}
        cont = True
        while cont:
            cont = False
            add_to_nonterms = set()
            for nt in curr_nt:
                for nt2, prod2 in self.rules.items():
                    for str in prod2:
                        if nt in str and nt2 not in add_to_nonterms and nt2 not in visited:
                            visited.add(nt2)
                            add_to_nonterms.add(nt2)
                            cont = True
            new_nonterms = new_nonterms.union(add_to_nonterms)
            curr_nt = add_to_nonterms

        new_rules = {}
        for nt, prod in self.rules.items():
            if nt in new_nonterms:
                new_rules[nt] = []
                for str in prod:
                    if self.is_terminal(str):
                        new_rules[nt].append(str)
                    else:
                        include = True
                        for char in str:
                            if not self.is_terminal(char) and char not in new_nonterms:
                                include = False
                        if include:
                            new_rules[nt].append(str)
        self.rules = new_rules

    def elim_unreachable(self):
        #new_rules = {self.start: self.rules[self.start]}
        new_rules = {}
        curr_nonterms = set(self.start)
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
                if len(str) == 1 and str.isupper():
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
        #print(not_unit_prods)
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
        #cont = True
        new_grammar = self.rules
        nts_to_replace = self.find_null_prod(new_grammar)
        cont = True if len(nts_to_replace) > 0 else False

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
                #if 'ε' in prods and nt != self.start and nt in nts_to_replace:
                if nt in nts_to_replace and nt != self.start:
                    new_grammar[nt].remove('ε')

            nts_to_replace = self.find_null_prod(new_grammar)

            if len(nts_to_replace) > 0:
                cont = False if nts_to_replace == set([self.start]) and start_ep else True
            else:
                cont = False

        for nt, prods in new_grammar.items():
            new_grammar[nt] = self.unique(prods)

        self.rules = new_grammar
        self.reduce()

    def reduce(self):
        self.elim_nonterminating()
        self.elim_unreachable()

    def reduce_no_units_or_nulls(self):
        self.reduce()
        self.elim_null()
        self.elim_unit()

    def new_ss(self):
        self.rules['0'] = self.start
        self.start = '0'

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
                if t.upper() not in self.nonterminals:
                    new_nt[t.upper()] = [t]
                    new_nt_rev[t] = t.upper()
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

    def convert_to_gnf(self):
        #self.find_terms_nonterms()
        self.convert_to_cnf()
        self.determine_ordering()
        self.check_ij_form()
        self.fix_gnform()

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
