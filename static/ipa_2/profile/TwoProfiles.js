
var left_profile = document.getElementById("slidecontainer");
var right_profile = document.getElementById("slidecontainer_right");
var leftActionButton = document.getElementById("leftAction");
var leftIgnoreButton = document.getElementById("leftIgnore");
var rightActionButton = document.getElementById("rightAction");
var rightIgnoreButton = document.getElementById("rightIgnore");
var subjectResonseForm = document.getElementById("subjectResonseForm");
var subjectResonses = document.getElementById("subjectResonses");
var currentTrial = document.getElementById("trial");
var responseTimes = document.getElementById("RTs");
var profilesSides = document.getElementById("profilesSides");
var profilesList = document.getElementById("profilesList");
var profilesListLeft = document.getElementById("profilesListLeft");
var profilesListRight = document.getElementById("profilesListRight");
var instructionContainer = document.getElementById("instructionContainer");
var textContainer = document.getElementById("textContainer");
var nextInstructionButton = document.getElementById("NextInstructionButton");
var chooseSetContainer = document.getElementById("chooseSetContainer");
var setAButton = document.getElementById("setAButton");
var setCButton = document.getElementById("setCButton");
var trialFeatureOrder = document.getElementById("trialFeatureOrder");
var buttonsTable = document.getElementById("buttonsTable");
var trials_set = document.getElementById("trials_set");
var nextTrialButton = document.getElementById("nextTrialButton");

var PeofileWaitTime = 1000 // 7000; // 15 seconds until button appears
var BetweenProfilesInterval = 4000// 1000; // 1 seconds between profiles
var BetweenProfilesIntervalButtons = 6000// 1000; // 1 seconds between profiles

var db_features = "features";
var current_profile = 0;
var task_profiles = {
                      "A": task_profiles_A,
                      "C": task_profiles_C,
                    }
var chosenSet = "" // A or C

var no_one_counter = 0;
var title = "Title new";
var right_end = "r";
var left_end = "l";
var value = "4";

var shootActionText = shootAction.innerText;
var helpActionText = helpAction.innerText;
var ignoreActionText = ignoreAction.innerText;
var shootThisProfileText = shootThisProfile.innerText;
var helpThisProfileText = helpThisProfile.innerText;
var ignoreThisProfileText = ignoreThisProfile.innerText;
var youChoseText = youChose.innerText;
var actionReferenceWord = {"shoot":shootThisProfileText,"help":helpThisProfileText}
var actionWord = {"shoot":shootActionText,"help":helpActionText}
var sidesNames = {"left": "שמאל", "right": "ימין"}
explanationsTextsVariables.style.display = "none";
var gameMatrices = {"shoot":shootMatrix,"help":helpMatrix}
var profileChosenSide = "";


function getDecisionText(chosenSide) {
  text = youChoseText + " " + actionWord[current_game] + " " + actionReferenceWord[current_game] + " " + sidesNames[chosenSide] + "\n"
  notChosenSide = "right"
  if(chosenSide == "right"){
    notChosenSide = "left"
  }
  text = text + "ו" + youChoseText + " " + ignoreActionText + " " + ignoreThisProfileText + " " + sidesNames[notChosenSide]
  return text
}

function makeDecision(chosenSide){
  profileChosenSide = chosenSide;
  text = getDecisionText(chosenSide);
  explanationsTexts.style.display = "block";
  explanationsTextsPar.innerText = text;
  gameMatrices[current_game].style.display = "block";
  other_game = "help";
  if(current_game=="help"){
    other_game = "shoot";
  }
    gameMatrices[other_game].style.display = "none";
}



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

function changeFontSize(fontSize) {
  var cols = document.getElementsByClassName('side');
  for(i = 0; i < cols.length; i++) {
    cols[i].style.fontSize  = fontSize + "px";
  }
}

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
containers = [left_profile, right_profile];
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
sides = [left, right]

var t0;
var t1;

function _getStringFormField(val){
  return val.toString() + ",";
}

