import React from 'react'
import '../App.css';
import { Redirect } from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import Routes from '../Routes'
import AutomataInput from '../inputInfo/AutomataInput'
import Conversions from '../Conversions'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  rules: any,
  startSym: string,
  showOps: boolean,
  opSelection: string,
  opSelectionText: string
}

export default class CFGAns extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = {
      rules: null, //{}
      startSym: null,
      showOps: false
    }
  }

  componentDidMount (){
    //console.log(this.props.location.answer)
    if (this.props.location && this.props.location.answer){
      this.setState({
        rules: this.props.location.answer.rules,
        startSym: this.props.location.answer.startSym
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    if (this.props.location && this.props.location.answer &&
    ((!prevProps.location.answer.startSym && this.props.location.answer.startSym) ||
    prevProps.location.answer.rules !== this.props.location.answer.rules)){
      this.setState({
        rules: this.props.location.answer.rules,
        startSym: this.props.location.answer.startSym
      })
    }
  }

  setSelection = (selection, text) => {
    this.setState({
      opSelection: selection,
      opSelectionText: text,
      showOps: false
    })
  }
  render() {
    var postBody = {
      fromInput: false,
      rules: this.state.rules,
      startSym: this.state.startSym
    }

    return (
      <div id="dnfa_ans" className="wrapper">
        <Header/>
        <h1 className='regex'>CFG Answer</h1>
        <div className='cfgBox'>
          { this.state.rules && (
            Object.keys(this.state.rules).map( (nt, index) => (
              <div>
                <label>{nt + (nt === this.state.startSym ? '*' : '') + ' → ' }</label>
                <input
                  type="text"
                  value={this.state.rules[nt].join(' | ')}
                  onChange={(event) => {}}
                />
                <br/><br/>
              </div>
              //nt --> prods
            ))
          )}
        </div>
        {!this.state.answer && (
          <div>
            <div className="dropdown">
              <button
                className="enterButton"
                onClick={() => {
                  var showOps = this.state.showOps
                  this.setState({ showOps: !showOps })
                }}>
                Show Options ↓
              </button>
              { this.state.showOps === true && (
                <div className="dropdownOptions">
                  <div onClick={this.setSelection.bind(null, Conversions.cfgToPda, 'CFG to PDA')}>CFG to PDA</div>
                  <div onClick={this.setSelection.bind(null, Conversions.simplifyGrammar, 'Simplify Grammar')}>Simplify Grammar</div>
                  <div onClick={this.setSelection.bind(null, Conversions.elimNull, 'Eliminate Null Productions')}>Eliminate Null Productions</div>
                  <div onClick={this.setSelection.bind(null, Conversions.elimUnit, 'Eliminate Unit Productions')}>Eliminate Unit Productions</div>
                  <div onClick={this.setSelection.bind(null, Conversions.chomsky, 'Chomsky Normal Form')}>Chomsky Normal Form</div>
                  <div onClick={this.setSelection.bind(null, Conversions.greibach, 'Greibach Normal Form')}>Greibach Normal Form</div>
                  <div onClick={this.setSelection.bind(null, Conversions.ffpSets, 'First, Follow, and Predict Sets')}>First, Follow, and Predict Sets</div>
                  <div onClick={this.setSelection.bind(null, Conversions.parseTable, 'Parse Table')}>Parse Table</div>
                  <div onClick={this.setSelection.bind(null, Conversions.leftRecursion, 'Remove Left Recursion')}>Remove Left Recursion</div>
                  <div onClick={this.setSelection.bind(null, Conversions.commonSubexpression, 'Eliminate Common Subexpression')}>Eliminate Common Subexpression</div>
                </div>
              )}
            </div>
            {this.state.opSelection && (
              <button
                className="enterButton"
                onClick={this.makeFlaskPostFromAns.bind(null, postBody,
                  ApiRoutes.cfgInput, this.state.opSelection)}
              >
                {this.state.opSelectionText}
              </button>
            )}
          </div>
        )}

        { this.state.answer && this.state.opSelection &&
          <Redirect to={{
            pathname: this.determinePath(this.state.opSelection ? this.state.opSelection : ''),
            answer: this.state.answer
          }}
            onClick={this.setState({ answer: null })} />
        }
      </div>
    )
  }
}
