from tkinter import Label
from PIL import Image, ImageTk, ImageSequence


class AnimatedGIF(Label):
    def __init__(self, master, filename):
        self.master = master
        self.filename = filename
        self.sequence = []
        self.load_image()

        first_image = self.sequence[0]
        self.image = ImageTk.PhotoImage(first_image)

        super().__init__(master, image=self.image)
        self.pack()

        self.delay = first_image.info['duration']
        self.current_frame = 0

        self.after(self.delay, self.play)

    def load_image(self):
        im = Image.open(self.filename)
        for frame in ImageSequence.Iterator(im):
            self.sequence.append(frame.copy())

    def play(self):
        self.current_frame = (self.current_frame + 1) % len(self.sequence)
        self.image = ImageTk.PhotoImage(self.sequence[self.current_frame])
        self.configure(image=self.image)

        self.after(self.sequence[self.current_frame].info['duration'], self.play)
