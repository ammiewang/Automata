import React from 'react'
import '../App.css';
import { Link } from 'react-router-dom'
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  terminals: Array<any>,
  nonterminals: Array<any>,
  table: Array<Array<any>>
}

export default class TableAns extends React.Component {
  constructor(props:Props){
    super(props)
    this.state = {
      terminals: [],
      nonterminals: [],
      table: []
    }
  }

  componentDidMount (){
    console.log(this.props.location.answer)
    if (this.props.location && this.props.location.answer){
      this.setState({
        terminals: this.props.location.answer.terminals,
        nonterminals: this.props.location.answer.nonterminals,
        table: this.props.location.answer.table
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    console.log(this.props.location.answer)
    if (this.props.location && this.props.location.answer &&
    !prevProps.location.answer.terminals && this.props.location.answer.terminals){
      this.setState({
        terminals: this.props.location.answer.terminals,
        nonterminals: this.props.location.answer.nonterminals,
        table: this.props.location.answer.table
      })
    }
  }

  render() {
    var width
    if (this.state.terminals.length > 0){
      width = 238*(this.state.terminals + 1) + 100
      width = width.toString() + 'px'
    } else {
      width = '100%'
    }

    return (
      <div className="wrapper">
        <Header/>
        <h1 className='dnfaInput'>PARSE TABLE</h1>
        <div className='dfaBox' style={{ width: width }}>
          { this.state.terminals.length > 0 && this.state.nonterminals.length > 0 &&
            this.state.table.length > 0 && (
            <table id='original_table' className='center'>
              <thead>
                <tr>
                  <th></th>
                  {this.state.terminals.map( (letter) => (
                    <th key={letter}>{letter}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
              {
                this.state.nonterminals.map( (nt, row) => (
                  <tr>
                    {
                      Array.from(Array(this.state.terminals.length + 1).keys()).map((col) => (
                        <td>
                          {col === 0 && (
                            <label style={{ paddingRight: '5px' }}>{nt}</label>
                          )}
                          {col !== 0 && (
                            <input
                              type='text'
                              key={row + ' ' + col}
                              value={this.state.table[row][col-1]}
                              onChange={ (event) => {} }
                            />
                          )}
                        </td>
                      ))
                    }
                  </tr>
                ))
              }
              </tbody>
            </table>
            )
          }
        </div>

      </div>
    )
  }
}
