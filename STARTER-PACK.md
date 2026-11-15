# Repository-only starter downloads

The independent Zeke app now has a starter download catalog in
`zeke-app-manifest.json`. App APK updates remain in this repository too.

On independent1/independent2, reopen Zeke and press **Download songs** or
**Resume**. If you already chose **Use my own songs**, use the download option
in Settings. No new APK is required for this catalog change. Allow about
31 MB to finish, then choose **Start singing**.

The three starter songs are 00001 Twinkle Twinkle Little Star, 00002 Mary Had a
Little Lamb, and 00003 Hot Cross Buns. They contain new MIDI arrangements and
timed lyrics. The included soundfont download is **GeneralUser GS v2.0.3** by
S. Christian Collins, not Major or Dreamsam. Select **Zeke Starter Sound -
GeneralUser GS** in Sound if necessary.

[Starter release and files](https://github.com/zekeKhairu-newbie/zekekhairu-oke/releases/tag/starter-pack-v1)

Every initial app download URL points to a release asset in this repository.
GitHub serves its release files through its own asset CDN normally. This does
not connect the app to Kara-Okay's asset server. The old `okay.kara` update
catalog has not been changed to the independent-app catalog.

Credits, license, source pin, song list and generation/validation scripts are
under `starter/`. The song ZIP and SF2 are release assets. They are stored in
the format expected by the existing pack loader, with exact byte counts and
SHA-256 in the manifest. Both required items must finish to make the built-in
startup readiness condition true. No fake completion flag is used.

This is a small starter/test library, not a copy of Kara-Okay's catalog. Keep
the soundfont license and contributor credit with redistributions. New MIDI
arrangements are dedicated to CC0-1.0. Future library packs must use unique
song codes and have compatible MIDI/KAR contents and distribution rights.

Before replacing this manifest, retain all existing catalog items you want
to keep: the app normally prunes files omitted from a nonempty catalog.
These downloads still need end-to-end testing on an Android phone.
