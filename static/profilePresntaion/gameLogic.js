rowA = document.getElementsByClassName("A");
rowB = document.getElementsByClassName("B");
showMatrixButton = document.getElementById("showMatrixButton");
matrixContainer = document.getElementById("matrixContainer");

rowATop = rowA[0];
rowABottom = rowA[1];

rowBTop = rowB[0];
rowBBottom = rowB[1];

aChoice = document.getElementById("A");
bChoice = document.getElementById("B");

rows = [{"Top" : rowATop, "Bottom": rowABottom, "button": aChoice},
        {"Top" : rowBTop, "Bottom": rowBBottom, "button": bChoice}];

function HighLightRow(rowTop, rowBottom){
  rowTop.classList.toggle("rowHighligt");
  rowTop.classList.toggle("topRowHighligt");
  rowBottom.classList.toggle("rowHighligt");
  rowBottom.classList.toggle("bottomRowHighligt");
};

function ChooseRow(rowIndex){
  rows[rowIndex]["Top"].classList.toggle("rowSelected");
  rows[rowIndex]["Bottom"].classList.toggle("rowSelected");
  rows[rowIndex]["button"].classList.toggle("rowSelected");
  otherIndex = (rowIndex - 1) * (rowIndex - 1)
  rows[otherIndex]["Top"].classList.remove("rowSelected");
  rows[otherIndex]["Bottom"].classList.remove("rowSelected");
  rows[otherIndex]["button"].classList.remove("rowSelected");

};

aChoice.addEventListener("mouseover", function(){HighLightRow(rowATop, rowABottom)});
aChoice.addEventListener("mouseout", function(){HighLightRow(rowATop, rowABottom)});
bChoice.addEventListener("mouseover", function(){HighLightRow(rowBTop, rowBBottom)});
bChoice.addEventListener("mouseout", function(){HighLightRow(rowBTop, rowBBottom)});

//  Develop a selection feedback that overides all the rest of the event
aChoice.addEventListener("click", function(){ChooseRow(0)});
bChoice.addEventListener("click", function(){ChooseRow(1)});

matrixContainer.style.display = "none";
showMatrixButton.addEventListener("click" , function(){
  matrixContainer.style.display = "block";
});
//
// topRowHighligt
// bottomRowHighligt
