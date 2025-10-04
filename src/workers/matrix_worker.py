class MatrixWorker:
    def __init__(self, matrix, ascii_converter):
        self.matrix = matrix
        self.ascii_converter = ascii_converter

    def run(self):
        return self.process_matrix()

    def process_matrix(self):
        # Convert the matrix to ASCII using the provided converter
        ascii_art = self.ascii_converter.convert(self.matrix)
        return ascii_art