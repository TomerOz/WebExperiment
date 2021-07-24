
// variable instructions_list is recived from the html

var nextButton = document.getElementById("NextStepButton");
var instructionTextContainer = document.getElementById("instructionContainer");
var instructionsForm = document.getElementById('instructionsForm');
var testForm = document.getElementById('testForm');
var showMatrixButton = document.getElementById('showMatrixButton');

currentInstruction = 0;
correctAnswers = ["Ready button", 1, 0];
currentQuestion = 0;
wasCorrect = false;

function HandleInstructions() {
  if(wasCorrect){
    if(currentInstruction < instructions_list.length) {
      instructionTextContainer.textContent = instructions_list[currentInstruction];
      if(currentInstruction == instructions_list.length-1){
        testForm.style.display = "block";
      };
      currentInstruction += 1;
    };
  };
};

nextButton.addEventListener("click", HandleInstructions);

function recieveChoice(rowIndex){
  if(rowIndex == correctAnswers[currentQuestion]){
    currentQuestion += 1;
    wasCorrect = true;
    HandleInstructions();
    if(currentQuestion < correctAnswers.length){
      wasCorrect = false;
    };
  };
};

wasCorrect = true;
HandleInstructions();
wasCorrect = false;



aChoice.addEventListener("click", function(){recieveChoice(0)});
bChoice.addEventListener("click", function(){recieveChoice(1)});
showMatrixButton.addEventListener("click", function(){recieveChoice("Ready button")});

if(errorsJSON.length > 0){
  testForm.style.display = "block";
  instructionTextContainer.textContent = instructions_list[instructions_list.length-1];
  showMatrixButton.click();
  showMatrixButton.removeEventListener("click", function(){recieveChoice("Ready button")})
  aChoice.removeEventListener("click", function(){recieveChoice(0)});
  bChoice.removeEventListener("click", function(){recieveChoice(1)});
}
