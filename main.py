from PIL import Image, ImageDraw, ImageFilter

logo_path = "renovate_logo.png"
profile_path = "Shion1305.jpeg"

logo_src = Image.open(logo_path).convert("RGBA")
profile_src = Image.open(profile_path).convert("RGBA")


def center_crop_face(img):
    w, h = img.size
    side = min(w, h)
    cx, cy = w // 2, int(h * 0.42)
    left = max(0, cx - side // 2)
    top = max(0, cy - side // 2)
    right = min(w, left + side)
    bottom = min(h, top + side)
    left = right - side
    top = bottom - side
    return img.crop((left, top, right, bottom))


def make_bubble_no_shadow(profile_square, diameter):
    bubble = profile_square.resize((diameter, diameter), Image.Resampling.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, diameter - 1, diameter - 1), fill=255)

    bubble_circle = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    bubble_circle.paste(bubble, (0, 0), mask)

    border = diameter // 35

    canvas = Image.new("RGBA", (diameter + 2 * border, diameter + 2 * border), (0, 0, 0, 0))

    outer_mask = Image.new("L", canvas.size, 0)
    od = ImageDraw.Draw(outer_mask)
    od.ellipse((0, 0, canvas.size[0] - 1, canvas.size[1] - 1), fill=255)

    # White border
    border_layer = Image.new("RGBA", canvas.size, (255, 255, 255, 255))
    canvas.paste(border_layer, (0, 0), outer_mask)

    # Inner bubble
    canvas.paste(bubble_circle, (border, border), mask)

    return canvas


def upscale(img, size):
    up = img.resize((size, size), Image.Resampling.LANCZOS)
    up = up.filter(ImageFilter.UnsharpMask(radius=2, percent=160, threshold=3))
    return up


size = 2048
logo = upscale(logo_src, size)
profile_sq = center_crop_face(profile_src)

# Bigger bubble, no shadow
bubble_d = int(size * 0.25)
bubble = make_bubble_no_shadow(profile_sq, bubble_d)

out = logo.copy()
margin = int(size * 0.11)
x = margin
y = size - bubble.size[1] - margin

out.alpha_composite(bubble, (x, y))

out_path = "renovate_shion1305_branded.png"
out.save(out_path)

out_path
