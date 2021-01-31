import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Header from '../Header'

export default class RegexOps extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div id="operation" className="wrapper">
          <h1 className='regexTitle'>REGULAR EXPRESSION</h1>
          <h2>CHOOSE OPERATION</h2>
          <div id="reop" className="wrapper">
            <div className='buttonLink'>
              <Link to={{
                pathname: '/regex/input',
                operation: 're2dfa'
              }}>
                 <button id="re2dfa" className="circle regex button">RegEx to DFA</button>
              </Link>
            </div>
            <div className='buttonLink'>
              <Link to={{
                pathname: '/regex/input',
                operation: 'recomp'
              }}>
                 <button id="recomp" className="circle regex button">RegEx Complement</button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
