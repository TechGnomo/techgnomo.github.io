const articles = [
  {
    id: "wifi-no-connection",
    title: "User cannot connect to Wi-Fi",
    category: "Networking",
    level: "Beginner",
    summary: "Basic troubleshooting flow for a device that cannot connect to a wireless network.",
    steps: [
      "Confirm whether the issue affects one device or multiple devices.",
      "Check that Wi-Fi is enabled on the device.",
      "Forget the network and reconnect using the correct password.",
      "Restart the device and test again.",
      "Restart the router or access point if multiple users are affected.",
      "Check IP address settings and confirm the device is receiving an address.",
      "Escalate if the access point, DHCP server or network configuration may be failing."
    ],
    escalation: "Escalate to network support if multiple users are affected, the device cannot obtain an IP address, or the access point appears offline."
  },
  {
    id: "slow-computer",
    title: "Computer is running slowly",
    category: "Hardware / Software",
    level: "Beginner",
    summary: "A simple checklist for slow workstation performance.",
    steps: [
      "Ask when the issue started and whether anything changed recently.",
      "Restart the computer if it has not been restarted recently.",
      "Check available disk space.",
      "Open Task Manager or Activity Monitor to review CPU, memory and disk usage.",
      "Close unnecessary startup applications.",
      "Check for pending system updates.",
      "Run an approved malware scan if behaviour looks suspicious."
    ],
    escalation: "Escalate if the device has hardware errors, repeated crashes, suspected malware, or performance does not improve after basic checks."
  },
  {
    id: "password-reset",
    title: "Password reset request",
    category: "Accounts",
    level: "Beginner",
    summary: "Safe process for handling a user password reset request.",
    steps: [
      "Verify the user's identity according to company policy.",
      "Confirm which account or system they cannot access.",
      "Check whether the account is locked, expired or disabled.",
      "Reset the password using the approved admin portal.",
      "Ask the user to sign in and change the temporary password if required.",
      "Remind the user not to reuse old passwords or share credentials."
    ],
    escalation: "Escalate if identity cannot be verified, the account is disabled for security reasons, or there are signs of compromise."
  },
  {
    id: "printer-not-printing",
    title: "Printer is not printing",
    category: "Peripherals",
    level: "Beginner",
    summary: "Troubleshooting flow for a local or network printer issue.",
    steps: [
      "Check if other users can print to the same printer.",
      "Confirm the printer has power, paper and no visible error message.",
      "Check the print queue and clear stuck jobs if appropriate.",
      "Restart the printer and try again.",
      "Confirm the correct printer is selected.",
      "Reinstall or reconnect the printer if only one device is affected.",
      "Check network connection if it is a shared printer."
    ],
    escalation: "Escalate if the printer has hardware faults, repeated paper jams, firmware errors or network connectivity issues."
  },
  {
    id: "email-not-syncing",
    title: "Email is not syncing",
    category: "Email",
    level: "Beginner",
    summary: "Checklist for mailbox sync problems on desktop or mobile.",
    steps: [
      "Check whether webmail works in the browser.",
      "Confirm internet connection is working.",
      "Restart the mail app.",
      "Check mailbox storage or quota.",
      "Confirm account password has not changed.",
      "Remove and re-add the account if approved by policy.",
      "Check service status if multiple users are affected."
    ],
    escalation: "Escalate if webmail is also unavailable, multiple users are affected, or the mailbox appears corrupted."
  },
  {
    id: "phishing-email",
    title: "Possible phishing email",
    category: "Security",
    level: "Intermediate",
    summary: "First response steps when a user reports a suspicious email.",
    steps: [
      "Tell the user not to click links, open attachments or reply.",
      "Ask whether they clicked anything or entered credentials.",
      "Collect sender, subject and time received.",
      "Use the approved reporting process or phishing report button.",
      "If credentials were entered, start password reset and account protection process.",
      "Check whether the email was sent to other users."
    ],
    escalation: "Escalate immediately to security if the user clicked a link, opened an attachment, entered credentials, or multiple users received the same message."
  },
  {
    id: "vpn-not-connecting",
    title: "VPN is not connecting",
    category: "Networking",
    level: "Intermediate",
    summary: "Support flow for remote users who cannot connect to VPN.",
    steps: [
      "Confirm the user's internet connection works without VPN.",
      "Check username, password and MFA prompt.",
      "Confirm the VPN client is up to date.",
      "Restart the VPN client and device.",
      "Check for error messages and record the exact wording.",
      "Test from another network if possible.",
      "Check service status or known outages."
    ],
    escalation: "Escalate if authentication is failing, MFA is not working, the VPN gateway may be down, or the client shows certificate/configuration errors."
  },
  {
    id: "new-user-setup",
    title: "New user workstation setup",
    category: "Onboarding",
    level: "Beginner",
    summary: "Basic checklist for preparing a workstation for a new starter.",
    steps: [
      "Confirm user details, role, start date and required applications.",
      "Prepare device and apply standard updates.",
      "Create or confirm required user accounts.",
      "Install approved business applications.",
      "Configure email, browser, printers and VPN if required.",
      "Test login before handover.",
      "Document asset number and assigned equipment."
    ],
    escalation: "Escalate if account provisioning fails, licensing is missing, or required access has not been approved."
  }
];

