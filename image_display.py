import tkinter as tk
from PIL import Image, ImageTk
import cv2


class ImageDisplay:
    """
    Manages displaying images on a Tkinter Canvas.
    Keeps aspect ratio and resizes images to fit within the display area.
    """

    def __init__(self, canvas, max_width=700, max_height=550):
        self.canvas = canvas
        self.max_width = max_width
        self.max_height = max_height
        self.photo_image = None
        self.current_image = None  # Store last image for resizing

        # Re-center image automatically if window resizes
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _on_canvas_resize(self, event):
        """Re-display image when canvas size changes."""
        if self.current_image is not None:
            self.display_image(self.current_image)

    def display_image(self, cv_image):
        """
        Converts OpenCV image → Tkinter display format and centers it.
        Returns resized dimensions for status bar updates.
        """
        self.current_image = cv_image

        if cv_image is None:
            self.canvas.delete("all")
            return None

        try:
            if len(cv_image.shape) == 2:
                rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)
            else:
                rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("Image conversion failed:", e)
            self.canvas.delete("all")
            return None

        pil_image = Image.fromarray(rgb_image)

        width, height = pil_image.size
        if width == 0 or height == 0:
            return None

        ratio = min(self.max_width / width, self.max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(pil_image)

        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        x = canvas_width // 2 if canvas_width > 1 else self.max_width // 2
        y = canvas_height // 2 if canvas_height > 1 else self.max_height // 2

        self.canvas.create_image(x, y, image=self.photo_image, anchor=tk.CENTER)

        return new_width, new_height
