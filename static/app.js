const phraseEl = document.getElementById("phrase");
const makeBtn = document.getElementById("make");
const copyBtn = document.getElementById("copy");
const lists = {
  verbs: document.querySelector('ul[data-kind="verbs"]'),
  adjectives: document.querySelector('ul[data-kind="adjectives"]'),
  nouns: document.querySelector('ul[data-kind="nouns"]'),
};
const kindToList = { verb: "verbs", adjective: "adjectives", noun: "nouns" };

// Show which word each column contributed, so the lists read as the source.
function light(parts) {
  document.querySelectorAll(".col li.lit").forEach((li) => li.classList.remove("lit"));
  for (const [kind, listName] of Object.entries(kindToList)) {
    const match = [...lists[listName].children].find((li) => li.textContent === parts[kind]);
    if (match) match.classList.add("lit");
  }
}

let busy = false;

async function makeBullshit() {
  if (busy) return;
  busy = true;
  try {
    const res = await fetch("/api/phrase");
    if (!res.ok) throw new Error(res.status);
    const parts = await res.json();
    phraseEl.textContent = parts.phrase;
    light(parts);
  } catch (err) {
    phraseEl.textContent = "the server stopped generating bullshit — check the terminal";
  } finally {
    busy = false;
  }
}

makeBtn.addEventListener("click", (e) => {
  e.preventDefault(); // the form submit is the no-JS fallback
  makeBullshit();
});

document.addEventListener("keydown", (e) => {
  if (e.key !== "Enter" || e.metaKey || e.ctrlKey) return;
  if (e.target.closest("button, a, input, textarea")) return;
  e.preventDefault();
  makeBullshit();
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(phraseEl.textContent);
    copyBtn.textContent = "Copied";
  } catch (err) {
    copyBtn.textContent = "Copy failed";
  }
  setTimeout(() => (copyBtn.textContent = "Copy"), 1400);
});

light(phraseEl.dataset); // the phrase Flask rendered into the page
