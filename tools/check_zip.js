#!/usr/bin/env node
/* ZIP rules for /bah/by-zip/. Run: node tools/check_zip.js */
var parse = require('../assets/zip-lookup.js').parseDutyZip;
var fails = [];
function ok(cond, msg) { if (!cond) fails.push(msg); }
function noRate(raw) {
  var r = parse(raw);
  ok(!r.zip, raw + ' must not return a ZIP, got ' + JSON.stringify(r));
  ok(!!r.error, raw + ' needs an error message');
}
ok(parse('22204').zip === '22204', '22204');
ok(parse('  22204  ').zip === '22204', 'trimmed 22204');
ok(parse('22204-1234').zip === '22204', 'ZIP+4 hyphen');
ok(parse('222041234').zip === '22204', 'ZIP+4 nine digits');
noRate('');
noRate('   ');
noRate('2220');
noRate('222045');
noRate('2a2204');
noRate('22204-12');
noRate('abcde');
if (fails.length) {
  console.error(fails.join('\n'));
  process.exit(1);
}
console.log('zip checks ok');
