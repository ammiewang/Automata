from automata.state import state
from automata.dfa import DFA

import json

def make_dfa_json(d):
    state_names = [str(s.id) for s in d.states]
    start_state = str(d.start_state.id)
    accept_states = [str(s.id) for s in d.accept_states]
    transitions = {str(s.id): {letter:str(s2.id) for letter, s2 in s.outpaths.items()} for s in d.states}
    alphabet = d.alphabet
    return {'stateNames': state_names, 'startState': start_state, 'acceptStates': accept_states,\
        'transitions': transitions, 'alphabet': alphabet}

def make_cfg_json(c):
    new_rules = {}
    for nt, prods in c.rules.items():
        new_rules[nt] = []
        for str in prods:
            s = ' '.join(str)
            new_rules[nt].append(s)
    return {'startSym': c.start, 'rules': new_rules}

def make_sets_json(c):
    new_firsts = {}
    for nt, fstset in c.firsts.items():
        new_firsts[nt] = list(fstset)

    new_follows = {}
    for nt, folset in c.follows.items():
        new_follows[nt] = list(folset)

    new_predicts = {}
    for prod, predset in c.predicts.items():
        lhs, rhs = prod
        new_predicts[lhs + ' → ' + rhs] = list(predset)

    all_sets = {'firsts': new_firsts, 'follows': new_follows, 'predicts': new_predicts}
    #all_sets.update(make_cfg_json(c))

    return all_sets

def make_pda_json(p):
    if len(p.transitions) == 0:
        p.flatten_transitions()
    if len(p.input_alphabet) == 0:
        p.get_input_alphabet()

    new_transitions = []
    for s1, inp, sym1, s2, sym2 in p.transitions:
        new_transitions.append([str(s1.id), inp, sym1, str(s2.id), ' '.join(sym2)])

    return {'transitions': new_transitions, 'startState': str(p.start_state.id), 'acceptStates': [str(acc.id) for acc in p.accept_states], \
        'inputAlphabet': list(p.input_alphabet), 'stackAlphabet': list(p.stack_symbols), 'initStackSymbol': p.init_stack_symbol}

def make_table_json(c):
    if len(c.terminals) == 0:
        c.find_terms_nonterms()
    terms = list(c.terminals)
    terms.append('$')
    try:
        terms.remove('ε')
    except:
        pass
    nonterms = list(c.nonterminals)

    table = [['' for _ in range(len(terms))] for _ in range(len(nonterms))]

    for pair, rules in c.parse_table.items():
        nt, term = pair
        table[ nonterms.index(nt) ][ terms.index(term) ] = ', '.join([(nt + ' → ' + prod) for prod in rules])

    return {'terminals': terms, 'nonterminals': nonterms, 'table': table}
