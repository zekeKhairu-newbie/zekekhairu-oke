"""Create original MIDI arrangements of three traditional/public-domain songs.

No Kara-Okay library files, recordings or soundfonts are used in these songs.
The new arrangements and generated MIDI data are dedicated to CC0-1.0.
"""
from pathlib import Path
import hashlib
import json
import struct
import zipfile

ROOT = Path(__file__).resolve().parent
PPQ = 480
TEMPO = 600000  # 100 beats/minute

def vlq(value):
    data = [value & 127]
    value >>= 7
    while value:
        data.insert(0, (value & 127) | 128)
        value >>= 7
    return bytes(data)

def meta(kind, text):
    data = text.encode('ascii') if isinstance(text, str) else text
    return bytes([255, kind]) + vlq(len(data)) + data

def track(events, finish):
    # Stable sorting preserves explicit same-time program/meta order.
    events = sorted(events, key=lambda event: event[0])
    output, previous = bytearray(), 0
    for tick, message in events:
        output.extend(vlq(tick - previous))
        output.extend(message)
        previous = tick
    output.extend(vlq(max(finish, previous) - previous))
    output.extend(meta(47, b''))
    return b'MTrk' + struct.pack('>I', len(output)) + output

def make_song(code, title, phrases):
    control = [(0, meta(3, title)), (0, meta(81, TEMPO.to_bytes(3, 'big'))),
               (0, meta(88, bytes([4, 2, 24, 8]))),
               (0, meta(1, '@KMIDI KARAOKE FILE')), (0, meta(1, '@V0100')),
               (0, meta(1, '@T' + title)), (0, meta(1, '@TTraditional')),
               (0, meta(2, 'New MIDI arrangement: CC0-1.0; Zeke starter pack'))]
    melody = [(0, meta(3, 'Melody')), (0, bytes([192, 0])),
              (0, bytes([176, 7, 90])), (0, bytes([176, 10, 64]))]
    backing = [(0, meta(3, 'Accompaniment')), (0, bytes([193, 24])),
               (0, bytes([194, 32])), (0, bytes([177, 7, 52])),
               (0, bytes([178, 7, 60]))]
    tick = PPQ * 4
    lyric_count = 0
    for line_index, (syllables, pitches, durations, chord) in enumerate(phrases):
        assert len(syllables) == len(pitches) == len(durations)
        phrase_start = tick
        for i, (syllable, pitch, beats) in enumerate(zip(syllables, pitches, durations)):
            duration = round(PPQ * beats)
            prefix = ('\\' if line_index == 0 else '/') if i == 0 else ''
            control.append((tick, meta(5, prefix + syllable)))
            melody.extend([(tick, bytes([144, pitch, 80])),
                           (tick + max(1, duration - 35), bytes([128, pitch, 0]))])
            lyric_count += 1
            tick += duration
        # A quiet guitar chord and bass pulse every two beats.
        pulse = phrase_start
        while pulse < tick:
            length = min(PPQ * 2, tick - pulse)
            for note in chord:
                backing.extend([(pulse, bytes([145, note, 45])),
                                (pulse + length - 30, bytes([129, note, 0]))])
            backing.extend([(pulse, bytes([146, chord[0] - 24, 52])),
                            (pulse + length - 30, bytes([130, chord[0] - 24, 0]))])
            pulse += PPQ * 2
    finish = tick + PPQ * 2
    midi = b'MThd' + struct.pack('>IHHH', 6, 1, 3, PPQ)
    midi += track(control, finish) + track(melody, finish) + track(backing, finish)
    filename = f'{code:05d} - {title} - Traditional.kar'
    (ROOT / filename).write_bytes(midi)
    return filename, midi, {'number': f'{code:05d}', 'title': title,
                          'artist': 'Traditional', 'lyric_events': lyric_count,
                          'seconds': round(finish / PPQ * TEMPO / 1e6, 2)}

C, F, G = [60, 64, 67], [60, 65, 69], [59, 62, 67]
twinkle = [
    (['Twin','kle ','twin','kle ','lit','tle ','star'], [60,60,67,67,69,69,67], [1]*6+[2], C),
    (['How ','I ','won','der ','what ','you ','are'], [65,65,64,64,62,62,60], [1]*6+[2], F),
    (['Up ','a','bove ','the ','world ','so ','high'], [67,67,65,65,64,64,62], [1]*6+[2], G),
    (['Like ','a ','dia','mond ','in ','the ','sky'], [67,67,65,65,64,64,62], [1]*6+[2], G),
]
twinkle += twinkle[:2]
mary = [
    (['Ma','ry ','had ','a ','lit','tle ','lamb'], [64,62,60,62,64,64,64], [1]*6+[2], C),
    (['Lit','tle ','lamb'], [62,62,62], [1,1,2], G),
    (['Lit','tle ','lamb'], [64,67,67], [1,1,2], C),
    (['Ma','ry ','had ','a ','lit','tle ','lamb'], [64,62,60,62,64,64,64], [1]*6+[2], C),
    (['Its ','fleece ','was ','white ','as ','snow'], [64,62,62,64,62,60], [1,1,1,1,1,3], C),
]
buns = [
    (['Hot ','cross ','buns'], [64,62,60], [1,1,2], C),
    (['Hot ','cross ','buns'], [64,62,60], [1,1,2], C),
    (['One ','a ','pen','ny ','two ','a ','pen','ny'], [60]*4+[62]*4, [.5]*8, G),
    (['Hot ','cross ','buns'], [64,62,60], [1,1,2], C),
]
results = [make_song(1, 'Twinkle Twinkle Little Star', twinkle),
           make_song(2, 'Mary Had a Little Lamb', mary),
           make_song(3, 'Hot Cross Buns', buns)]
credits = '''Zeke starter pack v1

Three new MIDI arrangements of traditional/public-domain melodies and words:
00001 Twinkle Twinkle Little Star (traditional melody; Jane Taylor, 1806 words)
00002 Mary Had a Little Lamb (traditional melody; Sarah Josepha Hale, 1830 words)
00003 Hot Cross Buns (traditional nursery rhyme)

These MIDI arrangements were newly generated for Zeke Khairu Oke; no upstream
Kara-Okay song files or recordings were copied. To the extent copyright applies
to this new arrangement work, it is dedicated to the public domain under CC0-1.0:
https://creativecommons.org/publicdomain/zero/1.0/

The separately downloaded GeneralUser GS soundfont is by S. Christian Collins,
and retains its own license. See GeneralUser-GS-LICENSE.txt and
https://github.com/mrbumpy409/GeneralUser-GS
It is not Major or Dreamsam.
'''
(ROOT / 'STARTER-CREDITS.txt').write_text(credits, encoding='utf-8')
with zipfile.ZipFile(ROOT / 'zeke-starter-songs-v1.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for filename, midi, details in results:
        archive.writestr('Zeke Starter/' + filename, midi)
    archive.writestr('STARTER-CREDITS.txt', credits)
    archive.writestr('GeneralUser-GS-LICENSE.txt', (ROOT / 'GeneralUser-GS-LICENSE.txt').read_bytes())
catalog = [details for _, _, details in results]
(ROOT / 'song-list.json').write_text(json.dumps(catalog, indent=2) + '\n')
print(json.dumps(catalog))
for filename in ('zeke-starter-songs-v1.zip', 'GeneralUser-GS.sf2'):
    data = (ROOT / filename).read_bytes()
    print(filename, len(data), hashlib.sha256(data).hexdigest())
