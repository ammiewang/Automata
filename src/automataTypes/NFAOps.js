import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Header from '../Header'

export default class NFAOps extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div id="operation" className="wrapper">
          <h1 className='nfaTitle'>NONDETERMINISTIC FINITE AUTOMATON</h1>
          <h2>CHOOSE OPERATION</h2>
          <div id="nfaop" className="wrapper">
            <Link to={{
              pathname: '/dnfa/generator',
              operation: 'nfa2dfa'
            }}>
               <button id="nfa2dfa" className="circle nfa button">NFA to DFA</button>
            </Link>
          </div>
        </div>
      </div>
    )
  }
}
