
var nextFeatureButton = document.getElementById("nextFeatureButton");
var slider = document.getElementById("myRange");

var mouseDown = 0;
document.body.onmousedown = function() {
  ++mouseDown;
}
document.body.onmouseup = function() {
  --mouseDown;
}

function changeCircles(){
  if(mouseDown){
    draw();
  };
};

function changeOnClickCircles(){
  draw();
};

slider.onmousemove = function(){changeCircles()};
slider.onmouseover = function(){changeCircles()};
slider.onclick = function(){changeOnClickCircles()};

function SaveReort(){
  // Code here should save report and change profile
  // ...
};

// circles report code:
var canvas = document.getElementById("myCanvas");
canvas.width = slider.getClientRects()[0].width*0.65
canvas.height = canvas.width/2
var ctx = canvas.getContext("2d");
var y = canvas.height/2;
r=canvas.width/4
var x1 = r/2 + canvas.width/2 + (50-(slider.value))
var x2 = canvas.width/ 2 - r/2 - (50-(slider.value))

function drawBall() {
  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x1, y, r, 0, Math.PI*2, 0);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();

  ctx.beginPath();
  ctx.fillStyle = "#af4c50";
  ctx.arc(x2, y, r, 0, Math.PI*2, 4);
  <!-- ctx.stroke(); -->
  ctx.linewidth = 2
  ctx.globalAlpha = 0.8;
  ctx.fill();
  ctx.closePath();
}

function draw(direction) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    x1 = r/2 + canvas.width/2 + (50-(slider.value))/100 * canvas.width/4
    x2 = canvas.width/ 2 - r/2 - (50-(slider.value))/100 * canvas.width/4
    drawBall();
}

function checkKey(e) {
  e = e || window.event;
  if (e.keyCode == '38') {
    // up arrow
  }
  else if (e.keyCode == '40') {
    // down arrow
  }
  else if (e.keyCode == '37') {
    // left arrow
    draw(-1)
  }
  else if (e.keyCode == '39') {
    // right arrow
    draw(1)
  }
};

drawBall();
if(document.title != "profile"){
  reportSections["max"].style.display = "none";
} else if (document.title == "profile"){
  // maxSimilaritySection.classList.add('profiles_size')
};





// Listen for the event.
body = document.getElementsByTagName("body")[0];
body.addEventListener("NewProfile", function(){draw()});
