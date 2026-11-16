
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from pathlib import Path

# Create an image containing text
image = Image.new("RGB", (1200, 1600), "white")
draw = ImageDraw.Draw(image)

draw.text(
    (100, 150),
    "COMPANY POLICY",
    fill="black"
)

draw.text(
    (100, 250),
    "1. Employees must arrive on time.",
    fill="black"
)

draw.text(
    (100, 350),
    "2. Leave requests require approval.",
    fill="black"
)

# Save the image
image_path = Path("exercises/scanned_page.png")
image.save(image_path)

# Embed the image inside a PDF
pdf_path = Path("samples/image_only.pdf")

pdf = canvas.Canvas(str(pdf_path), pagesize=(612, 792))
pdf.drawImage(
    str(image_path),
    0, 0,
    width=612,
    height=792
)
pdf.save()

print("Image-only PDF created:", pdf_path)
