var modal = document.getElementById("modal_id");
var column_modal = document.getElementById("column_modal");
var ticket_modal = document.getElementById("ticket_modal");


document.body.onload = function() {
    modal = document.getElementById("modal_id");
    column_modal = document.getElementById("column_modal");
    ticket_modal = document.getElementById("ticket_modal");
}

function toggle_modal(tid) {
    modal.style.display = "block";
    document.getElementById("tid_field").value = tid;

    ticket_modal.style.display = "block"
    column_modal.style.display = "none"
}

function toggle_col_modal() {
    modal.style.display = "block";
    
    ticket_modal.style.display = "none"
    column_modal.style.display = "block"
}

function toggle_delete_project_modal() {
    modal.style.display = "block";
    
    proj_delete_modal.style.display = "block" //change this to flex lol
}

function close_delete_project_modal() {
    modal.style.display = "none";
    
    proj_delete_modal.style.display = "none" 
}


window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}