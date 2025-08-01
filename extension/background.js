chrome.alarms.onAlarm.addListener(alarm => {
  if (alarm.name !== 'autoApplyAlarm') return;

  // Load the stored interval so we can reschedule
  chrome.storage.sync.get(
    ['firstName','lastName','specialty','experienceYears','email','password','urlSearch','autoRunSec'],
    res => {
      // Build payload
      const payload = {
        firstName:       res.firstName       || '',
        lastName:        res.lastName        || '',
        specialty:       res.specialty       || '',
        experienceYears: parseInt(res.experienceYears,10)||0,
        email:           res.email,
        password:        res.password,
        urlSearch:       res.urlSearch
      };

      // Hit your Flask API
      fetch('http://127.0.0.1:5000/apply_jobs', {
        method:  'POST',
        headers: {'Content-Type':'application/json'},
        body:    JSON.stringify(payload)
      })
      .then(r => r.text())
      .then(text => {
        console.log('Auto-run response:', text);
        const sec = parseInt(res.autoRunSec,10) || 0;
        if (sec > 0) {
          // Schedule the *next* run after sec seconds
          chrome.alarms.create('autoApplyAlarm', {
            when: Date.now() + sec * 1000
          });
        }
      })
      .catch(err => console.error('Auto-run error:', err));
    }
  );
});