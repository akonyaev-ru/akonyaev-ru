import os

with open('scripts/make_ascii_svg.py', 'r') as f:
    code = f.read()

start_idx = code.find('# eye blink animation')
end_idx = code.find('parts.append("</svg>")')
if start_idx != -1:
    code = code[:start_idx] + code[end_idx:]

css_insert = '''
  @keyframes portrait-zoom {
    0%, 70%, 100% { transform: scale(1); }
    75%, 95% { transform: scale(3.5); }
  }
  @keyframes sparkle-anim {
    0%, 78%, 90%, 100% { opacity: 0; transform: scale(0) rotate(0deg); }
    84% { opacity: 1; transform: scale(1) rotate(90deg); }
  }
  #portrait-layer {
    transform-origin: 604px 322px;
    animation: portrait-zoom 10s ease-in-out infinite;
  }
  #sparkle {
    transform-origin: 604px 322px;
    animation: sparkle-anim 10s ease-in-out infinite;
  }
'''
code = code.replace('</style>', css_insert + '</style>')

start_g = 'parts.append(\'<g id="portrait-layer">\')'
code = code.replace('for ry, line in enumerate(rows_txt):', start_g + '\nfor ry, line in enumerate(rows_txt):')

status_start = 'status_line_y = TITLEBAR_H + ART_H + PAD * 0.35'
sparkle_svg = '''
parts.append('</g>')
# Add a sparkle star
parts.append('<path id="sparkle" d="M604,302 Q604,322 584,322 Q604,322 604,342 Q604,322 624,322 Q604,322 604,302 Z" fill="#fff"/>')
'''
code = code.replace(status_start, sparkle_svg + '\n' + status_start)

with open('scratch/test_zoom.py', 'w') as f:
    f.write(code)
