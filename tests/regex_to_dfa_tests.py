from automata.regex import Regex

def test1():
    ex = Regex('(000* + 111*)*')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output

    States:  [9, 8, {4}, {1}, '∅', {6}]
    Start State:  {6}
    Accept States:  [8, 9, {6}]
    Outpaths:
    State: 9 , Outpaths:  [('0', {1}), ('1', 9)]
    State: 8 , Outpaths:  [('0', 8), ('1', {4})]
    State: {4} , Outpaths:  [('0', '∅'), ('1', 9)]
    State: {1} , Outpaths:  [('0', 8), ('1', '∅')]
    State: ∅ , Outpaths:  [('0', '∅'), ('1', '∅')]
    State: {6} , Outpaths:  [('0', {1}), ('1', {4})]
    """
#test1()

def test2():
    ex = Regex('(01 + 10)(01 + 10)(01 + 10)')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output

    States:  [{7}, 15, 16, '∅', {13}, {18}, {10}, {16}, {1}, {4}, 14]
    Start State:  {18}
    Accept States:  [16]
    Outpaths:
    State: {7} , Outpaths:  [('0', '∅'), ('1', 15)]
    State: 15 , Outpaths:  [('0', {13}), ('1', {16})]
    State: 16 , Outpaths:  [('0', '∅'), ('1', '∅')]
    State: ∅ , Outpaths:  [('0', '∅'), ('1', '∅')]
    State: {13} , Outpaths:  [('0', '∅'), ('1', 16)]
    State: {18} , Outpaths:  [('0', {1}), ('1', {4})]
    State: {10} , Outpaths:  [('0', 15), ('1', '∅')]
    State: {16} , Outpaths:  [('0', 16), ('1', '∅')]
    State: {1} , Outpaths:  [('0', '∅'), ('1', 14)]
    State: {4} , Outpaths:  [('0', 14), ('1', '∅')]
    State: 14 , Outpaths:  [('0', {7}), ('1', {10})]
    """

#test2()

def test3():
    ex = Regex('(0 +  1(01*0)*1)*')
    ex.dfa_maker()
    ex.my_dfa.print_dfa()

    """
    Correct Output
    
    States:  [{5}, 7, 6]
    Start State:  6
    Accept States:  [6]
    Outpaths:
    State: {5} , Outpaths:  [('1', {5}), ('0', 7)]
    State: 7 , Outpaths:  [('1', 6), ('0', {5})]
    State: 6 , Outpaths:  [('1', 7), ('0', 6)]
    """
#test3()
