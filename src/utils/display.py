class Display:
    def __init__(self):
        self.clear_terminal()

    def clear_terminal(self):
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

    def update_display(self, ascii_art):
        self.clear_terminal()
        print(ascii_art)

    def format_ascii_art(self, ascii_art):
        # Additional formatting can be added here if needed
        return ascii_art

    def show(self, ascii_art):
        formatted_art = self.format_ascii_art(ascii_art)
        self.update_display(formatted_art)