
// variable instructions_list is recived from the html

var a_features_reff_name_1 = a_features_1.textContent;
var a_features_reff_name_2 = a_features_2.textContent;
var c_features_reff_name_1 = c_features_1.textContent;
var c_features_reff_name_2 = c_features_2.textContent;


var nextButton = document.getElementById("NextInstructionButton");
var instructionTextContainer = document.getElementById("instructionContainer");
instructionsForm = document.getElementById('instructionsForm');
var fullScreenButton = document.getElementById('fullScreenButton');
var picturesContainer = document.getElementById('picturesContainer');

currentInstruction = 0;

function HandleInstructions() {
  if(currentInstruction < instructions_list.length) {
      instructionTextContainer.innerHTML = instructions_list[currentInstruction];

      if (subject_group == "C"){
        instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace(a_features_reff_name_1, c_features_reff_name_1);
        instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace(a_features_reff_name_2, c_features_reff_name_2);
        instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace("האישיים", "");
      }
      
      if(picturesPaths[currentInstruction] != "nan"){
        picturesContainer.innerHTML = '<img class="center" src="' + picturesPaths[currentInstruction]+ '" alt="">'
      } else {
        picturesContainer.innerHTML = ""
      }
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


if (subject_group == "C"){
  instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace(a_features_reff_name_1, c_features_reff_name_1);
  instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace(a_features_reff_name_2, c_features_reff_name_2);
  instructionTextContainer.innerHTML = instructionTextContainer.innerHTML.replace("האישיים", "");
}

nextButton.addEventListener("click", HandleInstructions);
