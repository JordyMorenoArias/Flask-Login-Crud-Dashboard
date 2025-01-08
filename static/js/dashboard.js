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

    fetch('/task', {
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
            cleanTasks();
            LoadTasks();
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

document.addEventListener('DOMContentLoaded', LoadTasks);
async function LoadTasks() {
    try {
        const respuesta = await fetch('/getTasks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!respuesta.ok) {
            throw new Error('La respuesta de la red no fue correcta');
        }

        const tasks = await respuesta.json();

        let parentDiv

        tasks.forEach(task => {

            if (task.status === 'Pendiente') {
                parentDiv = document.getElementById('column-ToDo');
            } else if (task.status === 'En Proceso') {
                parentDiv = document.getElementById('column-InProgress');
            } else {
                parentDiv = document.getElementById('column-Done');
            }

            let taskDiv = document.createElement('div');
            taskDiv.className = 'task-card';

            // Crear los elementos de la tarea
            let taskTitle = document.createElement('div');
            let taskDescription = document.createElement('div');
            let taskDate = document.createElement('div');
            let taskPriority = document.createElement('span');

            // Asignar clases a los elementos
            taskTitle.className = 'task-title';
            taskDescription.className = 'task-description';
            taskDate.className = 'task-date';
            const priorityClasses = {
                'Baja': 'task-priority low',
                'Media': 'task-priority medium',
                'Alta': 'task-priority high'
            };

            taskPriority.className = priorityClasses[task.priority] || 'task-priority default';

            // Asignar contenido a los elementos
            taskTitle.textContent = task.task_name;
            taskDescription.textContent = task.description;
            taskDate.textContent = task.expiration_date.split('00:00:00')[0].trim();
            taskPriority.textContent = task.priority;

            // Agregar los elementos al taskDiv
            taskDiv.appendChild(taskTitle);
            taskDiv.appendChild(taskDescription);
            taskDiv.appendChild(taskDate);
            taskDiv.appendChild(taskPriority);

            // Agregar el taskDiv al parentDiv
            parentDiv.appendChild(taskDiv);

        })

    } catch (error) {
        console.error('Error al cargar las tareas:', error);
    }
}

function cleanTasks() {
    const grandParentDivs = document.getElementsByClassName('task-grid');

    Array.from(grandParentDivs).forEach(grandParentDiv => {
        const excludeChildren = document.getElementsByClassName('column-header');

        Array.from(grandParentDiv.children).forEach(parentDiv => {
            Array.from(parentDiv.children).forEach(child => {
                if (!Array.from(excludeChildren).includes(child)) {
                    parentDiv.removeChild(child);
                }
            });
        });
    });
}