var nextFeatureButton = document.getElementById("nextFeatureButton");
var similarityValue = document.getElementById("similarityValue");

// circles report code:
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
var y = canvas.height/2;
var r = canvas.width/4
var x1 = r/2 + canvas.width/2 + (50-(similarityInput.value))
var x2 = canvas.width/ 2 - r/2 - (50-(similarityInput.value))

// MinMax circles report code
// Min:
var canvasMin = document.getElementById("CanvasMin");
var ctxMin = canvasMin.getContext("2d");
var yMin = canvasMin.height/2;
var rMin = canvasMin.width/4
var x1Min = r/2 + canvasMin.width/2 + (50-(30))
var x2Min = canvasMin.width/ 2 - r/2 - (50-(30))
// Max:
var canvasMax = document.getElementById("CanvasMax");
var ctxMax = canvasMax.getContext("2d");
var yMax = canvasMax.height/2;
var rMax = canvasMax.width/4
var x1Max = r/2 + canvasMax.width/2 + (50-(90))
var x2Max = canvasMax.width/ 2 - r/2 - (50-(90))
var reportColor = '#af4c50';
var reportColorMin = '#af4c9a';
var reportColorMax = '#af4c9a';

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
function DrawAgain(canvas, ctx, x1, x2, y, r, reportColor, similarityValue){
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    x1 = r/2 + canvas.width/2 + (50-(similarityValue))/100 * canvas.width/4
    x2 = canvas.width/ 2 - r/2 - (50-(similarityValue))/100 * canvas.width/4
    drawBall(ctx, x1, x2, y, r, reportColor);
};


var mouseDown = 0;
document.body.onmousedown = function() {
  ++mouseDown;
}
document.body.onmouseup = function() {
  --mouseDown;
}

function changeCircles(){
  if(similarityInput.value == minValue){
    reportColor = reportColorMin;
  } else if (similarityInput.value == maxValue){
    reportColor = reportColorMax;
  } else {
    reportColor = '#af4c50';
  }
  DrawAgain(canvas, ctx, x1, x2, y, r, reportColor, similarityInput.value);
};

function PresentAllCircles(){
  reportColor = '#af4c50';
  DrawAgain(canvasMax, ctxMax, x1Max, x2Max, yMax, rMax, reportColorMax, maxValue);
  DrawAgain(canvas, ctx, x1, x2, y, r, reportColor, similarityInput.value);
  DrawAgain(canvasMin, ctxMin, x1Min, x2Min, yMax, rMin, reportColorMin, minValue);
};

function AddMinMaxNames(){
  ctxMax.fillStyle = "white";
  ctxMax.font = '20px sans-serif';
  var textStringMax = maxName,
      textWidthMax = ctxMax.measureText(textStringMax).width;
  ctxMax.fillText(textStringMax , (canvasMax.width/2) - (textWidthMax / 2), (canvasMax.height / 2)+10);

  ctxMin.fillStyle = "white";
  ctxMin.font = '20px sans-serif';
  var textStringMin = minName,
      textWidthMin = ctxMin.measureText(textStringMax).width;
  ctxMin.fillText(textStringMin , (canvasMin.width/2) - (textWidthMin / 2), (canvasMin.height / 2)+10);
};


if(document.title != "profile"){
  reportSections["max"].style.display = "none";
} else if (document.title == "profile"){
  // maxSimilaritySection.classList.add('profiles_size')
};

function HideReoportSection(){
  similarityReportSection.style.display = "none";
  nextProfileButtonSection.style.display = "none";
  instrucionSection.style.display = "none";
};

HideReoportSection();
