class AsciiConverter:
    def __init__(self, ascii_chars):
        self.ascii_chars = ascii_chars

    def convert_pixel_to_ascii(self, pixel_value):
        # Normalize the pixel value to the range of ASCII characters
        ascii_index = int(pixel_value / 255 * (len(self.ascii_chars) - 1))
        return self.ascii_chars[ascii_index]

    def convert_matrix_to_ascii(self, matrix):
        ascii_matrix = []
        for row in matrix:
            ascii_row = ''.join(self.convert_pixel_to_ascii(pixel) for pixel in row)
            ascii_matrix.append(ascii_row)
        return ascii_matrix

    def set_ascii_chars(self, new_ascii_chars):
        self.ascii_chars = new_ascii_chars