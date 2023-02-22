var tickets_div = document.getElementById("tickets_div")
tickets_div.style.display = "none"

function toggle_ticket() {
    
    if (tickets_div.style.display == "none") {
        tickets_div.style.display = "flex"
    } else {
        tickets_div.style.display = "none"
    }
}
