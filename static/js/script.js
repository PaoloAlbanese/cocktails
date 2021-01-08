var theHtml = document.getElementById("theHtml");
var classList = theHtml.classList;

setTimeout(alertFunc, 300);

function alertFunc() {
$(document).ready(function() {

  
  document.getElementsByTagName("html")[0].style.visibility = "visible";


    while (classList.length > 0) {
   classList.remove(classList.item(0));
} 

});
}

function clearFields(){
        localStorage.removeItem('description');
        localStorage.removeItem('rName');
        localStorage.removeItem('rTime');
        localStorage.removeItem('timeNotes');
        localStorage.removeItem('tags');
        localStorage.removeItem('CookTime');
        localStorage.removeItem('RecipeId');
    }