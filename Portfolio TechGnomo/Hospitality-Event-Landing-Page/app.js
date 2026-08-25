const events = {
  alps: {
    title: "Tuesday & Wednesday — French Alps",
    shortTitle: "French Alps",
    heroText: "Three-course set menu inspired by the comfort of alpine French dining.",
    price: "$59 per person",
    detailTitle: "French Alps",
    description:
      "A three-course set menu designed to bring warm, rustic French alpine dining to the middle of the week.",
    packageName: "French Alps Set Menu",
    packagePrice: "$59 pp",
    packageNote: "Ideal for guests looking for a complete midweek dining experience.",
    features: [
      "Three-course set menu",
      "French-inspired comfort dishes",
      "Available Tuesday and Wednesday"
    ]
  },
  wine: {
    title: "Thursday — Wine Affair",
    shortTitle: "Wine Affair",
    heroText: "Order any main and add just $8 to enjoy a selected wine pairing.",
    price: "$8 add-on",
    detailTitle: "Wine Affair",
    description:
      "A midweek indulgence for wine lovers, designed to increase guest spend and create a more memorable dining experience.",
    packageName: "Main + Selected Wine Pairing",
    packagePrice: "$8 add-on",
    packageNote: "A simple upsell offer that adds value to any main course.",
    features: [
      "Available every Thursday",
      "Selected wine matched to the dish",
      "Designed as a low-barrier wine pairing experience"
    ]
  },
  fromage: {
    title: "Friday & Sunday — The Fromage Experience",
    shortTitle: "The Fromage Experience",
    heroText: "French cheese, wine and bistro dining in one complete experience.",
    price: "From $59 per person",
    detailTitle: "The Fromage Experience",
    description:
      "A celebration of French cheese, wine and classic bistro dining, ideal for weekend guests and premium table experiences.",
    packageName: "Cheese Platter + Main",
    packagePrice: "$59 / $69 pp",
    packageNote: "Add wine pairing for the full experience.",
    features: [
      "Cheese platter and choice of main",
      "Wine pairing option available",
      "Available Friday and Sunday"
    ]
  }
};

const eventCards = document.querySelectorAll(".event-card");

const featuredEventTitle = document.getElementById("featuredEventTitle");
const featuredEventText = document.getElementById("featuredEventText");
const featuredEventPrice = document.getElementById("featuredEventPrice");

const eventDetailTitle = document.getElementById("eventDetailTitle");
const eventDetailDescription = document.getElementById("eventDetailDescription");
const eventDetailList = document.getElementById("eventDetailList");

const eventPackageName = document.getElementById("eventPackageName");
const eventPackagePrice = document.getElementById("eventPackagePrice");
const eventPackageNote = document.getElementById("eventPackageNote");

const bookingForm = document.getElementById("bookingForm");
const guestName = document.getElementById("guestName");
const guestEmail = document.getElementById("guestEmail");
const eventSelect = document.getElementById("eventSelect");
const guestCount = document.getElementById("guestCount");
const formMessage = document.getElementById("formMessage");

function renderEvent(eventKey) {
  const selectedEvent = events[eventKey];

  featuredEventTitle.textContent = selectedEvent.title;
  featuredEventText.textContent = selectedEvent.heroText;
  featuredEventPrice.textContent = selectedEvent.price;

  eventDetailTitle.textContent = selectedEvent.detailTitle;
  eventDetailDescription.textContent = selectedEvent.description;

  eventPackageName.textContent = selectedEvent.packageName;
  eventPackagePrice.textContent = selectedEvent.packagePrice;
  eventPackageNote.textContent = selectedEvent.packageNote;

  eventDetailList.innerHTML = "";

  selectedEvent.features.forEach((feature) => {
    const item = document.createElement("li");
    item.textContent = feature;
    eventDetailList.appendChild(item);
  });

  eventCards.forEach((card) => {
    card.classList.toggle("active", card.dataset.event === eventKey);
  });
}

eventCards.forEach((card) => {
  card.addEventListener("click", () => {
    renderEvent(card.dataset.event);
  });
});

bookingForm.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!guestName.value.trim()) {
    formMessage.textContent = "Please enter your name.";
    return;
  }

  if (!guestEmail.value.trim()) {
    formMessage.textContent = "Please enter your email.";
    return;
  }

  if (!eventSelect.value) {
    formMessage.textContent = "Please select an event.";
    return;
  }

  if (!guestCount.value || Number(guestCount.value) <= 0) {
    formMessage.textContent = "Please enter the number of guests.";
    return;
  }

  formMessage.textContent = `Thanks ${guestName.value.trim()} — your enquiry for ${eventSelect.value} has been prepared.`;

  bookingForm.reset();
});

renderEvent("wine");