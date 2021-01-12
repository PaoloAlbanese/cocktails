        window.onload = function() {
        var storedDescription = localStorage.getItem("description");
        var storedName = localStorage.getItem("rName");
        var storedTime = localStorage.getItem("rTime");
        var storedCookTime = localStorage.getItem("CookTime");
        var storedTimeNotes = localStorage.getItem("timeNotes");
        document.getElementById('addTagBtn').disabled = true;
        

        if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
        }

        if (localStorage.getItem('tags') !== null) {
            console.log(`tags  exists`);
        } else {
            console.log(`tags not found`);
        }


            if (storedName) {
                rName = storedName;
            }
       
            else {
            rName = "";
            }
            var nameField = document.getElementById("recipe_name");
            nameField.value = rName;
            


            if (storedDescription) {
                description = storedDescription;
            }
       
            else {
            description = "";
            }
            var Descriptione = document.getElementById("recipe_description");
            Descriptione.innerHTML = description;


            if (storedTime) {
                rTime = storedTime;
            }
       
            else {
            rTime = "";
            }
            var timeField = document.getElementById("time");
            timeField.value = rTime;

            if (storedCookTime) {
                CookTime = storedCookTime;
            }
       
            else {
            CookTime = "";
            }
            var CookTimeField = document.getElementById("cook_time");
            CookTimeField.value = CookTime;

            if (storedTimeNotes) {
                timeNotes = storedTimeNotes;
            }
       
            else {
            timeNotes = "";
            }
            var timeNotesField = document.getElementById("time_notes");
            timeNotesField.value = timeNotes;

            
        };



        function keepFields(){
        description = document.getElementById("recipe_description").value;
        rName = document.getElementById("recipe_name").value;
        rTime = document.getElementById("time").value;
        timeNotes = document.getElementById("time_notes").value;
        CookTime = document.getElementById("cook_time").value;
        console.log(description)
        console.log(rName)

        if (rName) {
            localStorage.setItem('rName', rName);
        }
        else {
            var storedName = localStorage.getItem("rName");
        
        }
        
        if (description) {
            localStorage.setItem('description', description);
        }
        else {
            var storedDescription = localStorage.getItem("description");
        
        }

        if (rTime) {
            localStorage.setItem('rTime', rTime);
        }
        else {
            var storedTime = localStorage.getItem("rTime");
        
        }

        if (CookTime) {
            localStorage.setItem('CookTime', CookTime);
        }
        else {
            var storedCookTime = localStorage.getItem("CookTime");
        
        }

        if (timeNotes) {
            localStorage.setItem('timeNotes', timeNotes);
        }
        else {
            var storedTimeNotes = localStorage.getItem("timeNotes");
        
        }
        
    }

    


var tags = document.getElementById("tags");
var tag = document.getElementById("tag");
var tags = []
var addTagBtn = document.getElementById('addTagBtn');

    tag.addEventListener("change", function() {

        if (document.getElementById('sel_tags').checked) {
            document.getElementById("new_tag").disabled = true;
            document.getElementById("new_tag").value = "";
            document.getElementById("pick_tag").disabled= false;
            document.getElementById("pick_tag").required = true;
            if (document.getElementById("pick_tag").value == "select an existing tag"){
                addTagBtn.disabled=true;
            }
            else{
                addTagBtn.disabled=false;
            }     

            
        }
        else if (document.getElementById('other_tag').checked) {
            document.getElementById("new_tag").disabled = false;
            document.getElementById("new_tag").required = true;
            document.getElementById("pick_tag").disabled = true;
            
            addTagBtn.disabled=false;

        }
  });


  addTagBtn.addEventListener("click", function(){ 
      
    if (document.getElementById('sel_tags').checked) {
      printedTags.push(document.getElementById("pick_tag").value)
      localStorage.setItem('tags', JSON.stringify(printedTags));
        
      }
      else if (document.getElementById('other_tag').checked){
        printedTags.push(document.getElementById("new_tag").value)
        localStorage.setItem('tags', JSON.stringify(printedTags));
        
      } });


$(document).ready(function(){
    var valsel = $('#ingridient_unit1').children("option:selected").val();
    if (valsel == ''){
        $('#ingridient_unit1').removeClass('black_color').addClass('red_color');
    }
    else{
        $('#ingridient_unit1').removeClass('red_color').addClass('black_color');

    }
});

$('#ingridient_unit1').change(function(e) {
    var valsel = $(this).children("option:selected").val();
    if (valsel == ''){
        $(this).removeClass('black_color').addClass('red_color');
        console.log('funziona stacosa davero?', valsel )
    }
    else{
        $(this).removeClass('red_color').addClass('black_color');

    }
});