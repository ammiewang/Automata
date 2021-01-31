import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Routes from '../Routes'
import Header from '../Header'

export default class DFAOps extends React.Component {
  render() {
    return (
      <div>
        <Header/>
        <div id="operation" className="wrapper">
          <h1 className='dfaTitle'>DETERMINISTIC FINITE AUTOMATON</h1>
          <h2>CHOOSE OPERATION</h2>
          <div id="dfaop" className="wrapper">
            <div className='buttonLink'>
               <Link to={{
                 pathname: Routes.dnfaGenerator,
                 operation: 'dfa2re'
               }}>
                  <button id="dfa2re" className="circle dfa button">DFA to RegEx</button>
              </Link>
            </div>
            <div className='buttonLink'>
              <Link to={{
                pathname: Routes.dnfaGenerator,
                operation: 'mindfa'
              }}>
                <button id="mindfa" className="circle dfa button">Minimize DFA</button>
              </Link>
            </div>
         </div>
      </div>
    </div>
    )
  }
}
