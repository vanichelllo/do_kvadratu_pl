/**
 * ДО КВАДРАТУ: розклад із сайту → вкладка «Розклад уроків» Google-таблиці (Google Apps Script).
 *
 * Головний розклад — на сайті (кабінет → «Розклад занять»). Скрипт раз на годину бере його за особистим
 * посиланням і оновлює рядки таблиці:
 *   • нове заняття на сайті → новий рядок зі статусом «Ще рано» (рядок-зразок — останній урок цього учня:
 *     ціни, податки, «Subject» і формули копіюються з нього), вставляється за датою;
 *   • перенесення → нові дата й час, у «Інформація про перенесення уроку» — звідки перенесено;
 *   • скасування → «Не відбувся» і причина (лише для рядків «Ще рано»); повернули заняття на сайті → знову «Ще рано»;
 *   • звіт після заняття → «Тема» (якщо порожня);
 *   • заняття прибрали з сайту (завершили постійне) → «Не відбувся», «Видалено з розкладу на сайті».
 * Рядок і заняття зв'язує стовпець «ID на сайті» (скрипт додає його сам). Рядок без ID зв'язується з заняттям
 * того самого учня в ту саму дату (спершу — з тим самим часом). Оплату, ціни й податки скрипт не змінює ніколи,
 * клітинки з формулами — теж. Рядки не видаляються.
 *
 * ВСТАНОВЛЕННЯ (один раз):
 *   0. Спершу спробуйте на копії: Файл → Створити копію.
 *   1. На сайті перенесіть майбутні уроки з таблиці: кабінет → «Розклад занять» → «Таблиця розкладу».
 *      Там же — посилання для скрипта (…/calendar/t…-….json).
 *   2. У таблиці: Розширення → Apps Script, вставте цей файл замість вмісту Code.gs, збережіть.
 *   3. Налаштування проєкту (⚙️) → Властивості скрипта → додати SITE_FEED_URL = посилання з п. 1.
 *   4. Оберіть функцію setup і натисніть «Виконати», дозвольте доступ. Далі — щогодини саме;
 *      вручну — меню «ДО КВАДРАТУ → Оновити розклад із сайту» в таблиці.
 */

var SHEET_NAME = 'Розклад уроків';
var ID_HEADER = 'ID на сайті';
var COLUMNS = {
  type: 'Lesson type', name: 'Student', date: 'Start date', weekday: 'Weekday', subject: 'Subject',
  start: 'Start time', endDate: 'End Date', end: 'End time', month: 'Month', year: 'Year', status: 'Status1',
  topic: 'Тема', reason: 'Причина скасування уроку', moved: 'Інформація про перенесення уроку'
};
var UPCOMING = 'Ще рано';
var CANCELLED = 'Не відбувся';
var REMOVED_REASON = 'Видалено з розкладу на сайті';
var CANCELLED_REASON = 'Скасовано на сайті';


// ─── ЧИСТА ЛОГІКА (без звернень до таблиці) ─────────────────
function normalizeName(value) {
  return String(value || '').replace(/\s+/g, ' ').trim().toLowerCase();
}

function timeKey(value) {
  var match = /^\s*(\d{1,2}):(\d{2})/.exec(String(value || ''));
  return match ? ('0' + match[1]).slice(-2) + ':' + match[2] : '';
}

function dateKey(value) {
  var match = /^\s*(\d{1,2})\.(\d{1,2})\.(\d{4})/.exec(String(value || ''));
  return match ? ('0' + match[1]).slice(-2) + '.' + ('0' + match[2]).slice(-2) + '.' + match[3] : '';
}

function sortKey(date, time) {   // «dd.mm.yyyy», «HH:MM» → «yyyymmddHHMM» для порівняння
  var d = dateKey(date);
  return d ? d.slice(6) + d.slice(3, 5) + d.slice(0, 2) + (timeKey(time) || '00:00').replace(':', '') : '';
}

/**
 * header — перший рядок; rows / formulas — рядки 2… (getDisplayValues / getFormulas); feed — JSON із сайту.
 * Повертає {idCol, addHeader, ids, sets, inserts, stats}: ids — нове значення стовпця ID для кожного рядка,
 * sets — [{row, col, value}] (номери рядків і стовпців таблиці, з 1), inserts — [{after, template, values, order}].
 */
