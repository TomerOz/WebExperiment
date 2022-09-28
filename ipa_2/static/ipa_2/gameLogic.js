explanationTexts = document.getElementById("ExplanationTexts").textContent.split(",")

var [you_cohse,if_other,youll_get,otherll_get,and_if_other] = explanationTexts
var subjectChoice;
subjectChoice = "No Choice"

// Rows management:
rowA = document.getElementsByClassName("A");
rowB = document.getElementsByClassName("B");
aChoice = document.getElementById("A");
bChoice = document.getElementById("B");

rowATop = rowA[0];
rowABottom = rowA[1];

rowBTop = rowB[0];
rowBBottom = rowB[1];

rows = [{"Top" : rowATop, "Bottom": rowABottom, "button": aChoice},
        {"Top" : rowBTop, "Bottom": rowBBottom, "button": bChoice}];

function HighLightRow(rowTop, rowBottom){
  rowTop.classList.toggle("rowHighligt");
  rowTop.classList.toggle("topRowHighligt");
  rowBottom.classList.toggle("rowHighligt");
  rowBottom.classList.toggle("bottomRowHighligt");
};


aChoice.addEventListener("mouseover", function(){HighLightRow(rowATop, rowABottom)});
aChoice.addEventListener("mouseout", function(){HighLightRow(rowATop, rowABottom)});
bChoice.addEventListener("mouseover", function(){HighLightRow(rowBTop, rowBBottom)});
bChoice.addEventListener("mouseout", function(){HighLightRow(rowBTop, rowBBottom)});

// Cells management:
cellAa = document.getElementsByClassName("Aa");
cellAb = document.getElementsByClassName("Ab");
cellBa = document.getElementsByClassName("Ba");
cellBb = document.getElementsByClassName("Bb");

cells = [cellAa, cellAb, cellBa, cellBb];

function HighLightCell(cellGroup){
  for (var i = 0; i < cellGroup.length; i++)
    cellGroup[i].classList.toggle("cellHighlighted");
};

for (var j = 0; j < cells[0].length; j++) {
  cellAa[j].addEventListener("mouseover", function(){HighLightCell(cellAa)});
  cellAa[j].addEventListener("mouseout", function(){HighLightCell(cellAa)});

  cellAb[j].addEventListener("mouseover", function(){HighLightCell(cellAb)});
  cellAb[j].addEventListener("mouseout", function(){HighLightCell(cellAb)});

  cellBa[j].addEventListener("mouseover", function(){HighLightCell(cellBa)});
  cellBa[j].addEventListener("mouseout", function(){HighLightCell(cellBa)});

  cellBb[j].addEventListener("mouseover", function(){HighLightCell(cellBb)});
  cellBb[j].addEventListener("mouseout", function(){HighLightCell(cellBb)});
};


//  Choice Mangement
explantionsDiv = document.getElementsByClassName("explantions")[0];

function ChooseRow(rowIndex){
  rows[rowIndex]["Top"].classList.toggle("rowSelected");
  rows[rowIndex]["Bottom"].classList.toggle("rowSelected");
  rows[rowIndex]["button"].classList.toggle("rowSelected");
  otherIndex = (rowIndex - 1) * (rowIndex - 1)
  rows[otherIndex]["Top"].classList.remove("rowSelected");
  rows[otherIndex]["Bottom"].classList.remove("rowSelected");
  rows[otherIndex]["button"].classList.remove("rowSelected");
  explantionsDiv.style.display = "block";
  explantionsDiv.innerHTML  = ChoiceToText(rowIndex);
  subjectChoice = stratgies[rowIndex]
  nextProfileButton.disabled = false;
};

function RemoveRowsSelection(){
  rows[0]["Top"].classList.remove("rowSelected");
  rows[0]["Bottom"].classList.remove("rowSelected");
  rows[0]["button"].classList.remove("rowSelected");
  rows[1]["Top"].classList.remove("rowSelected");
  rows[1]["Bottom"].classList.remove("rowSelected");
  rows[1]["button"].classList.remove("rowSelected");
}

stratgies = [gamesJSON["A"], gamesJSON["B"]];
// payoffs arranged by others
subject_payoffs = [[gamesJSON["pA_Aa"], gamesJSON["pA_Ab"]],[gamesJSON["pA_Ba"], gamesJSON["pA_Bb"]]];
other_payoffs = [[gamesJSON["pB_Aa"], gamesJSON["pB_Ab"]],[gamesJSON["pB_Ba"], gamesJSON["pB_Bb"]]];

function ChoiceToText(rowIndex){
  youIfOther_a = subject_payoffs[rowIndex][0]
  youIfOther_b = subject_payoffs[rowIndex][1]
  otherIfOther_a = other_payoffs[rowIndex][0]
  otherIfOther_b = other_payoffs[rowIndex][1]

  var [you_cohse,if_other,youll_get,otherll_get,and_if_other] = explanationTexts
  choiceText = you_cohse + ": "  + "<strong>" +stratgies[rowIndex] + "</strong>"
  textIfOther_a =  if_other + " " + "<strong>" + stratgies[0] + "</strong>" + " " + youll_get + " " + youIfOther_a + " " + otherll_get + " " + otherIfOther_a
  textIfOther_b = and_if_other + " " + "<strong>" + stratgies[1] + "</strong>" + " " + youll_get + " " + youIfOther_b + " " + otherll_get + " " + otherIfOther_b
  finalText = choiceText + "<br>" + textIfOther_a + "<br>" + textIfOther_b
  return finalText
}

aChoice.addEventListener("click", function(){ChooseRow(0)});
bChoice.addEventListener("click", function(){ChooseRow(1)});

// Game display control
showMatrixButton = document.getElementById("showMatrixButton");
matrixContainer = document.getElementById("matrixContainer");


if(document.title != "profile"){
  matrixContainer.style.display = "none";
  showMatrixButton.addEventListener("click" , function(){
    matrixContainer.style.display = "block";
  });
}
