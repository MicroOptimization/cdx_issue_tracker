var assign_ticket = document.getElementById("ticket_list_div")
var add_user = document.getElementById("add_user_div")
var change_permissions = document.getElementById("permission_div")
var selected_user_id = undefined
var selected_user_css_id = undefined


//These 3 functions are to change the context div.
function toggle_assign_ticket() {
    assign_ticket.style.display = "flex"
    add_user.style.display = "none"
    change_permissions.style.display = "none"
}

function toggle_change_permissions() {
    assign_ticket.style.display = "none"
    add_user.style.display = "none"
    change_permissions.style.display = "flex"
}

function toggle_new_contributor() {
    assign_ticket.style.display = "none"
    add_user.style.display = "flex"
    change_permissions.style.display = "none"
}



$('.user_row').click(function(event) {
    //these 5 lines create the visual indicator that shows what user is being selected
    if (typeof selected_user_css_id !== 'undefined') {
        document.getElementById(selected_user_css_id).style.backgroundColor = "#1fcaca"
    }
    selected_user_css_id = event.target.id
    document.getElementById(selected_user_css_id).style.backgroundColor = "#70a3cf"

    //These 3 lines actually store the user_id of the user itself.
    input = event.target.id
    temp = input.split("_")
    selected_user_id = temp[2]    
});

function set_selected_user_id(id) {
    ele = document.getElementById(id)
    ele.value = selected_user_id
}