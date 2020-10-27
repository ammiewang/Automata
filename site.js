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
        document.getElementById("cfgop").style.display = "block";
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

  var table = document.createElement('table');
  table.setAttribute('class', 'center');
  table.setAttribute('id', 'original_table');
  table.classList.add('table');

  var thead = document.createElement('thead');
  var headRow = document.createElement('tr');

  var th = document.createElement('th');
  th.appendChild(document.createTextNode(''));
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
    var lab = document.createElement('label');
    if (accs.includes(i)){
      if (start_states.includes(i)){
        lab.innerHTML = "=> " + i + " F";
      } else{
        lab.innerHTML = i + " F";
      }
    } else{
      if (start_states.includes(i)){
        lab.innerHTML = "=> " + i;
      } else {
        lab.innerHTML = i;
      }
    }
    tr.appendChild(lab);
    for (var j = 0; j < alphabet.length; j++) {
      var td = document.createElement('td');
      td.classList.add("input");
      var input = document.createElement('input');
      input.type = "text";
      td.appendChild(input);
      tr.appendChild(td);
    }

    tbody.appendChild(tr);
  }

  table.appendChild(thead);
  table.appendChild(tbody);
  //newDiv.appendChild(table);
  $('#enter_dnfa_inp').before(table);

}

function dnfaGenRegex(){
  var prevDiv = document.getElementById("dnfa_inp");
  prevDiv.style.display = "none";
}
