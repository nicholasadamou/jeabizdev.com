import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location('release_badge', Path(__file__).with_name('update-release-badge.py'))
badge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(badge)


class ReleaseBadgeTests(unittest.TestCase):
    def test_refresh_updates_only_the_local_badge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('Preserve existing work')
            with patch.object(badge, 'latest', return_value='v1.2.3') as lookup:
                badge.main(['--repository', 'private/project'], root)
            self.assertEqual((root / '.github/badges/release.svg').read_text(), badge.render('v1.2.3'))
            self.assertEqual((root / 'README.md').read_text(), 'Preserve existing work')
            lookup.assert_called_once_with('private/project', badge.INCLUDE_PRERELEASES)

    def test_current_badge_is_not_rewritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / '.github/badges/release.svg'
            path.parent.mkdir(parents=True)
            path.write_text(badge.render('v1.0.0'))
            before = path.stat().st_mtime_ns
            with patch.object(badge, 'latest', return_value='v1.0.0'):
                badge.main(['--repository', 'private/project', '--check'], root)
            self.assertEqual(path.stat().st_mtime_ns, before)

    def test_check_refuses_stale_metadata_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(badge, 'latest', return_value='v2.0.0'):
                with self.assertRaisesRegex(RuntimeError, 'stale'):
                    badge.main(['--repository', 'private/project', '--check'], root)
            self.assertEqual(list(root.iterdir()), [])

    def test_authentication_failure_preserves_the_existing_badge(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / '.github/badges/release.svg'
            path.parent.mkdir(parents=True)
            path.write_text('Previous metadata')
            with patch.object(badge, 'latest', side_effect=RuntimeError('inaccessible')):
                with self.assertRaisesRegex(RuntimeError, 'inaccessible'):
                    badge.main(['--repository', 'private/project'], root)
            self.assertEqual(path.read_text(), 'Previous metadata')

    def test_absent_release_and_xml_metacharacters_render_honestly(self):
        self.assertEqual(ET.fromstring(badge.render(None)).attrib['aria-label'], 'release: no releases')
        tag = 'v1<&"/><script>alert(1)</script>'
        root = ET.fromstring(badge.render(tag))
        self.assertEqual(root.attrib['aria-label'], 'release: ' + tag)
        self.assertEqual(root.findall('.//{http://www.w3.org/2000/svg}script'), [])

    def test_prerelease_lookup_excludes_drafts_and_reads_all_pages(self):
        pages = [[{'draft': True, 'tag_name': 'draft', 'published_at': None}], [
            {'draft': False, 'tag_name': 'v2-beta', 'published_at': '2026-11-25T00:00:00Z'},
            {'draft': False, 'tag_name': 'v1', 'published_at': '2026-10-01T00:00:00Z'},
        ]]
        def api(*args):
            if args[0] == 'graphql':
                return {'data': {'repository': {'latestRelease': {'tagName': 'v1'}}}}
            self.assertEqual(args, ('--paginate', '--slurp', 'repos/private/project/releases?per_page=100'))
            return pages
        with patch.object(badge, 'api', api):
            self.assertEqual(badge.latest('private/project', True), 'v2-beta')
            self.assertEqual(badge.latest('private/project'), 'v1')

    def test_inaccessible_repository_is_not_an_empty_release_feed(self):
        with patch.object(badge, 'api', return_value={'data': {'repository': None}}):
            with self.assertRaisesRegex(RuntimeError, 'inaccessible'):
                badge.latest('private/project')

    def test_transport_failure_does_not_disclose_authenticated_output(self):
        result = type('Result', (), {'returncode': 1, 'stdout': '', 'stderr': 'synthetic-secret'})()
        with patch.object(badge.subprocess, 'run', return_value=result):
            with self.assertRaises(RuntimeError) as caught:
                badge.api('graphql')
        self.assertNotIn('synthetic-secret', str(caught.exception))


if __name__ == '__main__':
    unittest.main()
