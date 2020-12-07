from browser import document
from browser import window
import urllib.request

state_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/state.py")
exec(state_link.read())

pda_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/pda.py")
exec(pda_link.read())

cfg_link = urllib.request.urlopen("https://ammiewang.github.io/Automata/automata/cfg.py")
exec(cfg_link.read())

def make_pda():
  sts = set()
  num_transitions = len(document["pda_tab_body"].children)
  inp_alph = document["pda_inp_alphabet"].value.split()
  stack_alph = document["pda_stack_alphabet"].value.split()
  id_to_st = {}

  for i in range(num_transitions):
    st1 = document["pda_tab_body"].children[i].children[0].children[1].value
    inp1 = document["pda_tab_body"].children[i].children[0].children[3].value
    stack1 = document["pda_tab_body"].children[i].children[0].children[5].value
    st2 = document["pda_tab_body"].children[i].children[0].children[7].value
    stack2 = document["pda_tab_body"].children[i].children[0].children[9].value
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

  p = PDA(sts, document["pda_init_stack_sym"])
  p.start_state = id_to_st[document["pda_ss"].value]
  p.input_alphabet = set(inp_alph)
  p.stack_symbols = set(stack_alph)
  #p.stack_symbols.add(p.init_stack_symbol)
  acc_list = document["pda_accs"].value.split()
  p.accept_states = {id_to_st[i] for i in acc_list}
  return p

def render_cfg(c):
  tab = document["cfg_ans_table"]
  tbody = document.createElement("tbody")
  for nt, prods in c.rules.items():
    tr = document.createElement('tr')
    td = document.createElement('td')
    lab = document.createElement("label")
    if nt != c.start:
      lab.innerHTML = nt + " → "
    else:
      lab.innerHTML = nt + "* → "
    s = ''
    for str in prods:
        s2 = ' '.join(str)
        s += s2 + '  |  '
    s = s[:-5]
    inp = document.createElement('input')
    inp.type = 'text'
    inp.value = s
    td.append(lab)
    td.append(inp)
    tr.append(td)
    tbody.append(tr)
  tab.append(tbody)

def pda2cfg():
  p = make_pda()
  p.to_cfg()
  document["pda_transitions"].style.display = "none"
  document["cfg_ans"].style.display = "block"
  render_cfg(p.my_cfg)

def pda_ops(event):
  f = document["pda_gen"].getAttribute("from")
  document["pda_gen"].style.display = "none"
  if f == "pda2cfg":
    pda2cfg()

document["pda_enter"].bind("click", pda_ops)
