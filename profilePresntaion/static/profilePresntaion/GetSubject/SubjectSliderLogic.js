
var slidecontainer = document.getElementById("slidecontainer");
var hiddenInputs = document.getElementById("hiddenInputs");
var featuresForm = document.getElementById("featuresForm");
var nextFeatureButton = document.getElementById("nextFeatureButton");

db_features = "features_list"

var right_end = "r"
var left_end = "l"
var feature_title = "Title new"
var default_value = "50"

function InjectProfileDataToHTML(title, right_end, left_end, value){
  // the -"- is used for HTML properties while the
  // -'- encapsulates the hole JS string, as in: '<div class="className"'
  basicProfileHTMLText = '<h3 id="title">'+ title + '</h3>\
    <div class="row"> \
      <div class="column side">'+ left_end + '</div> \
      <div class="column middle"> \
          <input type="range" min="1" max="100" value='+ value + ' class="slider" name="' + title + '" id="' + title + '">\
      </div>\
      <div class="column side">'+ right_end + '</div>\
  </div>';

    return basicProfileHTMLText;
}

function getHiddenInputOfLastFeature(featureIndex){
  hiddenInputOfLastFeature = ' ';
  if(featureIndex >= 0){
    feature_title, right_end, left_end = GetProfileFeatureData(context[featureIndex]);
    value = document.getElementById(feature_title).value;
    console.log(value);
    hiddenInputOfLastFeature = ' <input type="hidden" name="'+ feature_title +'" value="' + value + '">';
  };
  return hiddenInputOfLastFeature;
}

function GetProfileFeatureData (feature) {
  feature_title = feature[0];
  right_end = feature[1];
  left_end = feature[2];
  return feature_title, right_end, left_end;
}

currentFeature = 0;
function InitializeProfilePresentation(){
  if(currentFeature < context.length){
    hiddenInputs.innerHTML = hiddenInputs.innerHTML + getHiddenInputOfLastFeature(currentFeature-1);
    feature = context[currentFeature];
    feature_title, right_end, left_end = GetProfileFeatureData(feature);
    slidecontainer.innerHTML = InjectProfileDataToHTML(feature_title, right_end, left_end, default_value);
    currentFeature += 1;
  } else {
    featuresForm.submit();
}};

InitializeProfilePresentation();

nextFeatureButton.addEventListener('click', InitializeProfilePresentation);
