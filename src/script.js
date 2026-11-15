const titleInput = document.getElementById("task-title");
const descriptionInput = document.getElementById("task-description");
const priorityInput = document.getElementById("task-priority");
const addButton = document.getElementById("add-task");
const taskList = document.getElementById("task-list");
const progressText = document.getElementById("progress-text");
const progressBar = document.getElementById("progress-bar");

let tasks = JSON.parse(localStorage.getItem("agileTasks")) || [];
let currentFilter = "all";

// Сохранение задач
function saveTasks() {
    localStorage.setItem("agileTasks", JSON.stringify(tasks));
}

// Добавление задачи
function addTask() {
    const title = titleInput.value.trim();

    if (!title) {
        alert("Введите название задачи!");
        return;
    }

    const task = {
        id: Date.now(),
        title: title,
        description: descriptionInput.value.trim(),
        priority: priorityInput.value,
        status: "To Do"
    };

    tasks.push(task);
    saveTasks();

    titleInput.value = "";
    descriptionInput.value = "";

    renderTasks();
}

// Отображение задач
function renderTasks() {
    taskList.innerHTML = "";

    const filteredTasks = currentFilter === "all"
        ? tasks
        : tasks.filter(task => task.status === currentFilter);

    filteredTasks.forEach(task => {
        const card = document.createElement("div");
        card.className = "task-card";

        const heading = document.createElement("h3");
        heading.textContent = task.title;

        const description = document.createElement("p");
        description.textContent = task.description || "Описание отсутствует";

        const priority = document.createElement("p");
        priority.textContent = "Приоритет: " + task.priority;

        const statusSelect = document.createElement("select");

        ["To Do", "In Progress", "Done"].forEach(status => {
            const option = document.createElement("option");
            option.value = status;
            option.textContent = status;
            option.selected = task.status === status;
            statusSelect.appendChild(option);
        });

        statusSelect.addEventListener("change", () => {
            task.status = statusSelect.value;
            saveTasks();
            renderTasks();
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Удалить";

        deleteButton.addEventListener("click", () => {
            tasks = tasks.filter(item => item.id !== task.id);
            saveTasks();
            renderTasks();
        });

        const actions = document.createElement("div");
        actions.className = "task-actions";
        actions.append(statusSelect, deleteButton);

        card.append(heading, description, priority, actions);
        taskList.appendChild(card);
    });

    updateProgress();
}

// Обновление прогресса
function updateProgress() {
    const completed = tasks.filter(task => task.status === "Done").length;
    const total = tasks.length;

    progressText.textContent =
        `Выполнено задач: ${completed} из ${total}`;

    progressBar.value = total === 0
        ? 0
        : (completed / total) * 100;
}

// Фильтрация задач
document.querySelectorAll(".filters button").forEach(button => {
    button.addEventListener("click", () => {
        currentFilter = button.dataset.filter;
        renderTasks();
    });
});

addButton.addEventListener("click", addTask);

// Первоначальное отображение
renderTasks();