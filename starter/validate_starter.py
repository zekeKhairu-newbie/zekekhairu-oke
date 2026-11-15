"""Validate downloaded bank structure and independently parse generated MIDI."""
from pathlib import Path
import collections
import json
import struct
import zipfile

ROOT = Path(__file__).resolve().parent

def read_vlq(data, pos):
    value = 0
    for _ in range(4):
        byte = data[pos]
        pos += 1
        value = value * 128 + (byte & 127)
        if byte < 128:
            return value, pos
    raise AssertionError('Invalid MIDI variable-length quantity')

def inspect_midi(data):
    assert data[:4] == b'MThd'
    length, fmt, tracks, division = struct.unpack('>IHHH', data[4:14])
    assert (length, fmt, tracks, division) == (6, 1, 3, 480)
    pos, lyrics, pitches, finishes = 14, [], [], []
    for _ in range(tracks):
        assert data[pos:pos+4] == b'MTrk'
        size = struct.unpack('>I', data[pos+4:pos+8])[0]
        end = pos + 8 + size
        pos += 8
        tick, running, active, ended = 0, None, collections.Counter(), False
        while pos < end:
            delta, pos = read_vlq(data, pos)
            tick += delta
            status = data[pos]
            if status >= 128:
                pos += 1
                running = status if status < 240 else None
            else:
                assert running is not None
                status = running
            if status == 255:
                kind = data[pos]
                count, pos = read_vlq(data, pos+1)
                payload = data[pos:pos+count]
                pos += count
                if kind == 5:
                    lyrics.append((tick, payload.decode('ascii')))
                if kind == 47:
                    assert count == 0 and pos == end
                    ended = True
            else:
                assert 128 <= status < 240
                count = 1 if status >> 4 in (12,13) else 2
                payload = data[pos:pos+count]
                pos += count
                assert len(payload) == count and all(byte < 128 for byte in payload)
                channel = status & 15
                if status >> 4 == 9 and payload[1] != 0:
                    active[(channel,payload[0])] += 1
                    if channel == 0:
                        pitches.append(tick)
                elif status >> 4 == 8 or (status >> 4 == 9 and payload[1] == 0):
                    active[(channel,payload[0])] -= 1
                    assert active[(channel,payload[0])] >= 0
        assert ended and not any(active.values()), 'Unbalanced MIDI notes'
        finishes.append(tick)
    assert pos == len(data)
    assert [tick for tick,_ in lyrics] == pitches, 'Lyrics must align to melody attacks'
    assert len(set(finishes)) == 1
    assert lyrics[0][1].startswith('\\')
    assert any(text.startswith('/') for _,text in lyrics)
    return len(lyrics)

def chunks(data, start, end):
    pos = start
    while pos + 8 <= end:
        name, size = data[pos:pos+4], struct.unpack('<I', data[pos+4:pos+8])[0]
        stop = pos + 8 + size
        assert stop <= end
        yield name, pos+8, stop
        pos = stop + (size & 1)
    assert pos == end

sf = (ROOT / 'GeneralUser-GS.sf2').read_bytes()
assert sf[:4] == b'RIFF' and sf[8:12] == b'sfbk'
assert struct.unpack('<I',sf[4:8])[0] + 8 == len(sf)
phdr = None
for kind, start, end in chunks(sf,12,len(sf)):
    if kind == b'LIST' and sf[start:start+4] == b'pdta':
        for kind2, start2, end2 in chunks(sf,start+4,end):
            if kind2 == b'phdr':
                phdr = sf[start2:end2]
assert phdr is not None and len(phdr) % 38 == 0
presets = set()
for pos in range(0,len(phdr)-38,38):
    preset, bank = struct.unpack('<HH',phdr[pos+20:pos+24])
    presets.add((bank,preset))
assert all((0,preset) in presets for preset in (0,24,32)), 'Missing starter instruments'
songlist = json.loads((ROOT / 'song-list.json').read_text())
with zipfile.ZipFile(ROOT / 'zeke-starter-songs-v1.zip') as archive:
    assert archive.testzip() is None
    songs = [name for name in archive.namelist() if name.endswith('.kar')]
    assert len(songs) == 3
    for name, details in zip(songs,songlist):
        count = inspect_midi(archive.read(name))
        assert count == details['lyric_events']
        print(name, ':',count,'aligned lyric/melody events; balanced notes')
    assert 'GeneralUser-GS-LICENSE.txt' in archive.namelist()
print('SF2 valid RIFF structure;',len(presets),'presets; all three starter instruments available')
