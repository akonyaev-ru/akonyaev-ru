import os, sys

with open('scripts/make_ascii_svg.py', 'r') as f:
    code = f.read()
code = code.replace('STATIC = bool(os.environ.get("STATIC"))', 'STATIC = True')
code = code.replace('parts.append("</svg>")', '''
# Eye highlights for testing
EYE1_X = PAD + 46 * CELL_W
EYE1_Y = art_top + 25 * CELL_H
EYE1_W = 7 * CELL_W
EYE1_H = 4 * CELL_H

EYE2_X = PAD + 56 * CELL_W
EYE2_Y = art_top + 25 * CELL_H
EYE2_W = 12 * CELL_W
EYE2_H = 4 * CELL_H

parts.append(f\'<rect x=\"{EYE1_X}\" y=\"{EYE1_Y}\" width=\"{EYE1_W}\" height=\"{EYE1_H}\" fill=\"red\" opacity=\"0.5\"/>\')
parts.append(f\'<rect x=\"{EYE2_X}\" y=\"{EYE2_Y}\" width=\"{EYE2_W}\" height=\"{EYE2_H}\" fill=\"blue\" opacity=\"0.5\"/>\')
parts.append("</svg>")
''')
with open('scratch/test_eyes.py', 'w') as f:
    f.write(code)
