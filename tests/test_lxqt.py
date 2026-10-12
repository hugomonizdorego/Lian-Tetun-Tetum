# SPDX-License-Identifier: GPL-3.0-or-later
import json,os,subprocess,sys,unittest,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
MANIFEST=json.loads((ROOT/'data/lxqt-manifest.json').read_text(encoding='utf-8'))

QT_CHECK=r'''
import json,sys,xml.etree.ElementTree as ET
from PyQt6.QtCore import QCoreApplication,QLocale,QTranslator
app=QCoreApplication([])
bad=[];checked=0
for ts,qm in json.loads(sys.argv[1]):
    tr=QTranslator()
    if not tr.load(qm):bad.append('cannot load '+qm);continue
    # QCoreApplication.translate passes UTF-8 source text (QTranslator.translate in PyQt is ASCII-only).
    app.installTranslator(tr)
    for ctx in ET.parse(ts).getroot().findall('context'):
        name=ctx.findtext('name')
        for m in ctx.findall('message'):
            t=m.find('translation')
            if t.get('type')=='unfinished':continue
            numerus=m.get('numerus')=='yes'
            want=t.findtext('numerusform') if numerus else t.text
            if numerus:want=want.replace('%Ln','5').replace('%n','5')  # Qt substitutes the count
            got=QCoreApplication.translate(name,m.findtext('source'),m.findtext('comment'),5 if numerus else -1)
            checked+=1
            if got!=want:bad.append((ts,name,m.findtext('source'),got))
    app.removeTranslator(tr)
# Tetun is unknown to QLocale (name() is "C"), but the locale-aware overload
# used by the loader patches still finds *_tet.qm through uiLanguages().
loc=QTranslator()
found=loc.load(QLocale.system(),'mainmenu','_',sys.argv[2])
print(json.dumps({'checked':checked,'bad':bad[:20],'name':QLocale.system().name(),'found':found}))
'''

class LxqtCatalogs(unittest.TestCase):
 maxDiff=None
 def test_manifest_matches_catalogs_and_coverage(self):
  self.assertEqual(len(MANIFEST),len(list((ROOT/'lxqt').glob('*_tet.ts'))))
  total=sum(c['messages_total'] for c in MANIFEST);done=sum(c['translated'] for c in MANIFEST)
  self.assertGreaterEqual(done/total,0.99)
  for c in MANIFEST:
   self.assertTrue(c['install_dir'].startswith('/usr/share/'))
   self.assertIn(c['license'],('LGPL-2.1-or-later','GPL-2.0-or-later'))
   self.assertTrue(all(len(u['commit'])==40 for u in c['upstream']))
   ts=ET.parse(ROOT/'lxqt'/(c['catalog']+'_tet.ts')).getroot()
   self.assertEqual(ts.get('language'),'tet_TL')
   self.assertEqual(sum(1 for _ in ts.iter('message')),c['messages_total'])
 def test_regeneration_is_stable(self):
  before={p.name:p.read_bytes() for p in (ROOT/'lxqt').glob('*.ts')}
  subprocess.run([sys.executable,str(ROOT/'scripts/generate_lxqt.py')],check=True,capture_output=True)
  self.assertEqual(before,{p.name:p.read_bytes() for p in (ROOT/'lxqt').glob('*.ts')})
 def test_tetun_checker_passes(self):
  subprocess.run([sys.executable,str(ROOT/'scripts/check_tetun.py')],check=True,capture_output=True)
 def test_qt_runtime_loads_every_lxqt_message(self):
  try:subprocess.run([sys.executable,'-c','import PyQt6.QtCore'],check=True,capture_output=True)
  except subprocess.CalledProcessError:self.skipTest('Optional Qt runtime verification requires python3-pyqt6')
  pairs=[(str(ts),str(ROOT/'build/lxqt'/(ts.stem+'.qm'))) for ts in sorted((ROOT/'lxqt').glob('*_tet.ts'))]
  env=dict(os.environ,LANG='tet_TL.UTF-8',LC_CTYPE='C.UTF-8',PYTHONUTF8='1',QT_QPA_PLATFORM='offscreen');env.pop('LANGUAGE',None);env.pop('LC_ALL',None);env.pop('LC_MESSAGES',None)
  run=subprocess.run([sys.executable,'-c',QT_CHECK,json.dumps(pairs),str(ROOT/'build/lxqt')],env=env,text=True,capture_output=True)
  self.assertEqual(run.returncode,0,run.stderr[-2000:])
  out=json.loads(run.stdout)
  self.assertEqual(out['bad'],[]);self.assertGreater(out['checked'],3500)
  self.assertEqual(out['name'],'C');self.assertTrue(out['found'])

if __name__=='__main__':unittest.main()
