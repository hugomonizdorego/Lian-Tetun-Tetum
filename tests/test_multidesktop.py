# SPDX-License-Identifier: GPL-3.0-or-later
import gettext, json, os, stat, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
import session
from catalog_tools import parse_po


class NativeCatalogChecks(unittest.TestCase):
    def test_all_exact_contexts_and_untranslated_fallback(self):
        templates = json.loads((ROOT/'data/native-templates.json').read_text())
        self.assertEqual(len(templates), 13)
        for record in templates:
            tr = gettext.translation(record['domain'], ROOT/'build/locale', languages=['tet'])
            seen = set()
            for msg in record['messages']:
                key = (msg['msgctxt'], msg['msgid'])
                self.assertNotIn(key, seen); seen.add(key)
                got = tr.pgettext(*key) if key[0] is not None else tr.gettext(key[1])
                self.assertEqual(got, msg['translation'])
                self.assertEqual(tr.pgettext('UNRELATED CONTEXT', key[1]), key[1])
            self.assertEqual(tr.gettext('UNTRANSLATED SENTINEL'), 'UNTRANSLATED SENTINEL')
            self.assertEqual(len(seen), record['translated_count'])
            self.assertEqual(tr.info()['language'], 'tet')
            subprocess.run(['msgfmt', '--check', '--check-format', '-o', os.devnull,
                            str(ROOT/'native'/(record['domain']+'.po'))], check=True)

    def test_po_and_manifest_match_canonical_selections(self):
        templates = json.loads((ROOT/'data/native-templates.json').read_text())
        manifest = json.loads((ROOT/'data/native-manifest.json').read_text())
        self.assertEqual([{k:v for k,v in t.items() if k not in ('messages','original_header')} for t in templates], manifest)
        for record in templates:
            entries = [e for e in parse_po((ROOT/'native'/(record['domain']+'.po')).read_text()) if e['msgid']]
            self.assertEqual(len(entries), record['translated_count'])
            self.assertLess(record['translated_count'], record['source_message_count'])
            self.assertEqual(len(record['source_po_sha256']), 64)
            self.assertTrue((ROOT/'upstream/native-notices'/(record['domain']+'.txt')).is_file())
            for entry in entries:
                self.assertNotIn('msgid_plural', entry)
                self.assertNotIn('%', entry['msgid'])
        self.assertFalse(list((ROOT/'upstream').rglob('*.pdf')))


