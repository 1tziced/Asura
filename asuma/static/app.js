// Только поведение интерфейса: окна, вкладки, меню. Бизнес-логики здесь нет.
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

const modal = $('#settings');
const menu = $('#acc-menu');

const openSettings = () => { menu.hidden = true; modal.hidden = false; $('.dialog', modal).focus?.(); };
const closeSettings = () => { modal.hidden = true; };

$$('[data-open="settings"]').forEach(b => b.addEventListener('click', openSettings));
$$('[data-close]').forEach(b => b.addEventListener('click', closeSettings));
modal.addEventListener('mousedown', e => { if (e.target === modal) closeSettings(); });

$$('[data-toggle]').forEach(b => b.addEventListener('click', e => {
  e.stopPropagation();
  $('#' + b.dataset.toggle).hidden = !$('#' + b.dataset.toggle).hidden;
}));
document.addEventListener('click', e => { if (!menu.contains(e.target)) menu.hidden = true; });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeSettings(); menu.hidden = true; } });

// Вкладки настроек
$$('.tab').forEach(tab => tab.addEventListener('click', () => {
  $$('.tab').forEach(t => t.classList.toggle('active', t === tab));
  $$('.pane').forEach(p => p.hidden = p.dataset.pane !== tab.dataset.tab);
}));

// Акцентный цвет
$$('.swatch').forEach(s => s.addEventListener('click', () => {
  document.documentElement.style.setProperty('--accent', s.dataset.accent);
  $$('.swatch').forEach(x => x.classList.toggle('on', x === s));
}));

// Кнопка play/pause (только значок)
const pm = $('#play-main');
pm.addEventListener('click', () => {
  $('.i-play', pm).hidden = !$('.i-play', pm).hidden;
  $('.i-pause', pm).hidden = !$('.i-pause', pm).hidden;
});
