from PIL import Image, ImageDraw

def create_icon():
    # Create a 256x256 image with transparent background
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a rounded rectangle background (dark blue/gray)
    bg_color = (40, 40, 40, 255)
    # corner_radius = 40
    draw.rounded_rectangle([(10, 10), (246, 246)], radius=40, fill=bg_color, outline=(60, 60, 60, 255), width=5)

    # Draw a download arrow (white)
    arrow_color = (255, 255, 255, 255)
    
    # Arrow shaft
    draw.rectangle([(108, 50), (148, 150)], fill=arrow_color)
    
    # Arrow head (triangle)
    draw.polygon([(80, 150), (176, 150), (128, 200)], fill=arrow_color)

    # Save as .ico
    image.save("app_icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("app_icon.ico created successfully.")

if __name__ == "__main__":
    create_icon()
