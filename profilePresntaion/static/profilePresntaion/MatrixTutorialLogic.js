
// variable instructions_list is recived from the html

var nextButton = document.getElementById("NextStepButton");
var instructionTextContainer = document.getElementById("instructionContainer");
instructionsForm = document.getElementById('instructionsForm');

currentInstruction = 0;
correctAnswers = [1, 0];
currentQuestion = 0;
wasCorrect = false;

function HandleInstructions() {
  if(wasCorrect){
    if(currentInstruction < instructions_list.length) {
      instructionTextContainer.textContent = instructions_list[currentInstruction];
      currentInstruction += 1;
    } else {
      // instructionTextContainer.textContent  = ""
      instructionsForm.submit();
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
