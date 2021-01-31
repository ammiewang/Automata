import React from 'react'
import Conversions from './Conversions'
import Routes from './Routes'
import './App.css'

export default class Header extends React.Component {
  render () {
    return (
      <div className="header">
        <div><a href="/">HOME</a></div>
        <div><div className="header circle" /></div>
        <div><a href="/dfa">DFA</a></div>
        <div><div className="header circle" /></div>
        <div><a href="/nfa">NFA</a></div>
        <div><div className="header circle" /></div>
        <div><a href="/regex">REGEX</a></div>
        <div><div className="header circle" /></div>
        <div><a href="/cfg">CFG</a></div>
        <div><div className="header circle" /></div>
        <div><a href="/pda">PDA</a></div>
      </div>
  )}
}
