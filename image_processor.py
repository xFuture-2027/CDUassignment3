"""
image_processor.py

This module encapsulates all image manipulation logic using OpenCV.
It provides a clean, reusable abstraction for image processing operations
while maintaining internal state management, including undo and redo support.

The ImageProcessor class is intentionally UI-agnostic and is designed to be
used by any front-end layer (GUI, CLI, or web-based interface).
"""

import cv2
import numpy as np
import os


class ImageProcessor:
    """
    High-level image processing engine built on top of OpenCV.

    Responsibilities:
    1. Load and persist image data.
    2. Maintain edit history through undo/redo stacks.
    3. Expose safe, reusable image transformation methods without exposing
       low-level OpenCV operations to the UI layer.
    """

    # ================================================================
    # SECTION 0: INITIALISATION AND STATE MANAGEMENT
    # ================================================================
    def __init__(self):
        """
        Initialise the processor with empty state containers.

        Attributes:
            original_image (numpy.ndarray):
                Immutable copy of the originally loaded image.
                Used to support full reset functionality.
            current_image (numpy.ndarray):
                Actively edited image reflecting the latest operation.
            image_path (str):
                File system path of the currently loaded image.
            history (list):
                Stack of previous image states used for undo operations.
            redo_stack (list):
                Stack of undone states used for redo operations.
        """
        self.original_image = None
        self.current_image = None
        self.image_path = None

        # History stacks enable non-destructive editing
        self.history = []
        self.redo_stack = []

    # ================================================================
    # SECTION 1: FILE OPERATIONS (LOAD / SAVE)
    # ================================================================
    def load_image(self, file_path):
        """
        Load an image from disk and initialise processing state.

        This method resets the edit history to ensure undo/redo
        operations apply only to the current image session.

        Args:
            file_path (str): Absolute or relative path to the image file.

        Returns:
            bool: True if the image loads successfully, False otherwise.
        """
        try:
            self.original_image = cv2.imread(file_path)

            # cv2.imread returns None if loading fails
            if self.original_image is None:
                return False

            self.current_image = self.original_image.copy()
            self.image_path = file_path

            # Initialise history with the original image state
            self.history = [self.current_image.copy()]
            self.redo_stack.clear()
            return True

        except Exception as e:
            print(f"Failed to load image: {e}")
            return False

    def save_image(self, file_path):
        """
        Save the current image state to disk.

        Args:
            file_path (str): Destination file path.

        Returns:
            bool: True if the save operation succeeds, False otherwise.
        """
        try:
            if self.current_image is not None:
                cv2.imwrite(file_path, self.current_image)
                return True
            return False

        except Exception as e:
            print(f"Failed to save image: {e}")
            return False

    def get_current_image(self):
        """
        Retrieve the current image for display purposes.

        Returns:
            numpy.ndarray: Current image in BGR colour format.
        """
        return self.current_image

    def get_image_info(self):
        """
        Extract metadata related to the current image.

        Returns:
            dict | None: Dictionary containing image dimensions,
                         channel count, and filename if available.
        """
        if self.current_image is None:
            return None

        height, width = self.current_image.shape[:2]

        # Determine channel count safely
        channels = self.current_image.shape[2] if len(self.current_image.shape) > 2 else 1

        return {
            'width': width,
            'height': height,
            'channels': channels,
            'filename': os.path.basename(self.image_path) if self.image_path else "Untitled"
        }

    # ================================================================
    # SECTION 2: HISTORY MANAGEMENT (UNDO / REDO)
    # ================================================================
    def add_to_history(self):
        """
        Store a snapshot of the current image state.

        This method is invoked prior to any mutating operation
        to support undo/redo functionality while limiting memory usage.
        """
        if self.current_image is not None:
            self.history.append(self.current_image.copy())

            # Limit history depth to avoid excessive memory consumption
            if len(self.history) > 10:
                self.history.pop(0)

            # Any new action invalidates the redo stack
            self.redo_stack.clear()

    def undo(self):
        """
        Revert the image to the previous state.

        Returns:
            bool: True if undo is successful, False if no history exists.
        """
        if len(self.history) > 1:
            self.redo_stack.append(self.current_image.copy())
            self.history.pop()
            self.current_image = self.history[-1].copy()
            return True
        return False

    def redo(self):
        """
        Reapply the most recently undone operation.

        Returns:
            bool: True if redo is successful, False otherwise.
        """
        if self.redo_stack:
            self.history.append(self.current_image.copy())
            self.current_image = self.redo_stack.pop()
            return True
        return False

    def reset_to_original(self):
        """
        Restore the image to its original unmodified state.
        """
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.history = [self.current_image.copy()]
            self.redo_stack.clear()

    # ================================================================
    # SECTION 3: INTERNAL VALIDATION HELPERS
    # ================================================================
    def _validate_image_loaded(self):
        """
        Ensure an image is loaded before processing.

        Returns:
            bool: True if an image is available for processing.
        """
        if self.current_image is None:
            print("No image loaded.")
            return False
        return True

    # ================================================================
    # SECTION 4: IMAGE TRANSFORMATION OPERATIONS
    # ================================================================
    def apply_grayscale(self):
        """
        Convert the current image to grayscale.

        The image is converted back to BGR format to ensure
        compatibility with downstream operations and display logic.
        """
        if not self._validate_image_loaded():
            return

        self.add_to_history()

        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def apply_blur(self, intensity=5):
        """
        Apply Gaussian blur to the image.

        Args:
            intensity (int): Kernel size controlling blur strength.
                             Must be an odd integer.
        """
        if not self._validate_image_loaded():
            return

        self.add_to_history()

        # GaussianBlur requires an odd kernel size
        if intensity % 2 == 0:
            intensity += 1

        intensity = max(1, min(99, intensity))

        self.current_image = cv2.GaussianBlur(
            self.current_image,
            (intensity, intensity),
            0
        )

    def apply_edge_detection(self, threshold1=100, threshold2=200):
        """
        Detect edges using the Canny edge detection algorithm.
        """
        if not self._validate_image_loaded():
            return

        self.add_to_history()

        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)

        # Convert to BGR for consistent image representation
        self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def adjust_brightness(self, value=0):
        """
        Adjust image brightness.

        Args:
            value (int): Brightness offset in range -255 to 255.
        """
        if not self._validate_image_loaded():
            return

        self.add_to_history()

        value = max(-255, min(255, int(value)))

        # HSV colour space allows brightness adjustment
        # without modifying hue or saturation
        hsv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        v = cv2.add(v, value)
        v = np.clip(v, 0, 255)

        hsv = cv2.merge([h, s, v])
        self.current_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    def adjust_contrast(self, value=1.0):
        """
        Adjust image contrast.

        Args:
            value (float): Contrast multiplier (0.1 to 3.0).
        """
        if not self._validate_image_loaded():
            return

        self.add_to_history()

        value = max(0.1, min(3.0, float(value)))

        self.current_image = cv2.convertScaleAbs(
            self.current_image,
            alpha=value,
            beta=0
        )

    def rotate_image(self, angle):
        """
        Rotate the image by a fixed angle.

        Args:
            angle (int): Rotation angle (90, 180, or 270 degrees).
        """
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
        """
        Flip the image along the specified axis.

        Args:
            direction (str): 'horizontal' or 'vertical'.
        """
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
        """
        Resize the image by a percentage factor.

        Args:
            scale_percent (int): Scaling percentage (1–500%).
        """
        if not self._validate_image_loaded():
            return

        scale_percent = max(1, min(500, int(scale_percent)))
        self.add_to_history()

        width = int(self.current_image.shape[1] * scale_percent / 100)
        height = int(self.current_image.shape[0] * scale_percent / 100)

        # Prevent invalid resize operations
        if width < 1 or height < 1:
            print("Resize skipped: resulting dimensions too small.")
            return

        self.current_image = cv2.resize(
            self.current_image,
            (width, height),
            interpolation=cv2.INTER_AREA if scale_percent < 100 else cv2.INTER_LINEAR
        )
