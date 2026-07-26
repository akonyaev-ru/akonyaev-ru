import math

def render_donut_chart(languages, x, y, radius, stroke_width):
    if not languages:
        return ""
    
    parts = []
    circumference = 2 * math.pi * radius
    current_offset = 0
    
    colors = ["var(--section)", "var(--key)", "var(--green)", "var(--accent)"]
    
    # Legend
    legend_x = x + radius + 30
    legend_y = y - radius + 10
    
    parts.append(f'<g transform="translate({x},{y}) rotate(-90)">')
    
    for i, lang in enumerate(languages):
        name = lang["name"]
        percent = lang["percent"]
        color = colors[i % len(colors)]
        
        dasharray = f"{circumference}"
        dashoffset = circumference - (percent / 100) * circumference
        
        # Add a tiny gap between segments if we want, but it's easier without
        # To rotate each segment, we use stroke-dashoffset but we also need to rotate the actual circle or adjust dashoffset correctly
        # Actually standard way: dasharray = "value rest", dashoffset = start_offset
        val = (percent / 100) * circumference
        rest = circumference - val
        
        # We need to rotate the group for each circle to start where the last one ended
        # Or easier: just use dasharray and offset.
        parts.append(
            f'<circle r="{radius}" cx="0" cy="0" fill="transparent" '
            f'stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-dasharray="{val} {rest}" '
            f'stroke-dashoffset="{-current_offset}"> '
            f'<title>{name}: {percent}%</title>'
            f'</circle>'
        )
        current_offset += val
        
        # Legend item
        parts.append(f'</g>') # close rotate group to add legend text normally
        
        ly = legend_y + i * 20
        parts.append(
            f'<circle cx="{legend_x}" cy="{ly-4}" r="5" fill="{color}"/>'
            f'<text x="{legend_x+12}" y="{ly}" fill="var(--ink)" font-size="12.5">{name} ({percent}%)</text>'
        )
        parts.append(f'<g transform="translate({x},{y}) rotate(-90)">') # reopen for next circle
        
    parts.append('</g>')
    return "".join(parts)

print(render_donut_chart([{"name": "Python", "percent": 60}, {"name": "JS", "percent": 40}], 100, 100, 40, 15))
