// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onClick += function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onClick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.oClick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function copyFunction() {
  /* Get the text field */
  var copyText = document.getElementById("myInput");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

   /* Copy the text inside the text field */
   navigator.clipboard
      .writeText(copyText.value)
      .then(() => {
        alert("successfully copied");
      })
      .catch(() => {
        alert("something went wrong");
      });
}
