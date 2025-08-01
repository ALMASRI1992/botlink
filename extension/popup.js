const fields = [
  'firstName','lastName','specialty',
  'experienceYears','email','password','urlSearch'
];

// --- LICENSE / PAYMENT LOGIC ---

// Hide the pay section and unlock full features
function enableFullFeatures() {
  document.getElementById('paySection').style.display = 'none';
  // e.g. remove any free-tier caps:
  document.getElementById('autoRunSecInput').removeAttribute('max');
}

// On load, check if we already have a valid license
async function checkLicense() {
  chrome.storage.sync.get('licenseKey', async res => {
    if (res.licenseKey) {
      try {
        const r = await fetch('https://yourdomain.com/validate-license', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ licenseKey: res.licenseKey })
        });
        if (r.ok) {
          enableFullFeatures();
        } else {
          chrome.storage.sync.remove('licenseKey');
        }
      } catch {
        // network error: let user retry
      }
    }
  });
}

// Subscribe button → open Stripe Checkout
document.getElementById('subscribeBtn').addEventListener('click', async () => {
  try {
    const res = await fetch('https://yourdomain.com/create-checkout-session', {
      method: 'POST'
    });
    const { url } = await res.json();
    chrome.tabs.create({ url });
  } catch {
    alert('Unable to start checkout. Please try again.');
  }
});

// Submit license key
document.getElementById('submitLicense').addEventListener('click', async () => {
  const key = document.getElementById('licenseInput').value.trim();
  try {
    const r = await fetch('https://yourdomain.com/validate-license', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ licenseKey: key })
    });
    if (r.ok) {
      chrome.storage.sync.set({ licenseKey: key });
      enableFullFeatures();
    } else {
      alert('Invalid license key');
    }
  } catch {
    alert('Network error validating license');
  }
});

// --- END LICENSE / PAYMENT LOGIC ---

// Load saved form + timers
function loadSettings() {
  chrome.storage.sync.get(
    fields.concat('delaySec','autoRunSec'),
    res => {
      fields.forEach(f => {
        if (res[f] !== undefined) {
          document.getElementById(f).value = res[f];
        }
      });
      if (res.delaySec !== undefined) {
        document.getElementById('delaySecInput').value = res.delaySec;
      }
      if (res.autoRunSec !== undefined) {
        document.getElementById('autoRunSecInput').value = res.autoRunSec;
      }
    }
  );
}

// Persist settings
function saveSettings(payload) {
  chrome.storage.sync.set(payload);
}

// Mark invalid inputs
function markInput(id, isError) {
  const el = document.getElementById(id);
  el.classList.toggle('input-error', isError);
}

// Validate all fields
function validateForm() {
  let ok = true;
  // Required non-empty
  fields.forEach(f => {
    const v = document.getElementById(f).value.trim();
    if (!v) { markInput(f, true); ok = false; }
    else     { markInput(f, false); }
  });
  // Email
  const email = document.getElementById('email').value.trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) {
    markInput('email', true); ok = false;
  } else markInput('email', false);
  // URL
  try {
    new URL(document.getElementById('urlSearch').value.trim());
    markInput('urlSearch', false);
  } catch {
    markInput('urlSearch', true);
    ok = false;
  }
  if (!ok) {
    const s = document.getElementById('status');
    s.className = 'error';
    s.textContent = 'Please correct highlighted fields.';
  }
  return ok;
}

// Show spinner + message
function showLoading(msg='') {
  const s = document.getElementById('status');
  s.className = 'loading';
  s.innerHTML = `<div class="spinner"></div>${msg}`;
}

// Core apply request
async function doApply() {
  showLoading('Running…');
  // Build payload
  const payload = {};
  fields.forEach(f => {
    let v = document.getElementById(f).value.trim();
    if (f==='experienceYears') v = parseInt(v,10)||0;
    payload[f] = v;
  });
  const delay   = parseInt(document.getElementById('delaySecInput').value,10)||0;
  const autoRun = parseInt(document.getElementById('autoRunSecInput').value,10)||0;
  payload.delaySec   = delay;
  payload.autoRunSec = autoRun;
  saveSettings(payload);

  try {
    const res = await fetch('http://127.0.0.1:5000/apply_jobs', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload)
    });
    const text = await res.text();
    console.log('Raw response:', text);
    const data = JSON.parse(text);
    const s = document.getElementById('status');
    s.className = data.status==='success'?'success':'error';
    s.textContent = data.message;
  } catch (err) {
    console.error(err);
    const s = document.getElementById('status');
    s.className = 'error';
    s.textContent = 'Network/server error';
  }
}

// Handle Start button
document.getElementById('applyButton').addEventListener('click', () => {
  document.getElementById('status').textContent = '';
  if (!validateForm()) return;

  const delay   = parseInt(document.getElementById('delaySecInput').value,10)||0;
  const autoRun = parseInt(document.getElementById('autoRunSecInput').value,10)||0;
  const cd = document.getElementById('countdown');

  // Schedule first alarm
  chrome.alarms.clear('autoApplyAlarm', () => {
    if (autoRun>0) {
      chrome.alarms.create('autoApplyAlarm',{
        when: Date.now() + autoRun*1000
      });
    }
  });

  // Initial delay countdown
  if (delay>0) {
    let t = delay;
    cd.textContent = `Starting in ${t}s…`;
    const iv = setInterval(() => {
      t--;
      if (t>0) cd.textContent = `Starting in ${t}s…`;
      else {
        clearInterval(iv);
        cd.textContent = '';
        doApply();
      }
    },1000);
  } else {
    cd.textContent = '';
    doApply();
  }
});

// Auto-fill saved values
document.getElementById('autoFillBtn').addEventListener('click', () => {
  loadSettings();
  const s = document.getElementById('status');
  s.className = 'loading';
  s.textContent = 'Auto-filled!';
});

// On popup open
document.addEventListener('DOMContentLoaded', () => {
  checkLicense();
  loadSettings();
});
