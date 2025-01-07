function ShowHideCreateTask(){
    var container = document.getElementsByClassName("create-Task-Container")[0];

    if(container.style.visibility === "hidden" || container.style.visibility === ""){
        container.style.visibility = "visible";
    }else{
        container.style.visibility = "hidden";
    }
}

// Ocultar al hacer clic en el fondo
function HideOnBackgroundClick(event) {
    var container = document.getElementsByClassName("create-Task-Container")[0];
    var taskForm = document.getElementsByClassName("create-task")[0];

    // Verificar que el clic no sea dentro del formulario
    if (!taskForm.contains(event.target)) {
        container.style.visibility = "hidden";
    }
}