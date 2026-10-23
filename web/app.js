const meetingList = document.querySelector('#meeting-list');
const connection = document.querySelector('#connection');
const toast = document.querySelector('#toast');
const roleButtons = [...document.querySelectorAll('.role')];

const tokens = {
  member: 'member-demo',
  organizer: 'organizer-demo',
};

const labels = {
  draft: 'Черновик',
  published: 'Опубликовано',
  completed: 'Завершено',
  cancelled: 'Отменено',
};

const transitions = {
  draft: ['published', 'cancelled'],
  published: ['completed', 'cancelled'],
  completed: [],
  cancelled: [],
};

let role = 'member';
let meetings = [];

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function showToast(message, isError = false) {
  toast.textContent = message;
  toast.classList.toggle('error', isError);
  toast.classList.add('show');
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove('show'), 2600);
}

async function request(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.message || data.code || 'Не удалось выполнить запрос');
  }
  return data;
}

function formatDate(value) {
  return new Intl.DateTimeFormat('ru-RU', {
    month: 'long', day: 'numeric', weekday: 'short', hour: '2-digit', minute: '2-digit',
  }).format(new Date(value));
}

function renderActions(meeting) {
  if (role === 'member') {
    const disabled = meeting.status !== 'published';
    return `<button class="action register" data-id="${meeting.id}" ${disabled ? 'disabled' : ''}>${disabled ? 'Запись недоступна' : 'Записаться'}</button>`;
  }
  const available = transitions[meeting.status] || [];
  if (!available.length) return '<button class="action" disabled>Нет доступных действий</button>';
  return available.map((target) => (
    `<button class="action secondary status-action" data-id="${meeting.id}" data-status="${target}">${labels[target]}</button>`
  )).join('');
}

function renderMeetings() {
  if (!meetings.length) {
    meetingList.innerHTML = '<p class="empty">Сейчас встреч нет.</p>';
    return;
  }
  meetingList.innerHTML = meetings.map((meeting, index) => `
    <article class="meeting-card">
      <div class="card-top">
        <span class="meeting-number">NO. ${String(index + 1).padStart(2, '0')}</span>
        <span class="badge badge-${escapeHtml(meeting.status)}">${labels[meeting.status]}</span>
      </div>
      <h3>${escapeHtml(meeting.title)}</h3>
      <p class="description">${escapeHtml(meeting.description || '')}</p>
      <div class="meta">
        <span>◷ ${escapeHtml(formatDate(meeting.startsAt))}</span>
        <span>⌖ ${escapeHtml(meeting.location)}</span>
      </div>
      <div class="card-actions">${renderActions(meeting)}</div>
    </article>
  `).join('');
}

async function loadMeetings() {
  meetingList.innerHTML = '<p class="empty">Загружаем встречи…</p>';
  try {
    meetings = await request('/meetings');
    connection.textContent = 'Локальный сервис подключён';
    connection.classList.add('online');
    renderMeetings();
  } catch (error) {
    connection.textContent = 'Нет подключения к локальному сервису';
    connection.classList.remove('online');
    meetingList.innerHTML = '<p class="empty">Не удалось загрузить встречи. Убедитесь, что сервис запущен.</p>';
    showToast(error.message, true);
  }
}

meetingList.addEventListener('click', async (event) => {
  const registerButton = event.target.closest('.register');
  const statusButton = event.target.closest('.status-action');
  try {
    if (registerButton) {
      registerButton.disabled = true;
      await request(`/meetings/${registerButton.dataset.id}/registrations`, {
        method: 'POST', headers: { Authorization: `Bearer ${tokens.member}` },
      });
      registerButton.textContent = 'Вы записаны';
      showToast('Запись создана. До встречи в книжном клубе!');
    }
    if (statusButton) {
      await request(`/meetings/${statusButton.dataset.id}/status`, {
        method: 'PATCH',
        headers: {
          Authorization: `Bearer ${tokens.organizer}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: statusButton.dataset.status }),
      });
      showToast(`Статус встречи изменён: «${labels[statusButton.dataset.status]}».`);
      await loadMeetings();
    }
  } catch (error) {
    if (registerButton) registerButton.disabled = false;
    showToast(error.message, true);
  }
});

roleButtons.forEach((button) => {
  button.addEventListener('click', () => {
    role = button.dataset.role;
    roleButtons.forEach((item) => item.classList.toggle('active', item === button));
    renderMeetings();
  });
});

document.querySelector('#refresh').addEventListener('click', loadMeetings);
loadMeetings();
