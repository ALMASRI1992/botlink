const API_BASE = 'https://autoapply-linkedin-f058600e4815.herokuapp.com';
const fields = [
  'firstName','lastName','specialty',
  'experienceYears','email','password','urlSearch'
];

// --- LICENSE / PAYMENT LOGIC ---
function enableFullFeatures() {
  document.getElementById('paySection').style.display = 'none';
  document.getElementById('autoRunSecInput').removeAttribute('max');
}

async function checkLicense() {
  chrome.storage.sync.get('licenseKey', async res => {
    if (res.licenseKey) {
      try {
        const r = await fetch(`${API_BASE}/validate-license`, {
          method: 'POST',
          headers: {'Content-Type':'application/json'},
          body: JSON.stringify({ licenseKey: res.licenseKey })
        });
        if (r.ok) enableFullFeatures();
        else    chrome.storage.sync.remove('licenseKey');
      } catch { /* network fail */ }
    }
  });
}

document.getElementById('subscribeBtn').addEventListener('click', async () => {
  try {
    const res = await fetch(`${API_BASE}/create-checkout-session`,{ method:'POST' });
    const { url } = await res.json();
    chrome.tabs.create({ url });
  } catch {
    alert('Unable to start checkout. Please try again.');
  }
});

document.getElementById('submitLicense').addEventListener('click', async () => {
  const key = document.getElementById('licenseInput').value.trim();
  try {
    const r = await fetch(`${API_BASE}/validate-license`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({licenseKey:key})
    });
    if (r.ok) {
      chrome.storage.sync.set({licenseKey:key});
      enableFullFeatures();
    } else {
      alert('Invalid license key');
    }
  } catch {
    alert('Network error validating license');
  }
});
// --- END LICENSE / PAYMENT LOGIC ---

function loadSettings() {
  chrome.storage.sync.get(fields.concat('delaySec','autoRunSec'), res => {
    fields.forEach(f => {
      if (res[f] !== undefined) document.getElementById(f).value = res[f];
    });
    if (res.delaySec   !== undefined) document.getElementById('delaySecInput').value   = res.delaySec;
    if (res.autoRunSec !== undefined) document.getElementById('autoRunSecInput').value = res.autoRunSec;
  });
}

function saveSettings(payload) {
  chrome.storage.sync.set(payload);
}

function markInput(id, isError) {
  document.getElementById(id).classList.toggle('input-error', isError);
}

function validateForm() {
  let ok = true;
  fields.forEach(f => {
    const v = document.getElementById(f).value.trim();
    if (!v) { markInput(f,true); ok=false; }
    else    { markInput(f,false); }
  });
  const email = document.getElementById('email').value.trim();
  if (!/^\S+@\S+\.\S+$/.test(email)) { markInput('email',true); ok=false; } else markInput('email',false);
  try {
    new URL(document.getElementById('urlSearch').value.trim());
    markInput('urlSearch',false);
  } catch {
    markInput('urlSearch',true);
    ok = false;
  }
  if (!ok) {
    const s = document.getElementById('status');
    s.className = 'error';
    s.textContent = 'Please correct highlighted fields.';
  }
  return ok;
}

function showLoading(msg='') {
  const s = document.getElementById('status');
  s.className = 'loading';
  s.innerHTML = `<div class="spinner"></div>${msg}`;
}

async function doApply() {
  showLoading('Running…');
  const payload = {};
  fields.forEach(f => {
    let v = document.getElementById(f).value.trim();
    if (f==='experienceYears') v = parseInt(v,10)||0;
    payload[f] = v;
  });
  const delaySec   = parseInt(document.getElementById('delaySecInput').value,10)||0;
  const autoRunSec = parseInt(document.getElementById('autoRunSecInput').value,10)||0;
  payload.delaySec   = delaySec;
  payload.autoRunSec = autoRunSec;
  saveSettings(payload);

  try {
    const res = await fetch(`${API_BASE}/apply_jobs`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
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

document.getElementById('applyButton').addEventListener('click', () => {
  document.getElementById('status').textContent = '';
  if (!validateForm()) return;

  const delaySec   = parseInt(document.getElementById('delaySecInput').value,10)||0;
  const autoRunSec = parseInt(document.getElementById('autoRunSecInput').value,10)||0;
  const cd = document.getElementById('countdown');

  chrome.alarms.clear('autoApplyAlarm', () => {
    if (autoRunSec>0) {
      chrome.alarms.create('autoApplyAlarm',{
        delayInMinutes: autoRunSec/60,
        periodInMinutes: autoRunSec/60
      });
    }
  });

  if (delaySec>0) {
    let t = delaySec;
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

document.getElementById('autoFillBtn').addEventListener('click', () => {
  loadSettings();
  const s = document.getElementById('status');
  s.className = 'loading';
  s.textContent = 'Auto-filled!';
});

// listen for background alarm
chrome.runtime.onMessage.addListener(msg => {
  if (msg==='runApply') doApply();
});

document.addEventListener('DOMContentLoaded', () => {
  checkLicense();
  loadSettings();
});