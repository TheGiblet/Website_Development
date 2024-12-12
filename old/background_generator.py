import random
from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk

def check_overlap(shape1, shape2):
    """Checks if two shapes overlap."""
    shape1_type, shape1_coords = shape1
    shape2_type, shape2_coords = shape2

    if shape1_type == 'circle' and shape2_type == 'circle':
        # Circle-circle overlap
        distance = ((shape1_coords[0] - shape2_coords[0])**2 + (shape1_coords[1] - shape2_coords[1])**2)**0.5
        return distance < (shape1_coords[2] + shape2_coords[2])

    elif shape1_type == 'circle' and shape2_type == 'rectangle':
        # Circle-rectangle overlap
        cx, cy = shape1_coords[0], shape1_coords[1]
        radius = shape1_coords[2]
        rx1, ry1 = shape2_coords[0][0], shape2_coords[0][1]
        rx2, ry2 = shape2_coords[1][0], shape2_coords[1][1]

        closest_x = max(rx1, min(cx, rx2))
        closest_y = max(ry1, min(cy, ry2))

        distance = ((closest_x - cx)**2 + (closest_y - cy)**2)**0.5
        return distance < radius

    elif shape1_type == 'rectangle' and shape2_type == 'circle':
        # Rectangle-circle overlap (same logic as circle-rectangle)
        return check_overlap(shape2, shape1)

    elif shape1_type == 'rectangle' and shape2_type == 'rectangle':
        # Rectangle-rectangle overlap
        r1x1, r1y1 = shape1_coords[0][0], shape1_coords[0][1]
        r1x2, r1y2 = shape1_coords[1][0], shape1_coords[1][1]
        r2x1, r2y1 = shape2_coords[0][0], shape2_coords[0][1]
        r2x2, r2y2 = shape2_coords[1][0], shape2_coords[1][1]

        return not (r1x2 < r2x1 or r1x1 > r2x2 or r1y2 < r2y1 or r1y1 > r2y2)

    # ... (Add other shape overlap checks: circle-triangle, triangle-rectangle, etc.) ...

    return False  # Default: no overlap

# ... (Other functions: point_in_triangle, sign, lines_intersect, on_segment) ...

def generate_background_image(filename):
    """Generates a background image with random shapes and lines."""
    img = Image.new('RGB', (800, 600), 'white')
    draw = ImageDraw.Draw(img)

    shapes = []

    # Generate random shapes without overlap
    for i in range(random.randint(10, 20)):
        shape_type = random.choice(['circle', 'rectangle', 'triangle'])
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # Determine if this shape should have a border
        have_border = random.choice([True, False])  
        border_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
        border_width = 3

        overlap = True
        attempts = 0
        while overlap and attempts < 100:
            attempts += 1
            if shape_type == 'circle':
                x1 = random.randint(50, 750)
                y1 = random.randint(50, 550)
                radius = random.randint(20, 80)
                new_shape = ('circle', (x1, y1, radius)) 
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
                    # Draw the border
                    draw.ellipse([(x1 - radius - border_width, y1 - radius - border_width), 
                                  (x1 + radius + border_width, y1 + radius + border_width)], fill=border_color)
                # Draw the filled circle on top
                draw.ellipse([(x1 - radius, y1 - radius), (x1 + radius, y1 + radius)], fill=color) 
            elif shape_type == 'rectangle':
                if have_border:
                    # Draw the border
                    draw.rectangle([(x1 - border_width, y1 - border_width), 
                                   (x2 + border_width, y2 + border_width)], fill=border_color)
                # Draw the filled rectangle on top
                draw.rectangle([(x1, y1), (x2, y2)], fill=color)
            elif shape_type == 'triangle':
                if have_border:
                    # Simplified border approach
                    draw.polygon([(x1 - border_width, y1 - border_width), 
                                  (x2 - border_width, y2 - border_width), 
                                  (x3 - border_width, y3 - border_width)], fill=border_color)
                # Draw the filled triangle on top
                draw.polygon([(x1, y1), (x2, y2), (x3, y3)], fill=color)

    # Generate random lines
    for i in range(random.randint(5, 15)):
        x1 = random.randint(50, 750)
        y1 = random.randint(50, 550)
        x2 = random.randint(50, 750)
        y2 = random.randint(50, 550)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        width = random.randint(1, 5)  
        draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

    img.save(filename)


# Generate a new background image each time the script is run
filename = f"images/background_{random.randint(1, 10000)}.png"  # Generate a unique filename
generate_background_image(filename)

print(f"Generated background image: {filename}")
