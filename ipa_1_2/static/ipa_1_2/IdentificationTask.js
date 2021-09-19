
var left_profile = document.getElementById("slidecontainer");
var right_profile = document.getElementById("slidecontainer_right");
var nextLeftButton = document.getElementById("Next_left");
var nextRightButton = document.getElementById("Next_right");
var noneOfThemButton = document.getElementById("NoneOfThem");
var subjectResonseForm = document.getElementById("subjectResonseForm");
var responseSignal = document.getElementById("responseSignal");
var subjectResonses = document.getElementById("subjectResonses");
var currentTrial = document.getElementById("trial");
var responseTimes = document.getElementById("RTs");
var profilesSides = document.getElementById("profilesSides");
var profilesList = document.getElementById("profilesList");
var instructionContainer = document.getElementById("instructionContainer");
var textContainer = document.getElementById("textContainer");
var nextInstructionButton = document.getElementById("NextInstructionButton");

var PeofileWaitTime = 15000; // 15 seconds until button appears
var BetweenProfilesInterval = 1000; // 1 seconds between profiles

var db_features = "features";
var current_profile = 0;
var all_profiles_ids = task_profiles["artificials"]["profiles_list"];

var title = "Title new";
var right_end = "r";
var left_end = "l";
var value = "4";

function InjectProfileDataToHTML(title, right_end, left_end, value, feature_name){
  basicProfileHTMLText = '<h3 id="title">'+ feature_name + '</h3>\
    <div class="row"> \
      <div class="column side">'+ left_end + '</div> \
      <div class="column middle"> \
          <input type="range" min="1" max="100" value='+ value + ' class="slider" id="myRange" disabled="disabled">\
      </div>\
      <div class="column side">'+ right_end + '</div>\
  </div>';
    return basicProfileHTMLText;
};

function GetProfileFeatureData (feature) {
  value = feature.value;
  left_end = feature.l;
  right_end = feature.r;
  name = feature.name_to_present;
  return right_end, left_end, value, name;
};

function GetProfileData(profile, features_list){
  text = ""
  for (i=0; i<features_list.length; i++ ) {
    feature = features_list[i]
    right_end, left_end, value, feature_name = GetProfileFeatureData(profile[feature]);
    // check if the property/key is defined in the object itself, not in parent
    if (profile.hasOwnProperty(feature)) {
      text += InjectProfileDataToHTML(feature_name, right_end, left_end, value, feature_name);
    }
  }
  return text
}

function _getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1) ) + min;
}

// theese lists right-left shoud match each other, and the html table cell sides
containers = [right_profile, left_profile];
// buttons = [nextRightButton, nextLeftButton]; to delete 22.08.21

// Trials management
trialCounter = 0;

// responses
pressed_button = ""; // right or left
buttons_presses = [];
profiles_possitions = [];
rts = [];
// constats:
left = "left";
right = "right";
noneOfThemValue = "no one"
sides = [right, left]

var t0;
var t1;

function _getStringFormField(val){
  return val.toString() + ",";
}

function RecordResponses(button){ // From button presss
  RecordTime();
  profile_id = task_profiles["artificials"]["profiles_list"][current_profile]
  buttons_presses.push(button);
  pressed_button = button;
  subjectResonses.value += _getStringFormField(buttons_presses[current_profile]);
  currentTrial.value = _getStringFormField(current_profile);
  responseTimes.value += _getStringFormField(rts[current_profile]);
  profilesSides.value += _getStringFormField(profiles_possitions[current_profile]);
  profilesList.value += _getStringFormField(task_profiles["artificials"][profile_id]["name"]);
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
  setTimeout(function(){Next_left.style.display = 'block';}, PeofileWaitTime);
  setTimeout(function(){Next_right.style.display = 'block';}, PeofileWaitTime);
}

function HideAndShowContainers(containers){
  containers[0].style.display = 'none';
  containers[1].style.display = 'none';
  Next_left.style.display = 'none';
  Next_right.style.display = 'none';
  responseSignal.style.display = 'none';
  setTimeout(function() {containers[0].style.display = 'block'}, BetweenProfilesInterval);
  setTimeout(function() {containers[1].style.display = 'block'}, BetweenProfilesInterval);
};

function InitializeProfilePresentation(current_profile){
  profile_id = task_profiles["artificials"]["profiles_list"][current_profile]
  var features_list = task_profiles["artificials"][profile_id]["features_order"];
  var profile_features = task_profiles["subject"][db_features];
  subject_profile_text = GetProfileData(profile_features, features_list);
  var profile_features = task_profiles["artificials"][profile_id][db_features];
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
noneOfThemButton.addEventListener("click",  function(){RecordResponses(noneOfThemValue)})



// starting first_trial
instructionContainer.style.display = "none"; // hiding instructions
InitializeProfilePresentation(current_profile);
