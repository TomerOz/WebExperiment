
var nextButton = document.getElementById("NextStepButton");
var instructionTextContainer = document.getElementById("instructionContainer");
var instructionsForm = document.getElementById('instructionsForm');
var testForm = document.getElementById('testForm');
var showMatrixButton = document.getElementById('showMatrixButton');
var changeButton = document.getElementById('changeButton');
var beforeReportMax = document.getElementById('beforeReportMax');
var beforeReportMin = document.getElementById('beforeReportMin');
var nextFeatureButton = document.getElementById("nextFeatureButton");
var moreSimilarityMax = document.getElementById('moreSimilarityMax');
var lessSimilarityMax = document.getElementById('lessSimilarityMax');
var moreSimilarityMin = document.getElementById('moreSimilarityMin');
var lessSimilarityMin = document.getElementById('lessSimilarityMin');
var timeOutIntervalIDs = [];

// circles report code 1 - Max:
var similarityInputMax = document.getElementById('similarityInputMax');
var canvas = document.getElementById("myCanvas");
canvas.height = canvas.width/2
var ctx = canvas.getContext("2d");
var y1 = canvas.height/2;
var r=canvas.width/4
var x1 = r/2 + canvas.width/2 + (50-(similarityInputMax.value))
var x2 = canvas.width/ 2 - r/2 - (50-(similarityInputMax.value))

// circles report code 2 - Min:
var similarityInputMin = document.getElementById('similarityInputMin');
var canvas2 = document.getElementById("myCanvas2");
canvas2.height = canvas2.width/2
var ctx2_2 = canvas2.getContext("2d");
var y2 = canvas2.height/2;
var r2 =canvas2.width/4
var x1_2 = r/2 + canvas2.width/2 + (50-(similarityInputMin.value))
var x2_2 = canvas2.width/ 2 - r/2 - (50-(similarityInputMin.value))

// Page flow control
var approve_1 = document.getElementById("approve_name_1");
var approve_2 = document.getElementById("approve_name_2");
var maxSimilarityReportSection = document.getElementById("MaxSimilarityReportSection");
var minSimilarityReportSection = document.getElementById("MinSimilarityReportSection");
var minSimilaritySection = document.getElementById("MinSimilaritySection");
var maxSimilaritySection = document.getElementById("MaxSimilaritySection");
var submitButton = document.getElementById("submitButton");
var maxSimilarityQuestion = document.getElementById("maxSimilarityQuestion");
var maxSimilarityQuestionText = document.getElementById("maxSimilarityQuestionText");
var minSimilarityQuestion = document.getElementById("minSimilarityQuestion");
var minSimilarityQuestionText = document.getElementById("minSimilarityQuestionText");
var maxSimilarity = document.getElementById("maxSimilarity");
var minSimilarity = document.getElementById("minSimilarity");

var currentInstruction = 0;
var correctAnswers = ["Ready button", 1, 0];
var currentQuestion = 0;
var wasCorrect = true;

var flowPhases = {"max": 0, "min": 0};
var sections = {"max": maxSimilaritySection, "min":minSimilaritySection};
var reportSections = {"max": maxSimilarityReportSection, "min":minSimilarityReportSection};
var flowOrder = [reportSections,sections];
var inputs = {"max": maxSimilarity, "min": minSimilarity};


function HandleInstructions() {
  if(wasCorrect){
    if(currentInstruction <= instructions_list.length) {
      instructionTextContainer.textContent = instructions_list[currentInstruction];
       testForm.style.display = "block";
      currentInstruction += 1;
    };
  };
};

function highlightWords(){
  for (var i = 0; i < wordsToHighlight.length; i++) {
    const regex = new RegExp(wordsToHighlight[i], 'g');
    minSimilarityQuestionText.innerHTML = minSimilarityQuestionText.innerHTML.replace(regex,"<strong>" + wordsToHighlight[i] + "</strong>");
    maxSimilarityQuestionText.innerHTML = maxSimilarityQuestionText.innerHTML.replace(regex,"<strong>" + wordsToHighlight[i] + "</strong>");
    beforeReportMax.innerHTML = beforeReportMax.innerHTML.replace(regex,"<strong>" + wordsToHighlight[i] + "</strong>");
    beforeReportMin.innerHTML = beforeReportMin.innerHTML.replace(regex,"<strong>" + wordsToHighlight[i] + "</strong>");
  };
};

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

function changeCircles2(){
  drawAgain2();
};

function changeOnClickCircles2(){
  drawAgain2();
};

function drawBall2() {
  ctx2_2.beginPath();
  ctx2_2.fillStyle = "#af4c50";
  ctx2_2.arc(x1_2, y2, r2, 0, Math.PI*2, 0);
  <!-- ctx2_2.stroke(); -->
  ctx2_2.linewidth = 2
  ctx2_2.globalAlpha = 0.8;
  ctx2_2.fill();
  ctx2_2.closePath();

  ctx2_2.beginPath();
  ctx2_2.fillStyle = "#af4c50";
  ctx2_2.arc(x2_2, y2, r2, 0, Math.PI*2, 4);
  <!-- ctx2_2.stroke(); -->
  ctx2_2.linewidth = 2
  ctx2_2.globalAlpha = 0.8;
  ctx2_2.fill();
  ctx2_2.closePath();
}

function drawAgain2(direction) {
    ctx2_2.clearRect(0, 0, canvas2.width, canvas2.height);
    x1_2 =  canvas.width/2 - (100 - similarityInputMin.value)*r/100
    x2_2 = canvas.width/2 + (100 - similarityInputMin.value)*r/100
    drawBall2();
};

