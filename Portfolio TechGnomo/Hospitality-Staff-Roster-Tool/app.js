const STORAGE_KEY = "hospitalityStaffRosterTool";

const weekNameInput = document.getElementById("weekName");
const labourBudgetInput = document.getElementById("labourBudget");
const saveWeekBtn = document.getElementById("saveWeekBtn");

const staffNameInput = document.getElementById("staffName");
const staffRoleInput = document.getElementById("staffRole");
const hourlyRateInput = document.getElementById("hourlyRate");
const addStaffBtn = document.getElementById("addStaffBtn");

const shiftStaffInput = document.getElementById("shiftStaff");
const shiftDayInput = document.getElementById("shiftDay");
const shiftAreaInput = document.getElementById("shiftArea");
const startTimeInput = document.getElementById("startTime");
const endTimeInput = document.getElementById("endTime");
const addShiftBtn = document.getElementById("addShiftBtn");

const heroWeekDisplay = document.getElementById("heroWeekDisplay");
const heroSummaryDisplay = document.getElementById("heroSummaryDisplay");

const staffCount = document.getElementById("staffCount");
const shiftCount = document.getElementById("shiftCount");
const totalHours = document.getElementById("totalHours");
const labourCost = document.getElementById("labourCost");

const budgetStatus = document.getElementById("budgetStatus");
const budgetHint = document.getElementById("budgetHint");
const averageShift = document.getElementById("averageShift");
const busiestDay = document.getElementById("busiestDay");
const rosterHealth = document.getElementById("rosterHealth");
const rosterHealthHint = document.getElementById("rosterHealthHint");

const staffTable = document.getElementById("staffTable");
const shiftTable = document.getElementById("shiftTable");
const resetBtn = document.getElementById("resetBtn");

let rosterData = {
  weekName: "",
  labourBudget: 0,
  staff: [],
  shifts: []
};

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(rosterData));
}

function loadData() {
  const savedData = localStorage.getItem(STORAGE_KEY);

  if (savedData) {
    rosterData = JSON.parse(savedData);
  }
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD"
  }).format(Number(amount || 0));
}

function formatHours(hours) {
  return `${Number(hours || 0).toFixed(1)}h`;
}

function timeToMinutes(time) {
  const [hours, minutes] = time.split(":").map(Number);
  return hours * 60 + minutes;
}

function calculateShiftHours(start, end) {
  const startMinutes = timeToMinutes(start);
  let endMinutes = timeToMinutes(end);

  if (endMinutes <= startMinutes) {
    endMinutes += 24 * 60;
  }

  return (endMinutes - startMinutes) / 60;
}

function getStaffById(staffId) {
  return rosterData.staff.find((staffMember) => staffMember.id === Number(staffId));
}

function getStaffHours(staffId) {
  return rosterData.shifts
    .filter((shift) => shift.staffId === Number(staffId))
    .reduce((total, shift) => total + Number(shift.hours), 0);
}

function getStaffCost(staffId) {
  const staffMember = getStaffById(staffId);

  if (!staffMember) return 0;

  return getStaffHours(staffId) * Number(staffMember.hourlyRate);
}

function calculateTotals() {
  const totalRosterHours = rosterData.shifts.reduce((total, shift) => {
    return total + Number(shift.hours);
  }, 0);

  const totalRosterCost = rosterData.shifts.reduce((total, shift) => {
    const staffMember = getStaffById(shift.staffId);

    if (!staffMember) return total;

    return total + Number(shift.hours) * Number(staffMember.hourlyRate);
  }, 0);

  return {
    totalRosterHours,
    totalRosterCost
  };
}

function setStatus(element, className) {
  element.classList.remove("good", "warning", "danger");
  element.classList.add(className);
}

function updateHero() {
  const totals = calculateTotals();

  weekNameInput.value = rosterData.weekName;
  labourBudgetInput.value = rosterData.labourBudget || "";

  heroWeekDisplay.textContent = rosterData.weekName || "No week selected";

  if (!rosterData.weekName) {
    heroSummaryDisplay.textContent = "Set up your roster week to begin.";
    return;
  }

  heroSummaryDisplay.textContent = `${rosterData.staff.length} staff, ${rosterData.shifts.length} shifts, ${formatHours(totals.totalRosterHours)} rostered.`;
}

