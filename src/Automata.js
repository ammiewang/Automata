import React from 'react'
import './App.css'
import { Link } from 'react-router-dom'

export default class Automata extends React.Component{
  render(){
    return (
      <div className="wrapper">
        <header className="wrapper">
          <title>Automata</title>
        </header>
        <div id="automata" className="wrapper">
          <h1 className='mainTitle'>AUTOMATA</h1>
          <h2>CHOOSE INPUT TYPE</h2>
          <div className='buttonLink'>
            <Link to='/dfa'><button id="dfa" className="circle main button">DFA</button></Link>
          </div>
          <div className='buttonLink'>
          <Link to='/nfa'><button id="nfa" className="circle main button">NFA</button></Link>
          </div>
          <div className='buttonLink'>
            <Link to='/regex'><button id="re" className="circle main button">RegEx</button></Link>
          </div>
          <div className='buttonLink'>
            <Link to='/cfg'><button id="cfg" className="circle main button">CFG</button></Link>
          </div>
          <div className='buttonLink'>
            <Link to='/pda'><button id="pda" className="circle main button">PDA</button></Link>
          </div>
       </div>
      </div>
    )
  }
}
