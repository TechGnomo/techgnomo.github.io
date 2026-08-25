const dishes = [
  {
    id: "crevettes",
    name: "Crevettes à l'Ail et Piment",
    category: "Entrée",
    description: "Garlic and chilli prawns with creamy bisque and root vegetable chips.",
    wine: "Pecorino from Langhorne Creek",
    wineType: "White Wine",
    wineDescription: "Fresh, textured and lightly aromatic white wine with enough acidity to balance chilli, garlic and bisque richness.",
    body: "Medium",
    acidity: "High",
    richness: "Medium",
    intensity: "High",
    matchScore: "94%",
    servingTemp: "8–10°C",
    glassware: "White wine glass",
    pairingStyle: "Contrast",
    serviceNote: "Serve chilled",
    reason: "The prawns, garlic and chilli need a wine with freshness and lift. Pecorino works well because its acidity cuts through the creamy bisque while its texture stands up to the intensity of the dish."
  },
  {
    id: "encornet",
    name: "Encornet d'Automne",
    category: "Entrée",
    description: "Sous-vide calamari salad on chickpea purée with crispy tentacles and sweet potato chips.",
    wine: "Côtes du Rhône Réserve Blanc",
    wineType: "White Wine",
    wineDescription: "Rounded southern French white with enough body for chickpea purée and enough freshness for seafood.",
    body: "Medium",
    acidity: "Medium",
    richness: "Medium",
    intensity: "Medium",
    matchScore: "91%",
    servingTemp: "9–11°C",
    glassware: "White wine glass",
    pairingStyle: "Complement",
    serviceNote: "Do not over-chill",
    reason: "The calamari needs freshness, while the chickpea purée and sweet potato bring roundness. A Côtes du Rhône Blanc complements the soft texture and savoury profile without overpowering the seafood."
  },
  {
    id: "blanquette",
    name: "Blanquette de Poulet",
    category: "Main",
    description: "Truffle-infused chicken breast with seasonal vegetables in creamy sauce.",
    wine: "Château Fontoy",
    wineType: "White Wine",
    wineDescription: "Elegant, balanced white wine that supports creamy sauce and truffle without overpowering the chicken.",
    body: "Medium",
    acidity: "Medium",
    richness: "High",
    intensity: "Medium",
    matchScore: "92%",
    servingTemp: "10–12°C",
    glassware: "Universal wine glass",
    pairingStyle: "Complement",
    serviceNote: "Slightly warmer than fridge temperature",
    reason: "The creamy sauce and truffle need a wine with texture and elegance. Château Fontoy works because it supports the richness while keeping the dish balanced and refined."
  },
  {
    id: "pot-au-feu",
    name: "Pot-au-Feu",
    category: "Main",
    description: "Slow-cooked beef cheek with parsnip risotto and jus.",
    wine: "Frescobaldi Remole",
    wineType: "Red Wine",
    wineDescription: "Medium-bodied Italian red with soft tannins and savoury fruit, ideal for slow-cooked beef.",
    body: "Medium",
    acidity: "Medium",
    richness: "High",
    intensity: "High",
    matchScore: "95%",
    servingTemp: "16–18°C",
    glassware: "Red wine glass",
    pairingStyle: "Complement",
    serviceNote: "Let breathe briefly",
    reason: "Slow-cooked beef cheek needs a red wine with enough structure but not excessive tannin. Frescobaldi Remole complements the jus and parsnip risotto while keeping the pairing smooth."
  },
  {
    id: "fromage",
    name: "French Cheese Platter",
    category: "Cheese",
    description: "Selection of French cheeses served with accompaniments.",
    wine: "Selected Wine Pairing",
    wineType: "White or Red",
    wineDescription: "A flexible pairing depending on the cheese selection, balancing creaminess, salt and intensity.",
    body: "Variable",
    acidity: "Medium–High",
    richness: "High",
    intensity: "Medium–High",
    matchScore: "90%",
    servingTemp: "Depends on wine",
    glassware: "Universal wine glass",
    pairingStyle: "Balance",
    serviceNote: "Match to strongest cheese",
    reason: "Cheese pairing depends on salt, fat and intensity. A good pairing needs enough acidity to refresh the palate and enough flavour to handle stronger cheeses."
  }
];

