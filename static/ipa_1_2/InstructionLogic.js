
// variable instructions_list is recived from the html

var nextButton = document.getElementById("NextInstructionButton");
var instructionTextContainer = document.getElementById("instructionContainer");
instructionsForm = document.getElementById('instructionsForm');
var fullScreenButton = document.getElementById('fullScreenButton');

currentInstruction = 0;

function HandleInstructions() {
  if(currentInstruction < instructions_list.length) {
      instructionTextContainer.textContent = instructions_list[currentInstruction];
      currentInstruction += 1;
  } else {
    // instructionTextContainer.textContent  = ""
    instructionsForm.submit();
  };
};
HandleInstructions()
nextButton.addEventListener("click", HandleInstructions);
