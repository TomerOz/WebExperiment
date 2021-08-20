
// variable instructions_list is recived from the html

var nextButton = document.getElementById("NextStepButton");
var instructionTextContainer = document.getElementById("instructionContainer");
var instructionsForm = document.getElementById('instructionsForm');
var testForm = document.getElementById('testForm');
var showMatrixButton = document.getElementById('showMatrixButton');
var changeButton = document.getElementById('changeButton');
var beforeReportMax = document.getElementById('beforeReportMax');
var beforeReportMin = document.getElementById('beforeReportMin');

currentInstruction = 0;
correctAnswers = ["Ready button", 1, 0];
currentQuestion = 0;
wasCorrect = false;

function HandleInstructions() {
  if(wasCorrect){
    if(currentInstruction <= instructions_list.length) {
      instructionTextContainer.textContent = instructions_list[currentInstruction];
       testForm.style.display = "block";
      // if(currentInstruction == instructions_list.length-1){
      //   testForm.style.display = "block";
      // };
      currentInstruction += 1;
    };
  };
};

nextButton.addEventListener("click", HandleInstructions);

function recieveChoice(rowIndex){
  if(rowIndex == correctAnswers[currentQuestion]){
    currentQuestion += 1;
    wasCorrect = true;
    HandleInstructions();
    if(currentQuestion < correctAnswers.length){
      wasCorrect = false;
    };
  };
};

wasCorrect = true;
HandleInstructions();
wasCorrect = false;

// second canvas2: -- coppied from getSimilarity.js:
var slider2 = document.getElementById("myRange2");

var mouseDown = 0;
document.body.onmousedown = function() {
  ++mouseDown;
}
document.body.onmouseup = function() {
  --mouseDown;
}

function changeCircles2(){
  if(mouseDown){
    draw2();
  };
};

function changeOnClickCircles2(){
  draw2();
};

slider2.onmousemove = function(){changeCircles2()};
slider2.onmouseover = function(){changeCircles2()};
slider2.onclick = function(){changeOnClickCircles2()};

function SaveReort2(){
  // Code here should save report and change profile
  // ...
};

// circles report code:
var canvas2 = document.getElementById("myCanvas2");
canvas2.width = slider2.getClientRects()[0].width*0.65
canvas2.height = canvas2.width/2
var ctx2_2 = canvas2.getContext("2d");
var y = canvas2.height/2;
r=canvas2.width/4
var x1_2 = r/2 + canvas2.width/2 + (50-(slider2.value))
var x2_2 = canvas2.width/ 2 - r/2 - (50-(slider2.value))

function drawBall2() {
  ctx2_2.beginPath();
  ctx2_2.fillStyle = "#af4c50";
  ctx2_2.arc(x1_2, y, r, 0, Math.PI*2, 0);
  <!-- ctx2_2.stroke(); -->
  ctx2_2.linewidth = 2
  ctx2_2.globalAlpha = 0.8;
  ctx2_2.fill();
  ctx2_2.closePath();

  ctx2_2.beginPath();
  ctx2_2.fillStyle = "#af4c50";
  ctx2_2.arc(x2_2, y, r, 0, Math.PI*2, 4);
  <!-- ctx2_2.stroke(); -->
  ctx2_2.linewidth = 2
  ctx2_2.globalAlpha = 0.8;
  ctx2_2.fill();
  ctx2_2.closePath();
}

function draw2(direction) {
    ctx2_2.clearRect(0, 0, canvas2.width, canvas2.height);
    x1_2 = r/2 + canvas2.width/2 + (50-(slider2.value))/100 * canvas2.width/4
    x2_2 = canvas2.width/ 2 - r/2 - (50-(slider2.value))/100 * canvas2.width/4
    drawBall2();
};

drawBall2();

// Page flow control

var approve_1 = document.getElementById("approve_name_1");
var approve_2 = document.getElementById("approve_name_2");
var maxSimilarityReportSection = document.getElementById("MaxSimilarityReportSection");
var minSimilarityReportSection = document.getElementById("MinSimilarityReportSection");
var minSimilaritySection = document.getElementById("MinSimilaritySection");
var maxSimilaritySection = document.getElementById("MaxSimilaritySection");
var submitButton = document.getElementById("submitButton");
var maxSimilarityQuestion = document.getElementById("maxSimilarityQuestion");
var minSimilarityQuestion = document.getElementById("minSimilarityQuestion");
var maxSimilarity = document.getElementById("maxSimilarity");
var minSimilarity = document.getElementById("minSimilarity");

var flowPhases = {"max": 0, "min": 0};
var sections = {"max": maxSimilaritySection, "min":minSimilaritySection};
var reportSections = {"max": maxSimilarityReportSection, "min":minSimilarityReportSection};
var flowOrder = [reportSections,sections];
approve_1.addEventListener("click", function(){showCircles("max")})
approve_2.addEventListener("click", function(){showCircles("min")})




function showCircles(circlesName){
  phase = flowPhases[circlesName];
  if(circlesName=="max" && phase==0){
    flowOrder[phase][circlesName].style.display = "block";
    flowPhases[circlesName] = phase + 1;
    let result = beforeReportMax.textContent.replaceAll("{}", maxSimilarity.value);
    beforeReportMax.textContent = result;
    maxSimilarityQuestion.style.display = "none";
  }

  // At the end of max after report
  if(circlesName=="max" && phase==1){
    flowPhases[circlesName] = phase + 1;
    sections["max"].style.display = "none";
    reportSections["max"].style.display = "none";
    sections["min"].style.display = "block";
    minSimilarityQuestion.style.display = "block";

    wasCorrect = true;
    HandleInstructions();
  }
  if(circlesName=="min" && phase==0){
    flowPhases[circlesName] = phase + 1;
    minSimilarityReportSection.style.display = "block"
    let result = beforeReportMin.textContent.replaceAll("{}", minSimilarity.value);
    beforeReportMin.textContent = result;
    minSimilarityQuestion.style.display = "none";
    submitButton.style.display = "block";
    approve_2.style.display = "none";
  }
};

sections["min"].style.display = "none";
reportSections["min"].style.display = "none";
submitButton.style.display = "none";