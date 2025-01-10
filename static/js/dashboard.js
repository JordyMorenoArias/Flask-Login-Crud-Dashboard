// Variable global para almacenar las tareas en formato JSON.
let selectedTask;

// Carga las tareas al cargar el DOM.
document.addEventListener('DOMContentLoaded', LoadTasks);

// Asocia el evento de guardar tarea al botón correspondiente.
document.querySelector(".btn-create-task").addEventListener("click", CreateTask);

document.querySelector(".btn-update-task").addEventListener("click", UpdateTask);

document.querySelector(".btn-delete-task").addEventListener("click", DeleteTask);


// Función para mostrar u ocultar el formulario de creación de tareas.
function ShowHideCreateTask() {
    // Selecciona el contenedor del formulario de creación de tareas.
    const containerCreate = document.getElementsByClassName("create-Task-Container")[0];

    // Alterna la visibilidad del formulario de creación.
    if (containerCreate.style.visibility === "hidden" || containerCreate.style.visibility === "") {
        containerCreate.style.visibility = "visible";
    } else {
        containerCreate.style.visibility = "hidden";
    }
}

// Función para mostrar u ocultar el formulario de actualización de tareas.
function ShowHideUpdateTask(task) {
    // Selecciona el contenedor del formulario de actualización de tareas.
    const containerUpdate = document.getElementsByClassName("update-Task-Container")[0];

    // Alterna la visibilidad del formulario de actualización.
    if (containerUpdate.style.visibility === "hidden" || containerUpdate.style.visibility === "") {
        containerUpdate.style.visibility = "visible";

        // Actualiza el formulario con los datos de la tarea seleccionada.
        selectedTask = task; // Guarda la tarea seleccionada globalmente.
        document.querySelector('.update-task-title').value = task.task_name;
        document.querySelector('.update-task-category').value = task.category;
        document.querySelector('.update-task-description').value = task.description;
        document.querySelector('.update-task-date').value = new Date(task.expiration_date).toISOString().split('T')[0];
        document.querySelector('.update-task-priority').value = task.priority;
        document.querySelector('.update-task-status').value = task.status;

    } else {
        containerUpdate.style.visibility = "hidden";
    }
}

// Función para ocultar los formularios de creación y actualización de tareas al hacer clic fuera de ellos.
function HideOnBackgroundClick(event) {
    // Selecciona los contenedores de los formularios.
    const containerCreate = document.getElementsByClassName("create-Task-Container")[0];
    const containerUpdate = document.getElementsByClassName("update-Task-Container")[0];

    // Selecciona los formularios de creación y actualización.
    const taskFormCreate = document.getElementsByClassName("create-task")[0];
    const taskFormUpdate = document.getElementsByClassName("update-task")[0];

    // Verifica si el clic ocurrió fuera del formulario de creación y oculta su contenedor.
    if (containerCreate && taskFormCreate && !taskFormCreate.contains(event.target)) {
        containerCreate.style.visibility = "hidden";
    }

    // Verifica si el clic ocurrió fuera del formulario de actualización y oculta su contenedor.
    if (containerUpdate && taskFormUpdate && !taskFormUpdate.contains(event.target)) {
        containerUpdate.style.visibility = "hidden";
    }
}