const dishSelect = document.getElementById("dishSelect");
const pairingBtn = document.getElementById("pairingBtn");

const heroDishDisplay = document.getElementById("heroDishDisplay");
const heroWineDisplay = document.getElementById("heroWineDisplay");

const dishCount = document.getElementById("dishCount");
const wineCount = document.getElementById("wineCount");
const matchScore = document.getElementById("matchScore");
const selectedCategory = document.getElementById("selectedCategory");

const dishCategory = document.getElementById("dishCategory");
const dishName = document.getElementById("dishName");
const dishDescription = document.getElementById("dishDescription");

const dishBody = document.getElementById("dishBody");
const dishAcidity = document.getElementById("dishAcidity");
const dishRichness = document.getElementById("dishRichness");
const dishIntensity = document.getElementById("dishIntensity");

const wineType = document.getElementById("wineType");
const wineName = document.getElementById("wineName");
const wineDescription = document.getElementById("wineDescription");

const servingTemp = document.getElementById("servingTemp");
const glassware = document.getElementById("glassware");
const pairingStyle = document.getElementById("pairingStyle");
const serviceNote = document.getElementById("serviceNote");

const pairingReason = document.getElementById("pairingReason");
const pairingTable = document.getElementById("pairingTable");

function populateDishSelect() {
  dishes.forEach((dish) => {
    const option = document.createElement("option");
    option.value = dish.id;
    option.textContent = dish.name;
    dishSelect.appendChild(option);
  });
}

function renderTable() {
  pairingTable.innerHTML = "";

  dishes.forEach((dish) => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${dish.name}</td>
      <td>${dish.category}</td>
      <td>${dish.wine}</td>
      <td>${dish.pairingStyle}</td>
    `;

    pairingTable.appendChild(row);
  });
}

function updateStats(selectedDish = null) {
  dishCount.textContent = dishes.length;
  wineCount.textContent = new Set(dishes.map((dish) => dish.wine)).size;

  if (selectedDish) {
    matchScore.textContent = selectedDish.matchScore;
    selectedCategory.textContent = selectedDish.category;
  } else {
    matchScore.textContent = "--";
    selectedCategory.textContent = "None";
  }
}

function renderPairing(dish) {
  heroDishDisplay.textContent = dish.name;
  heroWineDisplay.textContent = dish.wine;

  dishCategory.textContent = dish.category;
  dishName.textContent = dish.name;
  dishDescription.textContent = dish.description;

  dishBody.textContent = dish.body;
  dishAcidity.textContent = dish.acidity;
  dishRichness.textContent = dish.richness;
  dishIntensity.textContent = dish.intensity;

  wineType.textContent = dish.wineType;
  wineName.textContent = dish.wine;
  wineDescription.textContent = dish.wineDescription;

  servingTemp.textContent = dish.servingTemp;
  glassware.textContent = dish.glassware;
  pairingStyle.textContent = dish.pairingStyle;
  serviceNote.textContent = dish.serviceNote;

  pairingReason.textContent = dish.reason;

  updateStats(dish);
}

pairingBtn.addEventListener("click", () => {
  const selectedDishId = dishSelect.value;

  if (!selectedDishId) {
    alert("Please select a dish first.");
    return;
  }

  const selectedDish = dishes.find((dish) => dish.id === selectedDishId);

  renderPairing(selectedDish);
});

dishSelect.addEventListener("change", () => {
  const selectedDishId = dishSelect.value;

  if (!selectedDishId) return;

  const selectedDish = dishes.find((dish) => dish.id === selectedDishId);

  renderPairing(selectedDish);
});

populateDishSelect();
renderTable();
updateStats();