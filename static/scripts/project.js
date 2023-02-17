function toggle_minimize_desc() {
    var desc = document.getElementById("desc_div_id");
    if (desc.style.display != "none") {
        desc.style.display = "none"
    } else {
        desc.style.display = "flex"
    }

}