async function LoadTasks() {
    try {
        // Realiza una solicitud GET para obtener las tareas desde el servidor.
        const respuesta = await fetch('/get-tasks', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!respuesta.ok) {
            throw new Error('La respuesta de la red no fue correcta');
        }

        // Almacena las tareas en la variable global.
        const taskData = await respuesta.json();

        let parentDiv;

        // Itera sobre las tareas y las organiza según su estado.
        taskData.forEach(task => {
            // Selecciona la columna correspondiente según el estado de la tarea.
            switch (task.status) {
                case 'Pendiente':
                    parentDiv = document.getElementById('column-ToDo');
                    break;
                case 'En Proceso':
                    parentDiv = document.getElementById('column-InProgress');
                    break;
                case 'Completada':
                    parentDiv = document.getElementById('column-Done');
                    break;
            }

            // Verifica si parentDiv existe antes de continuar
            if (!parentDiv) {
                console.error(`No se encontró el contenedor para el estado: ${task.status}`);
                return; // Salta esta iteración si no se encuentra el contenedor
            }


            // Crea el contenedor principal de la tarea.
            let taskDiv = document.createElement('div');
            taskDiv.className = 'task-card';

            // Crea los elementos de la tarea.
            let taskId = document.createElement('p');
            let taskTitle = document.createElement('div');
            let taskDescription = document.createElement('div');
            let taskDate = document.createElement('div');
            let taskPriority = document.createElement('span');

            // Asigna clases a los elementos según su propósito.
            taskId.className = 'task-id';
            taskTitle.className = 'task-title';
            taskDescription.className = 'task-description';
            taskDate.className = 'task-date';

            // Define las clases de prioridad según el nivel.
            const priorityClasses = {
                'Baja': 'task-priority low',
                'Media': 'task-priority medium',
                'Alta': 'task-priority high'
            };

            taskPriority.className = priorityClasses[task.priority] || 'task-priority default';

            // Asigna contenido a los elementos de la tarea.
            taskId.textContent = task.task_Id;
            taskTitle.textContent = task.task_name;
            taskDescription.textContent = task.description;
            taskDate.textContent = task.expiration_date.split('00:00:00')[0].trim();
            taskPriority.textContent = task.priority;

            // Agrega los elementos al contenedor de la tarea.
            taskDiv.appendChild(taskId);
            taskDiv.appendChild(taskTitle);
            taskDiv.appendChild(taskDescription);
            taskDiv.appendChild(taskDate);
            taskDiv.appendChild(taskPriority);

            taskDiv.addEventListener('dblclick', () => ShowHideUpdateTask(task));

            // Agrega la tarea al contenedor principal correspondiente.
            parentDiv.appendChild(taskDiv);
        });

    } catch (error) {
        console.error('Error al cargar las tareas:', error);
    }
}

// Función para limpiar las columnas de tareas.
function cleanTasks() {
    // Selecciona las columnas de tareas.
    const grandParentDivs = document.getElementsByClassName('task-grid');

    Array.from(grandParentDivs).forEach(grandParentDiv => {
        const excludeChildren = document.getElementsByClassName('column-header');

        // Limpia las tareas de las columnas, excluyendo los encabezados.
        Array.from(grandParentDiv.children).forEach(parentDiv => {
            Array.from(parentDiv.children).forEach(child => {
                if (!Array.from(excludeChildren).includes(child)) {
                    parentDiv.removeChild(child);
                }
            });
        });
    });
}

// Limpia los formularios de creación y actualizacion de tareas y los oculta dependiendo de cual este abierto.
function clearForms() {
    if(document.querySelector('.create-Task-Container').style.visibility === 'visible'){

        document.querySelector('.create-task-title').value = '';
        document.querySelector('.create-task-category').value = 'personal';
        document.querySelector('.create-task-description').value = '';
        document.querySelector('.create-task-priority').value = '';
        document.querySelector('.create-task-date').value = '';
    
        document.querySelector('.create-Task-Container').style.visibility = 'hidden';
    }
    else if(document.querySelector('.update-Task-Container').style.visibility === 'visible'){

        document.querySelector('.update-task-title').value = '';
        document.querySelector('.update-task-category').value = 'personal';
        document.querySelector('.update-task-description').value = '';
        document.querySelector('.update-task-priority').value = '';
        document.querySelector('.update-task-date').value = '';
    
        document.querySelector('.update-Task-Container').style.visibility = 'hidden';
    }
}

//  Función para crear una nueva tarea.
//  Recopila los datos de la tarea desde el formulario de creación y los envía al servidor mediante una solicitud HTTP POST.
function CreateTask() {
    // Recopila los datos de la nueva tarea desde los campos del formulario.
    const dataTask = {
        task_name: document.querySelector(".create-task-title").value, // Nombre de la nueva tarea.
        category: document.querySelector(".create-task-category").value, // Categoría de la nueva tarea.
        description: document.querySelector(".create-task-description").value, // Descripción de la nueva tarea.
        priority: document.querySelector(".create-task-priority").value, // Prioridad de la nueva tarea.
        expiration_date: document.querySelector(".create-task-date").value // Fecha de vencimiento de la nueva tarea.
    };

    // Envía los datos de la nueva tarea al servidor.
    fetch('/create-Task', {
        method: 'POST', // Método HTTP utilizado para crear un nuevo recurso.
        headers: {
            'Content-Type': 'application/json' // Especifica que los datos se envían en formato JSON.
        },
        body: JSON.stringify(dataTask) // Convierte el objeto JavaScript a una cadena JSON para enviarlo al servidor.
    })
        .then(respuesta => {
            // Comprueba si la respuesta HTTP no es exitosa (código de estado diferente de 2xx).
            if (!respuesta.ok) {
                throw new Error('La respuesta de la red no fue correcta'); // Lanza un error si la respuesta es incorrecta.
            }
            return respuesta.json(); // Convierte la respuesta JSON a un objeto JavaScript.
        })
        .then(datos => {
            // Acciones a realizar si la solicitud fue exitosa.
            console.log('Éxito:', datos); // Imprime un mensaje en la consola indicando el éxito de la operación.
            clearForms(); // Limpia los campos del formulario de creación.
            cleanTasks(); // Limpia la lista de tareas actuales.
            LoadTasks(); // Carga nuevamente las tareas actualizadas desde el servidor.
        })
        .catch(error => {
            // Manejo de errores en caso de que ocurra un problema en la solicitud o el servidor.
            console.error('Error:', error); // Imprime el error en la consola.
        });
}


