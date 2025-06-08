const modeSwitch = document.getElementById('modeSwitch');
const urlInputSection = document.getElementById('urlInputSection');
const manualInputSection = document.getElementById('manualInputSection');
const previewSection = document.getElementById('previewSection');
const loading = document.getElementById('loading');
const resultDiv = document.getElementById('result');
const spinner = document.getElementById('spinner');


async function extractContent() {

  document.getElementById('previewHeadline').value = '';
  document.getElementById('previewContent').value = '';
  previewSection.classList.add('hidden');
  resultDiv.innerHTML = '';
  spinner.classList.add('hidden');
  loading.classList.add('hidden');

  const url = document.getElementById('urlInput').value.trim();
  if (!url) {
    alert('Please enter a URL');
    return;
  }
  loading.classList.remove('hidden');
  try {
    const res = await fetch('http://localhost:8000/api/extract', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    loading.classList.add('hidden');
    if (data.error) {
      alert(data.error);
      return;
    }
    document.getElementById('previewHeadline').value = data.headline || '';
    document.getElementById('previewContent').value = data.content || '';
    previewSection.classList.remove('hidden');
  } catch (err) {
    loading.classList.add('hidden');
    alert('Failed to extract article.');
  }
}

// Helper to get bias class and description
function getBiasClass(bias) {
  switch (bias.toLowerCase()) {
    case 'left-leaning': return 'bias-left';
    case 'centrist': return 'bias-centrist';
    case 'right-leaning': return 'bias-right';
    default: return '';
  }
}

function getBiasDescription(bias) {
  switch (bias.toLowerCase()) {
    case 'left-leaning': return 'This article shows a left-leaning perspective.';
    case 'centrist': return 'This article appears balanced and centrist.';
    case 'right-leaning': return 'This article shows a right-leaning perspective.';
    default: return 'Bias could not be determined.';
  }
}


async function predict() {
  spinner.classList.remove('hidden');
  loading.classList.remove('hidden');

  resultDiv.innerHTML = '';
  resultDiv.className = 'result-message';
  resultDiv.style = '';

  const headline = document.getElementById('previewHeadline').value;
  const content = document.getElementById('previewContent').value;
  let task_id = null;

  try {
    const response = await fetch("http://localhost:8000/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headline, content })
    });
    const result = await response.json();
    task_id = result.task_id;
  } catch (err) {
    resultDiv.innerText = "Prediction failed!";
    spinner.classList.add('hidden');
    loading.classList.add('hidden');
    resultDiv.className = "result-message error-message";
    return;
  }

  // Poll for result
  let prediction = null;
  while (true) {
    const res = await fetch(`http://localhost:8000/api/result/${task_id}`);
    const data = await res.json();
    if (data.status === "done") {
      prediction = data.prediction;
      break;
    }
    await new Promise(r => setTimeout(r, 500));
  }

  spinner.classList.add('hidden');
  loading.classList.add('hidden');

  const biasClass = getBiasClass(prediction);
  const biasDescription = getBiasDescription(prediction);

  resultDiv.innerHTML = `
    <div class="result-card">
      <div class="result-title">Prediction Result</div>
      <div class="result-bias ${biasClass}">${prediction}</div>
      <div class="result-details">${biasDescription}</div>
      <div class="result-footer">Powered by News Bias Detector</div>
    </div>
  `;

  resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
}



function showManualPreview() {
  const headline = document.getElementById('manualHeadline').value;
  const content = document.getElementById('manualContent').value;

  if (!headline || !content) {
    alert('Please enter both headline and content');
    return;
  }

  document.getElementById('previewHeadline').value = headline;
  document.getElementById('previewContent').value = content;
  previewSection.classList.remove('hidden');
}

function resetManualInputs() {
  document.getElementById('manualHeadline').value = '';
  document.getElementById('manualContent').value = '';
  document.getElementById('previewHeadline').value = '';
  document.getElementById('previewContent').value = '';
  previewSection.classList.add('hidden');
  resultDiv.innerHTML = '';
}

lucide.createIcons();
lucide.createIcons();

const themeSwitch = document.getElementById('themeSwitch');
const themeIcon = document.getElementById('themeIcon');

themeSwitch.addEventListener('change', () => {
  const isDark = themeSwitch.checked;
  document.body.classList.toggle('dark', isDark);
  themeIcon.textContent = isDark ? '🌙' : '🌞';
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

window.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  const isDark = savedTheme === 'dark';
  document.body.classList.toggle('dark', isDark);
  themeSwitch.checked = isDark;
  themeIcon.textContent = isDark ? '🌙' : '🌞';
});

const urlModeBtn = document.getElementById('urlModeBtn');
const manualModeBtn = document.getElementById('manualModeBtn');

urlModeBtn.addEventListener('click', () => {
  urlInputSection.classList.remove('hidden');
  manualInputSection.classList.add('hidden');
  previewSection.classList.add('hidden');
  resultDiv.innerHTML = '';

  urlModeBtn.classList.add('active');
  manualModeBtn.classList.remove('active');
});

manualModeBtn.addEventListener('click', () => {
  urlInputSection.classList.add('hidden');
  manualInputSection.classList.remove('hidden');
  previewSection.classList.add('hidden');
  resultDiv.innerHTML = '';

  manualModeBtn.classList.add('active');
  urlModeBtn.classList.remove('active');
});


function toggleMode() {
  // If URL mode is active, switch to manual; else switch to URL
  if (!urlInputSection.classList.contains('hidden')) {

    urlInputSection.classList.add('hidden');
    manualInputSection.classList.remove('hidden');
    previewSection.classList.add('hidden');
    resultDiv.innerHTML = '';
    manualModeBtn.classList.add('active');
    urlModeBtn.classList.remove('active');
  } else {

    urlInputSection.classList.remove('hidden');
    manualInputSection.classList.add('hidden');
    previewSection.classList.add('hidden');
    resultDiv.innerHTML = '';
    urlModeBtn.classList.add('active');
    manualModeBtn.classList.remove('active');
  }
}


document.addEventListener('keydown', function(e) {
  // Windows/Linux: Ctrl; Mac: Meta (Cmd)
  const ctrlOrCmd = e.ctrlKey || e.metaKey;

  // Extract (Ctrl+E)
  if (ctrlOrCmd && e.key.toLowerCase() === 'e') {
    e.preventDefault();
    const extractBtn = document.getElementById('extractButton');
    if (extractBtn && !extractBtn.disabled) extractBtn.click();
  }

  // Predict (Ctrl+P)
  if (ctrlOrCmd && e.key.toLowerCase() === 'p') {
    e.preventDefault();
    const predictBtn = document.getElementById('predictButton');
    if (predictBtn && !predictBtn.disabled) predictBtn.click();
  }

  // Switch Mode (Ctrl+M)
  if (ctrlOrCmd && e.key.toLowerCase() === 'm') {
    e.preventDefault();

    if (typeof toggleMode === 'function') {
      toggleMode();
    } else {
      const modeSwitch = document.getElementById('modeSwitch');
      if (modeSwitch) modeSwitch.click();
    }
  }
});

