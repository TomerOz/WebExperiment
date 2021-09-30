
// variable instructions_list is recived from the html

var nextButton = document.getElementById("NextInstructionButton");
var instructionTextContainer = document.getElementById("instructionContainer");
instructionsForm = document.getElementById('instructionsForm');
var fullScreenButton = document.getElementById('fullScreenButton');

currentInstruction = 0;

function HandleInstructions() {
  if(currentInstruction < instructions_list.length) {
      instructionTextContainer.innerHTML = instructions_list[currentInstruction];
      currentInstruction += 1;
  } else {
    // instructionTextContainer.textContent  = ""
    nextButton.disabled = true;
    instructionsForm.submit();
  };
};
HandleInstructions()

for (var i = 0; i < wordsToHighlight.length; i++) {
  instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace(wordsToHighlight[i],"<strong>" + wordsToHighlight[i] + "</strong>")
}
nextButton.addEventListener("click", HandleInstructions);
