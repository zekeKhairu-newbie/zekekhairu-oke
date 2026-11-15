# Independent Zeke application

The independent Zeke app uses Android application ID `com.zekekhairu.oke`.
Its initial candidate is `v1.5.6-independent1`, visible version `1.5.6`,
internal version code `10`, signed with the original Zeke release key.

Install it manually as a new app alongside the old Zeke/Kara-Okay package.
Do not uninstall the working old app until needed data has been backed up,
transferred where supported, and tested. Private app data and downloads do
not migrate automatically. Re-select shared folders with Android's picker
or import compatible files through the app where supported.

The independent app reads `zeke-app-manifest.json`. Its app metadata is also
mirrored in `zeke-app-release.json`. The old `okay.kara` build keeps using
`asset-manifest.json`, `apk-release.json` and `version.json`; those files must
not advertise an APK with the new application ID. A different application ID
cannot be delivered as an ordinary update to an existing installation.

Future independent Zeke updates must keep `com.zekekhairu.oke`, the same Zeke
signing certificate and an increasing version code greater than 10. Publish
the APK release asset first, verify its size and SHA-256, then update
`zeke-app-manifest.json.app` and `zeke-app-release.json` together. A GitHub
release alone is insufficient for the in-app updater, which reads the JSON.

Provider authorities and install-result action use `com.zekekhairu.oke`.
The absolute implementation class names still use `okay.kara`, deliberately:
the audio native library depends on its JNI class names. Those internal
class names do not determine which installed Android application is updated.

The catalog remains empty: no upstream songs, Major, Dreamsam or background
packages have been copied into this repository. A fresh install needs your
own compatible files until repository-hosted packages are supplied. See
`UPDATE-HOSTING.md` for catalog format and hosting details, but use the
independent manifest and version sequence for this application ID.

This is a prerelease. Static APK checks do not substitute for side-by-side
installation, audio playback, import, permissions and future update testing
on Android. No device was connected during the build.
