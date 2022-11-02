var nextFeatureButton = document.getElementById("nextFeatureButton");
var similarityValue = document.getElementById("similarityValue");

// circles report code:
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var y = canvas.height/2;
var r = canvas.width/4
var x1 = r/2 + canvas.width/2 + (50-(similarityInput.value))
var x2 = canvas.width/ 2 - r/2 - (50-(similarityInput.value))

var reportColor = '#af4c50';

function drawBall(ctx, x1, x2, y, r, reportColor) {
  // circle 1:
  ctx.beginPath();
  ctx.fillStyle = reportColor;
  ctx.arc(x1, y, r, 0, Math.PI*2, 0);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();

  // circle 2:
  ctx.beginPath();
  ctx.fillStyle = reportColor;
  ctx.arc(x2, y, r, 0, Math.PI*2, 4);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();
}

function DrawAgain(canvas, ctx, y, r, reportColor, similarityValue){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    x1 =  canvas.width/2 - (100 - similarityValue)*r/100
    x2 = canvas.width/2 + (100 - similarityValue)*r/100
    drawBall(ctx, x1, x2, y, r, reportColor);
};

function ClearCircles(canvas, ctx){
  ctx.clearRect(0, 0, canvas.width, canvas.height);
};

var mouseDown = 0;
document.body.onmousedown = function() {
  ++mouseDown;
}
document.body.onmouseup = function() {
  --mouseDown;
}

function changeCircles(){
  DrawAgain(canvas, ctx, y, r, reportColor, similarityInput.value);
};

function PresentAllCircles(){
  DrawAgain(canvas, ctx, y, r, reportColor, similarityInput.value);
};




if(document.title != "profile"){
  reportSections["max"].style.display = "none";
} else if (document.title == "profile"){
  // maxSimilaritySection.classList.add('profiles_size')
};
