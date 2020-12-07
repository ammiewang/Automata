function switchPages(came_from, selection) {
    var div1 = document.getElementById(came_from);
    div1.style.display = "none";
    if (came_from == "automata"){
      var div2 = document.getElementById("operation");
      div2.style.display = "block";
      if (selection == 1){
        document.getElementById("dfaop").style.display = "block";
      } else if (selection == 2){
        document.getElementById("nfaop").style.display = "block";
      } else if (selection == 3){
        document.getElementById("reop").style.display = "block";
      } else if (selection == 4){
        document.getElementById("cfgop").style.display = "flex";
        document.getElementById("cfgop").style.flexWrap = "wrap";
        document.getElementById("cfgop").style.flexDirection = "row";
      } else if (selection == 5){
        document.getElementById("pdaop").style.display = "block";
      }
    } else if (came_from == "dfaop"){
      var div2 = document.getElementById("operation");
      div2.style.display = "none";
      var div3 = document.getElementById("dnfa_gen");
      div3.style.display = "block";
      if (selection == 1){
        div3.setAttribute("from", "dfa2re");
      } else if (selection == 2){
        div3.setAttribute("from", "mindfa");
      }
    } else if (came_from == "nfaop"){
      var div2 = document.getElementById("operation");
      div2.style.display = "none";
      var div3 = document.getElementById("dnfa_gen");
      div3.style.display = "block";
      div3.setAttribute("from", "nfa2dfa")
    } else if (came_from == "reop"){
      var div2 = document.getElementById("operation");
      div2.style.display = "none";
      var div3 = document.getElementById("re_inp");
      div3.style.display = "block";
      if (selection == 1){
        div3.setAttribute("from", "re2dfa");
      } else if (selection == 2){
        div3.setAttribute("from", "recomp");
      }
    } else if (came_from == "pdaop"){
      var div2 = document.getElementById("operation");
      div2.style.display = "none";
      var div3 = document.getElementById("pda_gen");
      div3.style.display = "block";
      div3.setAttribute("from", "pda2cfg")
    } else if (came_from == "cfgop"){
      var div2 = document.getElementById("operation");
      div2.style.display = "none";
      var div3 = document.getElementById("cfg_inp");
      div3.style.display = "block";
      if (selection == 1){
        div3.setAttribute("from", "cfg2pda")
      }
    }
}

function enterDNFA(){
  var num_states = document.getElementById("num_states").value;
  var start_states = document.getElementById("ss").value.split(" ").map(function(value){
    return parseInt(value);});//document.getElementById("ss").value;
  var accs = document.getElementById("accs").value.split(" ").map(function(value){
    return parseInt(value);});
  var alphabet = document.getElementById("alphabet").value.split(" ");

  document.getElementById("dnfa_gen").style.display = "none";
  var newDiv = document.getElementById("dnfa_inp");
  newDiv.style.display = "block";

  var divBox = document.createElement("div");
  divBox.setAttribute('class', 'dfaBox');

  var table = document.createElement('table');
  table.setAttribute('class', 'center');
  table.setAttribute('id', 'original_table');
  //table.classList.add('table');

  var thead = document.createElement('thead');
  var headRow = document.createElement('tr');

  var th = document.createElement('th');
  th.appendChild(document.createTextNode('State'));
  headRow.appendChild(th);

  for (i in alphabet) {
    var th = document.createElement('th');
    th.appendChild(document.createTextNode(alphabet[i]));
    headRow.appendChild(th);
  }

  thead.appendChild(headRow);

  var tbody = document.createElement('tbody');
  tbody.setAttribute("id", "rows");

  for (var i = 0; i < parseInt(num_states); i++) {
    var tr = document.createElement('tr');
    for (var j = 0; j < alphabet.length + 1; j++) {
      var td = document.createElement('td');
      td.classList.add("input");
      var input = document.createElement('input');
      input.type = "text";
      if (j==0){
        input.setAttribute("class", "smallbox")
      }
      td.appendChild(input);
      tr.appendChild(td);
    }

    tbody.appendChild(tr);
  }

  table.appendChild(thead);
  table.appendChild(tbody);

  var width = 238*(alphabet.length) + 100;

  divBox.appendChild(table);
  divBox.style.width = width.toString() + 'px';
  newDiv.appendChild(divBox);
  //newDiv.appendChild(table);
  $('#enter_dnfa_inp').before(divBox);

}

function dnfaGenRegex(){
  var prevDiv = document.getElementById("dnfa_inp");
  prevDiv.style.display = "none";
}

function enterPDA(){
  document.getElementById("pda_gen").style.display = "none";
  var transitions = document.getElementById("pda_transitions");
  transitions.style.display = "block";
}

function newPDArow(){
  var tab_body = document.getElementById("pda_tab_body");
  var tr = document.createElement('tr');
  var td = document.createElement('td');
  var lab = document.createElement('label');
  lab.innerHTML = 'δ ( ';
  lab.setAttribute("class", "biglabel");
  var st1 = document.createElement('input');
  st1.type = 'text';
  st1.setAttribute("class", "smallbox");
  var lab2 = document.createElement('label');
  lab2.innerHTML = ' , ';
  lab2.setAttribute("class", "biglabel");
  var inpsym1 = document.createElement('input');
  inpsym1.type = 'text';
  inpsym1.setAttribute("class", "smallbox");
  var lab3 = document.createElement('label');
  lab3.innerHTML = ' , ';
  lab3.setAttribute("class", "biglabel");
  var stacksym1 = document.createElement('input');
  stacksym1.type = 'text';
  stacksym1.setAttribute("class", "smallbox");
  var lab4 = document.createElement('label');
  lab4.innerHTML = ' ) = ( ';
  lab4.setAttribute("class", "biglabel");
  var st2 = document.createElement('input');
  st2.type = 'text';
  st2.setAttribute("class", "smallbox");
  var lab5 = document.createElement('label');
  lab5.innerHTML = ' , ';
  lab5.setAttribute("class", "biglabel");
  var stacksym2 = document.createElement('input');
  stacksym2.type = 'text';
  stacksym2.setAttribute("class", "smallbox");
  var lab6 = document.createElement('label');
  lab6.innerHTML = ' )';

  td.appendChild(lab);
  td.appendChild(st1);
  td.appendChild(lab2);
  td.appendChild(inpsym1);
  td.appendChild(lab3);
  td.appendChild(stacksym1);
  td.appendChild(lab4);
  td.appendChild(st2);
  td.appendChild(lab5);
  td.appendChild(stacksym2);
  td.appendChild(lab6);
  tr.appendChild(td);
  tab_body.append(tr);
}

function newCFGrow(){
  var tab_body = document.getElementById("cfg_tab_body");
  var tr = document.createElement('tr');
  var td = document.createElement('td');

  var nonterm = document.createElement('input');
  nonterm.type = 'text';
  nonterm.setAttribute("class", "smallbox");

  var lab = document.createElement('label');
  lab.innerHTML = ' → ';
  lab.setAttribute("class", "biglabel");

  var prods = document.createElement('input');
  prods.type = 'text';

  td.appendChild(nonterm);
  td.appendChild(lab);
  td.appendChild(prods);
  tr.appendChild(td);
  tab_body.append(tr);
}
