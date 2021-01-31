import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Automata from './Automata'
import DFAOps from './automataTypes/DFAOps'
import NFAOps from './automataTypes/NFAOps'
import RegexOps from './automataTypes/RegexOps'
import CFGOps from './automataTypes/CFGOps'
import PDAOps from './automataTypes/PDAOps'
import DNFAGenerator from './inputInfo/DNFAGenerator'
import DNFAInput from './inputInfo/DNFAInput'
import RegexAns from './results/RegexAns'
import DFAns from './results/DFAns'
import RegexInput from './inputInfo/RegexInput'
import CFGInput from './inputInfo/CFGInput'
import PDAGenerator from './inputInfo/PDAGenerator'
import PDAInput from './inputInfo/PDAInput'
import CFGAns from './results/CFGAns'
import SetAns from './results/SetAns'
import PDAns from './results/PDAns'
import TableAns from './results/TableAns'
import Routes from './Routes'

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path={Routes.home} component={Automata} />
        <Route exact path={Routes.dfa} component={DFAOps} />
        <Route exact path={Routes.nfa} component={NFAOps} />
        <Route exact path={Routes.regex} component={RegexOps} />
        <Route exact path={Routes.cfg} component={CFGOps} />
        <Route exact path={Routes.pda} component={PDAOps} />
        <Route path={Routes.dnfaGenerator} component={DNFAGenerator} />
        <Route path={Routes.dnfaInput} component={DNFAInput} />
        <Route path={Routes.regexAnswer} component={RegexAns} />
        <Route path={Routes.dfaAnswer} component={DFAns} />
        <Route path={Routes.regexInput} component={RegexInput} />
        <Route path={Routes.pdaGenerator} component={PDAGenerator} />
        <Route path={Routes.pdaInput} component={PDAInput} />
        <Route path={Routes.cfgAnswer} component={CFGAns} />
        <Route path={Routes.cfgInput} component={CFGInput} />
        <Route path={Routes.setsAnswer} component={SetAns} />
        <Route path={Routes.pdaAnswer} component={PDAns} />
        <Route path={Routes.tableAnswer} component={TableAns} />
      </Switch>
    </Router>
  );
}

export default App;
