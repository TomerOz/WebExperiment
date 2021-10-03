var slidecontainer = document.getElementById("slidecontainer");
var resonsesForm = document.getElementById("subjectResonseForm");
var profilesList = document.getElementById("profilesList");
var showReportButton = document.getElementById('showReportButton');
var moreSimilarity = document.getElementById('moreSimilarity');
var lessSimilarity = document.getElementById('lessSimilarity');
var similarityInput = document.getElementById('similarityInput');
var subjectResonses = document.getElementById('subjectResonses');
var profilesDescriptions = document.getElementById('profilesDescriptions'); // the hidden input fiel in the hidden form
var similarityReportSection = document.getElementById("SimilarityReportSection");
var instrucionSection = document.getElementById("instrucion");
var nextProfileButtonSection = document.getElementById("NextProfileButtonSection");
var trialFeatureOrder = document.getElementById("trialFeatureOrder");
var presentProfileAgainButton = document.getElementById("presentProfileAgainButton");
var featuresTable = document.getElementById("featuresTable");
var nextFeatureButton = document.getElementById("nextFeatureButton");
var inTaskInstructions = document.getElementById("inTaskInstructions");
var inTaskInstructionsText = document.getElementById("inTaskInstructionsText");
var nextFromInstructionsButton = document.getElementById("nextFromInstructions");
var nextProfileButton = document.getElementById("NextProfileButton");

const event = new Event('NewProfile');

var minwWordsPerDescription = 0;
var milisecondsPerFeature = 1000; //2000;
var countDownMiliSeconds = 100; //1500;
var buttonActivationDelay = 60; //6000; // cnages in presentProfileAgain
var buttonActivationDelayOriginal = 60 // 6000
var featuresPresentaionNumber = 1; // indicating the first presentaion
var presentationNumber = 2; // total ammount of presentation
var db_features = "features"
var current_profile = 0;
var all_profiles_ids = context["profiles_list"]
var title = "Title new"
var right_end = "r"
var left_end = "l"
var value = "4"
var t0;
var t1;
var reportT0
var reportT1
var rts = [];
var pRts = [];
var featuresOrderOfPresentation = [];
var preProfile = "מיד תחל הצגת פרופיל חדש"
var texts_pre_profile = [preProfile, 3,2,1]
var pre_profile_counter = 0
var feature_presentaion_index;
var buttonClicked = false;
var intervalID;
var changeRate = 25;
var contiousDelay = 500;
var direction;
var sim_value = parseInt(similarityInput.value);
var nPracticeTrials = n_practice_trials // n_practice_trials comes from views
var instructionEndOfPracticePresnted = false;
var timeOutIntervalIDs = [];

function shuffle(array) {
  let currentIndex = array.length,  randomIndex;
  // While there remain elements to shuffle...
  while (currentIndex != 0) {
    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;
    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }
  return array;
}

function array_move(arr, old_index, new_index) {
    if (new_index >= arr.length) {
        var k = new_index - arr.length + 1;
        while (k--) {
            arr.push(undefined);
        }
    }
    arr.splice(new_index, 0, arr.splice(old_index, 1)[0]);
    return arr; // for testing
};

function getShuffledNoReppetition(array){
  arrayOriginal = array.slice();
  shuffle(array);
  middleIndexes = [...Array(array.length).keys()];
  middleIndexes = middleIndexes.slice(1,middleIndexes.length-1);
  while ((array[0] == arrayOriginal[0]) || (array[0] == arrayOriginal[array.length-1]) || (array[array.length-1] == arrayOriginal[array.length-1]) || (array[array.length-1] == arrayOriginal[0])){
    shuffle(array);
  };
  return array;
};

function InjectProfileDataToHTML(title, right_end, left_end, value){
  basicProfileHTMLText = '<br><br><br>\
    <h4 id="title">'+ title + '</h4> <br>\
    <div class="row"> \
      <div class="column side">'+ left_end + '</div> \
      <div class="column middle"> \
          <input type="range" min="1" max="100" value='+ value + ' class="slider" id="featureRange" disabled="disabled">\
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
};

function startReportPhase(){
  if(reportT0 == null){
    reportT0 = new Date();
  }
  featuresTable.style.display = "none";
  slidecontainer.innerHTML = "";
  body = document.getElementsByTagName("body")[0];
  instrucionSection.style.display = "block";
  similarityReportSection.style.display = "block";
  PresentAllCircles(); // event NewProfile is defined in Slider logic
  nextProfileButtonSection.style.display = "block";
};

function InitializeProfilePresentation(current_profile){
  RecordTime();
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];
  slidecontainer.innerHTML = "";
  if(feature_presentaion_index < features_list.length-1) {
    delayActivateButton();
    feature_presentaion_index += 1;
    feature = profile_features[features_list[feature_presentaion_index]];
    right_end, left_end, value = GetProfileFeatureData(feature);
    // check if the property/key is defined in the object itself, not in parent
    if (profile_features.hasOwnProperty(features_list[feature_presentaion_index])) {
      slidecontainer.innerHTML = InjectProfileDataToHTML(profile_features[features_list[feature_presentaion_index]].name_to_present, right_end, left_end, value);
      featuresOrderOfPresentation.push(context[all_profiles_ids[current_profile]]["features_order"][feature_presentaion_index])
      InitiateTimeCount();
    };
  } else if(featuresPresentaionNumber < presentationNumber) {
    feature_presentaion_index = -1;
    featuresPresentaionNumber++;
    getShuffledNoReppetition(context[all_profiles_ids[current_profile]]["features_order"]);
    InitializeProfilePresentation(current_profile);
  } else {
      t0 = null; // reseting the time
      startReportPhase();
  };
};

