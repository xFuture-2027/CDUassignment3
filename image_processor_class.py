import cv2
import numpy as np
import os


class ImageProcessor:
    """
    Handles the heavy lifting for image edits using OpenCV.
    Keeps the image data safe and provides easy tools to change it.
    """
    
    def __init__(self):
        """Sets up the processor and gets our history list ready for undos."""
        self.original_image = None
        self.current_image = None
        self.image_path = None
        self.history = []  # We'll stash old versions here so we can undo mistakes
        self.redo_stack = [] # We'll stash undone versions here so we can redo them
        
    def load_image(self, file_path):
        """
        Grabs an image from your computer.
        
        Args:
            file_path (str): Where the file lives.
            
        Returns:
            bool: True if we got it, False if something broke.
        """
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                return False
            self.current_image = self.original_image.copy()
            self.image_path = file_path
            # Start our history with this fresh image
            self.history = [self.current_image.copy()]
            self.redo_stack = [] # Clear redo stack on new load
            return True
        except Exception as e:
            print(f"Oops, couldn't load that: {e}")
            return False
            
    # ... (skipping save_image, get_current_image, get_image_info methods as they don't need changes) ...

    def save_image(self, file_path):
        """
        Saves your masterpiece to disk.
        
        Args:
            file_path (str): Where executed to save it.
            
        Returns:
            bool: True if it worked, False if the disk said no.
        """
        try:
            if self.current_image is not None:
                cv2.imwrite(file_path, self.current_image)
                return True
            return False
        except Exception as e:
            print(f"Trouble saving the file: {e}")
            return False
    
    def get_current_image(self):
        """
        Returns the image we're currently working on.
        Required so the GUI can show it to you.
        
        Returns:
            numpy.ndarray: The image data (in BGR because OpenCV is quirky).
        """
        return self.current_image
    
    def get_image_info(self):
        """
        Digs up the stats on the current image.
        
        Returns:
            dict: Width, height, channels, and filename.
        """
        if self.current_image is None:
            return None
        
        height, width = self.current_image.shape[:2]
        # Check if it's color (3 channels) or grayscale (1 channel)
        channels = self.current_image.shape[2] if len(self.current_image.shape) > 2 else 1
        
        return {
            'width': width,
            'height': height,
            'channels': channels,
            'filename': os.path.basename(self.image_path) if self.image_path else "Untitled"
        }
    
    def add_to_history(self):
        """Snapshots the current image before we change it."""
        if self.current_image is not None:
            self.history.append(self.current_image.copy())
            # Keep only the last 10 changes to save RAM
            if len(self.history) > 10:
                self.history.pop(0)
            # If we make a new change, we can't redo old stuff anymore
            self.redo_stack.clear()
    
    def undo(self):
        """
        Steps back in time to the previous image version.
        
        Returns:
            bool: True if we went back, False if there's nowhere to go.
        """
        if len(self.history) > 1:
            # Save current state to redo stack before undoing
            self.redo_stack.append(self.current_image.copy())
            
            self.history.pop()  # Toss the current broken state
            self.current_image = self.history[-1].copy() # Restore the good one
            return True
        return False

    def redo(self):
        """
        Steps forward to the state we just undid.
        
        Returns:
            bool: True if we went forward, False if there's nowhere to go.
        """
        if self.redo_stack:
            # Save current state to history (so we can undo this redo)
            self.history.append(self.current_image.copy())
            
            # Restore from redo stack
            self.current_image = self.redo_stack.pop()
            return True
        return False
    
    def reset_to_original(self):
        """Scraps all changes and goes back to how it started."""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self.history = [self.current_image.copy()]
    
    # ==================== Image Processing Tools ====================
    
    def apply_grayscale(self):
        """
        Drains the color out of the image.
        """
        if self.current_image is not None:
            self.add_to_history()
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            # We convert back to BGR so the rest of the code doesn't freak out about channel numbers
            self.current_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    def apply_blur(self, intensity=5):
        """
        Makes things fuzzy using a Gaussian blur.
        
        Args:
            intensity (int): How blurry? (Must be an odd number).
        """
        if self.current_image is not None:
            self.add_to_history()
            # GaussianBlur demands an odd number, so we force it
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
        Finds the edges using the Canny algorithm.
        Essentially outlines the important stuff.
        
        Args:
            threshold1 (int): Lower bound for edge detection.
            threshold2 (int): Upper bound for edge detection.
        """
        if self.current_image is not None:
            self.add_to_history()
            # Canny works best on grayscale
            gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, threshold1, threshold2)
            # Convert back to BGR for display consistency
            self.current_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    def adjust_brightness(self, value=0):
        """
        Brightens or darkens the image.
        We switch to HSV mode because it's smarter for brightness than RGB.
        
        Args:
            value (int): How much brighter (-100 to 100).
        """
        if self.current_image is not None:
            self.add_to_history()
            # HSV splits color (Hue/Sat) from brightness (Value)
            hsv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            
            # Boost the 'V' channel
            v = cv2.add(v, value)
            v = np.clip(v, 0, 255) # Make sure we don't go over the max brightness
            
            # Put it back together
            hsv = cv2.merge([h, s, v])
            self.current_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    def adjust_contrast(self, value=1.0):
        """
        Makes the darks darker and lights lighter (or the opposite).
        
        Args:
            value (float): 1.0 is normal. >1.0 pops the colors, <1.0 washes them out.
        """
        if self.current_image is not None:
            self.add_to_history()
            # convertScaleAbs is a fast way to do linear transforms
            self.current_image = cv2.convertScaleAbs(
                self.current_image, 
                alpha=value, 
                beta=0
            )
    
    def rotate_image(self, angle):
        """
        Spins the image around defined angles.
        
        Args:
            angle (int): 90, 180, or 270 degrees.
        """
        if self.current_image is not None:
            self.add_to_history()
            if angle == 90:
                self.current_image = cv2.rotate(
                    self.current_image, 
                    cv2.ROTATE_90_CLOCKWISE
                )
            elif angle == 180:
                self.current_image = cv2.rotate(
                    self.current_image, 
                    cv2.ROTATE_180
                )
            elif angle == 270:
                self.current_image = cv2.rotate(
                    self.current_image, 
                    cv2.ROTATE_90_COUNTERCLOCKWISE
                )
    
    def flip_image(self, direction):
        """
        Mirrors the image.
        
        Args:
            direction (str): 'horizontal' (left-right) or 'vertical' (up-down).
        """
        if self.current_image is not None:
            self.add_to_history()
            if direction == 'horizontal':
                # 1 means flip around y-axis
                self.current_image = cv2.flip(self.current_image, 1)
            elif direction == 'vertical':
                # 0 means flip around x-axis
                self.current_image = cv2.flip(self.current_image, 0)
    
    def resize_image(self, scale_percent):
        """
        Shrinks or grows the image.
        
        Args:
            scale_percent (int): 100 is normal size. 50 is half, 200 is double.
        """
        if self.current_image is not None:
            self.add_to_history()
            # Do the math for new size
            width = int(self.current_image.shape[1] * scale_percent / 100)
            height = int(self.current_image.shape[0] * scale_percent / 100)
            
            # Resize it
            self.current_image = cv2.resize(
                self.current_image, 
                (width, height), 
                interpolation=cv2.INTER_AREA
            )