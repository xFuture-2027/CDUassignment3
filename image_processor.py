import cv2
import numpy as np
import os


class ImageProcessor:
    """
    A robust wrapper class for OpenCV image processing operations.

    Responsibilities:
    1. Manage image loading and saving.
    2. Maintain an Undo/Redo history stack to prevent data loss.
    3. Provide high-level methods for common image manipulations
       (grayscale, blur, edge detection, brightness, contrast, rotation, flip, resize).
    """

    # ----------------------------------------------------------------------------------------------------------------
    # SECTION 0: INITIALIZATION
    # ----------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the processor with empty states.

        Attributes:
            original_image (numpy.ndarray): The pristine copy of the loaded image (for resetting).
            current_image (numpy.ndarray): The active image being edited.
            image_path (str): File path of the loaded image.
            history (list): Stack of previous image states for 'Undo'.
            redo_stack (list): Stack of undone states for 'Redo'.
        """
        self.original_image = None
        self.current_image = None
        self.image_path = None

        # History stacks for time-traveling through edits
        self.history = []
        self.redo_stack = []

    # ----------------------------------------------------------------------------------------------------------------
    # SECTION 1: FILE OPERATIONS (Load/Save)
    # ----------------------------------------------------------------------------------------------------------------
    def load_image(self, file_path):
        """Load image from disk into memory."""
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                return False
            self.current_image = self.original_image.copy()
            self.image_path = file_path
            self.history = [self.current_image.copy()]
            self.redo_stack = []
            return True
        except Exception as e:
            print(f"Failed to load image: {e}")
            return False

    def save_image(self, file_path):
        """Save current image to disk."""
        try:
            if self.current_image is not None:
                cv2.imwrite(file_path, self.current_image)
                return True
            return False
        except Exception as e:
            print(f"Failed to save image: {e}")
            return False

    def get_current_image(self):
        """Return the current image (BGR format)."""
        return self.current_image

    def get_image_info(self):
        """Return width, height, channels, and filename of current image."""
        if self.current_image is None:
            return None

        height, width = self.current_image.shape[:2]
        channels = self.current_image.shape[2] if len(self.current_image.shape) > 2 else 1

        return {
            'width': width,
            'height': height,
            'channels': channels,
            'filename': os.path.basename(self.image_path) if self.image_path else "Untitled"
        }

    # ----------------------------------------------------------------------------------------------------------------
    # SECTION 2: HISTORY MANAGEMENT (Undo/Redo)
    # ----------------------------------------------------------------------------------------------------------------
    def add_to_history(self):
        """Snapshots the current image before making changes."""
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            if len(self.history) > 10:
                self.history.pop(0)
            self.redo_stack.clear()

    def undo(self):
        """Undo last change."""
        if len(self.history) > 1:
            self.redo_stack.append(self.current_image.copy())
            self.history.pop()
            self.current_image = self.history[-1].copy()
            return True
        return False

    def redo(self):
        """Redo last undone change."""
        if self.redo_stack:
            self.history.append(self.current_image.copy())
            self.current_image = self.redo_stack.pop()
            return True
        return False

    def reset_to_original(self):
        """Reset image to original state."""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.history = [self.current_image.copy()]
            self.redo_stack.clear()

    # ----------------------------------------------------------------------------------------------------------------
    # SECTION 3: PRIVATE HELPERS
    # ----------------------------------------------------------------------------------------------------------------
    def _validate_image_loaded(self):
        """Ensure an image is loaded before processing."""
        if self.current_image is None:
            print("No image loaded.")
            return False
        return True

    # ----------------------------------------------------------------------------------------------------------------
    # SECTION 4: IMAGE TRANSFORMATIONS
    # ----------------------------------------------------------------------------------------------------------------
    def apply_grayscale(self):
        """Convert image to grayscale."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def apply_blur(self, intensity=5):
        """Apply Gaussian blur."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        if intensity % 2 == 0:
            intensity += 1
        intensity = max(1, min(99, intensity))
        self.current_image = cv2.GaussianBlur(self.current_image, (intensity, intensity), 0)

    def apply_edge_detection(self, threshold1=100, threshold2=200):
        """Detect edges using Canny algorithm."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness(self, value=0):
        """Adjust image brightness (-255 to 255)."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        value = max(-255, min(255, int(value)))
        hsv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v = np.clip(v, 0, 255)
        hsv = cv2.merge([h, s, v])
        self.current_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def adjust_contrast(self, value=1.0):
        """Adjust image contrast (0.1 to 3.0)."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        value = max(0.1, min(3.0, float(value)))
        self.current_image = cv2.convertScaleAbs(self.current_image, alpha=value, beta=0)

    def rotate_image(self, angle):
        """Rotate image by 90, 180, or 270 degrees."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        if angle == 90:
            code = cv2.ROTATE_90_CLOCKWISE
        elif angle == 180:
            code = cv2.ROTATE_180
        elif angle == 270:
            code = cv2.ROTATE_90_COUNTERCLOCKWISE
        else:
            print("Invalid rotation angle.")
            return
        self.current_image = cv2.rotate(self.current_image, code)

    def flip_image(self, direction):
        """Flip image horizontally or vertically."""
        if not self._validate_image_loaded():
            return
        self.add_to_history()
        if direction == 'horizontal':
            self.current_image = cv2.flip(self.current_image, 1)
        elif direction == 'vertical':
            self.current_image = cv2.flip(self.current_image, 0)
        else:
            print("Invalid flip direction.")

    def resize_image(self, scale_percent):
        """Resize image by percentage (1–500%)."""
        if not self._validate_image_loaded():
            return
        scale_percent = max(1, min(500, int(scale_percent)))
        self.add_to_history()
        width = int(self.current_image.shape[1] * scale_percent / 100)
        height = int(self.current_image.shape[0] * scale_percent / 100)
        if width < 1 or height < 1:
            print("Resize skipped: dimensions too small.")
            return
        self.current_image = cv2.resize(
            self.current_image,
            (width, height),
            interpolation=cv2.INTER_AREA if scale_percent < 100 else cv2.INTER_LINEAR
        )
