
var slidecontainer = document.getElementById("slidecontainer");

db_features = "features"
var current_profile = 0
var all_profiles_ids = context["profiles_list"]

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

// Check new change using features_order
function InitializeProfilePresentation(current_profile){
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];
  slidecontainer.innerHTML = "";
  for (var feature in features_list) {
      right_end, left_end, value = GetProfileFeatureData(profile_features[feature]);
      // check if the property/key is defined in the object itself, not in parent
      if (profile_features.hasOwnProperty(feature)) {
        slidecontainer.innerHTML += InjectProfileDataToHTML(feature, right_end, left_end, value);
          // console.log(key, profile_features[key]);
      }
    }
}

// Recording of strategy choice
aChoice = document.getElementById("A");
bChoice = document.getElementById("B");
resonsesForm = document.getElementById("subjectResonseForm");
subjectResonses = document.getElementById("subjectResonses");
explantionsDiv = document.getElementsByClassName("explantions")[0];

stratgies = [gameJSON["A"], gameJSON["B"]];
subjectStrategyChoice = "";

function RecordChoice(rowIndex){
  if(subjectStrategyChoice == stratgies[rowIndex]){
    // Second click on the same choice, which is canceling of choice
    subjectStrategyChoice = "";
  } else {
    subjectStrategyChoice = stratgies[rowIndex];
  };
};

aChoice.addEventListener("click", function(){RecordChoice(0)});
bChoice.addEventListener("click", function(){RecordChoice(1)});

InitializeProfilePresentation(current_profile);

var nextProfileButton = document.getElementById("NextProfileButton");
nextProfileButton.addEventListener("click",function(){
  if(subjectStrategyChoice == ""){
    // no response, request a resonse
    explantionsDiv.innerHTML  = "Please chooce one alternative!";
  }
  else {
    subjectResonses.value += "," + subjectStrategyChoice;
    subjectStrategyChoice = ""; // clearing resonse to avoid tow recording of a trial
    current_profile +=1;
    if(current_profile < all_profiles_ids.length){
      InitializeProfilePresentation(current_profile);
    } else {
      resonsesForm.submit();
  }};
});
