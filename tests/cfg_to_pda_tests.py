from automata.cfg import CFG

def test1():
    rules = {'S': ['aSb', 'A'], 'A': ['ε']}
    c = CFG(rules)
    c.start = 'S'
    c.convert_to_pda()
    c.my_pda.print_pda()
#test1()

def test2():
    rules = {'S': ['aSa', 'bSb', 'ε', 'b', 'a']}
    c = CFG(rules)
    c.start = 'S'
    c.convert_to_pda()
    c.my_pda.print_pda()
#test2()
