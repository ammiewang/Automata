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
  transitions: any,
  startState: string,
  acceptStates: Array<string>,
  inputAlphabet: Array<string>,
  stackAlphabet: Array<string>,
  initStackSymbol: string
}

export default class PDAns extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = {
      rules: null, //{}
      startSym: null
    }
  }

  componentDidMount (){
    //console.log(this.props.location.answer)
    if (this.props.location && this.props.location.answer){
      this.setState({
        transitions: this.props.location.answer.transitions,
        startState: this.props.location.answer.startState,
        acceptStates: this.props.location.answer.acceptStates,
        inputAlphabet: this.props.location.answer.inputAlphabet,
        stackAlphabet: this.props.location.answer.stackAlphabet,
        initStackSymbol: this.props.location.answer.initStackSymbol
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    //console.log('update')
    //console.log(this.props.location.answer.alphabet)
    if (this.props.location && this.props.location.answer &&
    !prevProps.location.answer.transitions && this.props.location.answer.transitions){
      this.setState({
        transitions: this.props.location.answer.transitions,
        startState: this.props.location.answer.startState,
        acceptStates: this.props.location.answer.acceptStates,
        inputAlphabet: this.props.location.answer.inputAlphabet,
        stackAlphabet: this.props.location.answer.stackAlphabet,
        initStackSymbol: this.props.location.answer.initStackSymbol
      })
    }
  }

  render() {
    var postBody = {
      transitions: this.state.transitions,
      alphabet: this.state.inputAlphabet ? this.state.inputAlphabet : [],
      startStates: this.state.startState ? this.state.startState : null,
      acceptStates: this.state.acceptStates ? this.state.acceptStates : [],
      stackAlphabet: this.state.stackAlphabet ? this.state.stackAlphabet : [],
      initStackSym: this.state.initStackSymbol ? this.state.initStackSymbol : null
    }
    return (
      <div id="pda_ans">
        <Header/>
        <h1 className='dnfaChartTitle'>PDA INFORMATION</h1>
        <div >
          {this.state.startState && (
            <div className="inputBox">
              <div>
                <label>START STATE: </label>
              </div>
              <div>
                <input
                  type="text"
                  value={this.state.startState}
                  onChange={ event => this.setState({ startState: event.target.value })}
                />
                <br/><br/>
              </div>
              <div>
                <label>ACCEPT STATE(S): </label>
              </div>
              <div>
                <input
                  type="text"
                  value={this.state.acceptStates.join(' ')}
                  onChange={ event => this.setState({ acceptStates: event.target.value.split() })}
                />
                <br/><br/>
              </div>
              <div>
                <label>INPUT ALPHABET: </label>
              </div>
              <div>
                <input
                  type="text"
                  value={this.state.inputAlphabet.join(' ')}
                  onChange={ event => this.setState({ acceptStates: event.target.value.split() })}
                />
                <br/><br/>
              </div>
              <div>
                <label>STACK ALPHABET: </label>
              </div>
              <div>
                <input
                  type="text"
                  value={this.state.stackAlphabet.join(' ')}
                  onChange={ event => this.setState({ acceptStates: event.target.value.split() })}
                />
                <br/><br/>
              </div>
              <div>
                <label>INITIAL STACK SYMBOL: </label>
              </div>
              <div>
                <input
                  type="text"
                  value={this.state.initStackSymbol}
                  onChange={ event => this.setState({ acceptStates: event.target.value.split() })}
                />
                <br/><br/>
              </div>
            </div>
          )}
        </div>
        <h1 className="dnfaInput">PDA Answer</h1>
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
                      value={ this.state.transitions[row][0] }
                      onChange={ event => {/*this.changeAtIndex(row, 0, event.target.value)*/} }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="smallbox"
                      value={ this.state.transitions[row][1] }
                      onChange={ event => {/*this.changeAtIndex(row, 0, event.target.value)*/} }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="smallbox"
                      value={ this.state.transitions[row][2] }
                      onChange={ event => {/*this.changeAtIndex(row, 0, event.target.value)*/} }
                    />
                    <label className="biglabel"> ) = ( </label>
                    <input
                      type="text"
                      className="smallbox"
                      value={ this.state.transitions[row][3] }
                      onChange={ event => {/*this.changeAtIndex(row, 0, event.target.value)*/} }
                    />
                    <label className="biglabel"> , </label>
                    <input
                      type="text"
                      className="mediumbox"
                      value={ this.state.transitions[row][4] }
                      onChange={ event => {/*this.changeAtIndex(row, 0, event.target.value)*/} }
                    />
                    <label className="biglabel"> )</label>
                  </td>
                </tr>
              ))}

            </tbody>
          </table>)}
        </div>
        { !this.state.answer && (
          <div className="wrapper">
            <button
            className="enterButton"
            onClick={this.makeFlaskPostFromAns.bind(null, postBody,
              ApiRoutes.pdaInput, Conversions.pdaToCfg)}
            >
              PDA to CFG
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
