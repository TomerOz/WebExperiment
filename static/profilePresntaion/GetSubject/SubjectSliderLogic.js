

// var slider = document.getElementById("myRange");
// slider.addEventListener("input", function showValue() { console.log(slider.value)})
// // slider.value =context[1].TomerOz[2];
//
// var title = document.getElementById("myRange");
// var endR = document.getElementById("myRange");
// var endL = document.getElementById("myRange");
var slidecontainer = document.getElementById("slidecontainer");

db_features = "features_list"

var right_end = "r"
var left_end = "l"
var feature_title = "Title new"
var default_value = "50"

function InjectProfileDataToHTML(title, right_end, left_end, value){
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

function GetProfileFeatureData (feature) {
  feature_title = feature[0];
  right_end = feature[1];
  left_end = feature[2];
  return feature_title, right_end, left_end;
}

function InitializeProfilePresentation(){
  context.forEach((feature, i) => {
      feature_title, right_end, left_end = GetProfileFeatureData(feature);
      slidecontainer.innerHTML += InjectProfileDataToHTML(feature_title, right_end, left_end, default_value);
      });
  }

InitializeProfilePresentation();
