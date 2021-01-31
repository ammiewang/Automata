import React from 'react'
import '../App.css';
import Header from '../Header'

type Props = {
  location?: any
}

type State = {
  //rules: any,
  //startSym: string,
  firsts: any,
  follows: any,
  predicts: any
}

export default class SetAns extends React.Component {
  constructor(props:Props){
    super(props)
    this.state = {
      // rules: null, //{}
      // startSym: ''
      firsts: null,
      follows: null,
      predicts: null
    }
  }

  componentDidMount (){
    //console.log(this.props.location.answer)
    if (this.props.location && this.props.location.answer){
      this.setState({
        // rules: this.props.location.answer.rules,
        // startSym: this.props.location.answer.startSym
        firsts: this.props.location.answer.firsts,
        follows: this.props.location.answer.follows,
        predicts: this.props.location.answer.predicts
      })
    }
  }

  componentDidUpdate(prevProps: Props) {
    //console.log('update')
    //console.log(this.props.location.answer.alphabet)
    if (this.props.location && this.props.location.answer &&
    !prevProps.location.answer.firsts && this.props.location.answer.firsts){
      this.setState({
        // rules: this.props.location.answer.rules,
        // startSym: this.props.location.answer.startSym
        firsts: this.props.location.answer.firsts,
        follows: this.props.location.answer.follows,
        predicts: this.props.location.answer.predicts
      })
    }
  }

  render() {
    return (
      <div id="sets_ans" className="wrapper">
        <Header/>
        <h1 className='dnfaInput'>FIRST SETS</h1>
        <div className='dfaBox setBox'>
          { this.state.firsts && (
            Object.keys(this.state.firsts).map( (nt, index) => (
              <div>
                <label style={{ paddingRight: '10px' }}>{'FIRST(' + nt + ') → {' }</label>
                <input
                  type="text"
                  value={this.state.firsts[nt].join(', ')}
                  onChange={(event) => {}}
                />
                <label style={{ paddingLeft: '10px' }}>}</label>
                <br/><br/>
              </div>
            ))
          )}
        </div>
        <h1 className='dnfaInput'>FOLLOW SETS</h1>
        <div className='dfaBox setBox'>
          { this.state.follows && (
            Object.keys(this.state.follows).map( (nt, index) => (
              <div>
                <label style={{ paddingRight: '10px' }}>{'FOLLOW(' + nt + ') → {' }</label>
                <input
                  type="text"
                  value={this.state.follows[nt].join(', ')}
                  onChange={(event) => {}}
                />
                <label style={{ paddingLeft: '10px' }}>}</label>
                <br/><br/>
              </div>
            ))
          )}
        </div>
        <h1 className='dnfaInput'>PREDICT SETS</h1>
        <div className='dfaBox setBox'>
          { this.state.predicts && (
            Object.keys(this.state.predicts).map( (nt, index) => (
              <div>
                <label style={{ paddingRight: '10px' }}>{'PREDICT(' + nt + ') → {' }</label>
                <input
                  type="text"
                  value={this.state.predicts[nt].join(', ')}
                  onChange={(event) => {}}
                />
                <label style={{ paddingLeft: '10px' }}>}</label>
                <br/><br/>
              </div>
            ))
          )}
        </div>
      </div>
    )
  }
}
