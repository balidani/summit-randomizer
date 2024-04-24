import random
import struct

def generate_synth_patch_name():
    first_parts = [
      'bio', 'tri', 'synth', 'flu', 'modular', 'phase', 'nebula', 'gli', 'flam', 'plain', 'blip', 'grave', 'gravy', 'storm',
      'prism', 'slice', 'clav', 'frag', 'glum', 'grump', 'scrump', 'corp', 'thor', 'kling', 'plex', 'bro', 'drone', 'snare', 'crystal', 'blur', 'frozen', 'glow',
      'hoop', 'jolt', 'crack', 'morph', 'nova', 'prod', 'quart', 'riff', 'steel', 'thermo', 'warp', 'xeno', 'zoom',
      'ultra', 'super', 'mega', 'giga', 'terra', 'drip', 'slow', 'quick', 'math', 'pre', 'post', 'vax', 'vox', 'hex', 'fit', 'smooth',
      'cool', 'poop', 'rizz', 'jazz', 'swift', 'book', 'spell', 'wiz', 'sex', 'borg', 'lazy', 'hazy', 'fish', 'chicken', 'cheese', 'egg', 'spam',
      'over', 'under', 'mello', 'cloud', 'rev', 'cow', 'thunk', 'stub', 'cryo', 'crypto', 'small', 'dev', 'push', 'slip', 'string', 'brass', 'wind', 'awe',
      'para', 'saw', 'square', 'sine', 'volt', 'fuzz', 'funk', 'slam', 'swing', 'beat', 'roach', 'lick', 'joint',
      'poly', 'mono', 'sub', 'rizz', 'fenk', 'mid'
    ]
    last_parts = [
      'ex', 'sonar', 'ion', 'ium', 'burst', 'tron', 'delve', 'ty', 'sky', 'ious', 'uno', 'otto', 'kink', 'axis', 'muse', 'nitro', 
      'polar', 'quark', 'rune', 'solar', 'bus', 'verve', 'wisp', 'xylo', 'arp', 'swarm', 'vox', 'citron', 'ether', 
      'tale', 'space', 'core', 'havoc', 'less', 'haze', 'smack', 'slap', 'mirage', 'oble', 'opus', 'pixel', 'quint', 'ology', 'phobia', 
      'tempo', 'ior', 'pool', 'age', 'ear', 'jib', 'jig', 'hull', 'keel', 'pill', 'fill', 'tastic', 'phone', 'phony', 'odge', 'ed',
      'matic', 'ness', 'born', 'made', 'ish', 'ify', 'axe', 'est', 'juice', 'ful', 'some', 'sim', 'er', 'off', 'up', 'on', 'ette',
      'pope', 'hit', 'osaur', 'math',
    ]

    structure = [first_parts, last_parts]

    while True:
      last = None
      parts = []
      for part in structure:
        p = random.choice(part)
        if last and p.startswith(last[-1]):
          p = p[1:]
        parts.append(p)
        last = p

      name = ''.join(parts)
      name = name.replace('ae', 'e')
      name = name.capitalize()
      if len(name) <= 16:
        return name

_Byte = lambda x: lambda: struct.pack('B', x)
_TwoByte = lambda x, y: lambda: struct.pack('BB', x, y)
_Range = lambda x, y: lambda: struct.pack('B', random.randrange(x, y + 1))
_Choice = lambda *x: lambda: struct.pack('B', random.choice(x))

_Two = lambda x, y: lambda: x() + y()
_TwoRange = lambda x, y: _Two(_Range(x, y), _Byte(0x0))

_ALWAYS_CHOOSE_PARAMS = {
  0x6D: (2, b"Mixer Osc1", _TwoByte(0x7F, 0x40), _TwoRange(0x60, 0x7f)),
  0x6F: (2, b"Mixer Osc2", _TwoByte(0x7F, 0x40), _TwoRange(0x60, 0x7f)),
  0x71: (2, b"Mixer Osc3", _TwoByte(0x7F, 0x40), _TwoRange(0x60, 0x7f)),
  0x81: (2, b"Filter Frequency", _TwoByte(0x7f, 0x40), _TwoRange(0x30, 0x7f)),
  0x36: (1, b"Oscillator 1 Wave", _Byte(0x02), _Range(0x0, 0x04)),
  0x37: (1, b"Oscillator 1 Wave More", _Byte(0x04), _Range(0x04, 0x3f)),
  0x4B: (1, b"Oscillator 2 Wave", _Byte(0x02), _Range(0x0, 0x04)),
  0x4C: (1, b"Oscillator 2 Wave More", _Byte(0x04), _Range(0x04, 0x3f)),
  0x60: (1, b"Oscillator 3 Wave", _Byte(0x02), _Range(0x0, 0x04)),
  0x61: (1, b"Oscillator 3 Wave More", _Byte(0x04), _Range(0x04, 0x3f)),
  
  0xC7: (1, b"FX Bypass", _Byte(0x0), _Byte(0x0)), # 0x1
}

