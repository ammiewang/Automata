import json
from flask import Flask
from flask import request
from DNFAGen import *
from PDACFGen import *

app = Flask(__name__, static_folder='../build', static_url_path='/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/dnfa/input', methods = ['GET', 'POST'])
def dfa_inp():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data['conversionType'] == 'dfa2re':
            regex = dfa2regex(data)
            return {'result': regex}
        elif data['conversionType'] == 'mindfa':
            minimized_dfa = mindfa(data)
            return {'result': minimized_dfa}
        elif data['conversionType'] == 'nfa2dfa':
            dfa_from_nfa = nfa2dfa(data)
            return {'result': dfa_from_nfa}

@app.route('/api/regex/input', methods = ['GET', 'POST'])
def regex_inp():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data['conversionType'] == 're2dfa':
            dfa_from_re = re2dfa(data)
            return {'result': dfa_from_re}
        elif data['conversionType'] == 'recomp':
            complemented = recomp(data)
            return {'result': complemented}

@app.route('/api/pda/input', methods = ['GET', 'POST'])
def pda_inp():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data['conversionType'] == 'pda2cfg':
            cfg_from_pda = pda2cfg(data)
            return {'result': cfg_from_pda}

@app.route('/api/cfg/input', methods = ['GET', 'POST'])
def cfg_inp():
    if request.method == 'POST':
        data = json.loads(request.data)
        if data['conversionType'] == 'simgram':
            new_grammar = simplify_grammar(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'cnf':
            new_grammar = cnf(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'gnf':
            new_grammar = gnf(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'ffpSets':
            all_sets = ffpSets(data)
            return {'result': all_sets}
        elif data['conversionType'] == 'leftRec':
            new_grammar = leftRec(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'comSub':
            new_grammar = comSub(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'elimNull':
            new_grammar = elimNull(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'elimUnit':
            new_grammar = elimUnit(data)
            return {'result': new_grammar}
        elif data['conversionType'] == 'cfg2pda':
            new_pda = cfg2pda(data)
            return {'result': new_pda}
        elif data['conversionType'] == 'parseTable':
            new_pt = parseTable(data)
            return {'result': new_pt}

if __name__ == "__main__":
    app.run()
