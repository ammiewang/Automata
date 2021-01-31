import React from 'react'
import '../App.css';
import { Link, Redirect } from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import Routes from '../Routes'
import AutomataInput from './AutomataInput'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  stateNames: Array<any>,
  transitions: Array<any>, //any //Array<Array<any>>
  answer: any,
  showInstructions: boolean
}

export default class DNFAInput extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = ({
      stateNames: this.makeInitialStates(),//this.makeInitialStates(),
      transitions: this.makeInitialTransitions(),
      showInstructions: false
    })
  }

  componentDidMount(){
    return true
  }

  makeInitialStates(){
    var statesArr = []
    if (this.props.location && this.props.location.data){
      for (let i = 0; i < this.props.location.data.numStates; i++){
        statesArr.push(null)
      }
    }
    return statesArr
  }

  makeInitialTransitions(){
    var transitionsArr = []
    if (this.props.location && this.props.location.data){
      for (let i = 0; i < this.props.location.data.numStates; i++){
        var transitionDict = {}
        for (let j = 0; j < this.props.location.data.alphabet.length; j++){
          transitionDict[this.props.location.data.alphabet[j]] = null
        }
        transitionsArr.push(transitionDict)
      }
    }
    return transitionsArr
  }

  changeStateName(entryNum, val) {
    var statesArr = this.state.stateNames
    statesArr[entryNum] = val
    this.setState({
      stateNames: statesArr
    })
  }

  changeTransitionEntry(entryNum, symbol, val) {
    var transitionsArr = this.state.transitions
    transitionsArr[entryNum][symbol] = val
    this.setState({
      transitions: transitionsArr
    })
  }

  willRender() {
    return true
  }

  render() {
    var width
    var hasOpData = this.props.location && this.props.location.operation
    var hasPropsData = this.props.location && this.props.location.data
    if (hasPropsData){
      width = 238*(this.props.location.data.alphabet.length) + 100
      width = width.toString() + 'px'
    } else {
      width = '100%'
    }
    return (
      <div id="dnfa_inp" className="wrapper">
        <Header/>
        <h1 className='dnfaInput'>DFA/NFA INPUT</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div>
            <div className="instructions">
              {"For a DFA/NFA with states {q0, ..., qn}, write each state name in a separate box in the first column."}
            </div>
            <div className="instructions">
              {"For deterministic transition δ(q0, a) = q1, type q1 in the row for q0 and the column for character a."}
            </div>
            <div className="instructions">
              {"For nondeterministic transition δ(q0, a) = {q1, ..., qm}, type q1,"}
              {"..., qn in the row for q0 and the column for character a, separated by space."}
            </div>
            <div className="instructions" style={{ fontWeight: 'bold'}}>
              {"To represent the empty transition, use ε (this one can be copy/pasted)."}
            </div>
          </div>
        )}
        <div className='dfaBox' style={{ width: width }}>
          { hasPropsData && (
            <table id='original_table' className='center'>
              <thead>
                <tr>
                  <th>State</th>
                  {this.props.location.data.alphabet.map( (letter) => (
                    <th key={letter}>{letter}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
              {
                Array.from(Array(this.props.location.data.numStates).keys()).map( (row) => (
                  <tr>
                    {
                      Array.from(Array(this.props.location.data.alphabet.length + 1).keys()).map((col) => (
                        <td>
                          { col === 0 && (
                            <input
                              type='text'
                              className='smallbox'
                              key={row + ' ' + col}
                              onChange={ (event) => {this.changeStateName(row, event.target.value)} }
                              />
                          )}
                          { col !== 0 && (
                            <input
                              type='text'
                              key={row + ' ' + col}
                              onChange={ (event) => {
                                this.changeTransitionEntry(row, this.props.location.data.alphabet[col-1], event.target.value)
                              }}/>
                          )}
                        </td>
                      ))
                    }
                  </tr>
                ))
              }
              </tbody>
            </table>
            )
          }
        </div>

        { !this.state.answer && (
          <button
          id="enter_dnfa_inp"
          className="enterButton"
          onClick={this.makeFlaskPost.bind(null, ({
            conversionType: this.props.location.operation,
            fromInput: true,
            stateNames: this.state.stateNames,
            transitions: this.state.transitions,
            alphabet: hasPropsData ? this.props.location.data.alphabet : [],
            startStates: hasPropsData ? this.props.location.data.startStates : null,
            acceptStates: hasPropsData ? this.props.location.data.acceptStates : []
          }), ApiRoutes.dnfaInput)}
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
