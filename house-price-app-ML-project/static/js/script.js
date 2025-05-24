// FILE: static/js/script.js

document.addEventListener("DOMContentLoaded", () => {
  const predictionForm = document.getElementById("prediction-form");
  const resultBox = document.getElementById("prediction-result");
  const loadingText = document.getElementById("loading");
  const exampleBtn = document.getElementById("example-fill");

  if (predictionForm) {
    predictionForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      resultBox.textContent = "";
      loadingText.hidden = false;

      const formData = new FormData(predictionForm);
      const payload = Object.fromEntries(formData.entries());
      for (const key in payload) {
        payload[key] = parseFloat(payload[key]);
      }

      try {
        const res = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (res.ok && data.prediction) {
          resultBox.textContent = `Predicted Price: $${parseInt(data.prediction).toLocaleString()}`;
        } else {
          resultBox.textContent = data.error || "Prediction failed.";
          resultBox.style.color = "var(--error-color)";
        }
      } catch (err) {
        resultBox.textContent = "An unexpected error occurred.";
        resultBox.style.color = "var(--error-color)";
      } finally {
        loadingText.hidden = true;
      }
    });
  }

  if (exampleBtn) {
    exampleBtn.addEventListener("click", () => {
      const examples = {
        GrLivArea: 1800,
        TotalBsmtSF: 1000,
        YearBuilt: 2005,
        FullBath: 2,
        GarageCars: 2,
        OverallQual: 7
      };
      for (const id in examples) {
        const input = document.getElementById(id);
        if (input) input.value = examples[id];
      }
    });
  }
});
