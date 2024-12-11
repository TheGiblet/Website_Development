import random
from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk

def check_overlap(shape1, shape2):
    """Checks if two shapes overlap."""

    if shape1[0] == 'circle' and shape2[0] == 'circle':
        # Circle-circle overlap
        distance = ((shape1[1][0] - shape2[1][0])**2 + (shape1[1][1] - shape2[1][1])**2)**0.5
        return distance < shape1[2] + shape2[2]

    elif shape1[0] == 'circle' and shape2[0] == 'rectangle':
        # Circle-rectangle overlap
        cx, cy = shape1[1]
        rx1, ry1, rx2, ry2 = shape2[1][0][0], shape2[1][0][1], shape2[1][1][0], shape2[1][1][1]
        closest_x = max(rx1, min(cx, rx2))
        closest_y = max(ry1, min(cy, ry2))
        distance = ((cx - closest_x)**2 + (cy - closest_y)**2)**0.5
        return distance < shape1[2]

    elif shape1[0] == 'rectangle' and shape2[0] == 'circle':
        # Rectangle-circle overlap (same logic as circle-rectangle)
        return check_overlap(shape2, shape1)

    elif shape1[0] == 'circle' and shape2[0] == 'triangle':
        # Circle-triangle overlap (simplified - checks if circle center is inside triangle)
        cx, cy = shape1[1]
        x1, y1, x2, y2, x3, y3 = shape2[1][0][0], shape2[1][0][1], shape2[1][1][0], shape2[1][1][1], shape2[1][2][0], shape2[1][2][1]
        return point_in_triangle(cx, cy, x1, y1, x2, y2, x3, y3)

    elif shape1[0] == 'triangle' and shape2[0] == 'circle':
        # Triangle-circle overlap
        return check_overlap(shape2, shape1)

    elif shape1[0] == 'rectangle' and shape2[0] == 'rectangle':
        # Rectangle-rectangle overlap
        r1x1, r1y1, r1x2, r1y2 = shape1[1][0][0], shape1[1][0][1], shape1[1][1][0], shape1[1][1][1]
        r2x1, r2y1, r2x2, r2y2 = shape2[1][0][0], shape2[1][0][1], shape2[1][1][0], shape2[1][1][1]
        return not (r1x2 < r2x1 or r1x1 > r2x2 or r1y2 < r2y1 or r1y1 > r2y2)

    elif shape1[0] == 'triangle' and shape2[0] == 'triangle':
        # Triangle-triangle overlap (check if any edge of one triangle intersects any edge of the other)
        triangle1_edges = [(shape1[1][0], shape1[1][1]), (shape1[1][1], shape1[1][2]), (shape1[1][2], shape1[1][0])]
        triangle2_edges = [(shape2[1][0], shape2[1][1]), (shape2[1][1], shape2[1][2]), (shape2[1][2], shape2[1][0])]
        for edge1 in triangle1_edges:
            for edge2 in triangle2_edges:
                if lines_intersect(edge1[0], edge1[1], edge2[0], edge2[1]):
                    return True
        return False

    elif shape1[0] == 'rectangle' and shape2[0] == 'triangle':
        # Rectangle-triangle overlap (check if any triangle edge intersects any rectangle edge, 
        # or if any rectangle corner is inside the triangle)
        rx1, ry1, rx2, ry2 = shape1[1][0][0], shape1[1][0][1], shape1[1][1][0], shape1[1][1][1]
        rect_edges = [((rx1, ry1), (rx2, ry1)), ((rx2, ry1), (rx2, ry2)), ((rx2, ry2), (rx1, ry2)), ((rx1, ry2), (rx1, ry1))]
        triangle_edges = [(shape2[1][0], shape2[1][1]), (shape2[1][1], shape2[1][2]), (shape2[1][2], shape2[1][0])]
        
        for edge1 in rect_edges:
            for edge2 in triangle_edges:
                if lines_intersect(edge1[0], edge1[1], edge2[0], edge2[1]):
                    return True
        
        x1, y1, x2, y2, x3, y3 = shape2[1][0][0], shape2[1][0][1], shape2[1][1][0], shape2[1][1][1], shape2[1][2][0], shape2[1][2][1]
        if point_in_triangle(rx1, ry1, x1, y1, x2, y2, x3, y3):
            return True
        if point_in_triangle(rx2, ry1, x1, y1, x2, y2, x3, y3):
            return True
        if point_in_triangle(rx2, ry2, x1, y1, x2, y2, x3, y3):
            return True
        if point_in_triangle(rx1, ry2, x1, y1, x2, y2, x3, y3):
            return True

        return False

    elif shape1[0] == 'triangle' and shape2[0] == 'rectangle':
        # Triangle-rectangle overlap
        return check_overlap(shape2, shape1)

    return False


