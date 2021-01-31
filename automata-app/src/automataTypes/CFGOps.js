import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Routes from '../Routes'
import Header from '../Header'

export default class CFGOps extends React.Component {
  render() {
    return (
      <div>
        <Header />
        <div id="operation" className="wrapper">
          <h1 className='cfgTitle'>CONTEXT FREE GRAMMAR</h1>
          <h2>CHOOSE OPERATION</h2>
          <div id="cfgop" className="wrapper flexContainer">
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'cfg2pda'
              }}>
                <button id="cfg2pda" className="circle cfg button">CFG to PDA</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'simgram'
              }}>
                <button id="simgram" className="circle cfg button">Simplify Grammar</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'elimNull'
              }}>
                <button id="elim_null" className="circle cfg button">
                  Eliminate Null Productions
                </button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'elimUnit'
              }}>
                <button id="elim_unit" className="circle cfg button">
                  Eliminate Unit Productions
                </button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'cnf'
              }}>
                <button id="cnf" className="circle cfg button">Chomsky Normal Form</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'gnf'
              }}>
                <button id="gnf" className="circle cfg button">Greibach Normal Form</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'ffpSets'
              }}>
                <button id="first_follow_predict" className="circle cfg button">First, Follow, and Predict Sets</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'parseTable'
              }}>
                <button id="parseTable" className="circle cfg button">Parse Table</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'leftRec'
              }}>
                <button id="leftRec" className="circle cfg button">Remove Left Recursion</button>
              </Link>
            </div>
            <div className="buttonLink">
              <Link to={{
                pathname: Routes.cfgInput,
                operation: 'comSub'
              }}>
                <button id="comSub" className="circle cfg button">Eliminate Common Subexpression</button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