function RecordResponses(){ // From button presss
  RecordTime();
  button = profileChosenSide;
  var profilesChoseSet = task_profiles[chosenSet];
  var idsChosenSet = task_profiles[chosenSet].profiles_list
  var profile_id_1 = idsChosenSet[current_profile][0]
  var profile_id_2 = idsChosenSet[current_profile][1]
  var profile_1 = profilesChoseSet[idsChosenSet[current_profile][0]]
  var profile_2 = profilesChoseSet[idsChosenSet[current_profile][1]]
  var profile_features_1 = profile_1.features;
  var profile_features_2 = profile_2.features;
  var name_1 = profile_1.name
  var name_2 =  profile_2.name

  buttons_presses.push(button);
  pressed_button = button;
  subjectResonses.value += _getStringFormField(buttons_presses[current_profile]);
  currentTrial.value = _getStringFormField(current_profile);
  responseTimes.value += _getStringFormField(rts[current_profile]);
  profilesSides.value += _getStringFormField(profiles_possitions[current_profile]);
  profilesList.value += _getStringFormField(name_1);
  trials_set.value += _getStringFormField(chosenSet);

  gameCooperativeHead.style.display = "none";
  gameCompetitiveHead.style.display = "none";
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
  setTimeout(function(){leftAction.style.display = 'block';}, PeofileWaitTime);
  setTimeout(function(){leftIgnore.style.display = 'block';}, PeofileWaitTime);
  setTimeout(function(){rightAction.style.display = 'block';}, PeofileWaitTime);
  setTimeout(function(){rightIgnore.style.display = 'block';}, PeofileWaitTime);
}

function HideAndShowContainers(containers){
  containers[0].style.display = 'none';
  containers[1].style.display = 'none';
  buttonsTable.style.display = "block"; // hiding instructions
  leftAction.style.display = 'none';
  leftIgnore.style.display = 'none';
  rightAction.style.display = 'none';
  rightIgnore.style.display = 'none';
  setTimeout(function() {containers[0].style.display = 'block'}, PeofileWaitTime);
  setTimeout(function() {containers[1].style.display = 'block'}, PeofileWaitTime);
};

function HideContainers(containers){
  containers[0].style.display = 'none';
  containers[1].style.display = 'none';
  buttonsTable.style.display = "block"; // hiding instructions
  leftAction.style.display = 'none';
  leftIgnore.style.display = 'none';
  rightAction.style.display = 'none';
  rightIgnore.style.display = 'none';
};

function InitializeProfilePresentation(current_profile){

  var profilesChoseSet = task_profiles[chosenSet];
  var idsChosenSet = task_profiles[chosenSet].profiles_list
  var profile_id_1 = idsChosenSet[current_profile][0]
  var profile_id_2 = idsChosenSet[current_profile][1]
  var profile_1 = profilesChoseSet[idsChosenSet[current_profile][0]]
  var profile_2 = profilesChoseSet[idsChosenSet[current_profile][1]]
  var profile_features_1 = profile_1.features;
  var profile_features_2 = profile_2.features;
  var name_1 = profile_1.name
  var name_2 =  profile_2.name

  trialFeatureOrder.value = trialFeatureOrder.value + profile_1["features_order"].toString() + "-**NextProfile**-";

  var features_list = profile_1.features_order

  text_1 = GetProfileData(profile_features_1, features_list);
  text_2 = GetProfileData(profile_features_2, features_list);;

  other_profile_1_side = _getRndInteger(0,1);
  other_profile_2_side = (other_profile_1_side - 1) * -1;

  positions_temp = ["Left = ", "Right = "];
  positions_temp[other_profile_1_side] = positions_temp[other_profile_1_side] + name_1;
  positions_temp[other_profile_2_side] = positions_temp[other_profile_2_side] + name_2;
  containers[other_profile_1_side].innerHTML = text_1;
  containers[other_profile_2_side].innerHTML = text_2;
  profiles_possitions.push(positions_temp.toString().replace(",", "//"));

  sides_profiles_lists = [profilesListLeft, profilesListRight]
  sides_profiles_lists[other_profile_1_side].value += _getStringFormField(name_1);
  sides_profiles_lists[other_profile_2_side].value += _getStringFormField(name_2);

  current_game = gameTypes[current_profile];
  gamesToActions = {"shoot": shootActionText, "help": helpActionText}
  leftAction.innerText = gamesToActions[current_game]
  rightAction.innerText = gamesToActions[current_game]

  if(chosenSet=="C"){
    changeFontSize(24);
  }

  HideAndShowContainers(containers);
  HandelResponseButtons(containers);
  InitiateTimeCount();
}

