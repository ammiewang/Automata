import React from 'react'
import '../App.css';
import {Link, Redirect} from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import AutomataInput from './AutomataInput'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  nonterminals: Array<any>,
  productions: Array<any>,
  showInstructions: boolean
}

export default class CFGInput extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = ({
      productions: [null],
      nonterminals: [null],
      showInstructions: false
    })
  }

  changeAtIndexProductions = (index, val) => {
    var productions = this.state.productions
    productions[index] = val
    this.setState({
      productions: productions
    })
  }

  changeAtIndexNonterminals = (index, val) => {
    var nonterminals = this.state.nonterminals
    nonterminals[index] = val
    this.setState({
      nonterminals: nonterminals
    })
  }

  addRow = () => {
    var productions = this.state.productions
    var nonterminals = this.state.nonterminals
    productions.push(null)
    nonterminals.push(null)
    this.setState({
      productions: productions,
      nonterminals: nonterminals
    })
  }

  render() {
    var hasOpData = this.props.location && this.props.location.operation
    return (
      <div id="cfg_inp_pg" className="wrapper">
        <Header/>
        <h1 className='regex'>CFG INPUT</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div>
            <div className="instructions">
              On the LHS, mark the starting nonterminal with an asterisk, *. If the starting nonterminal is S, write S* on the LHS.
            </div>
            <div className="instructions">
              Separate all characters by space (A0 → a A1 b). Separate different productions from the same
              nonterminal with a bar, |. For example, (A0 → a A1 b | a b). Different productions from the same
              nonterminal may also be separated onto different lines (A0 → a A1 b; A0 → a b).
            </div>
            <div className="instructions" style={{ fontWeight: 'bold'}}>
              {"To represent the empty string, use ε (this one can be copy/pasted)."}
            </div>
          </div>
        )}
        <div className="cfgBox">
          {this.state.nonterminals && (
            <table className="center" id="pda_inp_table">
            <tbody id="pda_tab_body">
              {Array.from(Array(this.state.nonterminals.length).keys()).map( (row) => (
                <tr>
                  <td className="input">
                    <input
                      type="text"
                      className="smallbox"
                      onChange={ event => this.changeAtIndexNonterminals(row, event.target.value) }
                    />
                    <label className="biglabel"> → </label>
                    <input
                      type="text"
                      onChange={ event => this.changeAtIndexProductions(row, event.target.value) }
                    />
                  </td>
                </tr>
              ))}

            </tbody>
          </table>)}
        </div>
        <button onClick={this.addRow.bind(null)} className="enterButton">+</button>
        { !this.state.answer && (
          <button
          id="enter_cfg_inp"
          className="enterButton"
          onClick={this.makeFlaskPost.bind(null, ({
            fromInput: true,
            conversionType: this.props.location.operation,
            nonterminals: this.state.nonterminals,
            productions: this.state.productions
          }), ApiRoutes.cfgInput)}
          >
            Enter
          </button>
        )}

        { this.state.answer &&
          <Redirect to={{
            pathname: this.determinePath(hasOpData ? this.props.location.operation : ''),
            answer: this.state.answer
          }} />
        }
      </div>
    )
  }
}
