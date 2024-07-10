class BoxOfStars:
    def __init__(self, width, height):
        self.print_box(width, height)

    def print_box(self, width, height):
        for i in range(height):
            if i == 0 or i == height - 1:
                print("*" * width)
            else:
                print("*" + " " * (width - 2) + "*")

