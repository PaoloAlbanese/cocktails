window.onload = function () {
    document.getElementById('addTagBtn').disabled = true;

    // to prevent form resubmission on page reload, 
    // tip from dtbaker on [Stackoverflow](https://stackoverflow.com/questions/6320113/how-to-prevent-form-resubmission-when-page-is-refreshed-f5-ctrlr)
    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href);
    }

    // only one tag input box available at a time, Add tag button enabled when a valid value is entered
    var tag = document.getElementById("tag");
    var addTagBtn = document.getElementById('addTagBtn');

    tag.addEventListener("change", function () {
        if (document.getElementById('sel_tags').checked) {
            document.getElementById("new_tag").disabled = true;
            document.getElementById("new_tag").value = "";
            document.getElementById("pick_tag").disabled = false;
            document.getElementById("pick_tag").required = true;
            if (document.getElementById("pick_tag").value == "select an existing tag") {
                addTagBtn.disabled = true;
            }
            else {
                addTagBtn.disabled = false;
            }

        }

        else if (document.getElementById('other_tag').checked) {
            document.getElementById("new_tag").disabled = false;
            document.getElementById("new_tag").required = true;
            document.getElementById("pick_tag").disabled = true;

            addTagBtn.disabled = false;


        }
    });


}
