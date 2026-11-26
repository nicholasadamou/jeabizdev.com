#!/usr/bin/env python3
"""Refresh the repository's release badge using the maintainer's gh login."""

import argparse
import html
import json
from pathlib import Path
import subprocess

INCLUDE_PRERELEASES = False


def api(*arguments):
    try:
        result = subprocess.run(
            ['gh', 'api', *arguments], text=True, capture_output=True, check=False, timeout=30,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError('GitHub release lookup timed out') from error
    if result.returncode:
        raise RuntimeError('GitHub release lookup failed; check gh authentication and repository access')
    response = json.loads(result.stdout)
    if isinstance(response, dict) and response.get('errors'):
        raise RuntimeError('GitHub could not resolve the repository release')
    return response


def latest(repository, include_prereleases=False):
    owner, name = repository.split('/', 1)
    query = '''query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) { latestRelease { tagName } }
    }'''
    data = api('graphql', '-f', 'query=' + query, '-f', 'owner=' + owner, '-f', 'name=' + name)
    repo = data['data']['repository']
    if repo is None:
        raise RuntimeError('Repository is inaccessible')
    release = repo['latestRelease']
    if include_prereleases:
        pages = api('--paginate', '--slurp', f'repos/{repository}/releases?per_page=100')
        releases = [item for page in pages for item in page if not item['draft']]
        return max(releases, key=lambda item: item['published_at'])['tag_name'] if releases else None
    return release['tagName'] if release else None


def render(tag):
    value = tag or 'no releases'
    escaped = html.escape(value, quote=True)
    value_width = max(28, len(value) * 7 + 12)
    width = 49 + value_width
    color = '#007ec6' if tag else '#9f9f9f'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="release: {escaped}">'
        f'<title>release: {escaped}</title>'
        f'<clipPath id="r"><rect width="{width}" height="20" rx="3"/></clipPath>'
        '<g clip-path="url(#r)"><rect width="49" height="20" fill="#555"/>'
        f'<rect x="49" width="{value_width}" height="20" fill="{color}"/></g>'
        '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        '<text x="24.5" y="14">release</text>'
        f'<text x="{49 + value_width / 2:g}" y="14">{escaped}</text>'
        '</g></svg>\n'
    )


def main(argv=None, root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', required=True, help='GitHub owner/repository')
    parser.add_argument('--include-prereleases', action='store_true', default=INCLUDE_PRERELEASES)
    parser.add_argument('--check', action='store_true', help='Fail on stale metadata without changing files')
    args = parser.parse_args(argv)
    if args.repository.count('/') != 1 or not all(args.repository.split('/')):
        parser.error('Expected owner/repository')
    svg = render(latest(args.repository, args.include_prereleases))
    path = (root or Path(__file__).resolve().parents[2]) / '.github/badges/release.svg'
    if path.exists() and path.read_text(encoding='utf-8') == svg:
        print('Release badge is current')
        return
    if args.check:
        raise RuntimeError('Release badge is stale; run this command without --check after publication')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding='utf-8')
    print('Updated .github/badges/release.svg; commit it, verify with Bellows, and push')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        raise SystemExit(str(error)) from None
