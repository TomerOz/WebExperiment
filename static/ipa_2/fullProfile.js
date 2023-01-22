
var profileContainer = document.getElementById("fullProfileContainer");

var BetweenProfilesInterval = 1000// 1000; // 1 seconds between profiles
var correctPass = "E22Gaya";
var timeSelfProfile = 3000;
var timeSelfOtherProfile = 6000;
var timeToReport = 0;
var InstructionsText1 = reportText1.textContent;
var InstructionsText2 = reportText2.textContent;
var InstructionsText3 = reportText3.textContent;

var a_features_reff_name_1 = a_features_1.textContent;
var a_features_reff_name_2 = a_features_2.textContent;
var c_features_reff_name_1 = c_features_1.textContent;
var c_features_reff_name_2 = c_features_2.textContent;

function InjectProfileDataToHTMLFull(title, right_end, left_end, value, feature_name){
  basicProfileHTMLText = '<h3 id="title">'+ feature_name + '</h3>\
    <div class="row"> \
      <div class="column sideFull">'+ left_end + '</div> \
      <div class="column middleFull"> \
      <canvas class="featureCanvas" id="' + "ID_" + feature_name + left_end + '" width="460" height="35" style="border:0px solid black;"></canvas>\
      </div>\
      <div class="column sideFull">'+ right_end + '</div>\
  </div>';
    return basicProfileHTMLText;
};

function changeWords() {
  if (subject_group == "C"){
    instrucion.innerHTML = instrucion.innerHTML.replace(a_features_reff_name_1, c_features_reff_name_1);
    instrucion.innerHTML = instrucion.innerHTML.replace(a_features_reff_name_2, c_features_reff_name_2);
    instrucion.innerHTML = instrucion.innerHTML.replace("האישיים", "");

    inTaskInstructionsText.innerHTML = inTaskInstructionsText.innerHTML.replace(a_features_reff_name_1, c_features_reff_name_1);
    inTaskInstructionsText.innerHTML = inTaskInstructionsText.innerHTML.replace(a_features_reff_name_2, c_features_reff_name_2);
    inTaskInstructionsText.innerHTML = inTaskInstructionsText.innerHTML.replace("האישיים", "");
    inTaskInstructionsText.innerHTML = inTaskInstructionsText.innerHTML.replace("השונים", "השונות");
  }
}
function changeFontSizeFull(fontSize) {
  var cols = document.getElementsByClassName('sideFull');
  for(i = 0; i < cols.length; i++) {
    cols[i].style.fontSize  = fontSize + "px";
  }
}
function paintCanvasesOtherFeture(feature_name, value, value_s) {
  var c = document.getElementById("ID_"+feature_name);
  var ctx = c.getContext("2d");
  // other value:
  ctx.fillStyle = "#FFAE42";
  rectHeight = 22;
  if(value==value_s){
    rectHeight = 11;
  }
  ctx.fillRect(value*4 + 20, 9, 20, rectHeight);

  ctx.stroke()
  instrucion.innerHTML = InstructionsText2;
  changeWords();
}

function paintSelfFeature(feature_name, value) {
  var c = document.getElementById("ID_"+feature_name);
  var ctx = c.getContext("2d");
  ctx.beginPath();
  // scale:
  ctx.fillStyle = "#d3d3d3";
  ctx.fillRect(20, 10, 420, 20);
  // self value:
  ctx.fillStyle = "#8A2BE2";
  ctx.fillRect(value*4 + 20, 9, 20, 22);
}

function GetProfileFeatureDataFull(feature) {
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
    right_end, left_end, value, feature_name = GetProfileFeatureDataFull(profile[feature]);
    // check if the property/key is defined in the object itself, not in parent
    if (profile.hasOwnProperty(feature)) {
      text += InjectProfileDataToHTMLFull(feature_name, right_end, left_end, value, feature_name);
    }
  }
  return text
}

function InitializeProfilePresentationFull(current_profile){
  var subject_features = subjectContext[subjectContext.profiles_list[0]][db_features];
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];

  profileContainer.innerHTML = "";
  profile_id = context[all_profiles_ids[current_profile]];
  text_1 = GetProfileData(profile_features, features_list);
  profileContainer.innerHTML = text_1;

  instrucion.innerHTML = InstructionsText1;
  changeWords();

  for (i=0; i<features_list.length; i++ ) {
    feature = features_list[i]
    right_end, left_end, value, feature_name = GetProfileFeatureDataFull(subject_features[feature]);
    // check if the property/key is defined in the object itself, not in parent
    if (profile_features.hasOwnProperty(feature)) {
      paintSelfFeature(feature_name+left_end, value);
    }
  }
  if(subject_group=="C"){
    changeFontSizeFull(25);
  }
  setTimeout(function(){
    for (ii=0; ii<features_list.length; ii++ ) {
      feature = features_list[ii]
      right_end, left_end, value, feature_name = GetProfileFeatureDataFull(profile_features[feature]);
      value_s = subject_features[feature].value
      // check if the property/key is defined in the object itself, not in parent
      if (profile_features.hasOwnProperty(feature)) {
        paintCanvasesOtherFeture(feature_name+left_end, value, value_s);
      }
    }
  }, timeSelfProfile);
  setTimeout(function(){
    instrucion.innerHTML = InstructionsText3;
    changeWords();

  }, timeSelfProfile+ timeSelfOtherProfile);
  reportTable.style.display = 'block';
  profileContainer.style.display = 'block';
}


function checkPass() {
  if (experimenterCode.value == correctPass){
    experimenterCodeDiv.style.display = "none";
    ProfileCountDown();
  }
}
experimenterCodeButton.addEventListener("click", checkPass);