// Función para actualizar una tarea existente en el servidor.
// Recoge los datos de los campos del formulario, los envía al servidor mediante una solicitud HTTP PUT, y realiza acciones posteriores según la respuesta del servidor.
function UpdateTask() {
    // Recopila los datos de la tarea desde los campos del formulario.
    const dataTask = {
        task_Id: selectedTask.task_Id, // ID de la tarea seleccionada previamente (global).
        task_name: document.querySelector(".update-task-title").value, // Nombre de la tarea.
        category: document.querySelector(".update-task-category").value, // Categoría de la tarea.
        description: document.querySelector(".update-task-description").value, // Descripción de la tarea.
        priority: document.querySelector(".update-task-priority").value, // Prioridad de la tarea.
        expiration_date: document.querySelector(".update-task-date").value, // Fecha de vencimiento de la tarea.
        status: document.querySelector(".update-task-status").value // Estado de la tarea.
    };

    // Envía una solicitud HTTP PUT al servidor para actualizar la tarea.
    fetch('/update-task', {
        method: 'PUT', // Método HTTP utilizado para actualizar recursos.
        headers: {
            'Content-Type': 'application/json' // Especifica que los datos se envían en formato JSON.
        },
        body: JSON.stringify(dataTask) // Convierte el objeto JavaScript a una cadena JSON para enviarlo al servidor.
    })
        .then(respuesta => {
            // Comprueba si la respuesta HTTP no es exitosa (código de estado diferente de 2xx).
            if (!respuesta.ok) {
                throw new Error('La respuesta de la red no fue correcta'); // Lanza un error si la respuesta es incorrecta.
            }
            return respuesta.json(); // Convierte la respuesta JSON a un objeto JavaScript.
        })
        .then(datos => {
            // Acciones a realizar si la solicitud fue exitosa.
            clearForms(); // Limpia los campos del formulario.
            cleanTasks(); // Limpia la lista de tareas actuales.
            LoadTasks(); // Carga nuevamente las tareas actualizadas.
        })
        .catch(error => {
            // Manejo de errores en caso de que ocurra un problema en la solicitud o el servidor.
            console.error('Error:', error); // Imprime el error en la consola.
        });
}

// Función para eliminar una tarea seleccionada mediante una solicitud DELETE al servidor.
function DeleteTask() {
    // Envía una solicitud DELETE a la ruta '/delete-task' del servidor.
    fetch('/delete-task', {
        method: 'DELETE', // Especifica el método HTTP DELETE.
        headers: {
            'Content-Type': 'application/json' // Indica que el cuerpo de la solicitud será en formato JSON.
        },
        body: JSON.stringify(selectedTask) // Convierte la tarea seleccionada (selectedTask) a formato JSON y la envía como cuerpo de la solicitud.
    })
    .then(respuesta => {
        // Verifica si la respuesta del servidor no es correcta (código de estado HTTP fuera de la categoría 200).
        if (!respuesta.ok) {
            throw new Error('La respuesta de la red no fue correcta'); // Lanza un error con un mensaje específico.
            return respuesta.json(); // (Nota: este retorno no se ejecutará debido al lanzamiento del error).
        }
    })
    .then(datos => {
        // Acciones a realizar si la solicitud DELETE fue exitosa y se obtuvieron datos del servidor.
        clearForms(); // Limpia los campos del formulario.
        cleanTasks(); // Limpia la lista de tareas actuales en la interfaz.
        LoadTasks(); // Recarga la lista de tareas para reflejar los cambios.
    })
    .catch(error => {
        // Manejo de errores en caso de que ocurra un problema en la solicitud o el servidor.
        console.error('Error:', error); // Imprime el error en la consola para diagnóstico.
    });
}



