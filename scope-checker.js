const scopeForm = document.getElementById("scopeForm");
const scopeEmpty = document.getElementById("scopeEmpty");
const scopeContent = document.getElementById("scopeContent");
const resultState = document.getElementById("resultState");
const scopeScore = document.getElementById("scopeScore");
const resultTitle = document.getElementById("result-title");
const coreAssumption = document.getElementById("coreAssumption");
const keepFeatures = document.getElementById("keepFeatures");
const laterFeatures = document.getElementById("laterFeatures");
const riskFlags = document.getElementById("riskFlags");
const nextTest = document.getElementById("nextTest");
const copyBrief = document.getElementById("copyBrief");
const emailBrief = document.getElementById("emailBrief");
const scopeStatus = document.getElementById("scopeStatus");

let currentBrief = "";

const testRecommendations = {
  interviews: "Interview five people who match the target user. Ask them to describe the last time the problem occurred, what they did, what it cost and what they have already tried. Do not pitch the solution until the end.",
  prototype: "Build a clickable prototype of only the core workflow. Give it to five target users with a realistic task and observe where they hesitate, fail or ask for clarification.",
  manual: "Deliver the promised outcome manually for three target users before automating it. Record every step, delay and exception; those observations should determine the real product workflow.",
  waitlist: "Publish one focused landing page explaining the user, problem and promised outcome. Send relevant people to it directly and measure qualified replies or sign-ups—not raw visits.",
  unsure: "Start with five problem interviews. Evidence about frequency, current alternatives and urgency will tell you whether the next test should be a prototype, manual service or landing page.",
};

function uniqueLines(value) {
  return [...new Set(
    String(value)
      .split(/\n|,/)
      .map((item) => item.trim())
      .filter(Boolean),
  )].slice(0, 20);
}

function fillList(element, items, emptyMessage) {
  element.replaceChildren();
  const values = items.length ? items : [emptyMessage];

  values.forEach((value) => {
    const item = document.createElement("li");
    item.textContent = value;
    element.appendChild(item);
  });
}

function calculateScore({ features, complexity, validationMethod, problem, outcome }) {
  let score = 94;
  score -= Math.max(features.length - 3, 0) * 7;
  score -= complexity.length * 5;
  score -= validationMethod === "unsure" ? 8 : 0;
  score -= problem.length < 45 ? 6 : 0;
  score -= outcome.length < 24 ? 5 : 0;
  return Math.max(25, Math.min(95, score));
}

function scoreLabel(score) {
  if (score >= 76) {
    return "Focused enough to test";
  }

  if (score >= 53) {
    return "Promising, but still broad";
  }

  return "Scope is carrying too much risk";
}

function buildBrief(data) {
  const coreFeatures = data.features.slice(0, 3);
  const later = data.features.slice(3);
  const risks = data.complexity.length
    ? data.complexity.map((item) => `${item}: confirm that the first test cannot work without it.`)
    : ["No major technical complexity selected. Keep the first test deliberately lightweight."];
  const cleanProblem = data.problem.replace(/[.!?]+$/, "");
  const problemClause = `${cleanProblem.charAt(0).toLowerCase()}${cleanProblem.slice(1)}`;
  const assumption = `For ${data.targetUser}, can ${data.productName} help them ${data.outcome.toLowerCase()} when ${problemClause}?`;
  const recommendation = testRecommendations[data.validationMethod] || testRecommendations.unsure;
  const score = calculateScore(data);

  return {
    score,
    title: scoreLabel(score),
    assumption,
    coreFeatures,
    later,
    risks,
    recommendation,
    text: [
      `MVP BRIEF — ${data.productName}`,
      "",
      `FIRST USER\n${data.targetUser}`,
      "",
      `PROBLEM\n${data.problem}`,
      "",
      `OUTCOME\n${data.outcome}`,
      "",
      `CORE ASSUMPTION\n${assumption}`,
      "",
      "KEEP IN THE FIRST TEST",
      ...coreFeatures.map((item, index) => `${index + 1}. ${item}`),
      "",
      "MOVE TO LATER",
      ...(later.length ? later.map((item) => `- ${item}`) : ["- No additional features listed"]),
      "",
      "COMPLEXITY TO PROVE NECESSARY",
      ...risks.map((item) => `- ${item}`),
      "",
      `NEXT TEST\n${recommendation}`,
      "",
      `SCOPE SIGNAL\n${score}/100 — ${scoreLabel(score)}`,
      "",
      "Generated locally with the free TechGnomo MVP Scope Checker.",
    ].join("\n"),
  };
}

scopeForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!scopeForm.reportValidity()) {
    return;
  }

  const formData = new FormData(scopeForm);
  const data = {
    productName: String(formData.get("productName") || "").trim(),
    targetUser: String(formData.get("targetUser") || "").trim(),
    problem: String(formData.get("problem") || "").trim(),
    outcome: String(formData.get("outcome") || "").trim(),
    features: uniqueLines(formData.get("features")),
    complexity: formData.getAll("complexity").map(String),
    validationMethod: String(formData.get("validationMethod") || "unsure"),
  };

  if (!data.features.length) {
    scopeStatus.textContent = "Add at least one proposed feature.";
    return;
  }

  const brief = buildBrief(data);
  currentBrief = brief.text;

  scopeScore.textContent = String(brief.score);
  resultTitle.textContent = brief.title;
  coreAssumption.textContent = brief.assumption;
  fillList(keepFeatures, brief.coreFeatures, "Define the single action that produces the promised outcome.");
  fillList(laterFeatures, brief.later, "No additional features listed. Protect this small scope.");
  fillList(riskFlags, brief.risks, "No major complexity selected.");
  nextTest.textContent = brief.recommendation;
  scopeEmpty.hidden = true;
  scopeContent.hidden = false;
  resultState.textContent = "READY";
  scopeStatus.textContent = "Brief generated locally. Nothing was uploaded.";

  window.techGnomoTrack?.("scope_result_generated", {
    scope_signal: brief.score,
    feature_count: data.features.length,
    complexity_count: data.complexity.length,
  });

  if (window.innerWidth < 992) {
    scopeContent.scrollIntoView({ behavior: "smooth", block: "start" });
  }
});

copyBrief?.addEventListener("click", async () => {
  if (!currentBrief) {
    return;
  }

  try {
    await navigator.clipboard.writeText(currentBrief);
    scopeStatus.textContent = "Brief copied to your clipboard.";
  } catch {
    const helper = document.createElement("textarea");
    helper.value = currentBrief;
    helper.setAttribute("readonly", "");
    helper.style.position = "fixed";
    helper.style.opacity = "0";
    document.body.appendChild(helper);
    helper.select();
    document.execCommand("copy");
    helper.remove();
    scopeStatus.textContent = "Brief copied to your clipboard.";
  }
});

emailBrief?.addEventListener("click", () => {
  if (!currentBrief) {
    return;
  }

  const productLine = currentBrief.split("\n")[0].replace("MVP BRIEF — ", "");
  const subject = `[MVP scope review] ${productLine}`;
  window.location.href = `mailto:gnomocode@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(currentBrief)}`;
});
