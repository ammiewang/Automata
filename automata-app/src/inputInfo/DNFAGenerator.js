import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  from: string,
  numStates: number,
  startStates: any, //any change to startStates
  acceptStates: Array<any>,
  alphabet: Array<any>,
  showInstructions: boolean
}

export default class DNFAGenerator extends React.Component {
  constructor(props:Props){
    super(props)
    this.state = ({
      from: null,
      numStates: null,
      startStates: null,
      acceptStates: null,
      alphabet: null,
      showInstructions: false
    })
  }

  render() {
    return (
      <div id="dnfa_gen">
        <Header/>
        <h1 className='dnfaChartTitle'>DFA/NFA CHART GENERATOR</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div className="instructions">Separate multiple states or alphabet characters by space.</div>
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
          <div><label htmlFor="alphabet">ALPHABET:</label></div>
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
        </div>
        <div className="wrapper">
          <Link to={{
            pathname:'/dnfa/input',
            operation: this.props.location && this.props.location.operation ?
              this.props.location.operation : null,
            data: {
              numStates: this.state.numStates,
              startStates: this.state.startStates,
              acceptStates: this.state.acceptStates,
              alphabet: this.state.alphabet
            }
          }}>
            <button id="enter_dnfa_gen" className="enterButton">Enter</button>
          </Link>
        </div>
      </div>
    )
  }
}