function planSync(header, rows, formulas, feed, now) {
  var col = {};
  for (var key in COLUMNS) {
    col[key] = header.indexOf(COLUMNS[key]);
    if (col[key] < 0) throw new Error('У вкладці немає стовпця «' + COLUMNS[key] + '»');
  }
  var idCol = header.indexOf(ID_HEADER);
  var addHeader = idCol < 0;
  if (addHeader) {
    idCol = 0;
    for (var h = 0; h < header.length; h++) if (String(header[h]).trim()) idCol = h + 1;
  }
  var cell = function (r, c) { return c < rows[r].length ? String(rows[r][c]) : ''; };
  var hasFormula = function (r, c) { return c < formulas[r].length && String(formulas[r][c]) !== ''; };

  var stats = {linked: 0, updated: 0, added: 0, cancelled: 0, removed: 0, unmatched: 0, skippedFormulas: 0};
  var ids = [], byId = {}, free = {};
  for (var r = 0; r < rows.length; r++) {
    var id = String(cell(r, idCol)).trim();
    ids.push(id);
    if (id) { byId[id] = r; continue; }
    var k = normalizeName(cell(r, col.name)) + '|' + dateKey(cell(r, col.date));
    (free[k] = free[k] || []).push(r);
  }

  var sets = [];
  var set = function (r, c, value) {
    if (cell(r, c) === String(value)) return false;
    if (hasFormula(r, c)) { stats.skippedFormulas++; return false; }
    sets.push({row: r + 2, col: c + 1, value: value});
    return true;
  };

  var seen = {}, inserts = [];
  var nowKey = now.getTime();
  feed.lessons.forEach(function (lesson, order) {
    var id = String(lesson.id);
    seen[id] = true;
    var r = byId.hasOwnProperty(id) ? byId[id] : undefined;
    if (r === undefined) {
      var candidates = (free[normalizeName(lesson.name) + '|' + lesson.date] || []).filter(function (i) { return !ids[i]; });
      var sameTime = candidates.filter(function (i) { return timeKey(cell(i, col.start)) === timeKey(lesson.start); });
      r = sameTime.length ? sameTime[0] : (candidates.length === 1 ? candidates[0] : undefined);
      if (r !== undefined) { ids[r] = id; stats.linked++; }
    }
    var startsAt = Date.parse(lesson.starts_at);
    if (r !== undefined) {
      var changed = false;
      var parts = lesson.date.split('.');
      if (dateKey(cell(r, col.date)) !== lesson.date) {
        changed = set(r, col.date, lesson.date) || changed;
        changed = set(r, col.weekday, String(lesson.weekday)) || changed;
        changed = set(r, col.month, String(Number(parts[1]))) || changed;
        changed = set(r, col.year, parts[2]) || changed;
      }
      if (dateKey(cell(r, col.endDate)) !== lesson.end_date) changed = set(r, col.endDate, lesson.end_date) || changed;
      if (timeKey(cell(r, col.start)) !== timeKey(lesson.start)) changed = set(r, col.start, lesson.start) || changed;
      if (timeKey(cell(r, col.end)) !== timeKey(lesson.end)) changed = set(r, col.end, lesson.end) || changed;
      if (lesson.moved_from) changed = set(r, col.moved, 'Перенесено з ' + lesson.moved_from) || changed;
      var status = cell(r, col.status);
      if (lesson.status === 'cancelled' && status === UPCOMING) {
        set(r, col.status, CANCELLED);
        if (!cell(r, col.reason)) set(r, col.reason, lesson.reason || CANCELLED_REASON);
        stats.cancelled++;
      } else if (lesson.status !== 'cancelled' && status === CANCELLED && startsAt > nowKey) {
        set(r, col.status, UPCOMING);
        set(r, col.reason, '');
        changed = true;
      }
      if (lesson.topic && !cell(r, col.topic)) changed = set(r, col.topic, lesson.topic) || changed;
      if (changed) stats.updated++;
      return;
    }
    if (lesson.status === 'cancelled') return;

    // Новий рядок: за датою, рядок-зразок — останній урок цього учня
    var key = sortKey(lesson.date, lesson.start), after = 1, template = null;
    for (var i = 0; i < rows.length; i++) {
      var rowKey = sortKey(cell(i, col.date), cell(i, col.start));
      if (rowKey && rowKey <= key) after = i + 2;
      if (normalizeName(cell(i, col.name)) === normalizeName(lesson.name)) template = i;
    }
    var p = lesson.date.split('.');
    var values = {};
    values[col.name] = lesson.name;
    values[col.date] = lesson.date;
    values[col.weekday] = String(lesson.weekday);
    values[col.start] = lesson.start;
    values[col.endDate] = lesson.end_date;
    values[col.end] = lesson.end;
    values[col.month] = String(Number(p[1]));
    values[col.year] = p[2];
    values[col.status] = UPCOMING;
    values[col.topic] = lesson.topic || '';
    values[col.reason] = '';
    values[col.moved] = '';
    values[idCol] = id;
    if (template === null) { values[col.type] = 'Індивідуальний'; values[col.subject] = lesson.name; }
    var skip = {};
    if (template !== null) for (var c in values) if (hasFormula(template, Number(c))) skip[c] = true;
    var cells = [];
    for (var c2 in values) if (!skip[c2]) cells.push({col: Number(c2) + 1, value: values[c2]});
    inserts.push({after: after, template: template === null ? null : template + 2, cells: cells, order: order});
    stats.added++;
  });

  // Заняття, яких на сайті більше немає (у межах вікна вивантаження)
  var from = sortKey(feed.from, '00:00'), to = sortKey(feed.to, '23:59');
  for (var j = 0; j < rows.length; j++) {
    var key2 = sortKey(cell(j, col.date), cell(j, col.start));
    if (!key2 || key2 < from || key2 > to || cell(j, col.status) !== UPCOMING) continue;
    if (ids[j] && !seen[ids[j]]) {
      set(j, col.status, CANCELLED);
      if (!cell(j, col.reason)) set(j, col.reason, REMOVED_REASON);
      stats.removed++;
    } else if (!ids[j]) {
      stats.unmatched++;
    }
  }
  return {idCol: idCol + 1, addHeader: addHeader, ids: ids, sets: sets, inserts: inserts, stats: stats};
}


