from PIL import Image, ImageDraw


def decode_image(path_to_png):
    """
    Decodes an image from the red channel values of each pixel
    Saves the decoded image

    :param path_to_png: The path to the image
    :return: None
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    # Loop through each pixel in the encoded image
    for x in range(0, x_size):
        for y in range(0, y_size):
            # Get red channel from the pixel
            pixel_value = red_channel.getpixel((x, y))

            # Convert to binary
            red_binary = bin(pixel_value)

            # Check the LSB and set the output pixel accordingly
            if red_binary[-1] == "1":
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_image.png")


def encode_image(path_to_png, text):
    """
    Encode text to an image using the red channel of pixels
    Saves the encoded image

    :param path_to_png: The path to the image
    :param text: The text to encode the image with
    :return: None
    """
    # Open the image to encode
    encoded_image = Image.open(path_to_png)
    encoded_image_pixels = encoded_image.load()

    # Create the decoded text
    text_image = write_text(text, encoded_image.size)

    # Loop through the image's pixels
    x_size, y_size = encoded_image.size
    for x in range(0, x_size):
        for y in range(0, y_size):
            # Image pixel
            encoded_pixel_value = encoded_image.getpixel((x, y))

            # Isolate the red channel and get the binary
            encoded_pixel_red = encoded_pixel_value[0]
            encoded_pixel_red_bin = bin(encoded_pixel_red)

            # Remove the LSB from the binary number
            encoded_pixel_no_lsb = encoded_pixel_red_bin[:-1]

            # Text image pixel
            text_pixel_value = text_image.getpixel((x, y))

            # Set the LSB depending on if text is present at that pixel
            if 255 in text_pixel_value:
                encoded_pixel_no_lsb += "1"
            else:
                encoded_pixel_no_lsb += "0"

            # Creat a new tuple and update the pixel
            new_tuple = (int(encoded_pixel_no_lsb, 2),) + encoded_pixel_value[1:]
            encoded_image_pixels[x, y] = new_tuple

    encoded_image.save("encoded_image.png")


def write_text(text_to_write, dimensions):
    """
    Create a black and white image with text

    :param text_to_write: The text to write
    :param dimensions: The dimensions for the image
    :return: An image object
    """
    image = Image.new("RGB", dimensions)
    image_text = ImageDraw.Draw(image)
    image_text.text((15, 15), text_to_write)

    return image


if __name__ == "__main__":
    example_text = '''
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et 
    dolore magna aliqua. Fames ac turpis egestas sed tempus urna et. Ullamcorper dignissim cras tincidunt lobortis 
    feugiat vivamus at augue eget. Ipsum dolor sit amet consectetur adipiscing. Ut sem viverra aliquet eget sit amet. 
    Ut lectus arcu bibendum at varius. Amet mattis vulputate enim nulla aliquet porttitor. Vel quam elementum 
    pulvinar etiam non quam lacus. Scelerisque purus semper eget duis. Aliquet lectus proin nibh nisl condimentum id 
    venenatis a.
    '''

    # encode_image("flower.png", example_text)
    # decode_image("encoded_image.png")
