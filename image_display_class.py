import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

class ImageDisplay:
    """
    Manages displaying images on a Tkinter Canvas.
    Ensuring images fit within specific dimensions while maintaining aspect ratio.
    """
    def __init__(self, canvas, max_width=700, max_height=550):
        self.canvas = canvas
        self.max_width = max_width
        self.max_height = max_height
        self.photo_image = None  # Keep reference to prevent garbage collection

    def display_image(self, cv_image):
        """
        Takes the raw OpenCV image data, converts it, resize it, and paints it onto the canvas centered.
        Also handles the tricky bit of keeping the aspect ratio correct.
        
        Args:
            cv_image: The image data (OpenCV format, BGR or Grayscale).
        """
        if cv_image is None:
            self.canvas.delete("all")
            return

        # Convert simple numpy array to something displayable if needed,
        # but usually we expect standard CV2 image (H, W, C)
        
        # Convert BGR (OpenCV) to RGB (PIL)
        try:
            if len(cv_image.shape) == 2:
                # Grayscale
                rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2RGB)
            else:
                # Color (BGR)
                rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Error converting image: {e}")
            return

        # 2. Convert to PIL Image
        pil_image = Image.fromarray(rgb_image)

        # 3. Calculate new dimensions to fit within max_width/height
        width, height = pil_image.size
        
        if width == 0 or height == 0:
            return
            
        ratio = min(self.max_width / width, self.max_height / height)
        
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        
        # 4. Resize image using LANCZOS for high quality
        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 5. Convert to ImageTk
        self.photo_image = ImageTk.PhotoImage(pil_image)

        # 6. Clear canvas and draw image centered
        self.canvas.delete("all")
        
        # We place it in the center of the canvas area we are given
        # Since we are passed the canvas, but we know the max dimensions we are trying to fill
        # we can assume center is max_width/2, max_height/2
        
        # Adjust center based on actual canvas size if available, but relying on passed max is safer for layout logic usually
        # Determine centering coordinates
        # Let's verify canvas size:
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # If canvas is not yet drawn/geometry not set, it might be 1x1.
        if canvas_width > 1 and canvas_height > 1:
            x = canvas_width // 2
            y = canvas_height // 2
        else:
            x = self.max_width // 2
            y = self.max_height // 2
        
        self.canvas.create_image(x, y, image=self.photo_image, anchor=tk.CENTER)
