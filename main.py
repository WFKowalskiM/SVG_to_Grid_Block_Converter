import xml.etree.ElementTree as ET

GRID_ROWS = 80 # Number of rows for map grid
GRID_COLS = 80 # Number of columns for map grid
svg_file = "./bigmap.svg" # map file

def get_svg_dimensions(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    tag = root.tag
    if '}' in tag:
        namespace = tag.split('}')[0].strip('{')
    else:
        namespace = ''

    width = root.attrib.get('width')
    height = root.attrib.get('height')

    return int(width) if width else None, int(height) if height else None

def parse_svg(svg_path):
    """Parse the SVG and extract lines and rectangles."""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    ns = {"svg": "http://www.w3.org/2000/svg"}

    # Extract lines
    lines = []
    for line in root.findall(".//svg:line", ns):
        x1 = float(line.get("x1", 0))
        y1 = float(line.get("y1", 0))
        x2 = float(line.get("x2", 0))
        y2 = float(line.get("y2", 0))
        lines.append(((x1, y1), (x2, y2)))

    # Extract rectangles
    rectangles = []
    for rect in root.findall(".//svg:rect", ns):
        x = float(rect.get("x", 0))
        y = float(rect.get("y", 0))
        width = float(rect.get("width", 0))
        height = float(rect.get("height", 0))
        if not width >= 9999.0 and not height >= 9999.0:
            rectangles.append((x, y, x + width, y + height))
    return lines, rectangles

def line_intersects_cell(line, cell_x, cell_y, cell_width, cell_height):
    """Check if a line intersects a grid cell."""
    (x1, y1), (x2, y2) = line
    cell_left = cell_x * cell_width
    cell_right = cell_left + cell_width
    cell_top = cell_y * cell_height
    cell_bottom = cell_top + cell_height

    def intersect(p1, p2, q1, q2):
        """Check if line segments p1-p2 and q1-q2 intersect."""
        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

    cell_edges = [
        ((cell_left, cell_top), (cell_right, cell_top)),  # Top
        ((cell_right, cell_top), (cell_right, cell_bottom)),  # Right
        ((cell_right, cell_bottom), (cell_left, cell_bottom)),  # Bottom
        ((cell_left, cell_bottom), (cell_left, cell_top)),  # Left
    ]

    for edge in cell_edges:
        if intersect((x1, y1), (x2, y2), *edge):
            return True

    return False

def rect_overlaps_cell(rect, cell_x, cell_y, cell_width, cell_height):
    """Check if a rectangle overlaps a grid cell."""
    x1, y1, x2, y2 = rect
    cell_left = cell_x * cell_width
    cell_right = cell_left + cell_width
    cell_top = cell_y * cell_height
    cell_bottom = cell_top + cell_height

    return not (
            x2 <= cell_left or  # Rectangle is completely left of the cell
            x1 >= cell_right or  # Rectangle is completely right of the cell
            y2 <= cell_top or  # Rectangle is completely above the cell
            y1 >= cell_bottom  # Rectangle is completely below the cell
    )
def get_unwalkable_cells(svg_path, image_width, image_height):
    """Determine unwalkable cells based on lines and rectangles in the SVG."""
    lines, rectangles = parse_svg(svg_path)

    cell_width = image_width / GRID_COLS
    cell_height = image_height / GRID_ROWS

    unwalkable_cells = set()

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            cell_key = f"{col},{row}"
            if cell_key in unwalkable_cells:
                continue

            for line in lines:
                if line_intersects_cell(line, col, row, cell_width, cell_height):
                    unwalkable_cells.add(f"{col},{row}")

            if cell_key not in unwalkable_cells:
                for rect in rectangles:
                    if rect_overlaps_cell(rect, col, row, cell_width, cell_height) and f"{col},{row}" not in unwalkable_cells:
                        unwalkable_cells.add(f"{col},{row}")
    return sorted(unwalkable_cells)

if __name__ == "__main__":
    image_width, image_height = get_svg_dimensions(svg_file)

    unwalkable_cells = get_unwalkable_cells(svg_file, image_width, image_height)

    # Output of unwalkable cells in the correct format for nav
    print("export const UNWALKABLE_CELLS = [")
    print(", ".join(f"'{cell}'" for cell in unwalkable_cells))
    print("];")
    print(len(unwalkable_cells))