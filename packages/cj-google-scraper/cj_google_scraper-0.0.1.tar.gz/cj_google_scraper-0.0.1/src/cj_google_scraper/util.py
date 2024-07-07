import io

from PIL import Image


# screenshot
def screenshot(elem):
    return Image.open(io.BytesIO(elem.screenshot_as_png))
