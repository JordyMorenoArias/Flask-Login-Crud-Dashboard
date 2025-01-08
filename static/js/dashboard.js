function ShowHideCreateTask() {
    var container = document.getElementsByClassName("create-Task-Container")[0];

    if (container.style.visibility === "hidden" || container.style.visibility === "") {
        container.style.visibility = "visible";
    } else {
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

document.querySelector(".save-task").addEventListener("click", CreateTask);
function CreateTask() {
    const dataTask = {
        titulo: document.querySelector(".txt-task-title").value,
        categoria: document.querySelector(".txt-task-category").value,
        descripcion: document.querySelector(".txt-task-description").value,
        prioridad: document.querySelector(".txt-task-priority").value,   
        fecha: document.querySelector(".txt-task-date").value,   
    }

    fetch('/task',{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataTask)
    })
    .then(respuesta => {
        if (!respuesta.ok) {
            throw new Error('La respuesta de la red no fue correcta');
        }
        return respuesta.json();
    })
    .then(datos => {
        console.log('Éxito:', datos);
        limpiarFormulario();
    })
    .catch(error => {
        console.error('Error:', error);
    });
 }

 function limpiarFormulario() {
    document.querySelector('.txt-task-title').value = '';
    document.querySelector('.txt-task-category').value = 'personal';
    document.querySelector('.txt-task-description').value = '';
    document.querySelector('.txt-task-priority').value = '';
    document.querySelector('.txt-task-date').value = 'low';
    
    document.querySelector('.create-Task-Container').style.visibility = 'hidden';
}