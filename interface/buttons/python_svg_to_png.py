# pip install pycairo
# pip install cairosvg
# conda install cairo
import cairosvg

# Convert SVG file to PNG
# cairosvg.svg2png(url="input.svg", write_to="output.png")

# Or convert SVG string data directly
#svg_code = '<svg ...>...</svg>'
#cairosvg.svg2png(bytestring=bytes(svg_code, 'UTF-8'), write_to="output.png")

# Load from file and write straight to a PNG file

file_name = "floor_2_button"

cairosvg.svg2png(
    url=file_name+".svg", 
    write_to=file_name+".png",
)

# Load from file and write straight to a PDF file
#cairosvg.svg2pdf(url="image.svg", write_to="output.pdf")
