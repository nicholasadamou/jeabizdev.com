# Release badges and local validation

The README uses a repository-hosted SVG, refreshed locally after publishing a
release. GitHub Actions runs CI on standard GitHub-hosted Ubuntu runners. Bellows remains
available for local badge validation.

```sh
python3 .github/scripts/update-release-badge.py \
  --repository nicholasadamou/jeabizdev.com
python3 .github/scripts/update-release-badge.py \
  --repository nicholasadamou/jeabizdev.com --check
bellows --repo .github/scripts run \
  --workflow .bellows/workflows/release-badges.yml --job release-badges
```

The helper uses your existing `gh` login and changes only the local
`.github/badges/release.svg`. Commit the refreshed SVG after publication.
A missing release displays “no releases”; `--check` fails on stale metadata
or inaccessible releases without writing.
The version follows GitHub’s latest stable release.

The scoped Bellows workflow runs eight offline badge tests in a pinned container
without GitHub credentials. It lives outside `.github/workflows` and is never
scheduled by GitHub Actions. Run the repository’s normal local validation before
pushing as well. Hosted CI gates automatic release publication; the local badge tools remain
available for refreshing the README badge after a release.
