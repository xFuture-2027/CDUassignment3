"""
main.py

Entry point for the Image Processing Application.
This module is responsible for initialising the GUI, coordinating user interactions,
and delegating image operations to the ImageProcessor and ImageDisplay components.

The design follows a modular architecture to improve maintainability, readability,
and separation of concerns.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

# Import application-specific modules
from image_processor import ImageProcessor
from image_display import ImageDisplay
from gui_setup import GUISetup


class ImageProcessorApp:
    """
    Central controller class for the application.

    This class acts as an integration layer between:
    - GUI components (Tkinter interface)
    - Image processing logic (ImageProcessor)
    - Image rendering logic (ImageDisplay)

    It manages user interactions and ensures that GUI events
    correctly trigger image processing operations.
    """

    def __init__(self, root):
        """
        Initialises the main application window and core components.

        Args:
            root (tk.Tk): The root Tkinter window that hosts all UI elements.
        """
        self.root = root
        self.root.title("HIT137 - Image Processing Application")
        self.root.geometry("1000x700")

        # Instantiate the image processing engine
        self.image_processor = ImageProcessor()

        # --------------------
        # Tkinter State Variables
        # --------------------
        # These variables maintain real-time UI state for sliders and controls
        self.blur_var = tk.IntVar(value=5)
        self.brightness_var = tk.IntVar(value=0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.scale_var = tk.IntVar(value=100)

        # Centralised variable registry for GUI binding
        self.variables = {
            'blur_var': self.blur_var,
            'brightness_var': self.brightness_var,
            'contrast_var': self.contrast_var,
            'scale_var': self.scale_var
        }

        # Construct GUI components
        self.setup_gui()

        # Initialise image display handler
        self.image_display = ImageDisplay(
            self.canvas,
            max_width=700,
            max_height=550
        )

    # ======================================================
    # GUI INITIALISATION
    # ======================================================

    def setup_gui(self):
        """
        Builds and configures all graphical interface components.

        GUI construction is delegated to the GUISetup class to
        maintain separation between interface layout and application logic.
        """
        callbacks = {
            'open_image': self.open_image,
            'save_image': self.save_image,
            'save_image_as': self.save_image_as,
            'exit_application': self.exit_application,
            'undo_operation': self.undo_operation,
            'redo_operation': self.redo_operation,
            'reset_image': self.reset_image,
            'apply_grayscale': self.apply_grayscale,
            'apply_blur': self.apply_blur,
            'apply_edge_detection': self.apply_edge_detection,
            'apply_brightness': self.apply_brightness,
            'apply_contrast': self.apply_contrast,
            'rotate_image': self.rotate_image,
            'flip_image': self.flip_image,
            'resize_image': self.resize_image,
            'update_blur_label': self.update_blur_label
        }

        # Initialise menu bar
        GUISetup.setup_menu(self.root, callbacks)

        # Create main canvas layout
        self.canvas = GUISetup.setup_main_layout(self.root)

        # Create control panel with sliders and buttons
        GUISetup.setup_control_panel(self.root, callbacks, self.variables)

        # Initialise status bar
        self.status_bar = GUISetup.setup_status_bar(self.root)

    # ======================================================
    # DISPLAY & STATUS MANAGEMENT
    # ======================================================

    def update_display(self):
        """
        Refreshes the displayed image and synchronises status information.
        """
        current_image = self.image_processor.get_current_image()
        self.image_display.display_image(current_image)
        self.update_status_bar()

    def update_status_bar(self):
        """
        Updates the status bar with metadata related to the currently loaded image.
        """
        info = self.image_processor.get_image_info()
        if info:
            status_text = (
                f"File: {info['filename']} | "
                f"Dimensions: {info['width']}x{info['height']} | "
                f"Channels: {info['channels']}"
            )
            self.status_bar.config(text=status_text)
        else:
            self.status_bar.config(text="No image loaded")

    def update_blur_label(self):
        """
        Updates the blur intensity label to reflect the current slider value.
        """
        value = self.blur_var.get()
        if 'blur_label' in self.variables:
            self.variables['blur_label'].config(text=f"Value: {value}")

    # ======================================================
    # FILE OPERATIONS
    # ======================================================

    def open_image(self):
        """
        Opens a file selection dialog and loads the selected image.
        """
        file_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            if self.image_processor.load_image(file_path):
                self.update_display()
                messagebox.showinfo("Success", "Image loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load image!")

    def save_image(self):
        """
        Saves changes to the original image file after user confirmation.
        """
        if self.image_processor.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return

        if self.image_processor.image_path:
            if messagebox.askyesno("Confirm Save", "Overwrite the original file?"):
                if self.image_processor.save_image(self.image_processor.image_path):
                    messagebox.showinfo("Success", "Image saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save image!")
        else:
            self.save_image_as()

    def save_image_as(self):
        """
        Saves the image to a new file path specified by the user.
        """
        if self.image_processor.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            if self.image_processor.save_image(file_path):
                messagebox.showinfo("Success", "Image saved successfully!")
            else:
                messagebox.showerror("Error", "Failed to save image!")

    def exit_application(self):
        """
        Gracefully exits the application after user confirmation.
        """
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    # ======================================================
    # IMAGE PROCESSING OPERATIONS
    # ======================================================

    def apply_grayscale(self):
        """Applies grayscale transformation to the image."""
        if self.image_processor.current_image is not None:
            self.image_processor.apply_grayscale()
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def apply_blur(self):
        """Applies blur effect based on user-defined intensity."""
        if self.image_processor.current_image is not None:
            self.image_processor.apply_blur(self.blur_var.get())
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def apply_edge_detection(self):
        """Applies edge detection algorithm to highlight contours."""
        if self.image_processor.current_image is not None:
            self.image_processor.apply_edge_detection()
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def apply_brightness(self):
        """Adjusts image brightness."""
        if self.image_processor.current_image is not None:
            self.image_processor.adjust_brightness(self.brightness_var.get())
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def apply_contrast(self):
        """Adjusts image contrast."""
        if self.image_processor.current_image is not None:
            self.image_processor.adjust_contrast(self.contrast_var.get())
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def rotate_image(self, angle):
        """
        Rotates the image by a specified angle.

        Args:
            angle (int): Rotation angle (90, 180, or 270 degrees).
        """
        if self.image_processor.current_image is not None:
            self.image_processor.rotate_image(angle)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def flip_image(self, direction):
        """
        Flips the image horizontally or vertically.

        Args:
            direction (str): Flip direction ('horizontal' or 'vertical').
        """
        if self.image_processor.current_image is not None:
            self.image_processor.flip_image(direction)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")

    def resize_image(self):
        """Resizes the image based on percentage scaling."""
        if self.image_processor.current_image is not None:
            self.image_processor.resize_image(self.scale_var.get())
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")


def main():
    """
    Application entry point.
    Initialises the Tkinter event loop.
    """
    root = tk.Tk()
    ImageProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
