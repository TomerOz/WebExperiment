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
var reportColorMin = '#CAB7A1';
var reportColorMax = '#B29576';

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
  if(current_profile < nPracticeTrials){
    if(similarityInput.value == minValue){
      reportColor = reportColorMin;
    } else if (similarityInput.value == maxValue){
      reportColor = reportColorMax;
    } else {
      reportColor = '#af4c50';
    }
  };
  DrawAgain(canvas, ctx, y, r, reportColor, similarityInput.value);
};

function PresentAllCircles(){
  if(current_profile < nPracticeTrials){
    reportColor = '#af4c50';
    DrawAgain(canvasMax, ctxMax, yMax, rMax, reportColorMax, maxValue);
    DrawAgain(canvas, ctx, y, r, reportColor, similarityInput.value);
    DrawAgain(canvasMin, ctxMin, yMax, rMin, reportColorMin, minValue);
    AddMinMaxNames();
  } else {
    reportColor = '#767676';
    ClearCircles(canvasMax, ctxMax);
    ClearCircles(canvasMin, ctxMin);
    canvasMax.style.display = "none";
    canvasMin.style.display = "none";
    DrawAgain(canvas, ctx, y, r, reportColor, similarityInput.value);
  }
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


function HideReoportSection(){
  similarityReportSection.style.display = "none";
  instrucionSection.style.display = "none";
  nextProfileButtonSection.style.display = "none";
};

HideReoportSection();

if(document.title != "profile"){
  reportSections["max"].style.display = "none";
} else if (document.title == "profile"){
  // maxSimilaritySection.classList.add('profiles_size')
};
