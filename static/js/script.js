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

window.addEventListener("scroll", SetScrollY);
        // setting the scroll position as local storage variable. it will be read py the 'PreserveScroll' script to preserve scroll position upon load
        function SetScrollY(){
            
            localStorage.setItem('scrollpos', window.scrollY);
            
            
        };

        window.onbeforeunload = function(e) {
            
                
            localStorage.setItem('scrollpos', window.scrollY);
            
        };

window.addEventListener("load", keepScroll);


// document.addEventListener("DOMContentLoaded", keepScroll);

// takes the local storage var scrollpos value and sets it as the page scrolling position if the current page and the refer are the same
 function keepScroll(){
    var elem = document.getElementById("contenuto");
    var scrollpos = localStorage.getItem('scrollpos');
    // var this_url = "{{this_url}}";
    var this_url = document.getElementById("this_url").value;
    // var referer_view ="{{referer_view}}";
    var referer_view = document.getElementById("referer_view").value;
    console.log( this_url, ' e ', referer_view )
    

            
            if (this_url == referer_view){
            
            if (scrollpos) {
                
            document.getElementById("contenuto").style.top = scrollpos;
            window.scroll(0,scrollpos)
           
            }
            else{
                window.scrollTo(0, 0);
             
            }
            }



};            