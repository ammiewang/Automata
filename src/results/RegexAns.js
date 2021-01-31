import React from 'react'
import '../App.css';
import {Redirect} from 'react-router-dom'
import ApiRoutes from '../ApiRoutes'
import Routes from '../Routes'
import AutomataInput from '../inputInfo/AutomataInput'
import Conversions from '../Conversions'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  regex: string
}

export default class RegexAns extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = {
      regex: ''
    }
  }

  componentDidMount (){
    if (this.props.location && this.props.location.answer){
      this.setState({
        regex: this.props.location.answer
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    if (this.props.location && this.props.location.answer &&
      this.props.location.answer !== prevProps.location.answer){
      this.setState({
        regex: this.props.location.answer
      })
    }
  }

  render() {
    var postBody = {
      regex: this.state.regex
    }
    return (
      <div id="reg_ans_pg" className="wrapper">
        <Header/>
        <h1 className='regex'>REGEX RESULT</h1>
        <div className="regexBox">
          <input
            type="text"
            id="reg_ans"
            onChange={ (event) => {} }
            value={this.state.regex && (
              this.state.regex
            )}/><br/><br/>
        </div>
        { !this.state.answer && (
          <div>
            <button
            className="enterButton"
            onClick={this.makeFlaskPostFromAns.bind(null, postBody,
              ApiRoutes.regexInput, Conversions.regexToDfa)}
            >
              Regex to DFA
            </button>
            <button
            className="enterButton"
            onClick={this.makeFlaskPostFromAns.bind(null, postBody,
              ApiRoutes.regexInput, Conversions.regexComplement)}
            >
              Complement Regex
            </button>
          </div>
        )}

        { this.state.answer && this.state.conversionType &&
          <Redirect to={{
            pathname: this.determinePath(this.state.conversionType ? this.state.conversionType : ''),
            answer: this.state.answer
          }}
            onClick={this.setState({ answer: null })}/>
        }
      </div>
    )
  }
}
