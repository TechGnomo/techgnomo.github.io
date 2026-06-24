const STORAGE_KEY = "personalTaskDashboard";

const taskTitleInput = document.getElementById("taskTitle");
const taskDescriptionInput = document.getElementById("taskDescription");
const taskCategoryInput = document.getElementById("taskCategory");
const taskPriorityInput = document.getElementById("taskPriority");
const taskStatusInput = document.getElementById("taskStatus");
const taskDueDateInput = document.getElementById("taskDueDate");
const addTaskBtn = document.getElementById("addTaskBtn");

const searchInput = document.getElementById("searchInput");
const statusFilter = document.getElementById("statusFilter");
const priorityFilter = document.getElementById("priorityFilter");
const clearFiltersBtn = document.getElementById("clearFiltersBtn");

const totalTasks = document.getElementById("totalTasks");
const highPriorityTasks = document.getElementById("highPriorityTasks");
const inProgressTasks = document.getElementById("inProgressTasks");
const completedTasks = document.getElementById("completedTasks");

const completionRate = document.getElementById("completionRate");
const nextDueTask = document.getElementById("nextDueTask");
const nextDueHint = document.getElementById("nextDueHint");
const currentFilter = document.getElementById("currentFilter");
const dashboardHealth = document.getElementById("dashboardHealth");
const dashboardHealthHint = document.getElementById("dashboardHealthHint");

const heroFocusTitle = document.getElementById("heroFocusTitle");
const heroFocusText = document.getElementById("heroFocusText");

const taskList = document.getElementById("taskList");
const resetBtn = document.getElementById("resetBtn");

let taskData = {
  tasks: []
};

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(taskData));
}

function loadData() {
  const savedData = localStorage.getItem(STORAGE_KEY);

  if (savedData) {
    taskData = JSON.parse(savedData);
  }
}

function formatDate(dateString) {
  if (!dateString) return "No due date";

  const date = new Date(`${dateString}T00:00:00`);

  return date.toLocaleDateString("en-AU", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

function getFilteredTasks() {
  const searchTerm = searchInput.value.toLowerCase().trim();
  const selectedStatus = statusFilter.value;
  const selectedPriority = priorityFilter.value;

  return taskData.tasks.filter((task) => {
    const matchesSearch =
      task.title.toLowerCase().includes(searchTerm) ||
      task.description.toLowerCase().includes(searchTerm) ||
      task.category.toLowerCase().includes(searchTerm);

    const matchesStatus =
      selectedStatus === "All" || task.status === selectedStatus;

    const matchesPriority =
      selectedPriority === "All" || task.priority === selectedPriority;

    return matchesSearch && matchesStatus && matchesPriority;
  });
}

function getNextDueTask() {
  const incompleteTasks = taskData.tasks
    .filter((task) => task.status !== "Completed" && task.dueDate)
    .sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));

  return incompleteTasks[0];
}

function getFocusTask() {
  const highPriority = taskData.tasks.find((task) => {
    return task.status !== "Completed" && task.priority === "High";
  });

  if (highPriority) return highPriority;

  const inProgress = taskData.tasks.find((task) => task.status === "In Progress");

  if (inProgress) return inProgress;

  return getNextDueTask();
}

function setStatus(element, className) {
  element.classList.remove("good", "warning", "danger");
  element.classList.add(className);
}

function updateStats() {
  const total = taskData.tasks.length;
  const highPriority = taskData.tasks.filter((task) => task.priority === "High").length;
  const inProgress = taskData.tasks.filter((task) => task.status === "In Progress").length;
  const completed = taskData.tasks.filter((task) => task.status === "Completed").length;

  totalTasks.textContent = total;
  highPriorityTasks.textContent = highPriority;
  inProgressTasks.textContent = inProgress;
  completedTasks.textContent = completed;

  const rate = total === 0 ? 0 : Math.round((completed / total) * 100);
  completionRate.textContent = `${rate}%`;

  if (rate >= 70) {
    setStatus(completionRate, "good");
  } else if (rate >= 35) {
    setStatus(completionRate, "warning");
  } else {
    setStatus(completionRate, "danger");
  }
}

