import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2, os
from image_processor import ImageProcessor

class ImageEditorGUI:
    # Main GUI class for HIT137 Image Editor.
    # Handles menu, buttons, sliders, canvas, and status bar.
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HIT137 Image Editor")
        self.root.geometry("1100x700")
        
        self.processor = ImageProcessor()
        self.tk_image = None
        self.image_path = None
        
        self.setup_menu()
        self.setup_ui()
        self.root.bind("<Configure>", self.redraw)
        
        # MENU
        def setup_menu(self):
            menubar = tk.Menu(self.root)
            file_menu = tk.Menu(menubar, tearoff = 0)
            file_menu.add_command(label="Open", command=self.open_image)
            file_menu.add_command(label="Save As", command=self.save_image)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            menubar.add_cascade(label="File", menu=file_menu)
            self.root.config(menu=menubar)
            
            # UI
            def setup_ui(self):
                # Canvas for displaying image
                self.canvas = tk.Canvas(self.root, bg="black")
                self.canvas = tk.pack(expand=True, fill=tk.BOTH)
                
                # Panel for buttons & sliders
                panel = tk.Frame(self.root)
                panel.pack(side=tk.BOTTOM, fill=tk.X)
                
                # Buttons
                tk.Button(panel, text="Grayscale", command=self.apply(self.processor.grayscale)).pack(side=tk.LEFT)
                tk.Button(panel, text="Edge", command=self.apply(self.processor.edge)).pack(side=tk.LEFT)
                tk.Button(panel, text="Rotate 90°", command=self.apply(lambda: self.processor.rotate(90))).pack(side=tk.LEFT)
                tk.Button(panel, text="Rotate 190°", command=self.apply(lambda: self.processor.rotate(180))).pack(side=tk.LEFT)
                tk.Button(panel, text="Rotate 270°", command=self.apply(lambda: self.processor.rotate(270))).pack(side=tk.LEFT)
                tk.Button(panel, text="Flip H", command=self.apply(lambda: self.processor.flip("horizontal"))).pack(side=tk.LEFT)
                tk.Button(panel, text="Flip V", command=self.apply(lambda: self.processor.flip("vertical"))).pack(side=tk.LEFT)
                tk.Button(panel, text="Undo", command=self.apply(self.processor.undo)).pack(side=tk.LEFT)
                tk.Button(panel, text="Redo", command=self.apply(self.processor.redo)).pack(side=tk.LEFT)
                
                # Sliders
                self.blur = tk.Scale(panel, from_=1, to=31, label="Blur", orient=tk.HORIZONTAL, command=lambda v: self.preview(self.processor.blur, int(v)))
                self.blur.pack(side=tk.LEFT)
                
                self.brightness = tk.Scale(panel, from_=-100, to=100, label="Brightness", orient=tk.HORIZONTAL, command=lambda v: self.preview(self.processor.brightness, int(v)))
                self.brightness.pack(side=tk.LEFT)
                
                self.contrast = tk.Scale(panel, from_=0.5, to=2.0, resolutiuon=0.1, label="Contrast", orient=tk.HORIZONTAL, command=lambda v: self.preview(self.processor.contrast, float(v)))
                self.contrast.set(1)
                self.contrast.pack(side=tk.LEFT)
                
                self.scale = tk.Scale(panel, from_=0.5, to=2.0, resolution=0.1, label="Scale", orient=tk.HORIZONTAL, command=lambda v: self.apply(lambda: self.processor.resize(float(v))) ())
                self.scale.set(1)
                self.scale.pack(side= tk.LEFT)
                
                # Status Bar
                self.status = tk.Label(self.root, bd=1, relief=tk.SUNKEN, anchor=tk.W)
                self.status.pack(side=tk.BOTTOM, fill=tk.X)
                
                # FILE
                def open_image(self):
                    path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png*.bmp")])
                    if path:
                        self.image_path = path
                        self.processor.load_image(path)
                        self.draw_image(self.processor.image)
                        self.update_status()
                        
                def save_image(self):
                    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
                    if path:
                        cv2.imwrite(path, self.processor.image)
                        
                # HELPERS
                def apply(self, func):
                    def wrapper():
                        if self.processor.image is None:
                            return
                        img = func()
                        self.draw_image(img)
                        self.update_status()
                     return wrapper
                 
                 def preview(self, func, value):
                     if self.processor.image is None:
                         return
                     img = func(value)
                     self.draw_image(img)
                     self.update_status()
                     
                # DISPLAY
                def draw_image(self, img):
                    self.canvas.delete("all")
                    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    pil = Image.fromarray(rgb)
                    cw, ch = self.canvas.winfo_width(), self.canvas.winfo_height()
                    iw, ih = pil.size
                    scale = min(cw / iw, ch / ih)
                    pil = pil.resize((int(iw * scale), int(ih * scale)), Image.LANCZOS)
                    self.tk_image = ImageTk.PhotoImage(pil)
                    self.canvas.create_image(cw//2, ch//2, image=self.tk_image, anchor=tk.CENTER)
                    
                def redraw(self, event):
                    if self.processor.image is not None:
                        self.draw_image(self.processor.image)
                        
                def update_status(self):
                    if self.processor.image is None: return
                    h, w = self.processor.image.shape[:2]
                    name = os.path.basename(self.image_path) if self.image_path else "Untitled"
                    self.status.config(text=f"{name} | {w} x {h} px")
                    
                def run(self):
                    self.root.mainloop()
                    
                    
                            
                    
                