def point_in_triangle(px, py, x1, y1, x2, y2, x3, y3):
    """Checks if a point is inside a triangle."""
    d1 = sign(px, py, x1, y1, x2, y2)
    d2 = sign(px, py, x2, y2, x3, y3)
    d3 = sign(px, py, x3, y3, x1, y1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def sign(px, py, x1, y1, x2, y2):
    return (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)

def lines_intersect(p1, q1, p2, q2):
    """Checks if two line segments intersect."""
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        return 1 if val > 0 else 2  # clock or counterclock wise

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False

def on_segment(p, q, r):
    """Checks if point q lies on line segment pr."""
    if (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and \
       (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1])):
        return True
    return False

# Create a new image with a white background
img = Image.new('RGB', (800, 600), 'white')
draw = ImageDraw.Draw(img)

shapes = []  # List to store shape information

# Generate random shapes without overlap
for i in range(random.randint(10, 20)):
    shape_type = random.choice(['circle', 'rectangle', 'triangle'])
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    # Determine if this shape should have a border
    have_border = random.choice([True, False])  
    border_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Choose a border color
    border_width = 3

    overlap = True
    attempts = 0
    while overlap and attempts < 100:
        attempts += 1
        if shape_type == 'circle':
            x1 = random.randint(50, 750)
            y1 = random.randint(50, 550)
            radius = random.randint(20, 80)
            new_shape = ('circle', (x1, y1), radius)
        elif shape_type == 'rectangle':
            x1 = random.randint(50, 700)
            y1 = random.randint(50, 500)
            x2 = x1 + random.randint(50, 150)
            y2 = y1 + random.randint(50, 150)
            new_shape = ('rectangle', ((x1, y1), (x2, y2)))
        elif shape_type == 'triangle':
            x1 = random.randint(100, 700)
            y1 = random.randint(100, 500)
            x2 = x1 + random.randint(-100, 100)
            y2 = y1 + random.randint(-100, 100)
            x3 = x1 + random.randint(-100, 100)
            y3 = y1 + random.randint(-100, 100)
            new_shape = ('triangle', ((x1, y1), (x2, y2), (x3, y3)))

        overlap = False
        for existing_shape in shapes:
            if check_overlap(new_shape, existing_shape):
                overlap = True
                break

    if not overlap:
        shapes.append(new_shape)
        if shape_type == 'circle':
            if have_border:
                # Draw the border (a slightly larger circle)
                draw.ellipse([(x1 - radius - border_width, y1 - radius - border_width), 
                              (x1 + radius + border_width, y1 + radius + border_width)], fill=border_color)
            # Draw the filled circle on top
            draw.ellipse([(x1 - radius, y1 - radius), (x1 + radius, y1 + radius)], fill=color) 
        elif shape_type == 'rectangle':
            if have_border:
                # Draw the border (a slightly larger rectangle)
                draw.rectangle([(x1 - border_width, y1 - border_width), 
                               (x2 + border_width, y2 + border_width)], fill=border_color)
            # Draw the filled rectangle on top
            draw.rectangle([(x1, y1), (x2, y2)], fill=color)
        elif shape_type == 'triangle':
            if have_border:
                # Drawing a border around a triangle is a bit more complex, 
                # you might need to draw lines along each edge with the specified width.
                # Here's a simplified approach (drawing a slightly larger triangle):
                draw.polygon([(x1 - border_width, y1 - border_width), 
                              (x2 - border_width, y2 - border_width), 
                              (x3 - border_width, y3 - border_width)], fill=border_color)
            # Draw the filled triangle on top
            draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color)

# Create a Tkinter window
window = tk.Tk()
window.title("Random Shapes Background")

# Convert PIL Image to Tkinter PhotoImage
photo = ImageTk.PhotoImage(img)

# Create a label to display the image
label = tk.Label(window, image=photo)
label.pack()

# Run the Tkinter event loop
window.mainloop()