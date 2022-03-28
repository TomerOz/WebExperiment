var getBonusButton = document.getElementById("getBonusButton");
var requestedSubject = document.getElementById("requestedSubject");
var resultSection = document.getElementById("result");

getBonusButton.addEventListener("click", function(){
  resultSection.textContent = "Subject " + requestedSubject.value + "  accuracy is " + bounuses[requestedSubject.value] +"%";
});
