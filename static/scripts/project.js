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


$('.desc_div').click(function(event) {
    console.log("desc div being clicked")
    
    console.log(edit_box.style.display)

    if (edit_box.style.display == "none") { //if edit box is out
        console.log("a")
        
        edit_box.style.display = "block";
        desc_box.style.display = "none";
        
    } else {
        console.log("b")
        edit_box.style.display = "none";
        desc_box.style.display = "block";
    }
    
});
/*
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}*/