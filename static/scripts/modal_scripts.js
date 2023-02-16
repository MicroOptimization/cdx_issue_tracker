var modal = document.getElementById("modal_id");

function toggle_modal(tid) {
    modal.style.display = "block";
    document.getElementById("tid_field").value = tid;
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}