import React from 'react'
import '../App.css';
import { Redirect } from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import AutomataInput from './AutomataInput'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  transitions: Array<Array<any>>,
  showInstructions: boolean
  //answer: any
}

export default class PDAInput extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = ({
      transitions: [[null, null, null, null, null]],
      showInstructions: false
    })
  }

  addRow = () => {
    var transitions = this.state.transitions
    transitions.push([null, null, null, null, null])
    this.setState({
      transitions: transitions
    })
  }

  changeAtIndex = (transitionNum, index, val) => {
    var transitions = this.state.transitions
    transitions[transitionNum][index] = val
    this.setState({
      transitions: transitions
    })
  }

  render (){
    var hasOpData = this.props.location && this.props.location.operation
    var hasPropsData = this.props.location && this.props.location.data
    return (
      <div id="pda_transitions" className="wrapper">
        <Header/>
        <h1 className='dnfaInput'>PDA TRANSITIONS</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div>
            <div className="instructions">
              {"If all symbols in the stack alphabet are only one character,"}
              {" for a transition δ(q0, a, X) = (q1, XY), write the transition exactly as it appears."}
            </div>
            <div className="instructions">
              {"If any symbol in the stack alphabet is longer than one character, stack symbols should be separated by space. "}
              {'For example, δ(q0, a, X0) = (q1, X0 Y0)'}
            </div>
            <div className="instructions" style={{ fontWeight: 'bold'}}>
              {"To represent the empty transition or a deletion from the top of the stack, use ε (this one can be copy/pasted)."}
            </div>
          </div>
        )}
        <div className="pdaBox">
          {this.state.transitions && (
            <table className="center" id="pda_inp_table">
            <tbody id="pda_tab_body">

              {Array.from(Array(this.state.transitions.length).keys()).map( (row) => (
                <tr>
                  <td className="input">
                    <label className="biglabel">δ ( </label>
                    <input
                      type="text"
                      className="smallbox"
                      onChange={ event => this.changeAtIndex(row, 0, event.target.value) }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="smallbox"
                      onChange={ event => this.changeAtIndex(row, 1, event.target.value) }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="smallbox"
                      onChange={ event => this.changeAtIndex(row, 2, event.target.value) }
                    />
                    <label className="biglabel"> ) = ( </label>
                    <input
                      type="text"
                      className="smallbox"
                      onChange={ event => this.changeAtIndex(row, 3, event.target.value) }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="mediumbox"
                      onChange={ event => this.changeAtIndex(row, 4, event.target.value) }
                    />
                    <label className="biglabel"> )</label>
                  </td>
                </tr>
              ))}

            </tbody>
          </table>)}
        </div>
        <button onClick={this.addRow.bind(null)} className="enterButton">+</button>
        { !this.state.answer && (
          <button
          id="pda_enter"
          className="enterButton"
          onClick={this.makeFlaskPost.bind(null, ({
            conversionType: this.props.location.operation,
            transitions: this.state.transitions,
            alphabet: hasPropsData ? this.props.location.data.alphabet : [],
            startStates: hasPropsData ? this.props.location.data.startStates : null,
            acceptStates: hasPropsData ? this.props.location.data.acceptStates : [],
            stackAlphabet: hasPropsData ? this.props.location.data.stackAlphabet : [],
            initStackSym: hasPropsData ? this.props.location.data.initStackSym : null
          }), ApiRoutes.pdaInput)}
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