function updateStats() {
  const totals = calculateTotals();

  staffCount.textContent = rosterData.staff.length;
  shiftCount.textContent = rosterData.shifts.length;
  totalHours.textContent = formatHours(totals.totalRosterHours);
  labourCost.textContent = formatCurrency(totals.totalRosterCost);
}

function updateOverview() {
  const totals = calculateTotals();

  if (rosterData.labourBudget > 0) {
    const difference = Number(rosterData.labourBudget) - totals.totalRosterCost;

    if (difference >= 0) {
      budgetStatus.textContent = `${formatCurrency(difference)} under`;
      budgetHint.textContent = `Budget: ${formatCurrency(rosterData.labourBudget)}.`;
      setStatus(budgetStatus, "good");
    } else {
      budgetStatus.textContent = `${formatCurrency(Math.abs(difference))} over`;
      budgetHint.textContent = `Budget: ${formatCurrency(rosterData.labourBudget)}.`;
      setStatus(budgetStatus, "danger");
    }
  } else {
    budgetStatus.textContent = "No budget";
    budgetHint.textContent = "Set a labour budget to track cost.";
    setStatus(budgetStatus, "warning");
  }

  if (rosterData.shifts.length > 0) {
    averageShift.textContent = formatHours(totals.totalRosterHours / rosterData.shifts.length);
    setStatus(averageShift, "good");
  } else {
    averageShift.textContent = "0h";
    setStatus(averageShift, "warning");
  }

  const dayTotals = {};

  rosterData.shifts.forEach((shift) => {
    dayTotals[shift.day] = (dayTotals[shift.day] || 0) + Number(shift.hours);
  });

  const busiestDayEntry = Object.entries(dayTotals).sort((a, b) => b[1] - a[1])[0];

  if (busiestDayEntry) {
    busiestDay.textContent = `${busiestDayEntry[0]} — ${formatHours(busiestDayEntry[1])}`;
    setStatus(busiestDay, "good");
  } else {
    busiestDay.textContent = "No shifts";
    setStatus(busiestDay, "warning");
  }

  if (rosterData.staff.length === 0) {
    rosterHealth.textContent = "Add staff";
    rosterHealthHint.textContent = "Start by adding team members.";
    setStatus(rosterHealth, "warning");
    return;
  }

  if (rosterData.shifts.length === 0) {
    rosterHealth.textContent = "Add shifts";
    rosterHealthHint.textContent = "Staff added, but no shifts rostered yet.";
    setStatus(rosterHealth, "warning");
    return;
  }

  if (rosterData.labourBudget > 0 && totals.totalRosterCost > rosterData.labourBudget) {
    rosterHealth.textContent = "Over budget";
    rosterHealthHint.textContent = "Roster cost is higher than the labour budget.";
    setStatus(rosterHealth, "danger");
    return;
  }

  rosterHealth.textContent = "Looks good";
  rosterHealthHint.textContent = "Roster has staff, shifts and is within budget if a budget is set.";
  setStatus(rosterHealth, "good");
}

function renderStaffOptions() {
  if (rosterData.staff.length === 0) {
    shiftStaffInput.innerHTML = `<option value="">Add staff first</option>`;
    return;
  }

  shiftStaffInput.innerHTML = `<option value="">Select staff member</option>`;

  rosterData.staff.forEach((staffMember) => {
    const option = document.createElement("option");
    option.value = staffMember.id;
    option.textContent = `${staffMember.name} — ${staffMember.role}`;
    shiftStaffInput.appendChild(option);
  });
}