// ─── РОБОТА З ТАБЛИЦЕЮ ───────────────────────────────────────
function onOpen() {
  SpreadsheetApp.getUi().createMenu('ДО КВАДРАТУ').addItem('Оновити розклад із сайту', 'syncFromMenu').addToUi();
}

function setup() {
  ScriptApp.getProjectTriggers().forEach(function (trigger) {
    if (trigger.getHandlerFunction() === 'syncSchedule') ScriptApp.deleteTrigger(trigger);
  });
  ScriptApp.newTrigger('syncSchedule').timeBased().everyHours(1).create();
  Logger.log(describe(syncSchedule()));
}

function syncFromMenu() {
  SpreadsheetApp.getUi().alert('Розклад оновлено', describe(syncSchedule()), SpreadsheetApp.getUi().ButtonSet.OK);
}

function describe(stats) {
  return 'Зв\'язано рядків із заняттями: ' + stats.linked + '\nОновлено: ' + stats.updated + '\nДодано нових: ' +
    stats.added + '\nСкасовано: ' + stats.cancelled + '\nПрибрано з сайту: ' + stats.removed +
    '\nМайбутніх рядків без пари на сайті: ' + stats.unmatched +
    (stats.skippedFormulas ? '\nКлітинок з формулами не чіпали: ' + stats.skippedFormulas : '');
}

function syncSchedule() {
  var url = PropertiesService.getScriptProperties().getProperty('SITE_FEED_URL');
  if (!url) throw new Error('Додайте SITE_FEED_URL у властивості скрипта (посилання зі сторінки розкладу на сайті).');
  var response = UrlFetchApp.fetch(url, {muteHttpExceptions: true});
  if (response.getResponseCode() !== 200) throw new Error('Сайт відповів ' + response.getResponseCode());
  var feed = JSON.parse(response.getContentText());

  var lock = LockService.getDocumentLock();
  lock.waitLock(30000);
  try {
    var sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
    var lastRow = sheet.getLastRow(), lastCol = sheet.getLastColumn();
    var header = sheet.getRange(1, 1, 1, lastCol).getDisplayValues()[0];
    var range = sheet.getRange(2, 1, Math.max(lastRow - 1, 1), lastCol);
    var plan = planSync(header, range.getDisplayValues(), range.getFormulas(), feed, new Date());

    if (plan.addHeader) sheet.getRange(1, plan.idCol).setValue(ID_HEADER);
    if (plan.ids.length) {
      sheet.getRange(2, plan.idCol, plan.ids.length, 1).setValues(plan.ids.map(function (id) { return [id]; }));
    }
    plan.sets.forEach(function (op) { sheet.getRange(op.row, op.col).setValue(op.value); });

    // Нові рядки — знизу вгору, щоб номери рядків вище не зсувалися; той самий «after» — від пізнішого до ранішого
    var done = [];
    plan.inserts.sort(function (a, b) { return b.after - a.after || b.order - a.order; }).forEach(function (op) {
      sheet.insertRowAfter(op.after);
      done.push(op.after);
      var target = op.after + 1;
      if (op.template !== null) {
        var t = op.template + done.filter(function (a) { return a < op.template; }).length;
        var width = Math.max(lastCol, plan.idCol);
        sheet.getRange(t, 1, 1, width).copyTo(sheet.getRange(target, 1, 1, width));
      }
      op.cells.forEach(function (c) { sheet.getRange(target, c.col).setValue(c.value); });
    });
    return plan.stats;
  } finally {
    lock.releaseLock();
  }
}

// Для перевірки логіки поза Google (node): module.exports у Apps Script не існує
if (typeof module !== 'undefined') module.exports = {planSync: planSync, sortKey: sortKey};
