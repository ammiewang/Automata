import React from 'react'
import '../App.css';
import {Link} from 'react-router-dom'
import Header from '../Header'

export default class PDAOps extends React.Component {
  render() {
    return (
      <div>
        <Header/>
        <div id="operation" className="wrapper">
          <h1 className='pdaTitle'>PUSHDOWN AUTOMATON</h1>
          <h2>CHOOSE OPERATION</h2>
          <div id="pdaop" className="wrapper">
            <Link to={{
              pathname: '/pda/generator',
              operation: 'pda2cfg'
            }}>
              <button id="pda2cfg" className="circle pda button">PDA to CFG</button>
            </Link>
          </div>
        </div>
      </div>
    )
  }
}