function updateOverview() {
  const nextTask = getNextDueTask();

  if (nextTask) {
    nextDueTask.textContent = nextTask.title;
    nextDueHint.textContent = `Due: ${formatDate(nextTask.dueDate)}.`;
    setStatus(nextDueTask, nextTask.priority === "High" ? "danger" : "warning");
  } else {
    nextDueTask.textContent = "No tasks";
    nextDueHint.textContent = "Add due dates to track deadlines.";
    setStatus(nextDueTask, "warning");
  }

  const filters = [];

  if (searchInput.value.trim()) {
    filters.push("Search active");
  }

  if (statusFilter.value !== "All") {
    filters.push(statusFilter.value);
  }

  if (priorityFilter.value !== "All") {
    filters.push(`${priorityFilter.value} priority`);
  }

  currentFilter.textContent = filters.length ? filters.join(" / ") : "All tasks";

  if (taskData.tasks.length === 0) {
    dashboardHealth.textContent = "Add tasks";
    dashboardHealthHint.textContent = "Start by adding your first task.";
    setStatus(dashboardHealth, "warning");
    return;
  }

  const incompleteHigh = taskData.tasks.filter((task) => {
    return task.priority === "High" && task.status !== "Completed";
  }).length;

  if (incompleteHigh > 0) {
    dashboardHealth.textContent = `${incompleteHigh} high priority`;
    dashboardHealthHint.textContent = "High priority tasks still need attention.";
    setStatus(dashboardHealth, "danger");
    return;
  }

  const incomplete = taskData.tasks.filter((task) => task.status !== "Completed").length;

  if (incomplete > 0) {
    dashboardHealth.textContent = "In progress";
    dashboardHealthHint.textContent = "You have active tasks to complete.";
    setStatus(dashboardHealth, "warning");
    return;
  }

  dashboardHealth.textContent = "All done";
  dashboardHealthHint.textContent = "All tasks are completed.";
  setStatus(dashboardHealth, "good");
}

function updateHeroFocus() {
  const focusTask = getFocusTask();

  if (!focusTask) {
    heroFocusTitle.textContent = "No tasks yet";
    heroFocusText.textContent = "Add a task to start organising your day.";
    return;
  }

  heroFocusTitle.textContent = focusTask.title;
  heroFocusText.textContent = `${focusTask.priority} priority • ${focusTask.status} • ${formatDate(focusTask.dueDate)}`;
}

function getPriorityClass(priority) {
  if (priority === "High") return "priority-high";
  if (priority === "Medium") return "priority-medium";
  return "priority-low";
}

function renderTasks() {
  const filteredTasks = getFilteredTasks();

  if (filteredTasks.length === 0) {
    taskList.innerHTML = `<p class="empty-state">No matching tasks found.</p>`;
    return;
  }

  taskList.innerHTML = "";

  filteredTasks.forEach((task) => {
    const card = document.createElement("article");
    card.className = "task-card";

    card.innerHTML = `
      <div class="task-top">
        <div>
          <h3>${task.title}</h3>
          <p>${task.description || "No description provided."}</p>
        </div>
      </div>

      <div class="task-badges">
        <span class="badge">${task.category}</span>
        <span class="badge ${getPriorityClass(task.priority)}">${task.priority}</span>
        <span class="badge ${task.status === "Completed" ? "status-completed" : ""}">${task.status}</span>
        <span class="badge">Due: ${formatDate(task.dueDate)}</span>
      </div>

      <div class="task-actions">
        <button class="small-btn" data-action="todo" data-id="${task.id}">To Do</button>
        <button class="small-btn" data-action="progress" data-id="${task.id}">In Progress</button>
        <button class="small-btn" data-action="complete" data-id="${task.id}">Complete</button>
        <button class="small-btn delete-btn" data-action="delete" data-id="${task.id}">Delete</button>
      </div>
    `;

    taskList.appendChild(card);
  });

  document.querySelectorAll("[data-action]").forEach((button) => {
    button.addEventListener("click", () => {
      const taskId = Number(button.dataset.id);
      const action = button.dataset.action;

      if (action === "delete") {
        taskData.tasks = taskData.tasks.filter((task) => task.id !== taskId);
      } else {
        const task = taskData.tasks.find((item) => item.id === taskId);

        if (task) {
          if (action === "todo") task.status = "To Do";
          if (action === "progress") task.status = "In Progress";
          if (action === "complete") task.status = "Completed";
        }
      }

      saveData();
      renderApp();
    });
  });
}

function renderApp() {
  updateStats();
  updateOverview();
  updateHeroFocus();
  renderTasks();
}

addTaskBtn.addEventListener("click", () => {
  const title = taskTitleInput.value.trim();
  const description = taskDescriptionInput.value.trim();
  const category = taskCategoryInput.value;
  const priority = taskPriorityInput.value;
  const status = taskStatusInput.value;
  const dueDate = taskDueDateInput.value;

  if (!title) {
    alert("Please enter a task title.");
    return;
  }

  const newTask = {
    id: Date.now(),
    title,
    description,
    category,
    priority,
    status,
    dueDate
  };

  taskData.tasks.push(newTask);

  taskTitleInput.value = "";
  taskDescriptionInput.value = "";
  taskDueDateInput.value = "";
  taskPriorityInput.value = "Low";
  taskStatusInput.value = "To Do";

  saveData();
  renderApp();
});

searchInput.addEventListener("input", renderApp);
statusFilter.addEventListener("change", renderApp);
priorityFilter.addEventListener("change", renderApp);

clearFiltersBtn.addEventListener("click", () => {
  searchInput.value = "";
  statusFilter.value = "All";
  priorityFilter.value = "All";

  renderApp();
});

resetBtn.addEventListener("click", () => {
  const confirmed = confirm("Are you sure you want to delete all tasks?");

  if (!confirmed) return;

  taskData = {
    tasks: []
  };

  saveData();
  renderApp();
});

loadData();
renderApp();