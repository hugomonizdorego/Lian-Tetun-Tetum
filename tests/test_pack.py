# SPDX-License-Identifier: GPL-3.0-or-later
import csv,gettext,json,locale,os,subprocess,sys,tempfile,unittest,unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'scripts')]
from eduka_tet import change_user,compile_locale,normalize,strip_block,tet_environment,BEGIN,END
from compile_qm import compile_ts

class CatalogChecks(unittest.TestCase):
 def setUp(self):
  with (ROOT/'data/glossary.csv').open(encoding='utf-8',newline='') as f:self.rows=list(csv.DictReader(f))
 def test_provenance_review_status_and_unique_keys(self):
  self.assertEqual(len({r['english'] for r in self.rows}),len(self.rows))
  self.assertEqual(len({r['id'] for r in self.rows}),len(self.rows))
  for r in self.rows:
   self.assertEqual(r['review_status'],'needs-INL-review')
   self.assertEqual(r['origin'],'original-project-draft')
   self.assertEqual(r['license'],'GPL-3.0-or-later OR GPL-2.0-or-later OR LGPL-2.0-or-later')
   self.assertEqual(r['tetun'],unicodedata.normalize('NFC',r['tetun']))
  m=json.loads((ROOT/'data/metadata.json').read_text());self.assertEqual(m['term_count'],len(self.rows));self.assertFalse(m['inl_approved'])
 def test_every_gettext_translation_and_plural_placeholder(self):
  tr=gettext.translation('edukasaun',ROOT/'build/locale',languages=['tet'])
  for r in self.rows:self.assertEqual(tr.gettext(r['english']),r['tetun'])
  for n in [0,1,2,315]:self.assertEqual(tr.ngettext('%d file','%d files',n)%n,'Arkivu '+str(n))
  self.assertEqual(tr.gettext('UNTRANSLATED SENTINEL'),'UNTRANSLATED SENTINEL')
  subprocess.run(['msgfmt','--check','--check-format','-o',os.devnull,str(ROOT/'po/tet.po')],check=True)
 def test_qt_runtime_all_messages_and_context_isolation(self):
  try:from PyQt5.QtCore import QTranslator,QCoreApplication
  except ImportError:self.skipTest('Optional Qt runtime verification requires python3-pyqt5')
  app=QCoreApplication.instance() or QCoreApplication([])
  for ts,qm in [(ROOT/'qt/edukasaun_tet.ts',ROOT/'build/qt/edukasaun_tet.qm'),(ROOT/'upstream/mainmenu_tet.ts',ROOT/'build/qt/mainmenu_tet.qm')]:
   tr=QTranslator();self.assertTrue(tr.load(str(qm)))
   for ctx in ET.parse(ts).getroot().findall('context'):
    for m in ctx.findall('message'):self.assertEqual(tr.translate(ctx.findtext('name'),m.findtext('source')),m.findtext('translation'))
   self.assertEqual(tr.translate('WRONG_CONTEXT','Open'),'')
 def test_qm_rejects_unsupported_numerus(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.ts';p.write_text('<TS><context><name>A</name><message numerus="yes"><source>%n</source><translation>X</translation></message></context></TS>')
   with self.assertRaises(ValueError):compile_ts(p,Path(d)/'bad.qm')
 def test_glossary_is_complete_and_has_no_remote_assets(self):
  s=(ROOT/'data/resources.html').read_text();self.assertEqual(s.count('<tr><td>'),len(self.rows));self.assertNotIn('<script src=',s);self.assertNotIn('<link href=',s)

class LocaleChecks(unittest.TestCase):
 def test_target_compile_date_months_currency_and_repeat_generation(self):
  with tempfile.TemporaryDirectory() as d:
   target=compile_locale(ROOT/'locale/tet_TL',Path(d));self.assertTrue((target/'.eduka-tet-owner').exists())
   env=dict(os.environ,LOCPATH=d,LC_ALL='tet_TL.UTF-8')
   code="import locale,datetime,json;locale.setlocale(locale.LC_ALL,'');print(json.dumps({'sample':datetime.datetime(2026,11,25,13).strftime('%A, %d %B %Y %T'),'months':[datetime.datetime(2026,m,1).strftime('%B') for m in range(1,13)],'money':locale.localeconv()['int_curr_symbol'],'yes':locale.nl_langinfo(locale.YESEXPR),'no':locale.nl_langinfo(locale.NOEXPR)},ensure_ascii=False))"
   got=json.loads(subprocess.check_output([sys.executable,'-c',code],env=env,text=True));self.assertEqual(got['sample'],'Kuarta, 25 Novembru 2026 13:00:00');self.assertEqual(got['months'][5:7],['Juñu','Jullu']);self.assertEqual(len(got['months']),12);self.assertEqual(got['money'],'USD ');self.assertRegex('sin',got['yes']);self.assertRegex('lae',got['no'])
   compile_locale(ROOT/'locale/tet_TL',Path(d))
   s=subprocess.check_output([str(ROOT/'bin/eduka-tet'),'run','--','date','-d','2026-11-25','+%A'],env=env,text=True);self.assertEqual(s.strip(),'Kuarta')
 def test_external_locale_and_symlink_are_not_overwritten(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/'tet_TL.utf8';target.mkdir();(target/'keep').write_text('external')
   with self.assertRaises(RuntimeError):compile_locale(ROOT/'locale/tet_TL',Path(d))
   self.assertEqual((target/'keep').read_text(),'external')
  with tempfile.TemporaryDirectory() as d:
   (Path(d)/'tet_TL.utf8').symlink_to(ROOT)
   with self.assertRaises(RuntimeError):compile_locale(ROOT/'locale/tet_TL',Path(d))
 def test_failed_compilation_preserves_existing_locale(self):
  with tempfile.TemporaryDirectory() as d:
   target=compile_locale(ROOT/'locale/tet_TL',Path(d));before=(target/'LC_TIME').read_bytes();bad=Path(d)/'bad';bad.write_text('invalid data\n')
   with self.assertRaises(subprocess.CalledProcessError):compile_locale(bad,Path(d))
   self.assertEqual((target/'LC_TIME').read_bytes(),before)

class SessionChecks(unittest.TestCase):
 def test_repeat_enable_and_disable_preserve_unrelated_settings(self):
  with tempfile.TemporaryDirectory() as d:
   home=Path(d);p=home/'.xsessionrc';original='export MY_SETTING=hello\n# existing comment\n';p.write_text(original)
   change_user(home,True,False);first=p.read_text();change_user(home,True,False);self.assertEqual(p.read_text(),first);self.assertEqual(first.count(BEGIN),1);self.assertEqual(first.count(END),1)
   p.write_text(first+'export EXTRA=keep\n');change_user(home,False,False);self.assertEqual(p.read_text(),original+'export EXTRA=keep\n');self.assertFalse((home/'.config/environment.d/60-eduka-tet.conf').exists());change_user(home,False,False)
 def test_user_edited_environment_is_preserved_before_any_session_change(self):
  with tempfile.TemporaryDirectory() as d:
   home=Path(d);p=home/'.xsessionrc';p.write_text('keep\n');e=home/'.config/environment.d/60-eduka-tet.conf';e.parent.mkdir(parents=True);e.write_text('custom')
   with self.assertRaises(RuntimeError):change_user(home,True,False)
   self.assertEqual(p.read_text(),'keep\n');self.assertEqual(e.read_text(),'custom')
 def test_user_symlink_and_malformed_blocks_are_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   home=Path(d);external=home/'external';external.write_text('keep');(home/'.xsessionrc').symlink_to(external)
   with self.assertRaises(RuntimeError):change_user(home,True,False)
   self.assertEqual(external.read_text(),'keep')
  with self.assertRaises(RuntimeError):strip_block('data\n'+BEGIN+'\nno end\n')
 def test_temporary_locale_clears_conflicting_categories(self):
  e=tet_environment({'LC_ALL':'C','LC_MESSAGES':'id_ID','LC_NUMERIC':'pt_PT','PATH':'/bin','LANG':'C'});self.assertEqual(e['LANG'],'tet_TL.UTF-8');self.assertEqual(e['LANGUAGE'],'tet:pt:en');self.assertFalse(any(k.startswith('LC_') for k in e));self.assertEqual(e['PATH'],'/bin')
 def test_unicode_normalization_preserves_lexical_and_dialect_distinctions(self):
  self.assertEqual(normalize('ha’u ne’e n\u0303 a\u0301 hare haree bainhira'),"ha'u ne'e ñ á hare haree bainhira");self.assertEqual(normalize('senhora companhia'),'senhora companhia')

if __name__=='__main__':unittest.main()