function changeCircles(){
  drawAgain();
};

function changeOnClickCircles(){
  drawAgain();
};

function drawBall() {
  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x1, y1, r, 0, Math.PI*2, 0);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();

  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x2, y1, r, 0, Math.PI*2, 4);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();
}

function drawAgain(direction) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    x1 =  canvas.width/2 - (100 - similarityInputMax.value)*r/100
    x2 = canvas.width/2 + (100 - similarityInputMax.value)*r/100
    drawBall();
}

function showCircles(circlesName){
  if(inputs[circlesName].value.length>0){
    phase = flowPhases[circlesName];
    if(circlesName=="max" && phase==0){
      flowOrder[phase][circlesName].style.display = "block";
      flowPhases[circlesName] = phase + 1;
      let result = beforeReportMax.textContent.replaceAll("{}", maxSimilarity.value);
      beforeReportMax.textContent = result;
      maxSimilarityQuestion.style.display = "none";
      wordsToHighlight.push(maxSimilarity.value);
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
      wordsToHighlight.push(minSimilarity.value);
      flowPhases[circlesName] = phase + 1;
      minSimilarityReportSection.style.display = "block"
      let result = beforeReportMin.textContent.replaceAll("{}", minSimilarity.value);
      beforeReportMin.textContent = result;
      minSimilarityQuestion.style.display = "none";
      submitButton.style.display = "block";
      approve_2.style.display = "none";
    };
  };
  highlightWords();
};

HandleInstructions();
wasCorrect = false;

drawBall2();
drawBall();

approve_1.addEventListener("click", function(){showCircles("max")})
approve_2.addEventListener("click", function(){showCircles("min")})

sections["min"].style.display = "none";
reportSections["min"].style.display = "none";
submitButton.style.display = "none";

nextButton.addEventListener("click", HandleInstructions);

reportSections["max"].style.display = "none";

// Listen for the event.
body = document.getElementsByTagName("body")[0];
body.addEventListener("NewProfile", function(){drawAgain()}); // event NewProfile is defined in similarityInputMax logic
highlightWords();


/////////////////////////////////////

var buttonClicked = false;
var intervalID;
var changeRate = 25;
var contiousDelay = 500;
var direction;
var sim_valueMax = parseInt(similarityInputMax.value);
var sim_valueMin = parseInt(similarityInputMax.value);

function clearAllIntervals(){
  for (var i = 0; i < timeOutIntervalIDs.length; i++) {
    clearInterval(timeOutIntervalIDs[i])};
  timeOutIntervalIDs = [];
};

function ChagngeSimilarityValue(direction){
  if (direction == "+"){
     sim_valueMax = Math.min(sim_valueMax+1, 100);
     similarityInputMax.value = sim_valueMax;
  }
  else if ( direction == "-") {
    sim_valueMax = Math.max(sim_valueMax-1, 0);
    similarityInputMax.value = sim_valueMax;
  };
};
function ContinuousPressChange(direction){
  if(buttonClicked==true){
    idTO = setTimeout(function(){ContinuousPressChange(direction)}, changeRate);
    timeOutIntervalIDs.push(idTO);
    ChagngeSimilarityValue(direction)
    changeCircles();
  };
};

function endMovement(){
  clearAllIntervals();
  buttonClicked = false;
}


moreSimilarityMax.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "+";
  ChagngeSimilarityValue(direction)
  changeCircles();
  idTO = setTimeout(function(){ContinuousPressChange(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

moreSimilarityMax.addEventListener("mouseup", endMovement);
moreSimilarityMax.addEventListener("mouseleave", endMovement);

lessSimilarityMax.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "-";
  ChagngeSimilarityValue(direction)
  changeCircles();
  idTO = setTimeout(function(){ContinuousPressChange(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

lessSimilarityMax.addEventListener("mouseup", endMovement);
lessSimilarityMax.addEventListener("mouseleave", endMovement);

function ChagngeSimilarityValue2(direction){
  if (direction == "+"){
     sim_valueMin = Math.min(sim_valueMin+1, 100);
     similarityInputMin.value = sim_valueMin;
  }
  else if ( direction == "-") {
    sim_valueMin = Math.max(sim_valueMin-1, 0);
    similarityInputMin.value = sim_valueMin;
  };
};

function ContinuousPressChange2(direction){
  if(buttonClicked==true){
    idTO = setTimeout(function(){ContinuousPressChange2(direction)}, changeRate);
    timeOutIntervalIDs.push(idTO);
    ChagngeSimilarityValue2(direction)
    changeCircles2();
  };
};

moreSimilarityMin.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "+";
  ChagngeSimilarityValue2(direction)
  changeCircles2();
  idTO = setTimeout(function(){ContinuousPressChange2(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

moreSimilarityMin.addEventListener("mouseup", endMovement);
moreSimilarityMin.addEventListener("mouseleave", endMovement);

lessSimilarityMin.addEventListener("mousedown", function(){
  buttonClicked = true;
  direction = "-";
  ChagngeSimilarityValue2(direction)
  changeCircles2();
  idTO = setTimeout(function(){ContinuousPressChange2(direction)}, contiousDelay);
  timeOutIntervalIDs.push(idTO);
});

lessSimilarityMin.addEventListener("mouseup", endMovement);
lessSimilarityMin.addEventListener("mouseleave", endMovement);
