import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_gradient_mask(width, height):
    color1 = (41, 98, 255) # Blue
    color2 = (170, 0, 255) # Purple
    overlay = Image.new("RGBA", (width, height))
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        for x in range(width):
            overlay.putpixel((x, y), (r, g, b, 255))
    return overlay

def create_app_icon(output_png, output_ico):
    size = (512, 512)
    # Create gradient background
    gradient = create_gradient_mask(size[0], size[1])
    
    # Create rounded mask
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    padding = 24
    draw_mask.rounded_rectangle([padding, padding, size[0]-padding, size[1]-padding], radius=100, fill=255)
    
    # Combine gradient and mask
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    img.paste(gradient, (0, 0), mask)
    
    draw = ImageDraw.Draw(img)
    
    # Try different fonts
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 185)
    except:
        font = ImageFont.load_default()
    
    # Letters centered using anchor="mm"
    # Moved slightly further apart
    draw.text((170, 256), "E", fill="white", font=font, anchor="mm")
    draw.text((342, 256), "ע", fill="white", font=font, anchor="mm")
    
    # Circular arrows
    cx, cy = 256, 256
    radius = 215 
    width = 30   
    
    bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
    
    # Arcs: 0 is 3 o'clock, clockwise.
    # Shortened slightly to give arrowhead room
    # Top arc: 195 to 330
    draw.arc(bbox, 195, 330, fill="white", width=width)
    
    # Bottom arc: 15 to 150
    draw.arc(bbox, 15, 150, fill="white", width=width)
    
    import math
    def draw_classic_arrowhead(draw_obj, center_x, center_y, outer_r, arc_width, angle_deg, direction=1):
        angle_rad = math.radians(angle_deg)
        mid_r = outer_r - arc_width / 2
        
        # Base of the arrow is AT the arc end
        base_center_x = center_x + mid_r * math.cos(angle_rad)
        base_center_y = center_y + mid_r * math.sin(angle_rad)
        
        # Perpendicular vector (radius vector direction)
        u_x = math.cos(angle_rad)
        u_y = math.sin(angle_rad)
        
        # Tangent vector (flow direction)
        v_x = -u_y if direction == 1 else u_y
        v_y = u_x if direction == 1 else -u_x
        
        # Arrowhead dimensions
        head_width = 80 # significantly wider than arc (30)
        head_len = 65
        
        # Two base points of the triangle
        # They extend outwards and inwards from base_center along the radius vector
        p1_x = base_center_x + u_x * (head_width / 2)
        p1_y = base_center_y + u_y * (head_width / 2)
        
        p2_x = base_center_x - u_x * (head_width / 2)
        p2_y = base_center_y - u_y * (head_width / 2)
        
        # Tip point (pushed forward along the tangent)
        tip_x = base_center_x + v_x * head_len
        tip_y = base_center_y + v_y * head_len
        
        draw_obj.polygon([(p1_x, p1_y), (p2_x, p2_y), (tip_x, tip_y)], fill="white")

    # Arrowheads at the end of the arcs
    draw_classic_arrowhead(draw, cx, cy, radius, width, 330, direction=1)
    draw_classic_arrowhead(draw, cx, cy, radius, width, 150, direction=1)
    
    os.makedirs(os.path.dirname(output_png), exist_ok=True)
    img.save(output_png)
    
    img.save(output_ico, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print(f"Created {output_png} and {output_ico}")

if __name__ == "__main__":
    create_app_icon("assets/app_icon.png", "assets/app_icon.ico")
