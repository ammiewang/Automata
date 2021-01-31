from automata.state import state
from automata.dfa import DFA
from automata.nfa import NFA
from automata.regex import Regex

from jsonifyAutomata import *

def make_dfa_wrapper(data):
    sts = []
    rows = len(data['stateNames'])
    cols = len(data['alphabet'])
    alph = data['alphabet']
    id_to_st = {}

    for i in range(rows):
        st_name = data['stateNames'][i]
        s = state(st_name)
        sts.append(s)
        id_to_st[st_name] = s

    if data['fromInput']:
        for i in range(rows):
            s = sts[i]
            s.outpaths = {}
            for j in range(cols):
                st2 = data['transitions'][i][alph[j]]
                if st2 is not None:
                    s.outpaths[alph[j]] = id_to_st[st2]
    else:
        for st, tr in data['transitions'].items():
            s = id_to_st[st]
            s.outpaths = {}
            for ch, st2 in tr.items():
                if st2 is not None:
                    s.outpaths[ch] = id_to_st[st2]

    d = DFA(sts)
    d.start_state = id_to_st[data['startStates']]
    d.alphabet = alph
    acc_list = data['acceptStates']
    d.accept_states = [id_to_st[i] for i in acc_list]
    return d

def make_nfa_wrapper(data):
    sts = []
    rows = len(data['stateNames'])
    cols = len(data['alphabet'])
    alph = data['alphabet']
    id_to_st= {}

    for i in range(rows):
        st_name = data['stateNames'][i]
        s = state(st_name)
        sts.append(s)
        id_to_st[st_name] = s

    for i in range(rows):
        s = sts[i]
        s.outpaths = {}
    for j in range(cols):
        st2 = data['transitions'][i][alph[j]]
        if st2 is not None:
            s.outpaths[alph[j]] = [id_to_st[ch] for ch in st2.split()]

    n = NFA(sts)
    ss_list = data['startStates'].split()
    n.start_states = [id_to_st[i] for i in ss_list]
    n.alphabet = alph
    acc_list = data['acceptStates']
    n.accept_states = [id_to_st[i] for i in acc_list]
    return n

def dfa2regex(data):
    d = make_dfa_wrapper(data)
    d.all_regex()
    return d.regex

def mindfa(data):
    d = make_dfa_wrapper(data)
    d.minimize()
    return make_dfa_json(d)

def nfa2dfa(data):
    n = make_nfa_wrapper(data)
    n.nfa_to_dfa()
    return make_dfa_json(n.my_dfa)

def re2dfa(data):
    r = Regex(data['regex'])
    r.dfa_maker()
    return make_dfa_json(r.my_dfa)

def recomp(data):
    r = Regex(data['regex'])
    r.complement_maker()
    return r.complement
