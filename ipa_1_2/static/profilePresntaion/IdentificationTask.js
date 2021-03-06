
var left_profile = document.getElementById("slidecontainer");
var right_profile = document.getElementById("slidecontainer_right");
var nextLeftButton = document.getElementById("Next_left");
var nextRightButton = document.getElementById("Next_right");
var subjectResonseForm = document.getElementById("subjectResonseForm");

var subjectResonses = document.getElementById("subjectResonses");
var currentTrial = document.getElementById("trial");
var responseTimes = document.getElementById("RTs");
var profilesSides = document.getElementById("profilesSides");

var instructionContainer = document.getElementById("instructionContainer");
var textContainer = document.getElementById("textContainer");
var nextInstructionButton = document.getElementById("NextInstructionButton");

db_features = "features"
var current_profile = 0
var all_profiles_ids = task_profiles["artificials"]

var title = "Title new"
var right_end = "r"
var left_end = "l"
var value = "4"


function InjectProfileDataToHTML(title, right_end, left_end, value){
  basicProfileHTMLText = '<h3 id="title">'+ title + '</h3>\
    <div class="row"> \
      <div class="column side">'+ left_end + '</div> \
      <div class="column middle"> \
          <input type="range" min="1" max="100" value='+ value + ' class="slider" id="myRange" disabled="disabled">\
      </div>\
      <div class="column side">'+ right_end + '</div>\
  </div>';

    return basicProfileHTMLText;
}

function GetProfileFeatureData (feature) {
  value = feature.value;
  left_end = feature.l;
  right_end = feature.r;
  return right_end, left_end, value;

}

function GetProfileData(profile, features_list){
  text = ""
  for (i=0; i<features_list.length; i++ ) {
    feature = features_list[i]
    right_end, left_end, value = GetProfileFeatureData(profile[feature]);
    // check if the property/key is defined in the object itself, not in parent
    if (profile.hasOwnProperty(feature)) {
      text += InjectProfileDataToHTML(feature, right_end, left_end, value);
    }
  }
  return text
}

function _getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

// theese list right-left shoud match each other, and the html table cell sides
containers = [right_profile, left_profile];
buttons = [nextRightButton, nextLeftButton];

// Trials management
trialCounter = 0;
firstFastTrial = 4; // trial index of quick phase
instructionsTrial = 3; // trial to present quick phase instructions

// responses
pressed_button = ""; // right or left
buttons_presses = [];
profiles_possitions = [];
rts = [];
// constats:
left = "left";
right = "right";
sides = [right, left]

var t0;
var t1;

function _getStringFormField(val){
  return val.toString() + ",";
}

function RecordResponses(button){ // From button presss
  RecordTime();
  buttons_presses.push(button);
  pressed_button = button;
  subjectResonses.value += _getStringFormField(buttons_presses[current_profile]);
  currentTrial.value = _getStringFormField(current_profile);
  responseTimes.value += _getStringFormField(rts[current_profile]);
  profilesSides.value += _getStringFormField(profiles_possitions[current_profile]);
  NextTrial(); // increases current_profile
}



function RecordTime() {
  t1 = new Date();
  rts.push(t1-t0);
}
function InitiateTimeCount() {
  t0 = new Date();
}

function HandelResponseButtons(containers){
  nextLeftButton.style.display = 'none';
  nextRightButton.style.display = 'none';
  if(trialCounter<instructionsTrial){
    setTimeout(function() {nextLeftButton.style.display = 'block'}, 2000);
    setTimeout(function() {nextRightButton.style.display = 'block'}, 2000);
  } else if(trialCounter===instructionsTrial){
    instructionContainer.style.display = 'block'
    textContainer.innerText = instructionText.preQuickPhase;
    containers[0].style.display = 'none';
    containers[1].style.display = 'none';
  } else {
    setTimeout(function() {nextLeftButton.style.display = 'block'}, 1000);
    setTimeout(function() {nextRightButton.style.display = 'block'}, 1000);
  };
}

function HideAndShowContainers(containers){
  containers[0].style.display = 'none';
  containers[1].style.display = 'none';
  if(trialCounter!=instructionsTrial){
    setTimeout(function() {containers[0].style.display = 'block'}, 1000);
    setTimeout(function() {containers[1].style.display = 'block'}, 1000);
  };
}

function InitiateQuickIdentificationTask(){
  instructionContainer.style.display = "none"; // hiding instructions
  current_profile -=1;
  NextTrial();
}


function InitializeProfilePresentation(current_profile){
  var profile_features = task_profiles["subject"][db_features];
  var features_list = task_profiles["subject"]["features_order"];
  subject_profile_text = GetProfileData(profile_features, features_list);
  var profile_features = task_profiles["artificials"][current_profile][db_features];
  var features_list = task_profiles["artificials"][current_profile]["features_order"];
  artificial_profile_text = GetProfileData(profile_features, features_list);;
  subject_side = _getRndInteger(0,1)
  other_side = (subject_side - 1) * -1
  containers[subject_side].innerHTML = subject_profile_text
  profiles_possitions.push(sides[subject_side])
  containers[other_side].innerHTML = artificial_profile_text
  HideAndShowContainers(containers);
  HandelResponseButtons(containers);
  InitiateTimeCount();
}


function NextTrial(){
  current_profile +=1;
  trialCounter +=1;
  if(current_profile < all_profiles_ids.length){
      InitializeProfilePresentation(current_profile);
    } else {
      subjectResonseForm.submit();
}};


nextLeftButton.addEventListener("click",  function(){RecordResponses(left)})
nextRightButton.addEventListener("click",  function(){RecordResponses(right)})

// starting first_trial
instructionContainer.style.display = "none"; // hiding instructions
InitializeProfilePresentation(current_profile);
nextInstructionButton.addEventListener("click",  function(){InitiateQuickIdentificationTask()});
// leftCell = document.getElementById("leftCell");
// rightCell = document.getElementById("rightCell");
// rightCell.innerHTML = leftCell.innerHTML;
