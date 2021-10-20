var signupContinue = document.getElementById("signupContinue");
var form = document.getElementById("register-form");
var flowInput = document.getElementById("flowInput");

signupContinue.addEventListener("click", function(){
  flowInput.value = "continue"
  form.submit()
})
