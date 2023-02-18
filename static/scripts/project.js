function toggle_minimize_desc() {
    var desc = document.getElementById("desc_div_id");
    if (desc.style.display != "none") {
        desc.style.display = "none"
    } else {
        desc.style.display = "flex"
    }
}

var edit_box = document.getElementById("edit_proj_desc")
var desc_box = document.getElementById("proj_desc")

edit_box.style.display = "none"
desc_box.style.display = "block"

var desc_div = document.getElementById("desc_div_id")


$('.desc_div').click(function(event) {
    if (edit_box.style.display == "none") { //if edit box is not out

        edit_box.style.display = "block";
        desc_box.style.display = "none";
        edit_box.removeAttribute('readonly');
        event.stopPropagation() //Look this up later. but basically it prevents function (a) from being invoked right now 
    }
});

//function (a)
window.addEventListener("click", edit_desc_listener);
window.addEventListener("keypress", edit_desc_listener);

//This function hides our edit box when we click off of it or press enter. and also updates our postgres db
function edit_desc_listener(event) {
    if ((event.target != edit_box) || (event.key === "Enter")) {
        //These two lines hide our edit box after we're done with it
        edit_box.style.display = "none";
        desc_box.style.display = "block";

        send_new_desc_info()
    }
}

function send_new_desc_info() {
    var pid = document.getElementById("pid_id").value; //Yes this is a hidden input field that stores our project id lol

    //the actual data that we're passing back to our flask function
    var desc_data = {
        "new_text": edit_box.value, 
        "project_id": pid
    };

    $.ajax({
        type: "POST", //method
        url: "/updatedesc", //this is the flask route
        data: JSON.stringify(desc_data), //I have no idea what this is
        contentType: "application/json",
        dataType: 'json', 
        success: function(result) { //when the response comes back and it's successful, run the code below
            //This updates the description with the new value from the textarea
            desc_box.innerHTML = edit_box.value; 
        } 
    });
}
