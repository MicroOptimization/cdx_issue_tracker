var tickets_div = document.getElementById("tickets_div")
tickets_div.style.display = "none"

var email_div = document.getElementById("email_div")
email_div.style.display = "flex"

function toggle_ticket() {
    
    if (tickets_div.style.display == "none") {
        reset_context_div()
        tickets_div.style.display = "flex"
    } else {
        reset_context_div()
    }
}

function toggle_email() {
    
    if (email_div.style.display == "none") {
        reset_context_div()
        email_div.style.display = "flex"
    } else {
        reset_context_div()
    }
}

function reset_context_div() {
    tickets_div.style.display = "none"
    email_div.style.display = "none"
}