function showInstructions(){
  text = "בקרוב תוצג בפניך סיטואציה חדשה ולאחר מכן פרופילים של שני אנשים חדשים"
  if(current_profile < 2) {
    text = text + "\n" + "\n" + "\n" + "אימון"
    BetweenProfilesInterval = 5000
    BetweenProfilesIntervalButtons = 7000
  }
  if(current_profile == 2) {
    text = text + "\n" + "\n" + "\n" + "האימון נגמר - כעת המטלה תמשיך באופן דומה לאימון"
    BetweenProfilesInterval = 7000
    BetweenProfilesIntervalButtons = 9000
  }
  if(current_profile > 2) {
    BetweenProfilesInterval = 4000
    BetweenProfilesIntervalButtons = 6000
  }

  trialInstruction.style.display = "block"; // hiding instructions
  trialInstructionHeader.innerText = text
  setTimeout(function() {trialInstruction.style.display = "none";}, BetweenProfilesInterval);
}
function NextTrial(){
  HideContainers(containers);

  buttonsTable.style.display = "none"; // hiding instructions
  explanationsTexts.style.display = "none";

  showInstructions();
  setTimeout(function() {showHideHeaders()}, BetweenProfilesInterval);
  setTimeout(function() {chooseSetContainer.style.display = "block";}, BetweenProfilesIntervalButtons);

  var profilesChoseSet = task_profiles[chosenSet];
  var idsChosenSet = task_profiles[chosenSet].profiles_list

  current_profile +=1;
  trialCounter +=1;
  if(current_profile >= idsChosenSet.length){
      subjectResonseForm.submit();
    };
};

function hideChooseSetContainer(){
  chooseSetContainer.style.display = "none";
}
function chooseFeaturesSet(set){
  chosenSet = set;
  hideChooseSetContainer();
  // set choice logic here...
  // ...
  // ...
  InitializeProfilePresentation(current_profile);
}

function showHideHeaders(){
  current_game = gameTypes[current_profile];
  if(current_game == "shoot"){
    gameCompetitiveHead.style.display = "block";
    gameCooperativeHead.style.display = "none";
  } else {
    gameCooperativeHead.style.display = "block";
    gameCompetitiveHead.style.display = "none";
  };
};


leftActionButton.addEventListener("click",  function(){makeDecision(left)})
leftIgnoreButton.addEventListener("click",  function(){makeDecision(left)})
rightActionButton.addEventListener("click",  function(){makeDecision(right)})
rightIgnoreButton.addEventListener("click",  function(){makeDecision(right)})
nextTrialButton.addEventListener("click",  function(){RecordResponses()})

setAButton.addEventListener("click",  function(){chooseFeaturesSet("A")})
setCButton.addEventListener("click",  function(){chooseFeaturesSet("C")})


// starting first_trial
instructionContainer.style.display = "none"; // hiding instructions
buttonsTable.style.display = "none"; // hiding instructions

gameCooperativeHead.style.display = "none";
gameCompetitiveHead.style.display = "none";
chooseSetContainer.style.display = "none";
helpMatrix.style.display = "none";
shootMatrix.style.display = "none";
explanationsTexts.style.display = "none";

showInstructions();
setTimeout(function() {showHideHeaders()}, BetweenProfilesInterval);
setTimeout(function() {chooseSetContainer.style.display = "block";}, BetweenProfilesIntervalButtons);
