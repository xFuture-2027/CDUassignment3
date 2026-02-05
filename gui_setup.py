import tkinter as tk
from tkinter import ttk

"""
gui_setup.py

This module builds all graphical components of the Image Editor application.
It separates UI layout from processing logic, supporting clean OOP structure.
"""

# =========================================================================
# TOOLTIP HELPER CLASS (HD-LEVEL UI POLISH)
# =========================================================================
class ToolTip:
    """Simple tooltip display for widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0",
                         relief=tk.SOLID, borderwidth=1)
        label.pack()

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()


class GUISetup:
    """Handles construction of all GUI components."""

    # =========================================================================
    # 1. MENU BAR
    # =========================================================================
    @staticmethod
    def setup_menu(root, callbacks):
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Open", command=callbacks['open_image'], accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=callbacks['save_image'], accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=callbacks['save_image_as'], accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=callbacks['exit_application'])

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        edit_menu.add_command(label="Undo", command=callbacks['undo_operation'], accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=callbacks['redo_operation'], accelerator="Ctrl+Y")
        edit_menu.add_command(label="Reset to Original", command=callbacks['reset_image'])

        # Keyboard Shortcuts
        root.bind('<Control-o>', lambda e: callbacks['open_image']())
        root.bind('<Control-s>', lambda e: callbacks['save_image']())
        root.bind('<Control-Shift-S>', lambda e: callbacks['save_image_as']())  # NEW
        root.bind('<Control-z>', lambda e: callbacks['undo_operation']())
        root.bind('<Control-y>', lambda e: callbacks['redo_operation']())

    # =========================================================================
    # 2. IMAGE DISPLAY AREA
    # =========================================================================
    @staticmethod
    def setup_main_layout(root):
        main_frame = tk.Frame(root, bg='#2b2b2b')
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas_frame = tk.Frame(main_frame, bg='#1e1e1e', bd=2, relief=tk.SUNKEN)
        canvas_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', width=700, height=550)
        canvas.pack(fill=tk.BOTH, expand=True)

        return canvas

    # =========================================================================
    # 3. CONTROL PANEL
    # =========================================================================
    @staticmethod
    def setup_control_panel(root, callbacks, variables):
        control_frame = tk.Frame(root, bg='#3c3c3c', width=280)
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        control_frame.pack_propagate(False)

        title_label = tk.Label(control_frame, text="Image Effects",
                               font=('Segoe UI', 14, 'bold'), bg='#3c3c3c', fg='white')
        title_label.pack(pady=(15, 10))

        btn_frame = tk.Frame(control_frame, bg='#3c3c3c')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        open_btn = tk.Button(btn_frame, text="📂 Open Image", command=callbacks['open_image'],
                             bg='#28a745', fg='black', relief=tk.FLAT)
        open_btn.pack(fill=tk.X, pady=2)
        ToolTip(open_btn, "Open an image file")

        reset_btn = tk.Button(btn_frame, text="↺ Reset Changes", command=callbacks['reset_image'],
                              bg='#dc3545', fg='black', relief=tk.FLAT)
        reset_btn.pack(fill=tk.X, pady=2)
        ToolTip(reset_btn, "Restore original image")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#3c3c3c', borderwidth=0)
        style.configure('TNotebook.Tab', background='#505050', foreground='white', padding=[10, 2])
        style.map('TNotebook.Tab', background=[('selected', '#007acc')])

        notebook = ttk.Notebook(control_frame, style='TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        GUISetup._setup_basic_filters_tab(notebook, callbacks, variables)
        GUISetup._setup_adjustments_tab(notebook, callbacks, variables)
        GUISetup._setup_transform_tab(notebook, callbacks, variables)

    # =========================================================================
    # FILTERS TAB
    # =========================================================================
    @staticmethod
    def _setup_basic_filters_tab(notebook, callbacks, variables):
        tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(tab, text='Filters')

        tk.Button(tab, text="Grayscale", command=callbacks['apply_grayscale'],
                  bg='#007acc', fg='black').pack(pady=10, fill=tk.X, padx=10)

        tk.Button(tab, text="Edge Detection", command=callbacks['apply_edge_detection'],
                  bg='#007acc', fg='black').pack(pady=5, fill=tk.X, padx=10)

        blur_frame = tk.LabelFrame(tab, text="Blur Effect", bg='#3c3c3c', fg='white')
        blur_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Scale(blur_frame, from_=1, to=51, orient=tk.HORIZONTAL,
                 variable=variables['blur_var'], bg='#3c3c3c',
                 command=lambda v: callbacks['update_blur_label']()).pack(fill=tk.X, padx=5)

        variables['blur_label'] = tk.Label(blur_frame,
                                           text=f"Value: {variables['blur_var'].get()}",
                                           bg='#3c3c3c', fg='#cccccc')
        variables['blur_label'].pack()

        tk.Button(blur_frame, text="Apply Blur", command=callbacks['apply_blur'],
                  bg='#007acc', fg='black').pack(pady=5, fill=tk.X, padx=5)

    # =========================================================================
    # ADJUST TAB
    # =========================================================================
    @staticmethod
    def _setup_adjustments_tab(notebook, callbacks, variables):
        tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(tab, text='Adjust')

        bright_frame = tk.LabelFrame(tab, text="Brightness", bg='#3c3c3c', fg='white')
        bright_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Scale(bright_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                 variable=variables['brightness_var'], bg='#3c3c3c').pack(fill=tk.X, padx=5)

        tk.Button(bright_frame, text="Apply Brightness", command=callbacks['apply_brightness'],
                  bg='#007acc', fg='black').pack(pady=5, fill=tk.X, padx=5)

        contrast_frame = tk.LabelFrame(tab, text="Contrast", bg='#3c3c3c', fg='white')
        contrast_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Scale(contrast_frame, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                 variable=variables['contrast_var'], bg='#3c3c3c').pack(fill=tk.X, padx=5)

        tk.Button(contrast_frame, text="Apply Contrast", command=callbacks['apply_contrast'],
                  bg='#007acc', fg='black').pack(pady=5, fill=tk.X, padx=5)

    # =========================================================================
    # TRANSFORM TAB
    # =========================================================================
    @staticmethod
    def _setup_transform_tab(notebook, callbacks, variables):
        tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(tab, text='Transform')

        rotate_frame = tk.LabelFrame(tab, text="Rotate", bg='#3c3c3c', fg='white')
        rotate_frame.pack(pady=10, padx=10, fill=tk.X)

        btn_frame = tk.Frame(rotate_frame, bg='#3c3c3c')
        btn_frame.pack(pady=5)

        for angle in [90, 180, 270]:
            tk.Button(btn_frame, text=f"{angle}°",
                      command=lambda a=angle: callbacks['rotate_image'](a),
                      bg='#6c757d', fg='black', width=5).pack(side=tk.LEFT, padx=3)

        flip_frame = tk.LabelFrame(tab, text="Flip", bg='#3c3c3c', fg='white')
        flip_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Button(flip_frame, text="Flip Horizontal",
                  command=lambda: callbacks['flip_image']('horizontal'),
                  bg='#007acc', fg='black').pack(pady=2, fill=tk.X, padx=5)

        tk.Button(flip_frame, text="Flip Vertical",
                  command=lambda: callbacks['flip_image']('vertical'),
                  bg='#007acc', fg='black').pack(pady=2, fill=tk.X, padx=5)

        resize_frame = tk.LabelFrame(tab, text="Resize/Scale", bg='#3c3c3c', fg='white')
        resize_frame.pack(pady=10, padx=10, fill=tk.X)

        tk.Scale(resize_frame, from_=10, to=200, orient=tk.HORIZONTAL,
                 variable=variables['scale_var'], bg='#3c3c3c').pack(fill=tk.X, padx=5)

        tk.Button(resize_frame, text="Apply Resize", command=callbacks['resize_image'],
                  bg='#007acc', fg='black').pack(pady=5, fill=tk.X, padx=5)

    # =========================================================================
    # STATUS BAR (NOW DYNAMIC)
    # =========================================================================
    @staticmethod
    def setup_status_bar(root):
        status_var = tk.StringVar()
        status_var.set("Ready - Load an image to start")

        status_bar = tk.Label(root, textvariable=status_var,
                              bd=1, relief=tk.SUNKEN, anchor=tk.W,
                              bg='#007acc', fg='white', font=('Segoe UI', 9))
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        return status_var
