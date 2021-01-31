import React from 'react'
import '../App.css';
import { Link, Redirect } from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import Routes from '../Routes'
import AutomataInput from '../inputInfo/AutomataInput'
import Conversions from '../Conversions'
import Header from '../Header'
//import DNFAInput from '../inputInfo/DNFAInput'

type Props = {
  location?: any
}

type State = {
  alphabet: Array<string>, //change to arr<any>??
  transitions: Array<any>, //might not be correct type? use any?
  startState: string, //any?
  acceptStates: Array<string>, //change to arr<any>??
  stateNames: Array<string> //change to arr<any>??
}

export default class DFAns extends AutomataInput {
  constructor(props:Props){
    super(props)
    console.log('in constructor')
    this.state = {
      alphabet: [],
      transitions: [],
      startState: null,
      acceptStates: [],
      stateNames: []
    }
  }

  componentDidMount (){
    if (this.props.location && this.props.location.answer){
      this.setState({
        alphabet: this.props.location.answer.alphabet,
        transitions: this.props.location.answer.transitions,
        startState: this.props.location.answer.startState,
        acceptStates: this.props.location.answer.acceptStates,
        stateNames: this.props.location.answer.stateNames
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    if (this.props.location && this.props.location.answer &&
      this.props.location.answer.alphabet && !prevProps.location.answer.alphabet){
      this.setState({
        alphabet: this.props.location.answer.alphabet,
        transitions: this.props.location.answer.transitions,
        startState: this.props.location.answer.startState,
        acceptStates: this.props.location.answer.acceptStates,
        stateNames: this.props.location.answer.stateNames
      })
    }
  }

  // makeFlaskPostFromAns = (postBody, url, conversionType) => {
  //   postBody.conversionType = conversionType
  //   this.setState({conversionType: conversionType})
  //   this.makeFlaskPost(postBody, url)
  // }

  render() {
    var width
    var hasStateData = this.state.alphabet
    if (hasStateData){
      width = 250*(this.state.alphabet.length) + 100
      width = width.toString() + 'px'
      // console.log(this.state.transitions)
    } else {
      width = '100%'
    }

    var postBody = {
      fromInput: false,
      stateNames: this.state.stateNames,
      transitions: this.state.transitions,
      alphabet: this.state.alphabet,
      startStates: this.state.startState,
      acceptStates: this.state.acceptStates
    }

    return (
      <div id="dnfa_ans" className="wrapper">
        <Header/>
        <h1 className='dnfaInput'>DFA Answer</h1>
        <div className='dfaBox' style={{ width: width }}>
          { hasStateData && (
            <table id='ans_table' className='center'>
              <thead>
                <tr>
                  <th>State</th>
                  {this.state.alphabet.map( (letter) => (
                    <th key={letter}>{letter}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
              {
                Array.from(Array(this.state.stateNames.length).keys()).map( (row) => (
                  <tr>
                    {
                      Array.from(Array(this.state.alphabet.length + 1).keys()).map((col) => (
                        <td>
                          { col === 0 && (
                            <label key={this.state.stateNames[row]}>
                              {this.state.stateNames[row] === this.state.startState ? '→ ' : '' }
                              {this.state.stateNames[row]}
                              {this.state.acceptStates.includes(this.state.stateNames[row]) ? ' F' : ''}
                            </label>
                          )}
                          { col !== 0 && (
                            <input
                              type='text'
                              key={row + ' ' + col}
                              onChange={ (event) => {} }
                              value={this.state.transitions[this.state.stateNames[row]][this.state.alphabet[col-1]] && (
                                this.state.transitions[this.state.stateNames[row]][this.state.alphabet[col-1]]
                              )}/>
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
          <div>
            <button
            className="enterButton"
            onClick={this.makeFlaskPostFromAns.bind(null, postBody,
              ApiRoutes.dnfaInput, Conversions.dfaToRegex)}
            >
              DFA to RegEx
            </button>
            <button
            className="enterButton"
            onClick={this.makeFlaskPostFromAns.bind(null, postBody,
              ApiRoutes.dnfaInput, Conversions.minDfa)}
            >
              Minimize DFA
            </button>
          </div>
        )}

        { this.state.answer && this.state.conversionType &&
          <Redirect to={{
            pathname: this.determinePath(this.state.conversionType ? this.state.conversionType : ''),
            answer: this.state.answer
          }}
            onClick={this.setState({ answer: null })} />
        }
      </div>
    )
  }
}
