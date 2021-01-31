import React from 'react'
import '../App.css';

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

export default class DFAns extends React.Component {
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
    //console.log(this.props.location.answer)
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
    //console.log('update')
    //console.log(this.props.location.answer.alphabet)
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

  render() {
    var width
    var hasStateData = this.state.alphabet
    if (hasStateData){
      width = 250*(this.state.alphabet.length) + 100
      width = width.toString() + 'px'
      console.log(this.state.transitions)
    } else {
      width = '100%'
    }
    return (
      <div id="dnfa_ans" className="wrapper">
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

      </div>
    )
  }
}