function renderStaffTable() {
  if (rosterData.staff.length === 0) {
    staffTable.innerHTML = `
      <tr>
        <td colspan="6" class="empty-row">No staff added yet.</td>
      </tr>
    `;
    return;
  }

  staffTable.innerHTML = "";

  rosterData.staff.forEach((staffMember) => {
    const hours = getStaffHours(staffMember.id);
    const cost = getStaffCost(staffMember.id);

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${staffMember.name}</td>
      <td>${staffMember.role}</td>
      <td>${formatCurrency(staffMember.hourlyRate)}</td>
      <td>${formatHours(hours)}</td>
      <td>${formatCurrency(cost)}</td>
      <td>
        <button class="delete-btn" data-staff-id="${staffMember.id}">Delete</button>
      </td>
    `;

    staffTable.appendChild(row);
  });

  document.querySelectorAll("[data-staff-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const staffId = Number(button.dataset.staffId);

      rosterData.staff = rosterData.staff.filter((staffMember) => staffMember.id !== staffId);
      rosterData.shifts = rosterData.shifts.filter((shift) => shift.staffId !== staffId);

      saveData();
      renderApp();
    });
  });
}

function renderShiftTable() {
  if (rosterData.shifts.length === 0) {
    shiftTable.innerHTML = `
      <tr>
        <td colspan="7" class="empty-row">No shifts added yet.</td>
      </tr>
    `;
    return;
  }

  shiftTable.innerHTML = "";

  const dayOrder = {
    Monday: 1,
    Tuesday: 2,
    Wednesday: 3,
    Thursday: 4,
    Friday: 5,
    Saturday: 6,
    Sunday: 7
  };

  const sortedShifts = [...rosterData.shifts].sort((a, b) => {
    return dayOrder[a.day] - dayOrder[b.day];
  });

  sortedShifts.forEach((shift) => {
    const staffMember = getStaffById(shift.staffId);
    const cost = staffMember ? shift.hours * staffMember.hourlyRate : 0;

    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${shift.day}</td>
      <td>${staffMember ? staffMember.name : "Deleted staff"}</td>
      <td>${shift.area}</td>
      <td>${shift.startTime} → ${shift.endTime}</td>
      <td>${formatHours(shift.hours)}</td>
      <td>${formatCurrency(cost)}</td>
      <td>
        <button class="delete-btn" data-shift-id="${shift.id}">Delete</button>
      </td>
    `;

    shiftTable.appendChild(row);
  });

  document.querySelectorAll("[data-shift-id]").forEach((button) => {
    button.addEventListener("click", () => {
      const shiftId = Number(button.dataset.shiftId);

      rosterData.shifts = rosterData.shifts.filter((shift) => shift.id !== shiftId);

      saveData();
      renderApp();
    });
  });
}

function renderApp() {
  updateHero();
  updateStats();
  updateOverview();
  renderStaffOptions();
  renderStaffTable();
  renderShiftTable();
}

saveWeekBtn.addEventListener("click", () => {
  const weekName = weekNameInput.value.trim();
  const labourBudget = Number(labourBudgetInput.value);

  if (!weekName) {
    alert("Please enter a week name.");
    return;
  }

  rosterData.weekName = weekName;
  rosterData.labourBudget = labourBudget || 0;

  saveData();
  renderApp();
});

addStaffBtn.addEventListener("click", () => {
  const name = staffNameInput.value.trim();
  const role = staffRoleInput.value;
  const hourlyRate = Number(hourlyRateInput.value);

  if (!name) {
    alert("Please enter the staff member name.");
    return;
  }

  if (!hourlyRate || hourlyRate <= 0) {
    alert("Please enter a valid hourly rate.");
    return;
  }

  const newStaffMember = {
    id: Date.now(),
    name,
    role,
    hourlyRate
  };

  rosterData.staff.push(newStaffMember);

  staffNameInput.value = "";
  hourlyRateInput.value = "";

  saveData();
  renderApp();
});

addShiftBtn.addEventListener("click", () => {
  const staffId = Number(shiftStaffInput.value);
  const day = shiftDayInput.value;
  const area = shiftAreaInput.value;
  const startTime = startTimeInput.value;
  const endTime = endTimeInput.value;

  if (!staffId) {
    alert("Please select a staff member.");
    return;
  }

  if (!startTime || !endTime) {
    alert("Please enter start and finish time.");
    return;
  }

  const hours = calculateShiftHours(startTime, endTime);

  if (hours <= 0) {
    alert("Shift hours must be greater than zero.");
    return;
  }

  const newShift = {
    id: Date.now(),
    staffId,
    day,
    area,
    startTime,
    endTime,
    hours
  };

  rosterData.shifts.push(newShift);

  startTimeInput.value = "";
  endTimeInput.value = "";

  saveData();
  renderApp();
});

resetBtn.addEventListener("click", () => {
  const confirmed = confirm("Are you sure you want to delete the full roster?");

  if (!confirmed) return;

  rosterData = {
    weekName: "",
    labourBudget: 0,
    staff: [],
    shifts: []
  };

  saveData();
  renderApp();
});

loadData();
renderApp();