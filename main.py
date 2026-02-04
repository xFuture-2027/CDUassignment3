import tkinter as tk
from tkinter import filedialog, messagebox

# Import our custom classes
from image_processor import ImageProcessor
from image_display import ImageDisplay
from gui_setup import GUISetup


class ImageProcessorApp:
    """
    The brains of the operation.
    This class ties together the GUI (what you see), the ImageProcessor (what does the work),
    and the ImageDisplay (how it shows up).
    """
    
    def __init__(self, root):
        """
        Starts the engine.
        
        Args:
            root: The main Tkinter window (the container for everything).
        """
        self.root = root
        self.root.title("HIT137 - Image Processing Application")
        self.root.geometry("1000x700")
        
        # Create instance of ImageProcessor (demonstrates class interaction)
        self.image_processor = ImageProcessor()
        
        # Initialize Tkinter variables for sliders
        self.blur_var = tk.IntVar(value=5)
        self.brightness_var = tk.IntVar(value=0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.scale_var = tk.IntVar(value=100)
        
        # Dictionary to store variables and labels
        self.variables = {
            'blur_var': self.blur_var,
            'brightness_var': self.brightness_var,
            'contrast_var': self.contrast_var,
            'scale_var': self.scale_var
        }
        
        # Setup GUI components using GUISetup class
        self.setup_gui()
        
        # Create ImageDisplay instance for displaying images
        self.image_display = ImageDisplay(self.canvas, max_width=700, max_height=550)
    
    def setup_gui(self):
        """
        Builds the interface.
        Keeps this file clean by offloading the heavy UI construction to GUISetup.
        """
        # Create callback dictionary for menu and buttons
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
        
        # Setup menu bar
        GUISetup.setup_menu(self.root, callbacks)
        
        # Setup main layout and get canvas
        self.canvas = GUISetup.setup_main_layout(self.root)
        
        # Setup control panel
        GUISetup.setup_control_panel(self.root, callbacks, self.variables)
        
        # Setup status bar
        self.status_bar = GUISetup.setup_status_bar(self.root)
    
    # ==================== Update Methods ====================
    
    def update_display(self):
        """Refreshes what you see on screen."""
        current_image = self.image_processor.get_current_image()
        self.image_display.display_image(current_image)
        self.update_status_bar()
    
    def update_status_bar(self):
        """Puts the file stats (size, name) into the bottom bar."""
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
        """Updates the little text next to the blur slider so you know the value."""
        value = self.blur_var.get()
        if 'blur_label' in self.variables:
            self.variables['blur_label'].config(text=f"Value: {value}")
    
    # ==================== File Menu Methods ====================
    
    def open_image(self):
        """
        Opens a file picker so you can choose an image.
        If it loads, we show it; if not, we complain.
        """
        file_path = filedialog.askopenfilename(
            title="Open Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
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
        Saves over the original file.
        We ask first because that's polite (and safer).
        """
        if self.image_processor.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        if self.image_processor.image_path:
            result = messagebox.askyesno(
                "Confirm Save", 
                "Overwrite the original file?"
            )
            if result:
                if self.image_processor.save_image(self.image_processor.image_path):
                    messagebox.showinfo("Success", "Image saved successfully!")
                else:
                    messagebox.showerror("Error", "Failed to save image!")
        else:
            self.save_image_as()
    
    def save_image_as(self):
        """Saves a copy with a new name."""
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
        """Double checks if you really want to quit."""
        result = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if result:
            self.root.quit()
    
    # ==================== Edit Menu Methods ====================
    
    def undo_operation(self):
        """Oops button. Goes back one step."""
        if self.image_processor.undo():
            self.update_display()
        else:
            messagebox.showinfo("Info", "Nothing to undo!")

    def redo_operation(self):
        """Un-oops button. Goes forward one step if you undid too much."""
        if self.image_processor.redo():
            self.update_display()
        else:
            messagebox.showinfo("Info", "Nothing to redo!")
    
    def reset_image(self):
        """Nuke everything and go back to the original image."""
        if self.image_processor.original_image is not None:
            self.image_processor.reset_to_original()
            self.update_display()
        else:
            messagebox.showwarning("Warning", "No image loaded!")
    
    # ==================== Image Processing Methods ====================
    
    def apply_grayscale(self):
        """Turns it black and white."""
        if self.image_processor.current_image is not None:
            self.image_processor.apply_grayscale()
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def apply_blur(self):
        """Makes it fuzzy based on the slider."""
        if self.image_processor.current_image is not None:
            intensity = self.blur_var.get()
            self.image_processor.apply_blur(intensity)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def apply_edge_detection(self):
        """Finds the outlines."""
        if self.image_processor.current_image is not None:
            self.image_processor.apply_edge_detection()
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def apply_brightness(self):
        """Make it brighter or darker."""
        if self.image_processor.current_image is not None:
            value = self.brightness_var.get()
            self.image_processor.adjust_brightness(value)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def apply_contrast(self):
        """Pop the colors or wash them out."""
        if self.image_processor.current_image is not None:
            value = self.contrast_var.get()
            self.image_processor.adjust_contrast(value)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def rotate_image(self, angle):
        """
        Spins the image.
        
        Args:
            angle (int): 90, 180, or 270.
        """
        if self.image_processor.current_image is not None:
            self.image_processor.rotate_image(angle)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def flip_image(self, direction):
        """
        Mirrors the image.
        
        Args:
            direction (str): 'horizontal' or 'vertical'.
        """
        if self.image_processor.current_image is not None:
            self.image_processor.flip_image(direction)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")
    
    def resize_image(self):
        """Streches or shrinks the image."""
        if self.image_processor.current_image is not None:
            scale = self.scale_var.get()
            self.image_processor.resize_image(scale)
            self.update_display()
        else:
            messagebox.showwarning("Warning", "Please load an image first!")


def main():
    """Ignition. Starts the whole app."""
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
