
var maxAnchor = document.getElementById("maxAnchor");
var minAnchor = document.getElementById("minAnchor");

function placeAnchors(value, id){
  maxAnchor.style.display = "block";
  minAnchor.style.display = "block";
  var similarity_report_rect = similarity_report.getBoundingClientRect();
  var slider_range = similarity_report_rect.right - similarity_report_rect.left;
  anchor_y = similarity_report_rect.y;
  anchor_x = value/100 * slider_range; // maxValue passed through html variable in profile.html

  var anchor_box = document.getElementById(id);
  var anchor_box_rect = anchor_box.getBoundingClientRect();
  var anchor_box_range = anchor_box_rect.right - anchor_box_rect.left;
  anchor_box.style.position = "absolute"
  anchor_box.style.left = (similarity_report_rect.left + anchor_x - (anchor_box_range)) + "px"
  anchor_box.style.top = anchor_y  + "px"

  profileDescription = document.getElementById("profileDescription");
  // profileDescription.style.width = (0.75 * slider_range) + "px";
}

function HideReoportSection(){
  maxAnchor.style.display = "none";
  minAnchor.style.display = "none";
  slider.style.display = "none";
  similarityReportSection.style.display = "none";
  nextProfileButtonSection.style.display = "none";
};

HideReoportSection();
