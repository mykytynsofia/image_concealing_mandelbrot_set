# Image Encoding and Decoding with Mandelbrot Set and Pseudorandom Shuffling

This project demonstrates an approach to encoding and decoding images using the Mandelbrot set, pseudorandom shuffling and LSB modifications. The purpose is to explore cryptographic steganography by embedding information within the fractal patterns of the Mandelbrot set.

## Functionality

1. **Image Encoding**:
   - Preprocesses an image into binary channels.
   - Shuffles image coordinates based on a pseudorandom sequence generated from the key.
   - Encodes data into the Mandelbrot set, adjusting iterations based on the binary data.

2. **Image Decoding**:
   - Decodes the information by reversing the shuffling and extracting binary data from the iteration counts of the Mandelbrot calculations.

## Example

### Original secret image

![image](https://github.com/mykytynsofia/image_concealing_mandelbrot_set/assets/71774322/ab94398c-64ae-44ed-85d8-b84f7990aa6b)


### The Mandelbrot Set with encoded  secret image in it

![image](https://github.com/mykytynsofia/image_concealing_mandelbrot_set/assets/71774322/7d5b032c-75b8-469c-a014-66f64a67e22f)

### Decoded image from the Mandelbrot set having the right key

![image](https://github.com/mykytynsofia/image_concealing_mandelbrot_set/assets/71774322/47d70a81-e70c-4b10-97af-3c1f4f8f701c)

### Decoded image from the Mandelbrot set having the wrong key

![image](https://github.com/mykytynsofia/image_concealing_mandelbrot_set/assets/71774322/423aa81c-d974-4231-b068-608423d8a18c)
