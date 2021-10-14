var ampH = 15;
var speed = 50;
var time = 0;
var color = "#ff0000";
var currentIntervalID;
var allIntervalIDsAmp = [];
var initCounter = 0;

function init() {
  	currentIntervalID = setInterval(OnDraw, speed);
    allIntervalIDsAmp.push(currentIntervalID);
    initCounter += 1; // originally for debugging
  }

function OnDraw() {
  time = time + 0.2;
	var amplitudeCanvas = document.getElementById("amplitudeCanvas");
	var dataLine = amplitudeCanvas.getContext("2d");

	dataLine.clearRect(0, 0, amplitudeCanvas.width, amplitudeCanvas.height);

	dataLine.beginPath();
	dataLine.moveTo(0, amplitudeCanvas.height * 0.5);
	for(cnt = -1; cnt <= amplitudeCanvas.width; cnt++){
		dataLine.lineTo(cnt, amplitudeCanvas.height * 0.5 - (Math.random() * 2 + Math.cos(time + cnt * 0.05) * ampH));
	};

	dataLine.lineWidth = 1
	dataLine.strokeStyle = color;
	dataLine.stroke();

};

function overColor() {
  color = "#ff0000";
};

function leaveColor() {
  color = "#0000ff";
};

function changeAmp(direction){
  ampH = ampH + 1*direction
  allIntervalIDsAmp.forEach((intervalIDi, i) => {
    clearInterval(intervalIDi);
  });
  speed = speed + 1*-1*direction
  init();
}

function resetAmplitues(){
  speed = 50;
  ampH =15;
  allIntervalIDsAmp.forEach((intervalIDi, i) => {
    clearInterval(intervalIDi);
  });
};

ampLess.addEventListener("click", function(){changeAmp(-1)})
ampMore.addEventListener("click", function(){changeAmp(1)})
