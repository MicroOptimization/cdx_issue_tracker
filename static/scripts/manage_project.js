var assign_ticket = document.getElementById("ticket_list_div")
var add_user = document.getElementById("add_user_div")
var change_permissions = document.getElementById("permission_div")

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