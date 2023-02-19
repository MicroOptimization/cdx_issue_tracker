function toggle_minimize_desc() {
    var desc = document.getElementById("desc_div_id");
    if (desc.style.display != "none") {
        desc.style.display = "none"
    } else {
        desc.style.display = "flex"
    }
}



/*We're making some fancy description editing stuff*/
var edit_box = document.getElementById("edit_proj_desc")
var desc_box = document.getElementById("proj_desc")
var desc_div = document.getElementById("desc_div_id")

//For some reason these are set by default even tho its in my css
edit_box.style.display = "none"
desc_box.style.display = "block"

$('.desc_div').click(function(event) {
    if (edit_box.style.display == "none") { //if edit box is not out

        edit_box.style.display = "block";
        desc_box.style.display = "none";
        edit_box.removeAttribute('readonly');
        event.stopPropagation() //Look this up later. but basically it prevents functions at (a) from being invoked right now 
        edit_box.focus()
        //functions at (a)
        window.addEventListener("click", edit_desc_listener);
        window.addEventListener("keypress", edit_desc_listener);
    }
});



//This function hides our edit box when we click off of it or press enter. and also updates our postgres db
function edit_desc_listener(event) {
    if ((event.target != edit_box) || (event.key === "Enter")) {
        //These two lines hide our edit box after we're done with it
        edit_box.style.display = "none";
        desc_box.style.display = "block";

        send_new_desc_info()

        //These two lines are gonna be useful because we're adding more similar effects, 
        //and these two functions are specific to the desc div, so they'd conflict.
        window.removeEventListener("click", edit_desc_listener);
        window.removeEventListener("keypress", edit_desc_listener);
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


/*this is very similar, but for the title instead of the description*/
var title_display = document.getElementById("title_display")
var edit_title = document.getElementById("edit_title")

title_display.style.display = "block"
edit_title.style.display = "none"


$('#title_span').click(function(event) {
    if (title_display.style.display == "block") {
        title_display.style.display = "none"
        edit_title.style.display = "block"

        window.addEventListener("click", edit_title_listener);
        window.addEventListener("keypress", edit_title_listener);
        event.stopPropagation()

        edit_title.focus()
    }/* else {
        title_display.style.display = "block"
        edit_title.style.display = "none"
    }*/
});


function edit_title_listener(event) {
    if ((event.target != edit_title) || (event.key === "Enter")) {
        //These two lines hide our edit box after we're done with it
        edit_title.style.display = "none";
        title_display.style.display = "block";

        send_new_title_info()

        //These two lines are gonna be useful because we're adding more similar effects, 
        //and these two functions are specific to the desc div, so they'd conflict.
        window.removeEventListener("click", edit_title_listener);
        window.removeEventListener("keypress", edit_title_listener);
    }
}

function send_new_title_info() {
    var pid = document.getElementById("pid_id").value; //Yes this is a hidden input field that stores our project id lol
    
    //the actual data that we're passing back to our flask function
    var title_data = {
        "new_title": edit_title.value, 
        "project_id": pid
    };

    $.ajax({
        type: "POST", //method
        url: "/updatetitle", //this is the flask route
        data: JSON.stringify(title_data), //I have no idea what this is
        contentType: "application/json",
        dataType: 'json', 
        success: function(result) { //when the response comes back and it's successful, run the code below
            //This updates the description with the new value from the textarea
            title_display.innerHTML = edit_title.value; 
        } 
    });
}





var cid = undefined;
var col_display = undefined; 
var col_edit = undefined;

$('.heading_label_div').click(function(event) {
    cid = event.target.id.split("_")[2]

    set_col_edit_variables()

    if (col_display.style.display == "block") {
        col_display.style.display = "none"
        col_edit.style.display = "block"

        window.addEventListener("click", edit_col_listener);
        window.addEventListener("keypress", edit_col_listener);
        event.stopPropagation()

        col_edit.focus()
    }
});

function set_col_edit_variables() {
    col_display = document.getElementById("display_col_" + cid)
    col_edit = document.getElementById("edit_col_" + cid)

    col_display.style.display = "block"
    col_edit.style.display = "none"
}

function edit_col_listener(event) {
    if ((event.target != col_edit) || (event.key === "Enter")) {
        //These two lines hide our edit box after we're done with it
        col_edit.style.display = "none";
        col_display.style.display = "block";

        send_new_col_info()

        //These two lines are gonna be useful because we're adding more similar effects, 
        //and these two functions are specific to the desc div, so they'd conflict.
        window.removeEventListener("click", edit_col_listener);
        window.removeEventListener("keypress", edit_col_listener);
    }
}

function send_new_col_info() {
    //the actual data that we're passing back to our flask function
    var col_data = {
        "new_title": col_edit.value, 
        "col_id": cid
    };
    $.ajax({
        type: "POST", //method
        url: "/updatecol", //this is the flask route
        data: JSON.stringify(col_data), //I have no idea what this is
        contentType: "application/json",
        dataType: 'json', 
        success: function(result) { //when the response comes back and it's successful, run the code below
            //This updates the description with the new value from the textarea
            col_display.innerHTML = col_edit.value; 
        } 
    });
}