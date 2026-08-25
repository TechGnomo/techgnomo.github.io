const STORAGE_KEY = "motorcycleMaintenanceTracker";

const bikeNameInput = document.getElementById("bikeName");
const bikeModelInput = document.getElementById("bikeModel");
const currentKmInput = document.getElementById("currentKm");
const saveBikeBtn = document.getElementById("saveBikeBtn");

const maintenanceTypeInput = document.getElementById("maintenanceType");
const maintenanceKmInput = document.getElementById("maintenanceKm");
const maintenanceDateInput = document.getElementById("maintenanceDate");
const maintenanceNotesInput = document.getElementById("maintenanceNotes");
const addMaintenanceBtn = document.getElementById("addMaintenanceBtn");

const bikeNameDisplay = document.getElementById("bikeNameDisplay");
const bikeModelDisplay = document.getElementById("bikeModelDisplay");

const summaryBike = document.getElementById("summaryBike");
const summaryKm = document.getElementById("summaryKm");
const summaryLogs = document.getElementById("summaryLogs");
const summaryPriority = document.getElementById("summaryPriority");

const oilStatus = document.getElementById("oilStatus");
const oilHint = document.getElementById("oilHint");
const chainStatus = document.getElementById("chainStatus");
const chainHint = document.getElementById("chainHint");
const tyreStatus = document.getElementById("tyreStatus");
const tyreHint = document.getElementById("tyreHint");
const regoStatus = document.getElementById("regoStatus");
const regoHint = document.getElementById("regoHint");

const maintenanceTable = document.getElementById("maintenanceTable");
const resetBtn = document.getElementById("resetBtn");

let trackerData = {
  bikeName: "",
  bikeModel: "",
  currentKm: 0,
  records: []
};

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(trackerData));
}

function loadData() {
  const savedData = localStorage.getItem(STORAGE_KEY);

  if (savedData) {
    trackerData = JSON.parse(savedData);
  }
}

function formatKm(km) {
  return `${Number(km || 0).toLocaleString("en-AU")} km`;
}

function getLatestRecord(types) {
  const matchingRecords = trackerData.records
    .filter((record) => types.includes(record.type))
    .sort((a, b) => Number(b.km) - Number(a.km));

  return matchingRecords[0];
}

function getKmSince(record) {
  if (!record) return null;
  return Number(trackerData.currentKm || 0) - Number(record.km || 0);
}

function setStatus(element, className) {
  element.classList.remove("good", "warning", "danger");
  element.classList.add(className);
}

function updateBikeProfile() {
  bikeNameInput.value = trackerData.bikeName;
  bikeModelInput.value = trackerData.bikeModel;
  currentKmInput.value = trackerData.currentKm || "";

  bikeNameDisplay.textContent = trackerData.bikeName || "No bike saved yet";
  bikeModelDisplay.textContent = trackerData.bikeModel || "Add your motorcycle details to begin.";

  summaryBike.textContent = trackerData.bikeName || "Not set";
  summaryKm.textContent = formatKm(trackerData.currentKm);
  summaryLogs.textContent = trackerData.records.length;
}

