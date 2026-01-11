const API_URL = "http://localhost:8000/search";

const queryInput = document.getElementById("query");
const resultsDiv = document.getElementById("results");
const statusDiv = document.getElementById("status");

queryInput.addEventListener("keydown", e => {
  if (e.key === "Enter") search();
});

async function search() {
  const query = queryInput.value.trim();
  if (!query) return;

  resultsDiv.innerHTML = "";
  statusDiv.textContent = "Searching…";

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    if (!res.ok) {
      throw new Error("Search failed");
    }

    const data = await res.json();
    renderResults(data);
    statusDiv.textContent = `${data.length} result(s) found`;
  } catch (err) {
    statusDiv.textContent = "Error connecting to backend";
  }
}

function renderResults(results) {
  resultsDiv.innerHTML = "";

  results.forEach(r => {
    const div = document.createElement("div");
    div.className = "result";

    div.innerHTML = `
      <div class="result-header">
        <h3>${escapeHtml(r.file)}</h3>
        <span class="score">${r.score.toFixed(3)}</span>
      </div>
      <pre>${escapeHtml(r.content)}</pre>
      <div class="explanation">💡 ${escapeHtml(r.explanation)}</div>
    `;

    resultsDiv.appendChild(div);
  });
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, c =>
    ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", "\"":"&quot;", "'":"&#39;" }[c])
  );
}
