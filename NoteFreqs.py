# -*- coding: utf-8 -*-
base_freq = 440

octaves = 3
notes = 12  # TODO Make a list of the notes instead

factor = 2 ** (1 / notes)
print("factor : ", factor)


def freq_from_a4(steps_up):
    return base_freq * (2 ** (1 / notes)) ** steps_up


print("freq + 12 : ", freq_from_a4(12))
cur_note = base_freq

for octave in range(0, octaves):
    all_notes = ""

    for note in range(0, notes):
        all_notes += str(cur_note) + ", "
        cur_note *= factor

    print("octave " + str(octave) + " : " + all_notes)
