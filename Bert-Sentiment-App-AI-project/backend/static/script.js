document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("btn");
  const micBtn = document.getElementById("micBtn");
  const textarea = document.getElementById("text");
  const resultDiv = document.getElementById("result");
  const loading = document.getElementById("loading");
  const themeSwitcher = document.getElementById("themeSwitcher");
  const languageInfo = document.getElementById("languageInfo");
  const highlightBox = document.getElementById("highlighted");

  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
    themeSwitcher.checked = true;
  }

  themeSwitcher.addEventListener("change", () => {
    document.body.classList.toggle("dark");
    localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
  });

  async function classifyText() {
    const text = textarea.value.trim();
    resultDiv.textContent = "";
    resultDiv.className = "result";
    languageInfo.textContent = "";
    highlightBox.classList.add("hidden");
    highlightBox.innerHTML = "";
    if (!text) {
      resultDiv.textContent = "⚠️ Please enter some text.";
      resultDiv.classList.add("negative");
      return;
    }

    loading.classList.remove("hidden");
    button.disabled = true;
    micBtn.disabled = true;
        try {
      const lang = detectLanguage(text);
      languageInfo.textContent = `🌐 Language Detected: ${lang}`;

      const keywords = extractKeywords(text);
      if (keywords.length) {
        highlightBox.innerHTML = highlightKeywords(text, keywords);
        highlightBox.classList.remove("hidden");
      }

      const response = await fetch("/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await response.json();

      if (response.ok) {
        const label = data.label.includes("positive")
          ? "✅ 预测结果：好评"
          : "❌ 预测结果：差评";
        resultDiv.textContent = `${label} (Confidence: ${data.confidence || 'N/A'}%)`;
        resultDiv.classList.add(data.label.includes("positive") ? "positive" : "negative");
      } else {
        resultDiv.textContent = `⚠️ Error: ${data.error}`;
        resultDiv.classList.add("negative");
      }
    } catch (err) {
      resultDiv.textContent = "⚠️ Network error.";
      resultDiv.classList.add("negative");
    } finally {
      loading.classList.add("hidden");
      button.disabled = false;
      micBtn.disabled = false;
    }
      }

function detectLanguage(text) {
  const zh = /[\u4e00-\u9fa5]/.test(text); // Chinese
  const ja = /[\u3040-\u30ff\u31f0-\u31ff]/.test(text); // Japanese
  const ko = /[\uac00-\ud7af]/.test(text); // Korean
  const ru = /[\u0400-\u04FF]/.test(text); // Russian
  const ar = /[\u0600-\u06FF]/.test(text); // Arabic
  const hi = /[\u0900-\u097F]/.test(text); // Hindi
  const he = /[\u0590-\u05FF]/.test(text); // Hebrew
  const th = /[\u0E00-\u0E7F]/.test(text); // Thai
  const tr = /\b(ve|bir|çok|için|ama|gibi)\b/i.test(text); // Turkish (approx)
  const fr = /\b(le|la|les|de|un|une|et)\b/i.test(text); // French (approx)
  const de = /\b(der|die|das|und|ein|eine|nicht)\b/i.test(text); // German (approx)
  const es = /\b(el|la|los|las|de|un|una|y|pero)\b/i.test(text); // Spanish (approx)
  const it = /\b(il|lo|la|gli|le|un|una|e)\b/i.test(text); // Italian (approx)

if (zh) return " 中国";
if (ja) return "🇯🇵 日本";
if (ko) return "🇰🇷 韩国";
if (ru) return "🇷🇺 俄罗斯";
if (ar) return "🇸🇦 沙特阿拉伯";
if (hi) return "🇮🇳 印度";
if (he) return "🇮🇱 以色列";
if (th) return "🇹🇭 泰国";
if (tr) return "🇹🇷 土耳其";
if (fr) return "🇫🇷 法国";
if (de) return "🇩🇪 德国";
if (es) return "🇪🇸 西班牙";
if (it) return "🇮🇹 意大利";

  return "🇬🇧 英语";  // English (fallback)
}

  function extractKeywords(text) {
    const keywords = ["love", "like", "hate", "amazing", "awful", "excellent", "terrible", "disappointed"];
    return keywords.filter(word => text.toLowerCase().includes(word));
  }

  function highlightKeywords(text, words) {
    let highlighted = text;
    words.forEach(word => {
      const re = new RegExp(`(${word})`, 'gi');
      highlighted = highlighted.replace(re, '<mark>$1</mark>');
    });
    return highlighted;
  }

  button.addEventListener("click", classifyText);
  textarea.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      classifyText();
    }
  });
    if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.addEventListener("click", () => {
      recognition.start();
    });

    recognition.onresult = (event) => {
      const speechResult = event.results[0][0].transcript;
      textarea.value = speechResult;
    };

    recognition.onerror = (event) => {
      alert("Speech recognition error: " + event.error);
    };
  } else {
    micBtn.style.display = "none";
  }
});