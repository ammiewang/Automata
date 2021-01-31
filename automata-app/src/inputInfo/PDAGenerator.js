import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  numStates: number,
  startStates: any, //any change to startStates
  acceptStates: Array<any>,
  alphabet: Array<any>,
  stackAlphabet: Array<any>,
  initStackSym: any,
  showInstructions: boolean
}

export default class PDAGenerator extends React.Component {
  constructor(props:Props){
    super(props)
    this.state = ({
      numStates: null,
      startStates: null,
      acceptStates: null,
      alphabet: null,
      stackAlphabet: null,
      initStackSym: null,
      showInstructions: false
    })
  }

  render() {
    return (
      <div id="dnfa_gen">
        <Header/>
        <h1 className='dnfaChartTitle'>PDA CHART GENERATOR</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div className="instructions">Separate multiple states or alphabet characters by space. Choose a one character initial stack symbol.</div>
        )}
        <div className="inputBox">
          <div><label htmlFor="num_states">NUMBER OF STATES:</label></div>
          <div>
            <input
              type="text"
              id="num_states"
              name="num_states"
              onChange={(event) => {
                this.setState({ numStates: parseInt(event.target.value) })
              }}/>
            <br/><br/>
          </div>
          <div><label htmlFor="ss">START STATE(S):</label></div>
          <div>
            <input
              type="text"
              id="ss"
              name="ss"
              onChange={(event) => {
                this.setState({ startStates: event.target.value })
              }}/>
            <br/><br/>
          </div>
          <div><label htmlFor="accs">ACCEPT STATE(S):</label></div>
          <div>
            <input
              type="text"
              id="accs"
              name="accs"
              onChange={(event) => {
                this.setState({ acceptStates: (event.target.value).split(" ") })
              }}/>
            <br/><br/>
          </div>
          <div><label htmlFor="alphabet">INPUT ALPHABET:</label></div>
          <div>
            <input
              type="text"
              id="alphabet"
              name="alphabet"
              onChange={(event) => {
                this.setState({ alphabet: (event.target.value).split(" ") })
              }}/>
            <br/><br/>
          </div>
          <div><label htmlFor="stackAlphabet">STACK ALPHABET:</label></div>
          <div>
            <input
              type="text"
              id="stackAlphabet"
              name="stackAlphabet"
              onChange={(event) => {
                this.setState({ stackAlphabet: (event.target.value).split(" ") })
              }}/>
            <br/><br/>
          </div>
          <div><label htmlFor="initStackSym">INITIAL STACK SYMBOL:</label></div>
          <div>
            <input
              type="text"
              id="initStackSym"
              name="initStackSym"
              onChange={(event) => {
                this.setState({ initStackSym: event.target.value })
              }}/>
            <br/><br/>
          </div>
        </div>

        <div className="wrapper">
          <Link to={{
            pathname:'/pda/input',
            operation: this.props.location && this.props.location.operation ?
              this.props.location.operation : null,
            data: {
              numStates: this.state.numStates,
              startStates: this.state.startStates,
              acceptStates: this.state.acceptStates,
              alphabet: this.state.alphabet,
              stackAlphabet: this.state.stackAlphabet,
              initStackSym: this.state.initStackSym
            }
          }}>
            <button id="enter_dnfa_gen" className="enterButton">Enter</button>
          </Link>
        </div>
      </div>
    )
  }
}
