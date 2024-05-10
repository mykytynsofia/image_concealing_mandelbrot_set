import numpy as np
from PIL import Image
import hashlib

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n

def hash_key_to_params(key):
    hash_object = hashlib.sha256(str(key).encode('utf-8'))
    hash_digest = hash_object.hexdigest()

    a = int(hash_digest[0:6], 16) % 100 + 1  # ensure a is in range[1, 100]
    c = int(hash_digest[6:12], 16) % 100 + 1  # Ensure c is in range [1, 100]
    m = int(hash_digest[12:18], 16) % 100 + 50  # Ensure m is in range [50, 149]

    return a, c, m

def load_and_preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    red_channel, green_channel, blue_channel = image.split()
    threshold = 128
    binary_red = np.where(np.array(red_channel) > threshold, 1, 0)
    binary_green = np.where(np.array(green_channel) > threshold, 1, 0)
    binary_blue = np.where(np.array(blue_channel) > threshold, 1, 0)
    img_size = binary_red.shape
    return (binary_red.flatten(), binary_green.flatten(), binary_blue.flatten()), img_size

def encode_image(image_path, max_iter, key):
    (red_bits, green_bits, blue_bits), img_size = load_and_preprocess_image(image_path)
    encoded_images = []
    for image_bits in [red_bits, green_bits, blue_bits]:
        bit_index = 0
        encoded_image = np.zeros(img_size, dtype=np.int32)
        N = img_size[0] * img_size[1]
        a, c, m = hash_key_to_params(key)
        x = [key]
        for i in range(1, N):
            x.append((a * x[i - 1] + c) % m)
        shuffle_mapping = sorted(range(N), key=lambda i: x[i])
        points = [(y, x) for y in range(img_size[0]) for x in range(img_size[1])]
        points = [points[i] for i in shuffle_mapping]
        for y, x in points:
            c = complex(x / img_size[1] * 3.5 - 2.5, y / img_size[0] * 2 - 1)
            iter_count = mandelbrot(c, max_iter)
            if bit_index < len(image_bits):
                if iter_count % 2 != image_bits[bit_index]:
                    iter_count = iter_count - iter_count % 2 + image_bits[bit_index]
                bit_index += 1
            encoded_image[y, x] = iter_count
        encoded_images.append(encoded_image)
    return encoded_images, img_size

def decode_image(encoded_images, img_size, max_iter, key):
    decoded_channels = []
    for encoded_image in encoded_images:
        message_bits = ''
        N = img_size[0] * img_size[1]
        a, c, m = hash_key_to_params(key)
        x = [key]
        for i in range(1, N):
            x.append((a * x[i - 1] + c) % m)
        shuffle_mapping = sorted(range(N), key=lambda i: x[i])
        points = [(y, x) for y in range(img_size[0]) for x in range(img_size[1])]
        points = [points[i] for i in shuffle_mapping]
        for y, x in points:
            m = encoded_image[y, x]
            message_bits += str(m % 2)
        binary_image = np.array([int(bit) for bit in message_bits]).reshape(img_size)
        grayscale_channel = binary_image * 255
        decoded_channels.append(grayscale_channel)
    decoded_image = np.stack(decoded_channels, axis=-1)
    return decoded_image

max_iter = 100

key = 42
image_path = "img.png"

encoded_image, img_size = encode_image(image_path, max_iter, key)

encoded_red, encoded_green, encoded_blue = [img.astype(np.uint8) for img in encoded_image]
combined_encoded_image = np.stack((encoded_red, encoded_green, encoded_blue), axis=-1)

combined_encoded_image_pil = Image.fromarray(combined_encoded_image)
combined_encoded_image_pil.save("combined_encoded_image.png")

decoded_image = decode_image(encoded_image, img_size, max_iter, key)

decoded_image_pil = Image.fromarray(decoded_image.astype(np.uint8))
decoded_image_pil.save("decoded_image_correct.png")

decoded_image_wrong = decode_image(encoded_image, img_size, max_iter, 41)

#wrong key
decoded_image_pil_wrong = Image.fromarray(decoded_image_wrong.astype(np.uint8))
decoded_image_pil_wrong.save("decoded_image_wrong.png")