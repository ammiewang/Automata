from automata.state import state
from automata.pda import PDA
from automata.cfg import CFG
from jsonifyAutomata import *

def make_pda(data):
    sts = set()
    num_transitions = len(data['transitions'])
    inp_alph = data['alphabet']
    stack_alph = data['stackAlphabet']
    id_to_st = {}

    for i in range(num_transitions):
        st1 = data['transitions'][i][0]
        inp1 = data['transitions'][i][1]
        stack1 = data['transitions'][i][2]
        st2 = data['transitions'][i][3]
        stack2 = data['transitions'][i][4]
        if st1 not in id_to_st:
            s = state(st1)
            sts.add(s)
            id_to_st[st1] = s
        if st2 not in id_to_st:
            s = state(st2)
            sts.add(s)
            id_to_st[st2] = s
        st = id_to_st[st1]
        if (inp1, stack1) not in st.outpaths:
            st.outpaths[(inp1, stack1)] = {(id_to_st[st2], stack2)}
        else:
            st.outpaths[(inp1, stack1)].add((id_to_st[st2], stack2))

    p = PDA(sts, data['initStackSym'])
    p.start_state = id_to_st[data['startStates']]
    p.input_alphabet = set(inp_alph)
    p.stack_symbols = set(stack_alph)
    #p.stack_symbols.add(p.init_stack_symbol)
    acc_list = data['acceptStates']
    p.accept_states = {id_to_st[i] for i in acc_list}
    return p

def make_cfg(data):
    if data['fromInput']:
        rules = {}
        nonterminals = data['nonterminals']
        productions = data['productions']
        start = 'S'
        i = 0
        for nt in nonterminals:
            prods = productions[i].split('|')
            new_prods = [str.split() for str in prods]
            if nt[-1] != '*':
                if nt not in rules:
                    rules[nt] = new_prods
                else:
                    rules[nt] += new_prods
            else:
                start = nt[:-1]
                if nt not in rules:
                    rules[nt[:-1]] = new_prods
                else:
                    rules[nt[:-1]] += new_prods
            i += 1
    else:
        rules = {}
        old_rules = data['rules']
        start = data['startSym']
        for nt, prods in old_rules.items():
            new_prods = [str.split() for str in prods]
            rules[nt] = new_prods

    c = CFG(rules)
    c.start = start
    return c

def pda2cfg(data):
    p = make_pda(data)
    p.print_pda()
    p.to_cfg()
    return make_cfg_json(p.my_cfg)

def simplify_grammar(data):
    c = make_cfg(data)
    c.reduce()
    #c.print_converted_cfg()
    return make_cfg_json(c)

def cnf(data):
    c = make_cfg(data)
    c.convert_to_cnf()
    #c.print_converted_cfg()
    return make_cfg_json(c)

def gnf(data):
    c = make_cfg(data)
    c.convert_to_gnf()
    #c.print_converted_cfg()
    return make_cfg_json(c)

def ffpSets(data):
    c = make_cfg(data)
    c.first_sets()
    #print(c.firsts)
    c.follow_sets()
    #print(c.follows)
    c.predict_sets()
    #print(c.predicts)
    return make_sets_json(c)

def leftRec(data):
    c = make_cfg(data)
    c.elim_left_rec_with_ep()
    return make_cfg_json(c)

def comSub(data):
    c = make_cfg(data)
    c.elim_common_subexpression()
    return make_cfg_json(c)

def elimNull(data):
    c = make_cfg(data)
    c.elim_null()
    return make_cfg_json(c)

def elimUnit(data):
    c = make_cfg(data)
    c.elim_unit()
    return make_cfg_json(c)

def cfg2pda(data):
    c = make_cfg(data)
    c.convert_to_pda()
    return make_pda_json(c.my_pda)

def parseTable(data):
    c = make_cfg(data)
    c.make_parse_table()
    #print(c.parse_table)
    return make_table_json(c)
