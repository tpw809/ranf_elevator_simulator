from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_button(size=256, arrow="up", pressed=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Metallic gradient background
    for i in range(size):
        shade = int(180 + 50 * (i / size))
        draw.ellipse([(i, i), (size - i, size - i)], fill=(shade, shade, shade))

    # Inner shadow for pressed state
    if pressed:
        img = img.filter(ImageFilter.GaussianBlur(3))

    # Arrow drawing
    arrow_color = (30, 30, 30)
    if arrow == "up":
        points = [(size*0.5, size*0.25), (size*0.75, size*0.65), (size*0.25, size*0.65)]
    else:
        points = [(size*0.25, size*0.35), (size*0.75, size*0.35), (size*0.5, size*0.75)]

    draw.polygon(points, fill=arrow_color)

    return img

# Generate both buttons
make_button(256, "up").save("elevator_up.png")
make_button(256, "down").save("elevator_down.png")
make_button(256, "up", pressed=True).save("elevator_up_pressed.png")
make_button(256, "down", pressed=True).save("elevator_down_pressed.png")
