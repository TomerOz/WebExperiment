
var slidecontainer = document.getElementById("slidecontainer");
var resonsesForm = document.getElementById("subjectResonseForm");
var profilesList = document.getElementById("profilesList");

var showReportButton = document.getElementById('showReportButton');

similarity_report = document.getElementById('myRange');
subjectResonses = document.getElementById('subjectResonses');
profilesDescriptions = document.getElementById('profilesDescriptions'); // the hidden input fiel in the hidden form
profileDescription = document.getElementById('profileDescription'); // the text box elemenet
similarityReportSection = document.getElementById("SimilarityReportSection");
nextProfileButtonSection = document.getElementById("NextProfileButtonSection");
trialFeatureOrder = document.getElementById("trialFeatureOrder");

var presentProfileAgainButton = document.getElementById("presentProfileAgainButton");
const event = new Event('NewProfile');
// const event_show_report = new Event('ShowReport');

var minwWordsPerDescription = 0;
var milisecondsPerFeature = 2000;

var db_features = "features"
var current_profile = 0
var all_profiles_ids = context["profiles_list"]

var title = "Title new"
var right_end = "r"
var left_end = "l"
var value = "4"

var t0;
var t1;
rts = [];

function InjectProfileDataToHTML(title, right_end, left_end, value){
  basicProfileHTMLText = '<h4 id="title">'+ title + '</h4> <br>\
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
}


function InitializeProfilePresentation(current_profile){

  InitiateTimeCount(); // move to the end of the preocess

  profileDescription.style.display = "none";
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];
  slidecontainer.innerHTML = "";

  feature = profile_features[features_list[feature_presentaion_index]];
  right_end, left_end, value = GetProfileFeatureData(feature);
  // check if the property/key is defined in the object itself, not in parent
  if (profile_features.hasOwnProperty(features_list[feature_presentaion_index])) {
    slidecontainer.innerHTML = InjectProfileDataToHTML(profile_features[features_list[feature_presentaion_index]].name_to_present, right_end, left_end, value);
    feature_presentaion_index += 1;
    if(feature_presentaion_index < features_list.length) {
        setTimeout(function(){
        InitializeProfilePresentation(current_profile);
      }, milisecondsPerFeature);
    } else {
      slidecontainer.innerHTML = "";
      body = document.getElementsByTagName("body")[0];
      similarityReportSection.style.display = "block";
      slider.style.display = "block";
      draw(); // event NewProfile is defined in Slider logic
      placeAnchors(maxValue, "maxAnchor");
      placeAnchors(minValue, "minAnchor");
      nextProfileButtonSection.style.display = "block";
    };
  };
};


var nextProfileButton = document.getElementById("NextProfileButton");
nextProfileButton.addEventListener("click",function(){
  if(document.title == "profile"){
    if(profileDescription.value.split(" ").length > minwWordsPerDescription){
      RecordTime();
      profile_dictionary = context[all_profiles_ids[current_profile]];
      profilesList.value = profilesList.value + profile_dictionary.name + "," ;
      subjectResonses.value = subjectResonses.value + similarity_report.value + ",";
      trialFeatureOrder.value = trialFeatureOrder.value + profile_dictionary.features_order.toString()+ "-**NextProfile**-";
      subjectRTs.value = rts.toString();
      profilesDescriptions.value = profilesDescriptions.value + "-**NextProfile**-" + profileDescription.value;

      profileDescription.value = "";
      profileDescription.placeholder="יש לכתוב כאן תיאור של האדם המוצג כאן";
      similarity_report.value = 50;
      preProfile = "מיד תחל הצגת פרופיל חדש";
      current_profile +=1;
      document.getElementsByTagName("body")[0].dispatchEvent(event); // Dispatch the event.
      if(current_profile < all_profiles_ids.length){
        pre_profile_counter = 0;
        HideReoportSection();
        ProfileCountDown();
      }
      else { // enf og trials
        resonsesForm.submit();
      };
    }
    else { // not enough words for description
      profilesDescriptions.style.color = "red";
      alert("Must enter Description");
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
});

function RecordTime() {
  t1 = new Date();
  rts.push(t1-t0);
}
function InitiateTimeCount() {
  t0 = new Date();
}

var preProfile = "מיד תחל הצגת פרופיל חדש"
var texts_pre_profile = [preProfile, 3,2,1]
var pre_profile_counter = 0
var feature_presentaion_index;

function ProfileCountDown() {
  if(pre_profile_counter < texts_pre_profile.length) {
    slidecontainer.innerHTML = texts_pre_profile[pre_profile_counter];
    pre_profile_counter +=1;
    profileDescription.style.display = "none";
    setTimeout(function(){ProfileCountDown()}, 1500);
  } else {
    feature_presentaion_index = 0;
    HideReoportSection();
    window.scrollTo(0, 0);
    InitializeProfilePresentation(current_profile);
  };
};


function PresentProfileAgain(){
  preProfile = "מיד תחל הצגה מחודשת של פרופיל זה"
  texts_pre_profile[0] = preProfile;
  feature_presentaion_index = 0;
  pre_profile_counter = 0
  HideReoportSection();
  ProfileCountDown();
};
presentProfileAgainButton.addEventListener("click", PresentProfileAgain);

ProfileCountDown();
