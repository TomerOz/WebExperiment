var nextFeatureButton = document.getElementById("nextFeatureButton");
var slider = document.getElementById("myRange");
var similarityValue = document.getElementById("similarityValue");

var mouseDown = 0;
document.body.onmousedown = function() {
  ++mouseDown;
}
document.body.onmouseup = function() {
  --mouseDown;
}

function changeCircles(){
  DrawAgain();
};

// circles report code:
var canvas = document.getElementById("myCanvas");
// canvas.width = slider.getClientRects()[0].width*0.52
// canvas.height = canvas.width/2
var ctx = canvas.getContext("2d");
var y = canvas.height/2;
r=canvas.width/4
var x1 = r/2 + canvas.width/2 + (50-(similarityInput.value))
var x2 = canvas.width/ 2 - r/2 - (50-(similarityInput.value))

function drawBall() {
  // circle 1:
  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x1, y, r, 0, Math.PI*2, 0);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();

  // circle 2:
  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x2, y, r, 0, Math.PI*2, 4);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();
}

function DrawAgain(){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    x1 = r/2 + canvas.width/2 + (50-(similarityInput.value))/100 * canvas.width/4
    x2 = canvas.width/ 2 - r/2 - (50-(similarityInput.value))/100 * canvas.width/4
    drawBall();
};


if(document.title != "profile"){
  reportSections["max"].style.display = "none";
} else if (document.title == "profile"){
  // maxSimilaritySection.classList.add('profiles_size')
};
