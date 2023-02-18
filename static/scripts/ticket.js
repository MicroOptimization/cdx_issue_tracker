var desc_div = document.getElementById("desc_div_id")
var desc_display = document.getElementById("desc_display")
var desc_edit = document.getElementById("desc_edit")
desc_display.style.display = "block"
desc_edit.style.display = "none"

$('#desc_div_id').click(function(event) {
    if (desc_edit.style.display == "none") {
        desc_display.style.display = "none"
        desc_edit.style.display = "block"

        event.stopPropagation()

        window.addEventListener("click", edit_desc_listener)
        window.addEventListener("keypress", edit_desc_listener)
    }
});

function edit_desc_listener(event) {
    console.log("here")
    if ((event.target != desc_edit) || (event.key === "Enter")) {
        desc_display.style.display = "block"
        desc_edit.style.display = "none"

        send_desc_info()

        window.removeEventListener("click", edit_desc_listener)
        window.removeEventListener("keypress", edit_desc_listener)
    }
}

function send_desc_info() {
    var tid = document.getElementById("tid_id").value; //Yes this is a hidden input field that stores our project id lol

    //the actual data that we're passing back to our flask function
    var desc_data = {
        "new_desc": desc_edit.value, 
        "ticket_id": tid
    };

    $.ajax({
        type: "POST", //method
        url: "/updateticketdesc", //this is the flask route
        data: JSON.stringify(desc_data), //I have no idea what this is
        contentType: "application/json",
        dataType: 'json', 
        success: function(result) { //when the response comes back and it's successful, run the code below
            //This updates the description with the new value from the textarea
            desc_display.innerHTML = desc_edit.value; 
        } 
    });
}