_MOD_MATRIX = {
  0xF9: (1, b"Mod Matrix Slot", _Byte(0x0), _Range(0x0, 0x0f)),
  0xFA: (1, b"Mod Matrix 1 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0xFB: (1, b"Mod Matrix 1 Source 2", _Byte(0x0), _Byte(0x0)),
  0xFC: (1, b"Mod Matrix 1 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0xFD: (1, b"Mod Matrix 1 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0xFE: (1, b"Mod Matrix 2 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0xFF: (1, b"Mod Matrix 2 Source 2", _Byte(0x0), _Byte(0x0)),
  0x100: (1, b"Mod Matrix 2 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x101: (1, b"Mod Matrix 2 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x102: (1, b"Mod Matrix 3 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x103: (1, b"Mod Matrix 3 Source 2", _Byte(0x0), _Byte(0x0)),
  0x104: (1, b"Mod Matrix 3 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x105: (1, b"Mod Matrix 3 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x106: (1, b"Mod Matrix 4 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x107: (1, b"Mod Matrix 4 Source 2", _Byte(0x0), _Byte(0x0)),
  0x108: (1, b"Mod Matrix 4 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x109: (1, b"Mod Matrix 4 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x10A: (1, b"Mod Matrix 5 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x10B: (1, b"Mod Matrix 5 Source 2", _Byte(0x0), _Byte(0x0)),
  0x10C: (1, b"Mod Matrix 5 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x10D: (1, b"Mod Matrix 5 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x10E: (1, b"Mod Matrix 6 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x10F: (1, b"Mod Matrix 6 Source 2", _Byte(0x0), _Byte(0x0)),
  0x110: (1, b"Mod Matrix 6 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x111: (1, b"Mod Matrix 6 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x112: (1, b"Mod Matrix 7 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x113: (1, b"Mod Matrix 7 Source 2", _Byte(0x0), _Byte(0x0)),
  0x114: (1, b"Mod Matrix 7 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x115: (1, b"Mod Matrix 7 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x116: (1, b"Mod Matrix 8 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  0x117: (1, b"Mod Matrix 8 Source 2", _Byte(0x0), _Byte(0x0)),
  0x118: (1, b"Mod Matrix 8 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x119: (1, b"Mod Matrix 8 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x11A: (1, b"Mod Matrix 9 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x11B: (1, b"Mod Matrix 9 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x11C: (1, b"Mod Matrix 9 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x11D: (1, b"Mod Matrix 9 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x11E: (1, b"Mod Matrix 10 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x11F: (1, b"Mod Matrix 10 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x120: (1, b"Mod Matrix 10 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x121: (1, b"Mod Matrix 10 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x122: (1, b"Mod Matrix 11 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x123: (1, b"Mod Matrix 11 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x124: (1, b"Mod Matrix 11 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x125: (1, b"Mod Matrix 11 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x126: (1, b"Mod Matrix 12 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x127: (1, b"Mod Matrix 12 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x128: (1, b"Mod Matrix 12 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x129: (1, b"Mod Matrix 12 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x12A: (1, b"Mod Matrix 13 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x12B: (1, b"Mod Matrix 13 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x12C: (1, b"Mod Matrix 13 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x12D: (1, b"Mod Matrix 13 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x12E: (1, b"Mod Matrix 14 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x12F: (1, b"Mod Matrix 14 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x130: (1, b"Mod Matrix 14 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x131: (1, b"Mod Matrix 14 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x132: (1, b"Mod Matrix 15 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x133: (1, b"Mod Matrix 15 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x134: (1, b"Mod Matrix 15 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x135: (1, b"Mod Matrix 15 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  # 0x136: (1, b"Mod Matrix 16 Source 1", _Byte(0x0), _Range(0x0, 0x17)),
  # 0x137: (1, b"Mod Matrix 16 Source 2", _Byte(0x0), _Byte(0x0)),
  # 0x138: (1, b"Mod Matrix 16 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x139: (1, b"Mod Matrix 16 Destination", _Byte(0x0), _Range(0x0, 0x30)),
  0x13A: (1, b"FX Mod Slot 1 Source 1", _Byte(0x0), _Range(0x0, 0x10)),
  0x13B: (1, b"FX Mod Slot 1 Source 2", _Byte(0x0), _Byte(0x0)),
  0x13C: (1, b"FX Mod Slot 1 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x13D: (1, b"FX Mod Slot 1 Destination", _Byte(0x0), _Range(0x0, 0x17)),
  0x13E: (1, b"FX Mod Slot 2 Source 1", _Byte(0x0), _Range(0x0, 0x10)),
  0x13F: (1, b"FX Mod Slot 2 Source 2", _Byte(0x0), _Byte(0x0)),
  0x140: (1, b"FX Mod Slot 2 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x141: (1, b"FX Mod Slot 2 Destination", _Byte(0x0), _Range(0x0, 0x17)),
  0x142: (1, b"FX Mod Slot 3 Source 1", _Byte(0x0), _Range(0x0, 0x10)),
  0x143: (1, b"FX Mod Slot 3 Source 2", _Byte(0x0), _Byte(0x0)),
  0x144: (1, b"FX Mod Slot 3 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x145: (1, b"FX Mod Slot 3 Destination", _Byte(0x0), _Range(0x0, 0x17)),
  0x146: (1, b"FX Mod Slot 4 Source 1", _Byte(0x0), _Range(0x0, 0x10)),
  0x147: (1, b"FX Mod Slot 4 Source 2", _Byte(0x0), _Byte(0x0)),
  0x148: (1, b"FX Mod Slot 4 Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0x149: (1, b"FX Mod Slot 4 Destination", _Byte(0x0), _Range(0x0, 0x17)),
}

# Size, name, default gen, random gen
_PARAMS = {
  # 0x0: (16, b"Patch name", None, None),
  # 0x10: (1, b"Patch Category", _Byte(0x0), _Byte(0x0)),
  # 0x11: (1, b"Patch Genre", _Byte(0x0), _Byte(0x0)),
  # 0x12: (1, b"Patch Version?", _Byte(0x01), _Byte(0x01)),
  # 0x20: (1, b"Voice Mode", _Byte(0x03), _Byte(0x03)),
  # 0x21: (1, b"Voice Unison", _Byte(0x0), _Byte(0x0)),
  # 0x22: (1, b"Voice Unison Detune", _Byte(0x19), _Byte(0x19)),
  # 0x23: (1, b"Voice Unison Spread", _Byte(0x0), _Byte(0x0)),
  # 0x24: (1, b"Voice Keyboard Octave", _Byte(0x40), _Byte(0x40)),
  # 0x25: (1, b"Glide Time", _Byte(0x3c), _Range(0x0, 0x7f)),
  # 0x26: (1, b"Voice Pre-Glide", _Byte(0x40), _Range(0x34, 0x4c)),
  # 0x27: (1, b"Glide On", _Byte(0x0), _Range(0x0, 0x01)),
  # 0x29: (1, b"Osc Common Diverge", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x2A: (1, b"Osc Common Drift", _Byte(0x0), _Range(0x0, 0x7f)),
  0x2B: (1, b"Osc Common Noise LPF", _Byte(0x7f), _Range(0x0, 0x7f)),
  0x2C: (1, b"OSC Common Noise HPF", _Byte(0x0), _Range(0x0, 0x7f)),
  0x2D: (1, b"Osc Common KeySync", _Byte(0x01), _Range(0x0, 0x01)),

  0x2E: (1, b"Oscillator 1 Range", _Byte(0x40), _Range(0x3f, 0x42)), # 16, 8, 4, 2
  # 0x2F: (2, b"Oscillator 1 Coarse", _TwoByte(0x40, 0x0), _TwoRange(0x3f, 0x41)),
  # 0x31: (2, b"Oscillator 1 Fine", _TwoByte(0x40, 0x0), _TwoRange(0x30, 0x50)),
  0x31: (2, b"Oscillator 1 Fine", _TwoByte(0x40, 0x0), _TwoRange(0x38, 0x48)),
  0x33: (1, b"Oscillator 1 ModEnv2>Pitch", _Byte(0x40), _Range(0x30, 0x50)),
  0x34: (2, b"Oscillator 1 LFO2 > Pitch", _TwoByte(0x40, 0x0), _Range(0x38, 0x48)),
  0x38: (1, b"Oscillator 1 Shape Source", _Byte(0x0), _Range(0x0, 0x02)),
  0x39: (1, b"Oscillator 1 Manual Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x3A: (1, b"Oscillator 1 ModEnv1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x3B: (1, b"Oscillator 1 LFO1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x3C: (1, b"Oscillator 1 Vsync", _Byte(0x0), _Range(0x0, 0x7f)),
  0x3D: (1, b"Oscillator 1 Saw Density", _Byte(0x0), _Range(0x0, 0x7f)),
  0x3E: (1, b"Oscillator 1 Saw Density Detune", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x3F: (1, b"Oscillator 1 Fixed Note", _Byte(0x0), _Byte(0x0)),
  0x40: (1, b"Oscillator 1 Bend Range", _Byte(0x4C), _Range(0x28, 0x58)),

  0x43: (1, b"Oscillator 2 Range", _Byte(0x40), _Range(0x3f, 0x42)),
  # 0x44: (2, b"Oscillator 2 Coarse", _TwoByte(0x40, 0x0), _TwoRange(0x0, 0x01)),
  0x46: (2, b"Oscillator 2 Fine", _TwoByte(0x40, 0x0), _TwoRange(0x38, 0x48)),
  0x48: (1, b"Oscillator 2 ModEnv2>Pitch", _Byte(0x40), _Range(0x30, 0x50)),
  0x49: (2, b"Oscillator 2 LFO2 > Pitch", _TwoByte(0x40, 0x0), _Range(0x38, 0x48)),
  0x4D: (1, b"Oscillator 2 Shape Source", _Byte(0x0), _Range(0x0, 0x02)),
  0x4E: (1, b"Oscillator 2 Manual Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x4F: (1, b"Oscillator 2 ModEnv1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x50: (1, b"Oscillator 2 LFO1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x51: (1, b"Oscillator 2 Vsync", _Byte(0x0), _Range(0x0, 0x7f)),
  0x52: (1, b"Oscillator 2 Saw Density", _Byte(0x0), _Range(0x0, 0x7f)),
  0x53: (1, b"Oscillator 2 Saw Density Detune", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x54: (1, b"Oscillator 2 Fixed Note", _Byte(0x0), _Byte(0x0)),
  0x55: (1, b"Oscillator 2 Bend Range", _Byte(0x4C), _Range(0x28, 0x58)),

  0x58: (1, b"Oscillator 3 Range", _Byte(0x40), _Range(0x3f, 0x42)),
  # 0x59: (2, b"Oscillator 3 Coarse", _TwoByte(0x40, 0x0), _TwoRange(0x0, 0x7f)),
  0x5B: (2, b"Oscillator 3 Fine", _TwoByte(0x40, 0x0), _TwoRange(0x38, 0x48)),
  0x5D: (1, b"Oscillator 3 ModEnv2>Pitch", _Byte(0x40), _Range(0x30, 0x50)),
  0x5E: (2, b"Oscillator 3 LFO2 > Pitch", _TwoByte(0x40, 0x0), _Range(0x38, 0x48)),
  0x62: (1, b"Oscillator 3 Shape Source", _Byte(0x0), _Range(0x0, 0x02)),
  0x63: (1, b"Oscillator 3 Manual Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x64: (1, b"Oscillator 3 ModEnv1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x65: (1, b"Oscillator 3 LFO1 > Shape", _Byte(0x40), _Range(0x0, 0x7f)),
  0x66: (1, b"Oscillator 3 Vsync", _Byte(0x0), _Range(0x0, 0x7f)),
  0x67: (1, b"Oscillator 3 Saw Density", _Byte(0x0), _Range(0x0, 0x7f)),
  0x68: (1, b"Oscillator 3 Saw Density Detune", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x69: (1, b"Oscillator 3 Fixed Note", _Byte(0x0), _Byte(0x0)),
  0x6A: (1, b"Oscillator 3 Bend Range", _Byte(0x4C), _Range(0x28, 0x58)),

  0x73: (2, b"Ring 1*2 Level", _TwoByte(0x0, 0x0), _TwoRange(0x0, 0x7f)),
  0x75: (2, b"Noise Level", _TwoByte(0x0, 0x0), _TwoRange(0x0, 0x7f)),
  # 0x77: (1, b"Mixer Patch Level", _Byte(0x40), _Range(0x0, 0x7f)),
  # 0x78: (1, b"Mixer VCA gain", _Byte(0x7f), _Range(0x0, 0x7f)),
  
  0x79: (1, b"Mixer FX Global Dry Level", _Byte(0x7f), _Range(0x0, 0x7f)),
  0x7A: (1, b"Mixer FX Global Wet Level", _Byte(0x7f), _Range(0x0, 0x7f)),
  0x7B: (1, b"Filter Overdrive", _Byte(0x0), _Range(0x0, 0x40)),
  0x7C: (1, b"Filter Post Drive", _Byte(0x0), _Range(0x0, 0x40)),
  0x7D: (1, b"Filter Slope", _Byte(0x01), _Range(0x0, 0x01)),
  # 0x7E: (1, b"Filter Shape", _Byte(0x0), _Range(0x0, 0x03)),
  0x7F: (1, b"Filter Key Tracking", _Byte(0x7f), _Range(0x0, 0x7f)),
  0x80: (1, b"Filter Resonance", _Byte(0x0), _Range(0x0, 0x7f)),
  0x83: (2, b"Filter LFO1 > Filter", _TwoByte(0x40, 0x0), _TwoRange(0x0, 0x7f)),
  0x85: (1, b"Filter Osc3 > Filter", _Byte(0x0), _Range(0x0, 0x7f)),
  0x86: (1, b"Filter Env Select", _Byte(0x01), _Range(0x0, 0x01)),
  0x87: (1, b"Filter AmpEnv > Filter", _Byte(0x40), _Range(0x0, 0x7f)),
  0x88: (1, b"Filter ModEnv1 > Filter", _Byte(0x40), _Range(0x0, 0x7f)),
  0x89: (1, b"Filter Divergence", _Byte(0x0), _Range(0x0, 0x7f)),

  # 0x8C: (1, b"Voice PanPosition", _Byte(0x40), _Range(0x0, 0x7f)),
  0x8D: (1, b"Voice SpreadMode", _Byte(0x0), _Range(0x0, 0x03)),
  # 0x90: (1, b"Amp Envelope Attack", _Byte(0x02), _Range(0x0, 0x7f)),
  # 0x91: (1, b"Amp Envelope Decay", _Byte(0x5a), _Range(0x0, 0x7f)),
  # 0x92: (1, b"Amp Envelope Sustain", _Byte(0x7f), _Range(0x0, 0x7f)),
  # 0x93: (1, b"Amp Envelope Release", _Byte(0x28), _Range(0x0, 0x7f)),
  0x94: (1, b"Amp Envelope Velocity", _Byte(0x40), _Range(0x0, 0x7f)),
  0x95: (1, b"Amp Envelope Trigger", _Byte(0x0), _Range(0x0, 0x01)),
  0x96: (1, b"Amp Envelope HoldTime", _Byte(0x0), _Range(0x0, 0x7f)),
  0x97: (1, b"Amp Envelope Repeats", _Byte(0x7f), _Range(0x01, 0x7f)),
  0x98: (1, b"Mod Envelope Select", _Byte(0x0), _Range(0x0, 0x01)),
  0x99: (1, b"Mod Envelope 1 Attack", _Byte(0x02), _Range(0x0, 0x7f)),
  0x9A: (1, b"Mod Envelope 1 Decay", _Byte(0x4b), _Range(0x0, 0x7f)),
  0x9B: (1, b"Mod Envelope 1 Sustain", _Byte(0x23), _Range(0x0, 0x7f)),
  0x9C: (1, b"Mod Envelope 1 Release", _Byte(0x2d), _Range(0x0, 0x7f)),
  0x9D: (1, b"Mod Envelope 1 Velocity", _Byte(0x40), _Range(0x0, 0x7f)),
  0x9E: (1, b"Mod Envelope 1 Trigger", _Byte(0x01), _Range(0x0, 0x01)),
  0x9F: (1, b"Mod Envelope 1 HoldTime", _Byte(0x0), _Range(0x0, 0x7f)),
  0xA0: (1, b"Mod Envelope 1 Repeats", _Byte(0x7f), _Range(0x01, 0x7f)),
  0xA1: (1, b"Mod Envelope 2 Attack", _Byte(0x02), _Range(0x0, 0x7f)),
  0xA2: (1, b"Mod Envelope 2 Decay", _Byte(0x4b), _Range(0x0, 0x7f)),
  0xA3: (1, b"Mod Envelope 2 Sustain", _Byte(0x23), _Range(0x0, 0x7f)),
  0xA4: (1, b"Mod Envelope 2 Release", _Byte(0x2d), _Range(0x0, 0x7f)),
  0xA5: (1, b"Mod Envelope 2 Velocity", _Byte(0x40), _Range(0x0, 0x7f)),
  0xA6: (1, b"Mod Envelope 2 Trigger", _Byte(0x01), _Range(0x0, 0x01)),
  0xA7: (1, b"Mod Envelope 2 HoldTime", _Byte(0x0), _Range(0x0, 0x7f)),
  0xA8: (1, b"Mod Envelope 2 Repeats", _Byte(0x7f), _Range(0x01, 0x7f)),
  0xA9: (1, b"LFO 1 Range", _Byte(0x0), _Range(0x00, 0x02)),
  0xAA: (2, b"LFO 1 Rate", _TwoByte(0x40, 0x0), _TwoRange(0x0, 0x7f)),
  0xAC: (1, b"LFO 1 Sync Rate", _Byte(0x10), _Range(0x0, 0x22)),
  0xAD: (1, b"LFO 1 Wave", _Byte(0x0), _Range(0x0, 0x03)),
  0xAE: (1, b"LFO 1 Phase", _Byte(0x0), _Range(0x0, 0x78)),
  0xAF: (1, b"LFO 1 Slew", _Byte(0x0), _Range(0x0, 0x7f)),
  0xB0: (1, b"LFO 1 Fade Time", _Byte(0x0), _Range(0x0, 0x7f)),
  0xB1: (1, b"LFO 1 Fade In/Out", _Byte(0x0), _Range(0x0, 0x03)),
  0xB2: (1, b"LFO 1 Fade Sync", _Byte(0x0), _Range(0x0, 0x01)),
  0xB3: (1, b"LFO 1 MonoTrig", _Byte(0x0), _Range(0x0, 0x01)),
  0xB4: (1, b"LFO 1 Repeats", _Byte(0x0), _Range(0x0, 0x7f)),
  0xB5: (1, b"LFO 1 Common", _Byte(0x0), _Range(0x0, 0x01)),
  0xB7: (1, b"LFO 2 Range", _Byte(0x0), _Range(0x0, 0x02)),
  0xB8: (2, b"LFO 2 Rate", _TwoByte(0x40, 0x0), _TwoRange(0x0, 0x7f)),
  0xBA: (1, b"LFO 2 Sync Rate", _Byte(0x10), _Range(0x0, 0x22)),
  0xBB: (1, b"LFO 2 Wave", _Byte(0x0), _Range(0x0, 0x03)),
  0xBC: (1, b"LFO 2 Phase", _Byte(0x0), _Range(0x0, 0x78)),
  0xBD: (1, b"LFO 2 Slew", _Byte(0x0), _Range(0x0, 0x7f)),
  0xBE: (1, b"LFO 2 Fade Time", _Byte(0x0), _Range(0x0, 0x7f)),
  0xBF: (1, b"LFO 2 Fade In/Out", _Byte(0x0), _Range(0x0, 0x03)),
  0xC0: (1, b"LFO 2 Fade Sync", _Byte(0x0), _Range(0x0, 0x01)),
  0xC1: (1, b"LFO 2 MonoTrig", _Byte(0x0), _Range(0x0, 0x01)),
  0xC2: (1, b"LFO 2 Repeats", _Byte(0x0), _Range(0x0, 0x7f)),
  0xC3: (1, b"LFO 2 Common", _Byte(0x0), _Range(0x0, 0x01)),
  0xC5: (1, b"Distortion level", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0xC7: (1, b"FX Bypass", _Byte(0x0), _Byte(0x01)),
  0xC8: (1, b"FX Global Routing", _Byte(0x0), _Range(0x0, 0x06)),
  0xCA: (1, b"Delay Level", _Byte(0x0), _Range(0x0, 0x7f)),
  0xCB: (1, b"Delay Time", _Byte(0x40), _Range(0x0, 0x7f)),
  0xCC: (1, b"Delay LR Ratio", _Byte(0x0), _Range(0x0, 0x0a)),
  0xCD: (1, b"Delay Width", _Byte(0x7f), _Range(0x0, 0x7f)),
  0xCE: (1, b"Delay Sync", _Byte(0x0), _Range(0x0, 0x01)),
  0xCF: (1, b"Delay Sync Time", _Byte(0x07), _Range(0x0, 0x12)),
  0xD0: (1, b"Delay Feedback", _Byte(0x40), _Range(0x0, 0x7f)),
  0xD1: (1, b"Delay LP Damp", _Byte(0x55), _Range(0x0, 0x7f)),
  0xD2: (1, b"Delay HP Damp", _Byte(0x0), _Range(0x0, 0x7f)),
  0xD3: (1, b"Delay Slew Rate", _Byte(0x20), _Range(0x0, 0x7f)),
  0xD4: (1, b"Delay TimeMode", _Byte(0x0), _Range(0x0, 0x03)),
  0xD7: (1, b"Reverb Level", _Byte(0x0), _Range(0x0, 0x7f)),
  0xD8: (1, b"Reverb Type", _Byte(0x01), _Range(0x0, 0x02)),
  0xD9: (1, b"Reverb Time", _Byte(0x5a), _Range(0x0, 0x7f)),
  0xDA: (1, b"Reverb Damping LP", _Byte(0x32), _Range(0x0, 0x7f)),
  0xDB: (1, b"Reverb Damping HP", _Byte(0x01), _Range(0x0, 0x7f)),
  0xDC: (1, b"Reverb Size", _Byte(0x40), _Range(0x0, 0x7f)),
  0xDD: (1, b"Reverb Mod", _Byte(0x40), _Range(0x0, 0x7f)),
  0xDE: (1, b"Reverb Mod Rate", _Byte(0x04), _Range(0x0, 0x7f)),
  0xDF: (1, b"Reverb Low Pass", _Byte(0x4a), _Range(0x0, 0x7f)),
  0xE0: (1, b"Reverb High Pass", _Byte(0x0), _Range(0x0, 0x7f)),
  0xE1: (1, b"Reverb Pre Delay", _Byte(0x28), _Range(0x0, 0x7f)),
  0xE3: (1, b"Chorus Level", _Byte(0x0), _Range(0x0, 0x7f)),
  0xE4: (1, b"Chorus Type", _Byte(0x01), _Range(0x0, 0x02)),
  0xE5: (1, b"Chorus Rate", _Byte(0x14), _Range(0x0, 0x7f)),
  0xE6: (1, b"Chorus Mod Depth", _Byte(0x40), _Range(0x0, 0x7f)),
  0xE7: (1, b"Chorus Feedback", _Byte(0x40), _Range(0x0, 0x7f)),
  0xE8: (1, b"Chorus LP", _Byte(0x5a), _Range(0x0, 0x7f)),
  0xE9: (1, b"Chorus HP", _Byte(0x02), _Range(0x0, 0x7f)),
  0xEA: (1, b"Chorus Mode", _Byte(0x0), _Range(0x0, 0x02)),
  0xEB: (2, b"Clock Rate", _TwoByte(0x3c, 0x00), _TwoRange(0x14, 0x78)),
  0xED: (1, b"Arp Clock Sync Rate", _Byte(0x03), _Range(0x0, 0x12)),
  0xEE: (1, b"Arp Type", _Byte(0x0), _Range(0x0, 0x06)),
  0xEF: (1, b"Arp Rythm", _Byte(0x0), _Range(0x0, 0x20)),
  0xF0: (1, b"Arp Octave", _Byte(0x0), _Range(0x0, 0x06)),
  0xF1: (1, b"Arp Clock Gate", _Byte(0x40), _Range(0x0, 0x7f)),
  0xF2: (1, b"Arp Clock Swing", _Byte(0x32), _Range(0x14, 0x50)),
  # 0xF3: (1, b"Arp Clock On", _Byte(0x0), _Range(0x0, 0x01)),
  # 0xF4: (1, b"Key Latch", _Byte(0x0), _Range(0x0, 0x01)),
  0xF5: (1, b"Arp KeySync", _Byte(0x0), _Range(0x0, 0x01)),
  0xF6: (1, b"Arp Velocity Mode", _Byte(0x0), _Range(0x0, 0x01)),

  # 0xF7: (1, b"Animate 1 Hold", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0xF8: (1, b"Animate 2 Hold", _Byte(0x0), _Range(0x0, 0x7f)),

  0x15A: (1, b"LFO 3 Wave", _Byte(0x0), _Range(0x0, 0x03)),
  0x15B: (1, b"LFO 3 Rate", _Byte(0x40), _Range(0x0, 0x7f)),
  0x15C: (1, b"LFO 3 RateSync", _Byte(0x10), _Range(0x0, 0x22)),
  0x15D: (1, b"LFO 4 Wave", _Byte(0x0), _Range(0x0, 0x03)),
  0x15E: (1, b"LFO 4 Rate", _Byte(0x40), _Range(0x0, 0x7f)),
  0x15F: (1, b"LFO 4 RateSync", _Byte(0x10), _Range(0x0, 0x22)),
  
  # 0x160: (1, b"OSC Common Tuning Table", _Byte(0x0), _Byte(0x0)),
  
  0x163: (1, b"Filter Shape Dual", _Byte(0x0), _Range(0x0, 0x08)),
  0x164: (1, b"Filter Frequency Separation", _Byte(0x40), _Range(0x0, 0x7f)),
  
  # 0x165: (1, b"Audio Input", _Byte(0x0), _Byte(0x0)),
  
  0x166: (1, b"FM OSC3->1 Switch", _Byte(0x0), _Range(0x0, 0x02)),
  0x167: (1, b"FM OSC3->1 Manual Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  0x168: (1, b"FM OSC3->1 Mod Env 2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  0x169: (1, b"FM OSC3->1 LFO2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  
  # 0x16A: (1, b"FM OSC1->2 Switch", _Byte(0x0), _Range(0x0, 0x02)),
  # 0x16B: (1, b"FM OSC1->2 Manual Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x16C: (1, b"FM OSC1->2 Mod Env 2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x16D: (1, b"FM OSC1->2 LFO2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),

  # 0x16E: (1, b"FM OSC2->3 Switch", _Byte(0x0), _Range(0x0, 0x02)),
  # 0x16F: (1, b"FM OSC2->3 Manual Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x170: (1, b"FM OSC2->3 Mod Env 2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x171: (1, b"FM OSC2->3 LFO2 Amount", _Byte(0x0), _Range(0x0, 0x7f)),
  
  0x172: (1, b"LFO 3/4 Select", _Byte(0x0), _Range(0x0, 0x01)),
  0x173: (1, b"LFO 3 Sync", _Byte(0x0), _Range(0x0, 0x01)),
  0x174: (1, b"LFO 4 Sync", _Byte(0x0), _Range(0x0, 0x01)),
  0x175: (1, b"Amp Envelope Loop", _Byte(0x0), _Range(0x0, 0x01)),
  0x176: (1, b"Mod Envelope 1 Loop", _Byte(0x0), _Range(0x0, 0x01)),
  0x177: (1, b"Mod Envelope 2 Loop", _Byte(0x0), _Range(0x0, 0x01)),

  # 0x178: (1, b"Amp Envelope Delay", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x179: (1, b"Mod Envelope 1 Delay", _Byte(0x0), _Range(0x0, 0x7f)),
  # 0x17A: (1, b"Mod Envelope 2 Delay", _Byte(0x0), _Range(0x0, 0x7f)),
  
  0x17B: (1, b"Arp Chance", _Byte(0x64), _Range(0x0a, 0x64)),
  0x17C: (1, b"Animate 1 Envelope Attack", _Byte(0x0), _Range(0x0, 0x7f)),
  0x17D: (1, b"Animate 1 Envelope Release", _Byte(0x0), _Range(0x0, 0x7f)),
  0x17E: (1, b"Animate 2 Envelope Attack", _Byte(0x0), _Range(0x0, 0x7f)),
  0x17F: (1, b"Animate 2 Envelope Release", _Byte(0x0), _Range(0x0, 0x7f)),
  0x180: (1, b"LFO3 Phase", _Byte(0x0), _Range(0x0, 0x78)),
  0x181: (1, b"LFO3 Slew", _Byte(0x0), _Range(0x0, 0x7f)),
  0x182: (1, b"LFO3 Fadetime", _Byte(0x0), _Range(0x0, 0x7f)),
  0x183: (1, b"LFO4 Phase", _Byte(0x0), _Range(0x0, 0x78)),
  0x184: (1, b"LFO4 Slew", _Byte(0x0), _Range(0x0, 0x7f)),
  0x185: (1, b"LFO4 Fadetime", _Byte(0x0), _Range(0x0, 0x7f)),
}

_TEMPLATE = b'\xf0\x00 )\x01\x11\x013\x01\x00\x00\x00\x01\x00\x00\x00Init Patch      \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x19\x00@<@\x00\x00\x00\x00\x7f\x00\x00@@\x00@\x00@@\x00\x02\x04\x00@@@\x00\x00@\x00L\x00\x00@@\x00@\x00@@\x00\x02\x04\x00@@@\x00\x00@\x00L\x00\x00@@\x00@\x00@@\x00\x02\x04\x00@@@\x00\x00@\x00L\x00\x00\x7f@\x00\x00\x00\x00\x00\x00\x00\x00@\x7f\x7f\x7f\x00\x00\x01\x00\x7f\x00\x7f@@\x00\x00\x01@@\x00\x00\x00@\x00\x00\x00\x02Z\x7f(@\x00\x00\x03\x00\x02K#-@\x01\x00\x03\x02K#-@\x01\x00\x03\x00@\x00\x10\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00@\x00\x10\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x7f\x00\x07@U\x00 \x00\x00\x00\x00\x01Z2\x01@@\x04J\x00(\x00\x00\x01\x14@@Z\x02\x00<\x00\x03\x00\x00\x00@2\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00\x00@\x00\x00@\x10\x00@\x10\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Init Patch      @\x7f\x00<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf7'

# log = {}

new_bank = []
offset = 0x10

for pp in range(128):
  patch_log = {}

  new_patch = list(_TEMPLATE)
  new_patch[13] = pp
  new_name = generate_synth_patch_name().capitalize()
  if len(new_name) > 16:
    raise 1
  for i in range(16):
    new_patch[0x10 + i] = ord(f"{new_name:16s}"[i])

  def Edit(item):
    ptr, param = item
    size, name, unused_make_default, make_random = param
    new_value = make_random()
    patch_log[name] = new_value.hex()

    for i, b in enumerate(new_value):
      new_patch[offset + ptr + i] = b

  for ptr, param in _ALWAYS_CHOOSE_PARAMS.items():
    Edit((ptr, param))

  # if pp > 64:
  for ptr, param in _MOD_MATRIX.items():
    Edit((ptr, param))

  for edit in range(64 + pp):
    item = random.choice(list(_PARAMS.items()))
    Edit(item)

  new_bank.extend(new_patch[:])
  # log[f'patch {pp:03d}'] = patch_log

bank_bytes = b''.join(map(lambda b: bytes([b]), new_bank))
with open('random.syx', 'wb') as f:
  f.write(bank_bytes)

# with open('log.txt', 'w') as f:
#   f.write(str(log))