function updateMaintenanceOverview() {
  const oilRecord = getLatestRecord(["Oil Change"]);
  const chainRecord = getLatestRecord(["Chain Clean", "Chain Adjustment"]);
  const tyreRecord = getLatestRecord(["Tyre Pressure"]);
  const regoRecord = getLatestRecord(["Rego", "Insurance"]);

  const oilKm = getKmSince(oilRecord);
  const chainKm = getKmSince(chainRecord);
  const tyreKm = getKmSince(tyreRecord);

  if (oilRecord) {
    oilStatus.textContent = `${formatKm(oilKm)} ago`;
    oilHint.textContent = `Last oil change at ${formatKm(oilRecord.km)}.`;

    if (oilKm >= 6000) {
      setStatus(oilStatus, "danger");
    } else if (oilKm >= 4500) {
      setStatus(oilStatus, "warning");
    } else {
      setStatus(oilStatus, "good");
    }
  } else {
    oilStatus.textContent = "No data";
    oilHint.textContent = "Add an oil change record.";
    setStatus(oilStatus, "warning");
  }

  if (chainRecord) {
    chainStatus.textContent = `${formatKm(chainKm)} ago`;
    chainHint.textContent = `Last chain record at ${formatKm(chainRecord.km)}.`;

    if (chainKm >= 1000) {
      setStatus(chainStatus, "danger");
    } else if (chainKm >= 600) {
      setStatus(chainStatus, "warning");
    } else {
      setStatus(chainStatus, "good");
    }
  } else {
    chainStatus.textContent = "No data";
    chainHint.textContent = "Add chain clean or adjustment.";
    setStatus(chainStatus, "warning");
  }

  if (tyreRecord) {
    tyreStatus.textContent = `${formatKm(tyreKm)} ago`;
    tyreHint.textContent = `Last tyre pressure check at ${formatKm(tyreRecord.km)}.`;

    if (tyreKm >= 1000) {
      setStatus(tyreStatus, "danger");
    } else if (tyreKm >= 500) {
      setStatus(tyreStatus, "warning");
    } else {
      setStatus(tyreStatus, "good");
    }
  } else {
    tyreStatus.textContent = "No data";
    tyreHint.textContent = "Add tyre pressure record.";
    setStatus(tyreStatus, "warning");
  }

  if (regoRecord) {
    regoStatus.textContent = regoRecord.type;
    regoHint.textContent = `Last ${regoRecord.type.toLowerCase()} record saved on ${regoRecord.date || "unknown date"}.`;
    setStatus(regoStatus, "good");
  } else {
    regoStatus.textContent = "No data";
    regoHint.textContent = "Add rego or insurance record.";
    setStatus(regoStatus, "warning");
  }

  if (!trackerData.bikeName) {
    summaryPriority.textContent = "Set bike first";
    return;
  }

  if (!oilRecord) {
    summaryPriority.textContent = "Add oil data";
    return;
  }

  if (oilKm >= 6000) {
    summaryPriority.textContent = "Oil service due";
    return;
  }

  if (!chainRecord || chainKm >= 1000) {
    summaryPriority.textContent = "Chain care due";
    return;
  }

  if (!tyreRecord || tyreKm >= 1000) {
    summaryPriority.textContent = "Check tyres";
    return;
  }

  summaryPriority.textContent = "Looks good";
}

function renderMaintenanceTable() {
  if (trackerData.records.length === 0) {
    maintenanceTable.innerHTML = `
      <tr>
        <td colspan="5" class="empty-row">No maintenance records yet.</td>
      </tr>
    `;
    return;
  }

  maintenanceTable.innerHTML = "";

  const sortedRecords = [...trackerData.records].sort((a, b) => Number(b.km) - Number(a.km));

  sortedRecords.forEach((record) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${record.type}</td>
      <td>${formatKm(record.km)}</td>
      <td>${record.date || "Not set"}</td>
      <td>${record.notes || "No notes"}</td>
      <td>
        <button class="delete-btn" data-id="${record.id}">Delete</button>
      </td>
    `;

    maintenanceTable.appendChild(row);
  });

  const deleteButtons = document.querySelectorAll(".delete-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const recordId = Number(button.dataset.id);

      trackerData.records = trackerData.records.filter((record) => record.id !== recordId);

      saveData();
      renderApp();
    });
  });
}

function renderApp() {
  updateBikeProfile();
  updateMaintenanceOverview();
  renderMaintenanceTable();
}

saveBikeBtn.addEventListener("click", () => {
  const bikeName = bikeNameInput.value.trim();
  const bikeModel = bikeModelInput.value.trim();
  const currentKm = Number(currentKmInput.value);

  if (!bikeName) {
    alert("Please enter a bike name.");
    return;
  }

  if (!bikeModel) {
    alert("Please enter a bike model.");
    return;
  }

  if (!currentKm || currentKm < 0) {
    alert("Please enter valid kilometres.");
    return;
  }

  trackerData.bikeName = bikeName;
  trackerData.bikeModel = bikeModel;
  trackerData.currentKm = currentKm;

  saveData();
  renderApp();
});

addMaintenanceBtn.addEventListener("click", () => {
  const type = maintenanceTypeInput.value;
  const km = Number(maintenanceKmInput.value);
  const date = maintenanceDateInput.value;
  const notes = maintenanceNotesInput.value.trim();

  if (!trackerData.bikeName) {
    alert("Please save a bike profile first.");
    return;
  }

  if (!km || km < 0) {
    alert("Please enter valid kilometres.");
    return;
  }

  const newRecord = {
    id: Date.now(),
    type,
    km,
    date,
    notes
  };

  trackerData.records.push(newRecord);

  maintenanceKmInput.value = "";
  maintenanceDateInput.value = "";
  maintenanceNotesInput.value = "";

  saveData();
  renderApp();
});

resetBtn.addEventListener("click", () => {
  const confirmed = confirm("Are you sure you want to delete all motorcycle data?");

  if (!confirmed) return;

  trackerData = {
    bikeName: "",
    bikeModel: "",
    currentKm: 0,
    records: []
  };

  saveData();
  renderApp();
});

loadData();
renderApp();