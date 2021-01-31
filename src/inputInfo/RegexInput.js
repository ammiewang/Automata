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
  regex: string,
  showInstructions: boolean
}

export default class RegexInput extends AutomataInput {
  constructor(props:Props){
    super(props)
    this.state = ({
      regex: '',
      showInstructions: false
    })
  }

  render() {
    var hasOpData = this.props.location && this.props.location.operation
    return (
      <div id="reg_inp_pg" className="wrapper">
        <Header/>
        <h1 className='regex'>REGEX INPUT</h1>
        <h3 onClick={ () => {
          var showInstructions = this.state.showInstructions
          this.setState({ showInstructions: !showInstructions })
        }}>
          {'INSTRUCTIONS ' + (this.state.showInstructions ? '↑' : '↓')}
        </h3>
        {this.state.showInstructions && (
          <div>
            <div className="instructions">
              This tool handles regular expressions which use concatention, union, and/or Kleene star.
            </div>
            <div className="instructions">
              <span>(), ab</span> {' = concatention, '}
              <span>+</span> {' = union, '}
              <span>*</span>{' = Kleene star'}
            </div>
            <div className="instructions" style={{ fontWeight: 'bold'}}>
              {"To represent the empty string, use ε (this one can be copy/pasted)."}
            </div>
          </div>
        )}
        <div className="regexBox">
          <input
            type="text"
            id="reg_ans"
            onChange={ (event) => {this.setState({ regex: event.target.value })} }
            /><br/><br/>
        </div>
        { !this.state.answer && (
          <button
          id="enter_dnfa_inp"
          className="enterButton"
          onClick={this.makeFlaskPost.bind(null, ({
            conversionType: this.props.location.operation,
            regex: this.state.regex
          }), ApiRoutes.regexInput)}
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
