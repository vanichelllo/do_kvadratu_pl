// Перевірка логіки tools/schedule_sheet_sync.gs без Google: node tools/schedule_sheet_sync.test.js
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const sandbox = {module: {exports: {}}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'schedule_sheet_sync.gs'), 'utf8'), sandbox);
const {planSync} = sandbox.module.exports;

const header = ['Lesson type', 'Student', 'Start date', 'Weekday', 'Subject', 'Start time', 'End Date', 'End time',
  'Price (Mindful of taxes)', 'Зняття з ФОП', 'Price (Mindful of summer costs & taxes)', 'Taxes', '', 'summer costs',
  'Price', 'Month', 'Year', 'Status1', 'Тема', 'Причина скасування уроку', 'Інформація про перенесення уроку',
  'Lesson index'];
const row = (name, date, start, end, status, topic = '') => {
  const [, m, y] = date.split('.');
  return ['Індивідуальний', name, date, '1', name + ' (5 клас)', start, date, end, '376', '+', '320', '24', '+', '56',
    '400', String(Number(m)), y, status, topic, '', '', '1'];
};
const rows = [
  row('Влад Пастушок', '19.10.2026', '16:00:00', '16:50:00', 'Оплачено', 'Натуральні числа'),
  row('Влад Пастушок', '26.10.2026', '16:00:00', '16:50:00', 'Ще рано'),
  row('Соломія Яковчук', '27.10.2026', '17:00:00', '17:50:00', 'Ще рано'),
  row('Влад Пастушок', '02.11.2026', '16:00:00', '16:50:00', 'Ще рано'),
  row('Меліса Алтунбаш', '02.11.2026', '19:30:00', '20:20:00', 'Ще рано'),
];
const formulas = rows.map(r => r.map(() => ''));
formulas[4][3] = '=WEEKDAY(C6;2)';   // у Меліси день тижня рахує формула
const lesson = (id, name, date, start, end, extra = {}) => Object.assign({
  id, name, date, start, end, end_date: date, weekday: 1, status: 'planned', reason: '', moved_from: '', topic: '',
  starts_at: date.split('.').reverse().join('-') + 'T' + start + '+02:00'}, extra);
const now = new Date('2026-10-22T18:00:00+03:00');
const feed = {from: '08.10.2026', to: '31.12.2026', lessons: [
  lesson(1, 'Влад Пастушок', '26.10.2026', '16:00:00', '16:50:00', {topic: 'Додавання натуральних чисел'}),
  lesson(2, 'Соломія Яковчук', '27.10.2026', '17:00:00', '17:50:00', {status: 'cancelled', reason: 'хворіє', weekday: 2}),
  lesson(3, 'Влад Пастушок', '02.11.2026', '16:00:00', '16:50:00'),
  lesson(4, 'Меліса Алтунбаш', '28.10.2026', '19:30:00', '20:20:00', {weekday: 3}),
  lesson(5, 'Нова Учениця', '29.10.2026', '15:00:00', '16:00:00', {weekday: 4}),
]};

// Перший запуск: зв'язування, скасування, тема, нові рядки
let plan = planSync(header, rows, formulas, feed, now);
assert.strictEqual(plan.addHeader, true);
assert.strictEqual(plan.idCol, 23);                      // перший вільний стовпець після «Lesson index»
assert.strictEqual(JSON.stringify(plan.ids), JSON.stringify(['', '1', '2', '3', '']));  // Мелісу 02.11 не зв'язано: на сайті її урок 28.10
const at = (r, c) => plan.sets.find(op => op.row === r && op.col === c);
assert.strictEqual(at(3, 19).value, 'Додавання натуральних чисел');   // тема — у «Тема»
assert.strictEqual(at(4, 18).value, 'Не відбувся');
assert.strictEqual(at(4, 20).value, 'хворіє');
assert.strictEqual(plan.stats.unmatched, 1);           // Меліса 02.11 — у таблиці є, на сайті немає
assert.strictEqual(plan.inserts.length, 2);
const melisa = plan.inserts.find(op => op.cells.some(c => c.value === '4'));
assert.strictEqual(melisa.after, 4);                   // після Соломії 27.10 (рядок 4), до 02.11
assert.strictEqual(melisa.template, 6);                // зразок — останній рядок Меліси
assert.ok(!melisa.cells.some(c => c.col === 4));       // день тижня — формула зразка, не перезаписуємо
const newbie = plan.inserts.find(op => op.cells.some(c => c.value === '5'));
assert.strictEqual(newbie.template, null);
assert.ok(newbie.cells.some(c => c.col === 1 && c.value === 'Індивідуальний'));

// Другий запуск: перенесення й прибране з сайту заняття
const linked = rows.map((r, i) => r.concat([plan.ids[i]]));
linked[2][17] = 'Не відбувся'; linked[2][19] = 'хворіє';
linked[1][18] = 'Додавання натуральних чисел';
const feed2 = {from: feed.from, to: feed.to, lessons: [
  lesson(1, 'Влад Пастушок', '26.10.2026', '16:00:00', '16:50:00', {topic: 'Додавання натуральних чисел'}),
  lesson(2, 'Соломія Яковчук', '27.10.2026', '17:00:00', '17:50:00', {weekday: 2}),            // повернули
  lesson(4, 'Меліса Алтунбаш', '28.10.2026', '19:30:00', '20:20:00', {weekday: 3}),
]};
feed2.lessons[0] = lesson(1, 'Влад Пастушок', '27.10.2026', '17:00:00', '17:50:00',
  {weekday: 2, moved_from: '26.10.2026 16:00', topic: 'Додавання натуральних чисел'});
