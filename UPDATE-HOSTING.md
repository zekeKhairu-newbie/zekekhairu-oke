# Zeke Khairu Oke downloads and updates

The repository-only APK reads `asset-manifest.json` from the `main` branch of
`zekeKhairu-newbie/zekekhairu-oke`. It no longer fetches the Kara-Okay manifest.
Existing v1.5.6 APKs need a manual installation of the signed repository-only
candidate once; changing these JSON files cannot redirect old installed code.

## Current status

The legacy asset-manifest.json catalog is intentionally empty. This repository now hosts an independent-app starter catalog (see STARTER-PACK.md). The older release-only channel has the app APK
and a songbook, but does not use those independent-app starter packages.
Do not claim that Major, Dreamsam or the upstream song library is hosted here.
The candidate keeps an installed catalog when it receives an empty catalog,
and will not prune files based on an empty catalog. Its asset and APK URL
getters reject links outside this repository, including old cached upstream
links. Existing downloaded files can still be used; missing files will not be
fetched from Kara-Okay. Real-device migration testing is still required.

## App updates

`asset-manifest.json.app` uses these fields:

* `versionCode`: strictly increasing Android internal version code.
* `versionName`: visible version name.
* `apk`: HTTPS GitHub release-asset URL in this repository.
* `bytes`: exact APK byte length.
* `sha256`: lowercase SHA-256 of that APK.
* `page`: release page.
* `notes`: array of strings.
* `minSdk`: minimum Android API level.

The repository-only candidate retains version name `1.5.6`, with code `9` (logo-fix repo2).
Future updates must have a code greater than 9. Keep the application ID
`okay.kara` and the existing release signing certificate. Do not remove the
APK hash, package or signing checks. `apk-release.json` mirrors the app object;
`version.json` is maintained for compatibility with older custom tooling.
The stock-derived updater reads `asset-manifest.json`, not those two files.

Upload a signed APK as a GitHub release asset and verify its public URL before
advertising it in the manifest. A draft release asset is not publicly available.
Do not put keystores, passwords or access tokens in the repository.

## Songs, soundfonts and backgrounds

Obtain the actual files and redistribution permission before publishing them.
Use release assets for large files. Allowed initial download URL prefixes are:

* `https://github.com/zekeKhairu-newbie/zekekhairu-oke/releases/download/`
* `https://raw.githubusercontent.com/zekeKhairu-newbie/zekekhairu-oke/main/`

GitHub may redirect a release download to its own asset CDN normally.

Each manifest item needs `id`, `key`, `kind`, `name`, `bytes`, `sha256`, and `url`.
Kinds used by this app include `songs`, `soundfont`, and `video`. Match the
existing v1.5.6 item IDs, storage keys and package format when migrating files;
changing only a URL is insufficient if the downloaded content differs. An
SF2 must be a real soundfont; song packages must match the app's expected
archive format. Preserve relevant optional/default/category/base/layered fields
from a verified compatible catalog. Keep all desired catalog items when
publishing a populated catalog: the app's normal pruning can remove files
omitted from a nonempty catalog. Test this on backed-up device data first.

The empty catalog is update infrastructure, not a replacement song library.
