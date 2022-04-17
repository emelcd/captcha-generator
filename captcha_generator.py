from turtle import fillcolor
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from string import ascii_letters, digits
from random import sample, randint
from uuid import uuid4

printable = ascii_letters + digits
BACKGROUND_COLOR = (randint(200, 255), randint(200, 255), randint(200, 255))


def generate_basis(text, width=250, height=100):
    """
    Generate captcha image
    :param text:
    :param width:
    :param height:
    :return:
    """
    # Create a black image
    image = Image.new(
        "RGB",
        (width, height),
        BACKGROUND_COLOR
    )
    # Get a font
    font = ImageFont.truetype("RobotoMono-Bold.ttf", 40)
    # Get a drawing context
    draw = ImageDraw.Draw(image)
    text_length = len(text)
    # Divide width and height by text length
    width_per_char = width / text_length
    height_per_char = height / text_length
    for i, char in enumerate(text):
        # Get the position of the character
        x = i * width_per_char + randint(0, int(width_per_char / 2))
        y = randint(0, int(height_per_char / 2))
        # Draw the character
        draw.text(
            (x, y),
            char,
            font=font,
            fill=(randint(0, 100), randint(0, 100), randint(0, 100)),
        )

    # Save image
    return image


def generate_text(length=6):
    """
    Generate random text
    :param length:
    :return:
    """
    return "".join(
        [printable[i] for i in sorted(sample(range(len(printable)), length))]
    )


def rotate(image, angle=10):
    """
    Rotate image
    :param image:
    :param angle:
    :return:
    """
    return image.rotate(
        randint(-angle / 2, angle / 2),
        expand=True,
        fillcolor=BACKGROUND_COLOR,
    )


def draw_lines(image):
    """
    Draw lines on image
    :param image:
    :param width:
    :param height:
    :return:
    """
    draw = ImageDraw.Draw(image)
    # draw 4 lines that cross the image
    for i in range(50):
        x1 = randint(0, image.width)
        y1 = randint(0, image.height)
        x2 = randint(0, image.width)
        y2 = randint(0, image.height)
        draw.line(
            (x1, y1, x2, y2), fill=(randint(0, 100), randint(0, 100), randint(0, 100))
        )
    return image


def blur(image):
    """
    Blur image
    :param image:
    :return:
    """
    return image.filter(ImageFilter.GaussianBlur(radius=2))


def crop_image(image, width=250, height=80):
    """
    Crop image
    :param image:
    :param width:
    :param height:
    :return:
    """
    return image.crop((0, 0, width, height))


def main_generator():
    """
    Main function
    :return:
    """
    text = generate_text()
    image = generate_basis(text)
    image = rotate(image)
    image = draw_lines(image)
    image = blur(image)
    image = crop_image(image)
    name_file = f"file/{uuid4()}.png"
    image.save(name_file)
    return [text,  name_file]

