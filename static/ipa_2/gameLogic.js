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

var stratgies;
var subject_payoffs;
var other_payoffs;
var currentGameName;
explantionsDiv = document.getElementsByClassName("explantions")[0];


function UpdateGame() {
  profile_data = context[all_profiles_ids[current_profile]];
  profile_game = profile_data.profile_games[profile_data.game_index];
  game = gamesJSON[profile_game];
  currentGameName = profile_game;

  stratgies = [game["A"], game["B"]];
  subject_payoffs = [[game["pA_Aa"], game["pA_Ab"]],[game["pA_Ba"], game["pA_Bb"]]];
  other_payoffs = [[game["pB_Aa"], game["pB_Ab"]],[game["pB_Ba"], game["pB_Bb"]]];

  profile_data.game_index++; // Setting ready the next game
}

function updateMatrixCells() {
  youAa.textContent = subject_payoffs[0][0];
  youAb.textContent = subject_payoffs[0][1];
  youBa.textContent = subject_payoffs[1][0];
  youBb.textContent = subject_payoffs[1][1];
  otherAa.textContent = other_payoffs[0][0];
  otherAb.textContent = other_payoffs[0][1];
  otherBa.textContent = other_payoffs[1][0];
  otherBb.textContent = other_payoffs[1][1];
  aChoice.textContent = stratgies[0];
  bChoice.textContent = stratgies[1];
  Aother.textContent = stratgies[0];
  Bother.textContent = stratgies[1];
}

function emptyMatrixCells() {
  aChoice.textContent = stratgies[0];
  bChoice.textContent = stratgies[1];
  Aother.textContent = stratgies[0];
  Bother.textContent = stratgies[1];
  
  youAa.textContent = " ";
  youAb.textContent = " ";
  youBa.textContent = " ";
  youBb.textContent = " ";
  otherAa.textContent = " ";
  otherAb.textContent = " ";
  otherBa.textContent = " ";
  otherBb.textContent = " ";
}

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
function HighLightRow(rowTop, rowBottom){
  rowTop.classList.toggle("rowHighligt");
  rowTop.classList.toggle("topRowHighligt");
  rowBottom.classList.toggle("rowHighligt");
  rowBottom.classList.toggle("bottomRowHighligt");
};

function HighLightCell(cellGroup){
  for (var i = 0; i < cellGroup.length; i++)
    cellGroup[i].classList.toggle("cellHighlighted");
};

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

function ChoiceToText(rowIndex){
  if(document.title != "profile"){
    stratgies = [gameJSON["A"], gameJSON["B"]];
    subject_payoffs = [[gameJSON["pA_Aa"], gameJSON["pA_Ab"]],[gameJSON["pA_Ba"], gameJSON["pA_Bb"]]];
    other_payoffs = [[gameJSON["pB_Aa"], gameJSON["pB_Ab"]],[gameJSON["pB_Ba"], gameJSON["pB_Bb"]]];

    youIfOther_a = subject_payoffs[rowIndex][0]
    youIfOther_b = subject_payoffs[rowIndex][1]
    otherIfOther_a = other_payoffs[rowIndex][0]
    otherIfOther_b = other_payoffs[rowIndex][1]
  } else {
    youIfOther_a = subject_payoffs[rowIndex][0]
    youIfOther_b = subject_payoffs[rowIndex][1]
    otherIfOther_a = other_payoffs[rowIndex][0]
    otherIfOther_b = other_payoffs[rowIndex][1]
  }

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
