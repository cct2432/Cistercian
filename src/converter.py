def to_cis(number: int) -> str:
  if isinstance(number, bool) or not isinstance(number, int):
    raise TypeError("Input must be an integer")
  if not (0 <= number <= 9999):
    raise ValueError("Input must be between 0000 and 9999")
  
  thousands = number // 1000
  hundreds = (number % 1000) // 100
  tens = (number % 100) // 10
  ones = number % 10
  digits = [thousands, hundreds, tens, ones]

  STROKE_MAP = {
    1: [((0, 0), (30, 0))],
    2: [((0, 25), (30, 25))],
    3: [((0, 0), (30, 25))],
    4: [((0, 25), (30, 0))],
    5: [((0, 0), (30, 0)), ((0, 25), (30, 0))],
    6: [((30, 0), (30, 25))],
    7: [((0, 0), (30, 0)), ((30, 0), (30, 25))],
    8: [((0, 25), (30, 25)), ((30, 0), (30, 25))],
    9: [((0, 0), (30, 0)), ((0, 25), (30, 25)), ((30, 0), (30, 25))],
  }

  QUADRANTS = [
    (-1, -1, 50, 90), (1, -1, 50, 90), (-1, 1, 50, 10), (1, 1, 50 ,10),
    ]

  # Center Line
  lines = [
    '<line x1="50" y1="10" x2="50" y2="90" stroke="black" stroke-width="4" stroke-linecap="round"/>'
  ]

  # Building Quadrants
  for digit, (sx, sy, ox, oy) in zip(digits, QUADRANTS):
    if digit in STROKE_MAP:
      for (x1, y1), (x2, y2) in STROKE_MAP[digit]:
        fx1 = ox + (x1 * sx)
        fy1 = oy + (y1 * sy)
        fx2 = ox + (x2 * sx)
        fy2 = oy + (y2 * sy)

        lines.append(
          f'<line x1="{fx1}" y1="{fy1}" x2="{fx2}" y2="{fy2}" stroke="black" stroke-width="4" stroke-linecap="round"/>'
        )
  # Build SVG
  svg_body = "\n  ".join(lines)
  return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">\n {svg_body}\n</svg>'

import re

def from_cis(svg_string: str) -> int:
    if not isinstance(svg_string, str):
        raise TypeError("Input must be an SVG string.")

    REVERSE_MAP = {
        frozenset({((0, 0), (30, 0))}): 1,
        frozenset({((0, 25), (30, 25))}): 2,
        frozenset({((0, 0), (30, 25))}): 3,
        frozenset({((0, 25), (30, 0))}): 4,
        frozenset({((0, 0), (30, 0)), ((0, 25), (30, 0))}): 5, # Matches your (30, 0)
        frozenset({((30, 0), (30, 25))}): 6,
        frozenset({((0, 0), (30, 0)), ((30, 0), (30, 25))}): 7,
        frozenset({((0, 25), (30, 25)), ((30, 0), (30, 25))}): 8,
        frozenset({((0, 0), (30, 0)), ((0, 25), (30, 25)), ((30, 0), (30, 25))}): 9,
    }

    line_pattern = re.compile(r'<line\s+x1="(\d+)"\s+y1="(\d+)"\s+x2="(\d+)"\s+y2="(\d+)"')
    matches = line_pattern.findall(svg_string)

    quadrant_lines = {1000: set(), 100: set(), 10: set(), 1: set()}

    for match in matches:
        x1, y1, x2, y2 = map(int, match)
      
        # Skip Center Line
        if (x1, x2) == (50, 50) and (y1, y2) in [(10, 90), (90, 10)]:
            continue
        
        # Find Quadrant
        if max(y1, y2) > 50 and min(x1, x2) < 50:
            ox, oy, sx, sy, place = 50, 90, -1, -1, 1000
        elif max(y1, y2) > 50 and max(x1, x2) > 50:
            ox, oy, sx, sy, place = 50, 90, 1, -1, 100
        elif min(y1, y2) < 50 and min(x1, x2) < 50:
            ox, oy, sx, sy, place = 50, 10, -1, 1, 10
        elif min(y1, y2) < 50 and max(x1, x2) > 50:
            ox, oy, sx, sy, place = 50, 10, 1, 1, 1
        else:
            continue

        local_x1, local_y1 = (x1 - ox) // sx, (y1 - oy) // sy
        local_x2, local_y2 = (x2 - ox) // sx, (y2 - oy) // sy

        local_line = tuple(sorted(((local_x1, local_y1), (local_x2, local_y2))))
        quadrant_lines[place].add(local_line)

    total = 0
    for place, lines in quadrant_lines.items():
        if not lines:
            continue # Digit is 0
        
        digit = REVERSE_MAP.get(frozenset(lines))
        if digit is None:
            raise ValueError(f"Unrecognized geometry found in the {place}s quadrant.")
        
        total += digit * place

    return total
