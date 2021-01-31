import React from 'react'
import '../App.css';
import { Link, Redirect } from 'react-router-dom'

type Props = {
  location?: any
}

type State = {
  stateNames: Array<any>,
  transitions: Array<any>, //any //Array<Array<any>>
  answer: any
}

export default class DNFAInput extends React.Component {
  constructor(props:Props){
    super(props)
    this.state = ({
      stateNames: this.makeInitialStates(),//this.makeInitialStates(),
      transitions: this.makeInitialTransitions()
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

  determinePath = () => {
    var url = '#'
    //console.log('hello???')
    if( this.props.location && this.props.location.operation){
      if (this.props.location.operation === 'dfa2re'){
        url = '/regex/answer'
      } else if (this.props.location.operation === 'mindfa' ||
        this.props.location.operation === 'nfa2dfa'){
        url = '/dfa/answer'
      }
    }
    return url
  }

  makeFlaskPost = (postBody) => {
    var that = this

    fetch('/api/dnfa/input', {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(postBody)
    })
    .then(res => {return res.json()})
    .then(data => {that.setState({ answer: data.result })})

  }

  render() {
    var width
    var hasPropsData = this.props.location && this.props.location.data
    if (hasPropsData){
      width = 238*(this.props.location.data.alphabet.length) + 100
      width = width.toString() + 'px'
    } else {
      width = '100%'
    }
    return (
      <div id="dnfa_inp" className="wrapper">
        <h1 className='dnfaInput'>DFA/NFA INPUT</h1>
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
            stateNames: this.state.stateNames,
            transitions: this.state.transitions,
            alphabet: hasPropsData ? this.props.location.data.alphabet : [],
            startStates: hasPropsData ? this.props.location.data.startStates : null,
            acceptStates: hasPropsData ? this.props.location.data.acceptStates : []
          }))}
          >
            Enter
          </button>
        )}

        { this.state.answer &&
          <Redirect to={{
            pathname: this.determinePath(),
            answer: this.state.answer
          }} />
        }


      </div>
    )
  }
}
