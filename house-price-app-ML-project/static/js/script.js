// FILE: static/js/script.js

const themeToggle = document.getElementById("theme-toggle");
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const root = document.documentElement;

// === THEME TOGGLE ===
if (themeToggle) {
  const currentTheme = localStorage.getItem("theme") || (prefersDark ? "dark" : "light");
  root.setAttribute("data-theme", currentTheme);
  themeToggle.addEventListener("click", () => {
    const newTheme = root.getAttribute("data-theme") === "light" ? "dark" : "light";
    root.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
  });
}

// === AJAX PREDICTION FORM ===
const predictionForm = document.getElementById("prediction-form");
if (predictionForm) {
  predictionForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const loading = document.getElementById("loading");
    const result = document.getElementById("prediction-result");
    loading.hidden = false;
    result.textContent = "";

    const formData = new FormData(predictionForm);
    const payload = Object.fromEntries(formData.entries());
    Object.keys(payload).forEach(k => payload[k] = parseFloat(payload[k]));

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();
      if (res.ok) {
        result.textContent = `Predicted Price: $${data.prediction.toLocaleString()}`;
      } else {
        result.textContent = `Error: ${data.error || 'Invalid input'}`;
      }
    } catch (error) {
      result.textContent = `Unexpected error occurred.`;
    } finally {
      loading.hidden = true;
    }
  });
}

// === DYNAMIC PLOTLY CHART ===
const plotEl = document.getElementById("eda-plot");
const selectEl = document.getElementById("feature-select");
if (plotEl && selectEl) {
  async function loadChart(feature) {
    try {
      const response = await fetch(`/static/data/mock_${feature}.json`);
      const chartData = await response.json();
      Plotly.newPlot("eda-plot", chartData.data, chartData.layout);
    } catch (err) {
      console.error("Failed to load chart:", err);
    }
  }

  selectEl.addEventListener("change", (e) => loadChart(e.target.value));
  loadChart(selectEl.value);

  const exportBtn = document.getElementById("download-chart");
  exportBtn?.addEventListener("click", () => Plotly.downloadImage(plotEl, {format: 'png', filename: 'eda_plot'}));
}
