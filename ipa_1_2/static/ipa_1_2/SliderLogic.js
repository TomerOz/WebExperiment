
var slidecontainer = document.getElementById("slidecontainer");
var resonsesForm = document.getElementById("subjectResonseForm");
var profilesList = document.getElementById("profilesList");

similarity_report = document.getElementById('myRange');
subjectResonses = document.getElementById('subjectResonses');
profilesDescriptions = document.getElementById('profilesDescriptions'); // the hidden input fiel in the hidden form
profileDescription = document.getElementById('profileDescription'); // the text box elemenet

const event = new Event('NewProfile');
const event_show_report = new Event('ShowReport');

minwWordsPerDescription = 12;

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
  basicProfileHTMLText = '<h3 id="title">'+ title + '</h3>\
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

// Check new change using features_order
function InitializeProfilePresentation(current_profile){
  InitiateTimeCount();
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];
  slidecontainer.innerHTML = "";
  for (var i=0; i<features_list.length; i++) {
    feature = profile_features[features_list[i]];
    right_end, left_end, value = GetProfileFeatureData(feature);
      // check if the property/key is defined in the object itself, not in parent
      if (profile_features.hasOwnProperty(features_list[i])) {
        slidecontainer.innerHTML += InjectProfileDataToHTML(profile_features[features_list[i]].name_to_present, right_end, left_end, value);
          // console.log(key, profile_features[key]);
      }
    }
}


var nextProfileButton = document.getElementById("NextProfileButton");
nextProfileButton.addEventListener("click",function(){
  if(document.title == "profile"){
    if(profileDescription.value.split(" ").length > minwWordsPerDescription){
      RecordTime();
      profilesList.value = profilesList.value + "," + context[all_profiles_ids[current_profile]].name;
      subjectResonses.value = subjectResonses.value + "," + similarity_report.value;
      subjectRTs.value = rts.toString();
      profilesDescriptions.value = profilesDescriptions.value + "-**NextProfile**-" + profileDescription.value;
      profileDescription.value = "";
      profileDescription.placeholder="יש לכתוב כאן תיאור של האדם המוצג כאן";
      similarity_report.value = 50;
      current_profile +=1;
      document.getElementsByTagName("body")[0].dispatchEvent(event); // Dispatch the event.
      if(current_profile < all_profiles_ids.length){
        window.scrollTo(0, 0);
        InitializeProfilePresentation(current_profile);
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
        InitializeProfilePresentation(current_profile);
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

InitializeProfilePresentation(current_profile);

profile_report_state = 1;
function ShowReport(){
  window.scrollTo(0, 0);
  if(profile_report_state==0){
    profile_report_state=1;
    document.getElementById("practiceTrialsInstructions").style.display = "block";
    document.getElementById("SimilarityReportSection").style.display = "block";
    document.getElementById("NextProfileButtonSection").style.display = "block";
    maxAnchor.style.display = "block";
    minAnchor.style.display = "block";
    document.getElementById("slidecontainer").style.display = "none";
    document.getElementsByTagName("body")[0].dispatchEvent(event_show_report); // Dispatch the event.
  } else {
    profile_report_state=0;
    document.getElementById("practiceTrialsInstructions").style.display = "none";
    document.getElementById("SimilarityReportSection").style.display = "none";
    document.getElementById("NextProfileButtonSection").style.display = "none";
    maxAnchor.style.display = "none";
    minAnchor.style.display = "none";
    document.getElementById("slidecontainer").style.display = "block";
  };

};

var showReportButton = document.getElementById('showReportButton');
showReportButton.addEventListener("click", ShowReport);
