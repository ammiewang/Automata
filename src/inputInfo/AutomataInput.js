import React from 'react'
import Conversions from '../Conversions'
import Routes from '../Routes'

class AutomataInput extends React.Component<Props,State> {

  makeFlaskPost = (postBody, url) => {
    var that = this

    fetch(url, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify(postBody)
    })
    .then(res => {return res.json()})
    .then(data => {that.setState({ answer: data.result })})
  }

  makeFlaskPostFromAns = (postBody, url, conversionType) => {
    postBody.conversionType = conversionType
    this.setState({conversionType: conversionType})
    this.makeFlaskPost(postBody, url)
  }

  determinePath = (operation) => {
    var url = '#'
    if (operation !== '') {
      if (operation === Conversions.dfaToRegex || operation === Conversions.regexComplement) {
        url = Routes.regexAnswer
      } else if (operation === Conversions.minDfa || operation === Conversions.nfaToDfa
        || operation === Conversions.regexToDfa) {
        url = Routes.dfaAnswer
      } else if (operation === Conversions.simplifyGrammar || operation === Conversions.elimNull
        || operation === Conversions.elimUnit || operation === Conversions.chomsky
        || operation === Conversions.greibach || operation === Conversions.leftRecursion
        || operation === Conversions.commonSubexpression || operation === Conversions.pdaToCfg) {
        console.log('hereee')
        url = Routes.cfgAnswer
      } else if (operation === Conversions.cfgToPda) {
        url = Routes.pdaAnswer
      } else if (operation === Conversions.ffpSets) {
        url = Routes.setsAnswer
      } else if (operation === Conversions.parseTable) {
        url = Routes.tableAnswer
      }
    }

    return url
  }

} export default AutomataInput;
