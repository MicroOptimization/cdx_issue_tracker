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
    console.log("desc div being clicked")
    
    console.log(edit_box.style.display)

    if (edit_box.style.display == "none") { //if edit box is not out
        console.log("a")
        
        edit_box.style.display = "block";
        desc_box.style.display = "none";
        edit_box.removeAttribute('readonly');
        event.stopPropagation() //Look this up later. but basically it prevents function (a) from being invoked right now 
    }
});

//function (a)
window.addEventListener("click", function(event) {
    if (event.target != edit_box) {
        edit_box.style.display = "none";
        desc_box.style.display = "block";

        //pass pid
        //pass text

        var desc_data = [ //the actual data that we're passing back to our flask function
            {"new_text": edit_box.value},
            {"project_id": 6}
        ];

        $.ajax({
            type: "POST", //method
            url: "/updatedesc", //this is the flask route
            data: JSON.stringify(desc_data), //I have no idea what this is
            contentType: "application/json",
            dataType: 'json' 
        });
        /*
        var server_data = [ //the actual data that we're passing back to our flask function
            {"QTc": 1},
            {"prolonged": 2},
            {"HR": 3},
            {"QT": 4},
            {"Sex": 5}
        ];

        $.ajax({
            type: "POST", //method
            url: "/process_qtc", //this is the flask route
            data: JSON.stringify(server_data), //I have no idea what this is
            contentType: "application/json",
            dataType: 'json' 
        });
        */
    }
});


