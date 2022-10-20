from PIL import Image

def test_handler(image):
    img = Image.open(image)
    img.resize((64, 64))
    img.save(f"./test.png")
    return True
