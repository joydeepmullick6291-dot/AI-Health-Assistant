document.addEventListener('DOMContentLoaded', async () => {
  const listEl = document.querySelector('[data-doctor-list]');
  const slotEl = document.querySelector('[data-slot-list]');
  const chipsEl = document.querySelector('[data-department-chips]');
  const doctorCountEl = document.querySelector('[data-doctor-count]');
  const slotCountEl = document.querySelector('[data-slot-count]');
  const bookingsListEl = document.querySelector('[data-bookings-list]');
  const bookingsCountEl = document.querySelector('[data-bookings-count]');
  const confirmPanel = document.querySelector('[data-confirmation-panel]');
  const confirmDoctor = document.querySelector('[data-confirm-doctor]');
  const confirmSlot = document.querySelector('[data-confirm-slot]');
  const confirmMessage = document.querySelector('[data-confirm-message]');
  const userNameEl = document.querySelector('[data-user-name]');
  const userIdEl = document.querySelector('[data-user-id]');
  const userAvatarEl = document.querySelector('[data-user-avatar]');
  let selectedDept = 'All';
  let selectedDoctor = null;
  let doctorsCache = [];

  const toast = (message) => {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();
    const el = document.createElement('div');
    el.className = 'toast';
    el.textContent = message;
    document.body.appendChild(el);
    requestAnimationFrame(() => el.classList.add('show'));
    setTimeout(() => {
      el.classList.remove('show');
      setTimeout(() => el.remove(), 200);
    }, 1800);
  };

  const renderUser = (user) => {
    if (!user) return;
    if (userNameEl && user.name) userNameEl.textContent = user.name;
    if (userIdEl && user.id) userIdEl.textContent = `PATIENT ID · ${user.id}`;
    if (userAvatarEl) userAvatarEl.textContent = (user.name || 'U').split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase();
  };

  const renderChips = (departments) => {
    const items = ['All', ...departments];
    chipsEl.innerHTML = items
      .map((dept) => `<button class="chip ${dept === selectedDept ? 'active' : ''}" type="button" data-dept="${dept}">${dept}</button>`)
      .join('');

    chipsEl.querySelectorAll('[data-dept]').forEach((btn) =>
      btn.addEventListener('click', () => {
        selectedDept = btn.dataset.dept;
        selectedDoctor = null;
        loadDoctors();
      })
    );
  };

  const showConfirmation = (doctorName, slotTime, appointmentId, status) => {
    confirmPanel?.classList.remove('hidden');
    if (confirmDoctor) confirmDoctor.textContent = doctorName;
    if (confirmSlot) confirmSlot.textContent = slotTime;
    if (confirmMessage) {
      confirmMessage.textContent = `${status || 'Appointment booked'}${appointmentId ? ` · ID: ${appointmentId}` : ''}`;
    }
    confirmPanel?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  const renderBookings = (bookings) => {
    bookingsCountEl.textContent = `${bookings.length} bookings`;
    bookingsListEl.innerHTML = bookings.length
      ? bookings
          .map(
            (b) => `
      <div class="booking-item">
        <div>
          <strong>${b.doctorName || b.doctor || 'Doctor'}</strong>
          <span>${b.slot || b.time || '-'}</span>
          <small>${b.department || ''} ${b.appointmentId ? '· ID ' + b.appointmentId : ''}</small>
        </div>
        <div class="booking-status">${b.status || 'Booked'}</div>
      </div>
    `
          )
          .join('')
      : '<div class="note empty-state">Booked appointments will appear here.</div>';
  };

  const renderSlots = (doctor) => {
    const slots = doctor?.slots?.length
      ? doctor.slots
      : [
          { time: '9:00 AM', type: 'Consultation' },
          { time: '11:30 AM', type: 'OPD' },
          { time: '2:00 PM', type: 'Follow-up' }
        ];

    slotCountEl.textContent = `${slots.length} slots`;
    slotEl.innerHTML = slots
      .map(
        (slot) => `
      <div class="slot">
        <strong>${slot.time}</strong>
        <span>${slot.type || 'Consultation'}</span>
        <button class="btn btn-primary book-slot-btn" type="button" data-book-slot="${doctor.id}" data-slot-time="${slot.time}">Book slot</button>
      </div>
    `
      )
      .join('');

    slotEl.querySelectorAll('.book-slot-btn').forEach((btn) =>
      btn.addEventListener('click', () => bookSlot(btn.dataset.bookSlot, btn.dataset.slotTime))
    );
  };

  const renderDoctors = (doctors) => {
    doctorCountEl.textContent = `${doctors.length} doctors`;
    listEl.innerHTML = doctors
      .map(
        (doctor) => `
      <button class="doctor-card card-surface ${selectedDoctor?.id === doctor.id ? 'active' : ''}" type="button" data-doctor="${doctor.id}">
        <div class="doctor-top">
          <div>
            <strong>${doctor.name}</strong>
            <span>${doctor.department}</span>
          </div>
          <span class="badge ${doctor.available ? 'primary' : 'blue'}">${doctor.available ? 'Available' : 'Busy'}</span>
        </div>
        <p>${doctor.experience || ''}</p>
        <div class="doctor-meta">
          <span>${doctor.rating || '4.8'} rating</span>
          <span>${doctor.fee || '₹500'} fee</span>
        </div>
      </button>
    `
      )
      .join('');

    listEl.querySelectorAll('[data-doctor]').forEach((btn) =>
      btn.addEventListener('click', () => {
        selectedDoctor = doctors.find((d) => d.id === btn.dataset.doctor);
        renderDoctors(doctors);
        renderSlots(selectedDoctor);
      })
    );

    if (!selectedDoctor && doctors[0]) {
      selectedDoctor = doctors[0];
      renderSlots(selectedDoctor);
    }
  };

  const createFallbackDoctors = async () => {
    const user = window.auth.getUser?.() || {};
    const seed = [
      { user_id: user.id || 0, specialization: 'Gynecology', license_number: 'LIC-1001', department: 'Gynecology', experience_years: 12 },
      { user_id: user.id || 0, specialization: 'General Medicine', license_number: 'LIC-1002', department: 'General Medicine', experience_years: 9 },
      { user_id: user.id || 0, specialization: 'Internal Medicine', license_number: 'LIC-1003', department: 'Internal Medicine', experience_years: 15 }
    ];

    const created = [];
    for (const d of seed) {
      try {
        const res = await window.api.post('/doctors/', d);
        created.push(res?.doctor || res || d);
      } catch (e) {
        created.push(d);
      }
    }

    doctorsCache = created.map((d, i) => ({
      id: d.id || `local-${i + 1}`,
      name: d.specialization || d.name || `Doctor ${i + 1}`,
      department: d.department || d.specialization || '',
      available: true,
      experience: `${d.experience_years || 0} years experience`,
      rating: '4.8',
      fee: '₹500',
      slots: []
    }));

    const departments = [...new Set(doctorsCache.map((d) => d.department).filter(Boolean))];
    renderChips(departments);
    const doctors = selectedDept === 'All' ? doctorsCache : doctorsCache.filter((d) => d.department === selectedDept);
    renderDoctors(doctors);
  };

  const loadDoctors = async () => {
    try {
      const data = await window.api.get('/doctors/');
      const doctors = Array.isArray(data) ? data : (data?.doctors || []);
      doctorsCache = doctors;

      const departments = [...new Set(doctors.map((d) => d.department).filter(Boolean))];
      renderChips(departments);

      const filtered = selectedDept === 'All' ? doctors : doctors.filter((d) => d.department === selectedDept);
      renderDoctors(filtered);

      if (!filtered.length) {
        listEl.innerHTML = '<div class="note empty-state">No doctors found.</div>';
        slotEl.innerHTML = '<div class="note empty-state">Select a doctor to see slots.</div>';
      } else if (!selectedDoctor && filtered[0]) {
        selectedDoctor = filtered[0];
        renderSlots(selectedDoctor);
      }
    } catch (e) {
      await createFallbackDoctors();
    }
  };

  const refreshBookings = async () => {
    try {
      const data = await window.api.get('/patient/appointments');
      renderBookings(data?.appointments || data || []);
    } catch (e) {
      renderBookings([]);
    }
  };

  const checkBookedAppointment = async (appointmentId) => {
    try {
      const data = await window.api.get(`/patient/appointments/${appointmentId}`);
      if (data?.appointment?.status) toast(`Status: ${data.appointment.status}`);
      return data?.appointment || null;
    } catch (e) {
      toast('Could not verify appointment status');
      return null;
    }
  };

  const bookSlot = async (doctorId, slotTime) => {
    const doctor = doctorsCache.find((d) => d.id === doctorId) || selectedDoctor;
    if (!doctor) return toast('Select a doctor first');

    try {
      const payload = { doctorId: doctor.id, department: doctor.department, slot: slotTime };
      const res = await window.api.post('/patient/appointments', payload);
      const appointmentId = res?.appointmentId || res?.id || res?.appointment?.id || '';
      const status = res?.status || res?.appointment?.status || 'Booked';

      showConfirmation(doctor.name, slotTime, appointmentId, status);
      toast(res?.message || `Booked ${doctor.name} at ${slotTime}`);

      await loadDoctors();
      await refreshBookings();

      if (appointmentId) setTimeout(() => checkBookedAppointment(appointmentId), 400);
    } catch (e) {
      toast('Booking failed');
    }
  };

  document.querySelector('[data-refresh-doctors]')?.addEventListener('click', loadDoctors);
  document.querySelector('[data-view-schedule]')?.addEventListener('click', () => {
    window.location.href = 'patient-dashboard.html#appointments';
  });

  try { renderUser(await window.auth.ensurePatient()); } catch (e) {}
  try { renderUser(window.auth.getUser?.()); } catch (e) {}
  try { renderUser((await window.api.get('/patient/dashboard'))?.patient); } catch (e) {}

  await loadDoctors();
  await refreshBookings();
});