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