plan = planSync(header.concat(['ID на сайті']), linked, linked.map(r => r.map(() => '')), feed2, now);
assert.strictEqual(plan.addHeader, false);
const at2 = (r, c) => (plan.sets.find(op => op.row === r && op.col === c) || {}).value;
assert.strictEqual(at2(3, 3), '27.10.2026');
assert.strictEqual(at2(3, 6), '17:00:00');
assert.strictEqual(at2(3, 21), 'Перенесено з 26.10.2026 16:00');
assert.strictEqual(at2(4, 18), 'Ще рано');             // скасування на сайті відмінили
assert.strictEqual(at2(5, 18), 'Не відбувся');         // урок 3 прибрали з сайту
assert.strictEqual(at2(5, 20), 'Видалено з розкладу на сайті');
assert.strictEqual(plan.inserts.length, 1);            // лише Меліса 28.10 (ще не зв'язана)
assert.strictEqual(at2(2, 18), undefined);             // оплачений минулий урок не чіпаємо

console.log('OK');

// Обгортка syncSchedule на імітації аркуша: вставка рядків за датою, копія рядка-зразка, ID, повторний запуск
function fakeSheet(grid) {   // grid[r][c] = {v, f}
  const width = () => Math.max(...grid.map(r => r.length));
  const cellAt = (r, c) => { while (grid.length < r) grid.push([]); const row = grid[r - 1];
    while (row.length < c) row.push({v: '', f: ''}); return row[c - 1]; };
  const range = (r, c, nr = 1, nc = 1) => ({
    getDisplayValues: () => Array.from({length: nr}, (_, i) => Array.from({length: nc}, (_, j) => cellAt(r + i, c + j).v)),
    getFormulas: () => Array.from({length: nr}, (_, i) => Array.from({length: nc}, (_, j) => cellAt(r + i, c + j).f)),
    setValues: values => values.forEach((vals, i) => vals.forEach((v, j) => Object.assign(cellAt(r + i, c + j), {v: String(v), f: ''}))),
    setValue: v => Object.assign(cellAt(r, c), {v: String(v), f: ''}),
    copyTo: target => target._fill(Array.from({length: nc}, (_, j) => Object.assign({}, cellAt(r, c + j)))),
    _fill: cells => cells.forEach((cell, j) => Object.assign(cellAt(r, c + j), cell)),
  });
  return {
    grid, getLastRow: () => grid.length, getLastColumn: width, getRange: range,
    insertRowAfter: r => grid.splice(r, 0, []),
  };
}
function runSync(sheet, feedObj) {
  const ctx = {module: {exports: {}}, Date, JSON, Math, Number, String, Object, Error,
    PropertiesService: {getScriptProperties: () => ({getProperty: () => 'https://example/feed.json'})},
    UrlFetchApp: {fetch: () => ({getResponseCode: () => 200, getContentText: () => JSON.stringify(feedObj)})},
    LockService: {getDocumentLock: () => ({waitLock() {}, releaseLock() {}})},
    SpreadsheetApp: {getActive: () => ({getSheetByName: () => sheet})}};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, 'schedule_sheet_sync.gs'), 'utf8') +
    '\nmodule.exports.result = syncSchedule();', ctx);
  return ctx.module.exports.result;
}
const grid = [header.concat(['', '', '']).map(v => ({v, f: ''}))].concat(rows.map((r, i) => r.map((v, c) => ({v, f: formulas[i][c] || ''}))));
const sheet = fakeSheet(grid);
let stats = runSync(sheet, feed);
const view = () => sheet.grid.slice(1).map(r => [r[1].v, r[2].v, r[5].v, r[17].v, (r[22] || {v: ''}).v]);
assert.strictEqual(sheet.grid[0][22].v, 'ID на сайті');
assert.strictEqual(JSON.stringify(view()), JSON.stringify([
  ['Влад Пастушок', '19.10.2026', '16:00:00', 'Оплачено', ''],
  ['Влад Пастушок', '26.10.2026', '16:00:00', 'Ще рано', '1'],
  ['Соломія Яковчук', '27.10.2026', '17:00:00', 'Не відбувся', '2'],
  ['Меліса Алтунбаш', '28.10.2026', '19:30:00', 'Ще рано', '4'],
  ['Нова Учениця', '29.10.2026', '15:00:00', 'Ще рано', '5'],
  ['Влад Пастушок', '02.11.2026', '16:00:00', 'Ще рано', '3'],
  ['Меліса Алтунбаш', '02.11.2026', '19:30:00', 'Ще рано', ''],
]));
const melisaRow = sheet.grid[4];
assert.strictEqual(melisaRow[14].v, '400');                  // ціна — з рядка-зразка
assert.strictEqual(melisaRow[3].f, '=WEEKDAY(C6;2)');        // формула зразка лишилася
assert.strictEqual(stats.added, 2);
stats = runSync(sheet, feed);                                 // повторний запуск нічого не дублює
assert.strictEqual(stats.added, 0);
assert.strictEqual(sheet.grid.length, 8);
console.log('OK: обгортка');
