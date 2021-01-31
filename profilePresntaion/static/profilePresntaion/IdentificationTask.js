
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
function InitializeProfilePresentation(current_profile){
  var profile_features = context[all_profiles_ids[current_profile]][db_features];
  slidecontainer.innerHTML = "";
  for (var feature in profile_features) {
      right_end, left_end, value = GetProfileFeatureData(profile_features[feature]);
      // check if the property/key is defined in the object itself, not in parent
      if (profile_features.hasOwnProperty(feature)) {
        slidecontainer.innerHTML += InjectProfileDataToHTML(feature, right_end, left_end, value);
          // console.log(key, profile_features[key]);
      }
    }
}

InitializeProfilePresentation(current_profile);

var nextProfileButton = document.getElementById("NextProfileButton");
nextProfileButton.addEventListener("click",function(){
  current_profile +=1;
  if(current_profile < all_profiles_ids.length){
      InitializeProfilePresentation(current_profile);
    } else {
      resonsesForm.submit();
  }});

leftCell = document.getElementById("leftCell");
rightCell = document.getElementById("rightCell");

rightCell.innerHTML = leftCell.innerHTML;
