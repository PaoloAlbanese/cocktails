        window.onload = function() {
        var storedDescription = localStorage.getItem("description");
        var storedName = localStorage.getItem("rName");
        var storedTime = localStorage.getItem("rTime");
        var storedCookTime = localStorage.getItem("CookTime");
        var storedTimeNotes = localStorage.getItem("timeNotes");
        // var storedRecipeId = localStorage.getItem("RecipeId");
        document.getElementById('addTagBtn').disabled = true;

        var nameField = document.getElementById("recipe_name");
        var Descriptione = document.getElementById("recipe_description");
        var timeField = document.getElementById("time");
        var CookTimeField = document.getElementById("cook_time");
        var timeNotesField = document.getElementById("time_notes");

        // var recipeExists = {{% recipe %}};
        // console.log( recipeExists)

        if (localStorage.getItem('tags') !== null) {
            console.log(`tags  exists`);
        } else {
            console.log(`tags not found`);
        }

            // if (storedRecipeId) {
            //     RecipeId = storedRecipeId;
            // }
       
            // else {
            // RecipeId = "";
            // }
            // var RecipeIdField = document.getElementById("recipe_id");
            // RecipeIdField.value = RecipeId;
            // console.log('RecipeId  est ', RecipeId)

            if (storedName) {
                rName = storedName;
                
                nameField.value = rName;
            }
       
            // else {
            // rName = "";
            // }
            // var nameField = document.getElementById("recipe_name");
            // nameField.value = rName;
            // nameField.value = "porcaccia la miseria";
            


            if (storedDescription) {
                description = storedDescription;
                Descriptione.innerHTML = description;
            }
       
            // else {
            // description = "";
            // }
            
            // Descriptione.innerHTML = description;


            if (storedTime) {
                rTime = storedTime;
                timeField.value = rTime;
            }
       
            // else {
            // rTime = "";
            // }
            
            // timeField.value = rTime;

            if (storedCookTime) {
                CookTime = storedCookTime;
                CookTimeField.value = CookTime;
            }
       
            // else {
            // CookTime = "";
            // }
            
            // CookTimeField.value = CookTime;

            if (storedTimeNotes) {
                timeNotes = storedTimeNotes;
                timeNotesField.value = timeNotes;
            }
       
            // else {
            // timeNotes = "";
            // }
            
            // timeNotesField.value = timeNotes;

            
        };



        function keepFields(){
        description = document.getElementById("recipe_description").value;
        rName = document.getElementById("recipe_name").value;
        rTime = document.getElementById("time").value;
        timeNotes = document.getElementById("time_notes").value;
        CookTime = document.getElementById("cook_time").value;
        // RecipeId = document.getElementById("recipe_id").value;
        console.log(description)
        console.log(rName)
        
        // if (RecipeId) {
        //     localStorage.setItem('RecipeId', RecipeId);
        // }
        // else {
        //     var storedRecipeId = localStorage.getItem("RecipeId");
        
        // }


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

    function clearFields(){
        localStorage.removeItem('description');
        localStorage.removeItem('rName');
        localStorage.removeItem('rTime');
        localStorage.removeItem('timeNotes');
        localStorage.removeItem('tags');
        localStorage.removeItem('CookTime');
        localStorage.removeItem('RecipeId');
    }


var tags = document.getElementById("tags");
var tag = document.getElementById("tag");
var tags = []
var addTagBtn = document.getElementById('addTagBtn');

    tag.addEventListener("change", function() {
        // var addTagBtn = document.getElementById('addTagBtn');
// window.onload = function display() {
        // if (document.getElementById('pick_tag').onFocus) {
        if (document.getElementById('sel_tags').checked) {
            document.getElementById("new_tag").disabled = true;
            document.getElementById("new_tag").value = "";
            // document.getElementById('other_tag').checked = false
            document.getElementById("pick_tag").disabled= false;
            document.getElementById("pick_tag").required = true;
            if (document.getElementById("pick_tag").value == "select a tag"){
                addTagBtn.disabled=true;
            }
            else{
                addTagBtn.disabled=false;
            }     
            
            console.log('sel tag selcted')
            console.log('tags', tags)
            
        }
        
        else if (document.getElementById('other_tag').checked) {
            // document.getElementById('sel_tags').checked = false
            // document.getElementById('new_tag').checked = false
            document.getElementById("new_tag").disabled = false;
            document.getElementById("new_tag").required = true;
            document.getElementById("pick_tag").disabled = true;
            
            addTagBtn.disabled=false;
           
            console.log('new tag selcted')
            console.log('tags', tags)
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

//   function addTag(){

//       if (document.getElementById('sel_tags').checked) {
//         printedTags.push(document.getElementById("pick_tag").value)
//       localStorage.setItem('tags', JSON.stringify(printedTags));
        
//       }
//       else if (document.getElementById('other_tag').checked){
//         printedTags.push(document.getElementById("new_tag").value)
//         localStorage.setItem('tags', JSON.stringify(printedTags));
        
//       }
      
        
     
      
//       console.log('printedTags', printedTags)

//   }


$(document).ready(function(){
    var valsel = $('#ingridient_unit1').children("option:selected").val();
    console.log('funziona stacosa?', valsel );
    if (valsel == ''){
        $('#ingridient_unit1').removeClass('black_color').addClass('red_color');
        console.log('funziona stacosa davero?', valsel )
    }
    else{
        $('#ingridient_unit1').removeClass('red_color').addClass('black_color');

    }
});

$('#ingridient_unit1').change(function(e) {
    var valsel = $(this).children("option:selected").val();
    console.log('funziona stacosa?', valsel );
    if (valsel == ''){
        $(this).removeClass('black_color').addClass('red_color');
        console.log('funziona stacosa davero?', valsel )
    }
    else{
        $(this).removeClass('red_color').addClass('black_color');

    }
});