// Next Trial - New profile:
function startNextTrial(){
  if(current_profile == nPracticeTrials-1 && instructionEndOfPracticePresnted == false){
    HideReoportSection();
    featuresTable.style.display = "block";
    instructionEndOfPracticePresnted = true;
    inTaskInstructions.style.display = "block";
    inTaskInstructionsText.innerHTML =  "Practice is over! it's time for questions? <br> Have any?";
    nextFeatureButton.style.display = "none";
  } else {
    inTaskInstructions.style.display = "none";
    if(document.title == "profile"){
      reportT1 = new Date();
      pRts.push(reportT1-reportT0);
      reportT0 = null; // reseting reportT0 to null

      profile_dictionary = context[all_profiles_ids[current_profile]];
      profilesList.value = profilesList.value + profile_dictionary.name + "," ;
      subjectResonses.value = subjectResonses.value + similarityInput.value + ",";
      trialFeatureOrder.value = trialFeatureOrder.value + featuresOrderOfPresentation.toString() + "-**NextProfile**-";
      featuresOrderOfPresentation = []; // emptying the list after data was saved
      subjectRTs.value = subjectRTs.value + rts.toString(); + + "-**NextProfile**-"
      profileRTs.value = pRts.toString();
      similarityInput.value = 0;
      sim_value = parseInt(similarityInput.value);
      preProfile = "מיד תחל הצגת פרופיל חדש";
      current_profile +=1;
      document.getElementsByTagName("body")[0].dispatchEvent(event); // Dispatch the event.
      if(current_profile < all_profiles_ids.length){
        pre_profile_counter = 0;
        featuresTable.style.display = "block";
        nextFeatureButton.disabled = true;
        buttonActivationDelay = buttonActivationDelayOriginal;
        featuresPresentaionNumber = 1;
        HideReoportSection();
        ProfileCountDown();
      } else { // enf og trials
        resonsesForm.submit();
      };
    } else { // not in profile presentation phase
      current_profile +=1;
      if(current_profile < all_profiles_ids.length){
        pre_profile_counter = 0;
        ProfileCountDown();
      } else {
        resonsesForm.submit();
      };
    };
  };
};

function RecordTime() {
  t1 = new Date();
  if(t0 != null){
    rts.push(t1-t0);
  }
}

function InitiateTimeCount() {
  t0 = new Date();
}

function ProfileCountDown() {
  nextFeatureButton.style.display = "none";
  if(pre_profile_counter < texts_pre_profile.length) {
    slidecontainer.innerHTML = texts_pre_profile[pre_profile_counter];
    pre_profile_counter +=1;
    setTimeout(function(){ProfileCountDown()}, countDownMiliSeconds);
  } else {
    feature_presentaion_index = -1;
    HideReoportSection();
    window.scrollTo(0, 0);
    nextFeatureButton.style.display = "block";
    InitializeProfilePresentation(current_profile);
  };
};

function PresentProfileAgain(){
  preProfile = "מיד תחל הצגה מחודשת של פרופיל זה"
  texts_pre_profile[0] = preProfile;
  feature_presentaion_index = -1;
  pre_profile_counter = 0;
  featuresPresentaionNumber = 1;
  getShuffledNoReppetition(context[all_profiles_ids[current_profile]]["features_order"]);
  featuresTable.style.display = "block";
  buttonActivationDelay = 0;
  HideReoportSection();
  ProfileCountDown();
};

function ChagngeSimilarityValue(direction){
  if (direction == "+"){
     sim_value = Math.min(sim_value+1, 100);
     similarityInput.value = sim_value;
  }
  else if ( direction == "-") {
    sim_value = Math.max(sim_value-1, 0);
    similarityInput.value = sim_value;
  };
};

function ContinuousPressChange(direction){
  if(buttonClicked==true){
    idTO = setTimeout(function(){ContinuousPressChange(direction)}, changeRate);
    timeOutIntervalIDs.push(idTO);
    ChagngeSimilarityValue(direction)
    changeCircles();
  };
};

function delayActivateButton(){
  nextFeatureButton.disabled = true;
  setTimeout(function(){
    nextFeatureButton.disabled = false;
  }, buttonActivationDelay)

}

moreSimilarity.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "+";
  ChagngeSimilarityValue(direction)
  changeCircles();
  idTO = setTimeout(function(){ContinuousPressChange(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

moreSimilarity.addEventListener("mouseup", function(){
  for (var i = 0; i < timeOutIntervalIDs.length; i++) {
    clearInterval(timeOutIntervalIDs[i]);
  }
  timeOutIntervalIDs = [];
  buttonClicked = false;
});

lessSimilarity.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "-";
  ChagngeSimilarityValue(direction)
  changeCircles();
  idTO = setTimeout(function(){ContinuousPressChange(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

lessSimilarity.addEventListener("mouseup", function(){
  for (var i = 0; i < timeOutIntervalIDs.length; i++) {
    clearInterval(timeOutIntervalIDs[i]);
  }
  timeOutIntervalIDs = [];
  buttonClicked = false;
});

nextFeatureButton.disabled = true;
nextFeatureButton.addEventListener("click", function() {InitializeProfilePresentation(current_profile)});
nextFromInstructionsButton.addEventListener("click", startNextTrial);
nextProfileButton.addEventListener("click",startNextTrial);
presentProfileAgainButton.addEventListener("click", PresentProfileAgain);

inTaskInstructions.style.display = "none";

ProfileCountDown();
