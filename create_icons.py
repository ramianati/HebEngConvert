from PIL import Image, ImageDraw

def create_gradient_mask(width, height):
    # Create blue to purple gradient
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

def draw_clipboard_icon(output_path):
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw clipboard body
    padding = 60
    rect = [padding, padding + 40, size[0] - padding, size[1] - padding]
    draw.rounded_rectangle(rect, radius=40, outline="white", width=40)
    
    # Draw clip
    clip_w = 160
    clip_h = 60
    clip_rect = [(size[0]-clip_w)//2, padding - 10, (size[0]+clip_w)//2, padding + 70]
    draw.rounded_rectangle(clip_rect, radius=20, fill="white")
    
    # Draw two internal lines
    line_padding = 140
    draw.line([line_padding, 220, size[0] - line_padding, 220], fill="white", width=25)
    draw.line([line_padding, 320, size[0] - line_padding, 320], fill="white", width=25)
    
    # Apply gradient
    gradient = create_gradient_mask(size[0], size[1])
    final = Image.new("RGBA", size, (0, 0, 0, 0))
    for x in range(size[0]):
        for y in range(size[1]):
            p = img.getpixel((x, y))
            if p[3] > 0:
                c = gradient.getpixel((x, y))
                final.putpixel((x, y), (c[0], c[1], c[2], p[3]))
    
    final.save(output_path)
    print(f"Created {output_path}")

def draw_copy_icon(output_path):
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Arrow
    arrow_y = size[1] // 2
    arrow_x_start = 20
    arrow_x_end = 220
    draw.line([arrow_x_start, arrow_y, arrow_x_end, arrow_y], fill="white", width=45)
    draw.polygon([arrow_x_end, arrow_y - 70, arrow_x_end + 90, arrow_y, arrow_x_end, arrow_y + 70], fill="white")
    
    # Mini Clipboard Silhouette on the right
    cb_x_start = 300
    cb_y_start = 80
    cb_w = 170
    cb_h = 350
    
    # Body
    draw.rounded_rectangle([cb_x_start, cb_y_start + 40, cb_x_start + cb_w, cb_y_start + cb_h], radius=25, outline="white", width=25)
    # Clip
    clip_w = 80
    draw.rounded_rectangle([cb_x_start + (cb_w-clip_w)//2, cb_y_start, cb_x_start + (cb_w+clip_w)//2, cb_y_start + 50], radius=10, fill="white")
    # Tiny lines
    draw.line([cb_x_start + 40, cb_y_start + 150, cb_x_start + cb_w - 40, cb_y_start + 150], fill="white", width=15)
    draw.line([cb_x_start + 40, cb_y_start + 230, cb_x_start + cb_w - 40, cb_y_start + 230], fill="white", width=15)

    # Apply gradient
    gradient = create_gradient_mask(size[0], size[1])
    final = Image.new("RGBA", size, (0, 0, 0, 0))
    for x in range(size[0]):
        for y in range(size[1]):
            p = img.getpixel((x, y))
            if p[3] > 0:
                c = gradient.getpixel((x, y))
                final.putpixel((x, y), (c[0], c[1], c[2], p[3]))
    
    final.save(output_path)
    print(f"Created {output_path}")

if __name__ == "__main__":
    import os
    if not os.path.exists("assets"):
        os.makedirs("assets")
    draw_clipboard_icon("assets/clipboard.png")
    draw_copy_icon("assets/copy.png")
