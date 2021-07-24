
var slidecontainer = document.getElementById("slidecontainer");
var resonsesForm = document.getElementById("subjectResonseForm");
var profilesList = document.getElementById("profilesList");

similarity_report = document.getElementById('myRange');
subjectResonses = document.getElementById('subjectResonses');

const event = new Event('NewProfile');



var db_features = "features"
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
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  var features_list = context[all_profiles_ids[current_profile]]["features_order"];
  slidecontainer.innerHTML = "";
  for (var i=0; i<features_list.length; i++) {
    feature = profile_features[features_list[i]];
    right_end, left_end, value = GetProfileFeatureData(feature);
      // check if the property/key is defined in the object itself, not in parent
      if (profile_features.hasOwnProperty(features_list[i])) {
        slidecontainer.innerHTML += InjectProfileDataToHTML(features_list[i], right_end, left_end, value);
          // console.log(key, profile_features[key]);
      }
    }
}



var nextProfileButton = document.getElementById("NextProfileButton");
nextProfileButton.addEventListener("click",function(){
  if(document.title == "profile"){
    profilesList.value = profilesList.value + "," + context[all_profiles_ids[current_profile]].name;
    subjectResonses.value = subjectResonses.value + "," + similarity_report.value
    similarity_report.value = 50;
    // Dispatch the event.
    document.getElementsByTagName("body")[0].dispatchEvent(event);
  };
  current_profile +=1;
  if(current_profile < all_profiles_ids.length){
    InitializeProfilePresentation(current_profile);
  } else {
    resonsesForm.submit();
  };
});

InitializeProfilePresentation(current_profile);