class MultiDesktopChecks(unittest.TestCase):
    def test_desktop_detection(self):
        for value, expected in [('GNOME:GNOME','gnome'),('X-Cinnamon','cinnamon'),('KDE','kde'),
                                ('plasma','kde'),('LXQt','lxqt'),('XFCE','xfce'),('COSMIC','cosmic'),
                                ('Hyprland','hyprland'),('unknown','generic')]:
            self.assertEqual(session.detect_desktop({'XDG_CURRENT_DESKTOP':value}), expected)

    def test_kde_restores_original_and_retains_later_unrelated_edits(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d); paths=session.locations(home); p=paths['plasma']; p.parent.mkdir()
            original='# user settings\n[Formats]\nLANG=id_ID.UTF-8\nLC_ALL=C\n[Translations]\nLANGUAGE=id:en\n[Other]\nkeep=yes\n'
            p.write_text(original)
            session.change_user(home, True, 'kde')
            self.assertEqual(session.ini_value(p.read_text(),'Formats','LC_ALL'),'')
            self.assertEqual(session.ini_value(p.read_text(),'Translations','LANGUAGE'),'tet:pt:en')
            session.change_user(home, True, 'kde')
            session.change_user(home, False)
            self.assertEqual(p.read_text(), original)
            session.change_user(home, True, 'kde'); p.write_text(p.read_text()+'added=later\n')
            session.change_user(home, False)
            self.assertEqual(session.ini_value(p.read_text(),'Formats','LANG'),'id_ID.UTF-8')
            self.assertIn('added=later', p.read_text())
            self.assertIn('keep=yes', p.read_text())
            self.assertFalse(paths['plasma_env'].exists())

    def test_kde_conflicting_user_language_edit_aborts_all_changes(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d); paths=session.locations(home); session.change_user(home,True,'kde')
            p=paths['plasma']; p.write_text(session.ini_set(p.read_text(),'Formats','LANG','pt_PT.UTF-8'))
            before=paths['profile'].read_text()
            with self.assertRaises(RuntimeError): session.change_user(home,False)
            self.assertEqual(paths['profile'].read_text(),before)
            self.assertEqual(session.ini_value(p.read_text(),'Formats','LANG'),'pt_PT.UTF-8')

    def test_gnome_accounts_service_success_restore_and_conflict(self):
        current=['id_ID.UTF-8']
        def api(value=None):
            if value is None:return current[0]
            current[0]=value
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);session.change_user(home,True,'gnome',True,api)
            self.assertEqual(current[0],session.LANG)
            session.change_user(home,False,account_api=api)
            self.assertEqual(current[0],'id_ID.UTF-8')
            session.change_user(home,True,'gnome',True,api);current[0]='pt_PT.UTF-8'
            before=session.locations(home)['profile'].read_text()
            with self.assertRaises(RuntimeError):session.change_user(home,False,account_api=api)
            self.assertEqual(session.locations(home)['profile'].read_text(),before)
            self.assertEqual(current[0],'pt_PT.UTF-8')

    def test_accounts_service_failure_rolls_back_files(self):
        def api(value=None):
            if value is None:return 'en_US.UTF-8'
            raise RuntimeError('Denied')
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);p=home/'.profile';p.write_text('keep\n')
            with self.assertRaises(RuntimeError):session.change_user(home,True,'gnome',True,api)
            self.assertEqual(p.read_text(),'keep\n')
            self.assertFalse((home/'.xsessionrc').exists())
            self.assertFalse(session.locations(home)['env'].exists())
            self.assertFalse(session.locations(home)['journal'].exists())

    def test_write_failure_rolls_back_and_journal_is_private(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d);p=home/'.profile';p.write_text('before\n');p.chmod(0o644)
            actual=session.write; calls=[0]
            def fail_once(path, text):
                calls[0]+=1
                if calls[0]==2:raise OSError('Simulated disk error')
                actual(path,text)
            with patch.object(session,'write',fail_once):
                with self.assertRaises(OSError):session.change_user(home,True,'generic')
            self.assertEqual(p.read_text(),'before\n')
            session.change_user(home,True,'generic')
            self.assertEqual(stat.S_IMODE(session.locations(home)['journal'].stat().st_mode),0o600)
            self.assertEqual(stat.S_IMODE(p.stat().st_mode),0o644)
            session.change_user(home,False)

    def test_xdg_paths_and_parent_symlink_preflight(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d)/'home';home.mkdir();config=Path(d)/'config';state=Path(d)/'state'
            with patch.object(Path,'home',return_value=home), patch.dict(os.environ,{'XDG_CONFIG_HOME':str(config),'XDG_STATE_HOME':str(state)}):
                session.change_user(home,True,'generic')
                self.assertTrue((config/'environment.d/60-eduka-tet.conf').exists())
                self.assertTrue((state/'eduka-tet/session.json').exists())
                session.change_user(home,False)
        with tempfile.TemporaryDirectory() as d:
            home=Path(d)/'home';home.mkdir();outside=Path(d)/'outside';outside.mkdir()
            (home/'.config').symlink_to(outside)
            with self.assertRaises(RuntimeError):session.change_user(home,True,'generic')
            self.assertFalse((home/'.profile').exists())
            self.assertFalse(list(outside.iterdir()))

    def test_legacy_migration_and_exact_restore_without_final_newline(self):
        with tempfile.TemporaryDirectory() as d:
            home=Path(d); paths=session.locations(home); paths['env'].parent.mkdir(parents=True)
            paths['env'].write_text(session.LEGACY_ENV)
            paths['xsession'].write_text('custom\n'+session.BEGIN+'\nold data\n'+session.END+'\n')
            paths['profile'].write_text('export CUSTOM=yes')
            session.change_user(home,True,'generic');session.change_user(home,False)
            self.assertEqual(paths['profile'].read_text(),'export CUSTOM=yes')
            self.assertEqual(paths['xsession'].read_text(),'custom\n')
            self.assertFalse(paths['env'].exists())

    def test_reversed_markers_and_duplicate_ini_keys(self):
        with self.assertRaises(RuntimeError):session.strip_block(session.END+'\n'+session.BEGIN+'\n')
        with self.assertRaises(RuntimeError):session.ini_set('[Formats]\nLANG=C\nLANG=id_ID\n','Formats','LANG',session.LANG)
        with self.assertRaises(RuntimeError):session.ini_set('[Formats]\nkeep=yes\n[Formats]\nLANG=C\n','Formats','LANG',session.LANG)


if __name__=='__main__':unittest.main()