const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const clearSearchBtn = document.getElementById("clearSearchBtn");

const articleList = document.getElementById("articleList");

const heroArticleTitle = document.getElementById("heroArticleTitle");
const heroArticleCategory = document.getElementById("heroArticleCategory");

const articleCount = document.getElementById("articleCount");
const categoryCount = document.getElementById("categoryCount");
const resultCount = document.getElementById("resultCount");
const selectedLevel = document.getElementById("selectedLevel");

const articleTitle = document.getElementById("articleTitle");
const articleCategory = document.getElementById("articleCategory");
const articleLevel = document.getElementById("articleLevel");
const articleSummary = document.getElementById("articleSummary");
const articleSteps = document.getElementById("articleSteps");
const articleEscalation = document.getElementById("articleEscalation");

let selectedArticleId = null;

function getCategories() {
  return [...new Set(articles.map((article) => article.category))];
}

function populateCategories() {
  const categories = getCategories();

  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category;
    option.textContent = category;
    categoryFilter.appendChild(option);
  });
}

function filterArticles() {
  const searchTerm = searchInput.value.toLowerCase().trim();
  const selectedCategory = categoryFilter.value;

  return articles.filter((article) => {
    const matchesSearch =
      article.title.toLowerCase().includes(searchTerm) ||
      article.summary.toLowerCase().includes(searchTerm) ||
      article.category.toLowerCase().includes(searchTerm) ||
      article.steps.join(" ").toLowerCase().includes(searchTerm);

    const matchesCategory =
      selectedCategory === "All" || article.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });
}

function renderArticleList() {
  const filteredArticles = filterArticles();

  resultCount.textContent = filteredArticles.length;

  if (filteredArticles.length === 0) {
    articleList.innerHTML = `
      <p class="article-summary">No matching articles found.</p>
    `;
    return;
  }

  articleList.innerHTML = "";

  filteredArticles.forEach((article) => {
    const button = document.createElement("button");
    button.className = "article-button";

    if (article.id === selectedArticleId) {
      button.classList.add("active");
    }

    button.innerHTML = `
      <strong>${article.title}</strong>
      <p>${article.category} • ${article.level}</p>
    `;

    button.addEventListener("click", () => {
      selectedArticleId = article.id;
      renderSelectedArticle(article);
      renderArticleList();
    });

    articleList.appendChild(button);
  });
}

function renderSelectedArticle(article) {
  heroArticleTitle.textContent = article.title;
  heroArticleCategory.textContent = `${article.category} • ${article.level}`;

  selectedLevel.textContent = article.level;

  articleTitle.textContent = article.title;
  articleCategory.textContent = article.category;
  articleLevel.textContent = article.level;
  articleSummary.textContent = article.summary;
  articleEscalation.textContent = article.escalation;

  articleSteps.innerHTML = "";

  article.steps.forEach((step) => {
    const listItem = document.createElement("li");
    listItem.textContent = step;
    articleSteps.appendChild(listItem);
  });
}

function updateStats() {
  articleCount.textContent = articles.length;
  categoryCount.textContent = getCategories().length;
  resultCount.textContent = articles.length;
  selectedLevel.textContent = "None";
}

searchInput.addEventListener("input", renderArticleList);
categoryFilter.addEventListener("change", renderArticleList);

clearSearchBtn.addEventListener("click", () => {
  searchInput.value = "";
  categoryFilter.value = "All";
  selectedArticleId = null;
  renderArticleList();
});

populateCategories();
updateStats();
renderArticleList();