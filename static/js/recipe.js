        window.onload = function() {
        document.getElementById('addTagBtn').disabled = true;


        if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
        }

// var tags = document.getElementById("tags");
var tag = document.getElementById("tag");
// var tags = []
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
            
            console.log('sel tag selcted')
            console.log('tags', tags)
            
        }
        
        else if (document.getElementById('other_tag').checked) {
            document.getElementById("new_tag").disabled = false;
            document.getElementById("new_tag").required = true;
            document.getElementById("pick_tag").disabled = true;
            
            addTagBtn.disabled=false;
           

        }
  });


        }
