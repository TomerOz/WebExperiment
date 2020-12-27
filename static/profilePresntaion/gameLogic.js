
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
  explantionsDiv.innerHTML  = ChoiceToText(rowIndex);

};

stratgies = [gameJSON["A"], gameJSON["B"]];
// payoffs arranged by others
subject_payoffs = [[gameJSON["pA_Aa"], gameJSON["pA_Ab"]],[gameJSON["pA_Ba"], gameJSON["pA_Bb"]]];
other_payoffs = [[gameJSON["pB_Aa"], gameJSON["pB_Ab"]],[gameJSON["pB_Ba"], gameJSON["pB_Bb"]]];
function ChoiceToText(rowIndex){
  youIfOther_a = subject_payoffs[rowIndex][0]
  youIfOther_b = subject_payoffs[rowIndex][1]
  otherIfOther_a = other_payoffs[rowIndex][0]
  otherIfOther_b = other_payoffs[rowIndex][1]

  choiceText = "You Chose: " + stratgies[rowIndex]
  textIfOther_a = "if other chooce " + stratgies[0] + " youll get " + youIfOther_a + " and the other will get " + otherIfOther_a
  textIfOther_b = "and if other chooce " + stratgies[1] + " youll get " + youIfOther_b + " and the other will get " + otherIfOther_b
  finalText = choiceText + "<br>" + textIfOther_a + "<br>" + textIfOther_b
  return finalText
}

aChoice.addEventListener("click", function(){ChooseRow(0)});
bChoice.addEventListener("click", function(){ChooseRow(1)});

// Game display control
showMatrixButton = document.getElementById("showMatrixButton");
matrixContainer = document.getElementById("matrixContainer");

matrixContainer.style.display = "none";
showMatrixButton.addEventListener("click" , function(){
  matrixContainer.style.display = "block";
});
