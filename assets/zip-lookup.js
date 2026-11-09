/* Duty-station ZIP check for /bah/by-zip/. Accepts exactly 5 digits or ZIP+4. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.PCSZip = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  function parseDutyZip(raw) {
    var s = String(raw == null ? '' : raw).trim();
    if (!s) return { error: 'Enter a ZIP code: 5 digits, or ZIP+4 as 12345-6789.' };
    if (/^\d{5}$/.test(s)) return { zip: s };
    if (/^\d{5}-\d{4}$/.test(s) || /^\d{9}$/.test(s)) return { zip: s.slice(0, 5) };
    if (/^\d+$/.test(s) && s.length < 5) return { error: s + ' is too short. Enter exactly 5 digits, or ZIP+4 as 12345-6789.' };
    if (/^\d+$/.test(s) && s.length > 5) return { error: s + ' is too long. Enter exactly 5 digits, or ZIP+4 as 12345-6789.' };
    return { error: 'Use only digits: 5 digits, or ZIP+4 as 12345-6789. ' + s + ' is not a ZIP code.' };
  }
  return { parseDutyZip: parseDutyZip };
});
