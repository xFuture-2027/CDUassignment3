import tkinter as tk
from tkinter import ttk

class GUISetup:
    """
    The Interface Architect.
    
    This static class is responsible for building the visual elements of the application.
    By separating the 'View' (GUI) code from the 'Controller' (Logic) code, 
    we keep the main file clean and easy to read.
    """

    # =========================================================================
    # 1. TOP SECTION: MENU BAR
    # =========================================================================
    
    @staticmethod
    def setup_menu(root, callbacks):
        """
        Constructs the top navigation bar (File, Edit).
        
        Args:
            root: The main Tkinter window.
            callbacks (dict): Dictionary connecting menu clicks to logic functions.
        """
        # Create the main menu container
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        
        # --- File Menu ---
        # 'tearoff=0' prevents the menu from being dragged out as a separate window
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Add commands with keyboard shortcuts listed
        file_menu.add_command(label="Open", command=callbacks['open_image'], accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=callbacks['save_image'], accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=callbacks['save_image_as'], accelerator="Ctrl+Shift+S")
        file_menu.add_separator() # Visual divider
        file_menu.add_command(label="Exit", command=callbacks['exit_application'])
        
        # --- Edit Menu ---
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        edit_menu.add_command(label="Undo", command=callbacks['undo_operation'], accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=callbacks['redo_operation'], accelerator="Ctrl+Y")
        edit_menu.add_command(label="Reset to Original", command=callbacks['reset_image'])
        
        # --- Bind Keyboard Shortcuts ---
        # This links the actual physical key presses to the functions
        root.bind('<Control-o>', lambda e: callbacks['open_image']())
        root.bind('<Control-s>', lambda e: callbacks['save_image']())
        root.bind('<Control-z>', lambda e: callbacks['undo_operation']())
        root.bind('<Control-y>', lambda e: callbacks['redo_operation']())

    # =========================================================================
    # 2. CENTER SECTION: IMAGE DISPLAY (CANVAS)
    # =========================================================================

    @staticmethod
    def setup_main_layout(root):
        """
        Creates the central area where the image is displayed.
        
        Structure:
        [ Main Frame (Dark Grey) ]
          └── [ Canvas Frame (Bordered) ]
                └── [ Canvas (The Drawing Board) ]

        Returns:
            tk.Canvas: The canvas object so the logic class can draw images on it.
        """
        # Main background container
        main_frame = tk.Frame(root, bg='#2b2b2b')
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Decorative frame to give the image a sunken/bordered look
        canvas_frame = tk.Frame(main_frame, bg='#1e1e1e', bd=2, relief=tk.SUNKEN)
        canvas_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # The actual canvas widget where pixels are drawn
        canvas = tk.Canvas(canvas_frame, bg='#1e1e1e', width=700, height=550)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        return canvas

    # =========================================================================
    # 3. RIGHT SECTION: CONTROL PANEL (SIDEBAR)
    # =========================================================================

    @staticmethod
    def setup_control_panel(root, callbacks, variables):
        """
        Builds the sidebar containing buttons, sliders, and tabs.
        """
        # Fixed width sidebar
        control_frame = tk.Frame(root, bg='#3c3c3c', width=280)
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        # prevent frame from shrinking to fit content (keeps it 280px wide)
        control_frame.pack_propagate(False) 
        
        # -- Title --
        title_label = tk.Label(
            control_frame, text="Image Effects", 
            font=('Segoe UI', 14, 'bold'), bg='#3c3c3c', fg='white'
        )
        title_label.pack(pady=(15, 10))
        
        # -- Global Action Buttons (Open / Reset) --
        btn_frame = tk.Frame(control_frame, bg='#3c3c3c')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame, text="📂 Open Image", command=callbacks['open_image'], 
                  bg='#28a745', fg='black', relief=tk.FLAT).pack(fill=tk.X, pady=2)
                  
        tk.Button(btn_frame, text="↺ Reset Changes", command=callbacks['reset_image'], 
                  bg='#dc3545', fg='black', relief=tk.FLAT).pack(fill=tk.X, pady=2)

        # -- Tabbed Interface (Notebook) --
        # Configure the style for the tabs to match the dark theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#3c3c3c', borderwidth=0)
        style.configure('TNotebook.Tab', background='#505050', foreground='white', padding=[10, 2])
        style.map('TNotebook.Tab', background=[('selected', '#007acc')], foreground=[('selected', 'white')])
        
        notebook = ttk.Notebook(control_frame, style='TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Delegate the creation of specific tabs to helper methods
        GUISetup._setup_basic_filters_tab(notebook, callbacks, variables)
        GUISetup._setup_adjustments_tab(notebook, callbacks, variables)
        GUISetup._setup_transform_tab(notebook, callbacks, variables)

    # =========================================================================
    # 4. INTERNAL TABS (HELPER METHODS)
    # =========================================================================

    @staticmethod
    def _setup_basic_filters_tab(notebook, callbacks, variables):
        """Helper: Populates the 'Filters' tab (Grayscale, Edge, Blur)."""
        basic_tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(basic_tab, text='Filters')
        
        # 1. Simple Click Effects
        tk.Button(basic_tab, text="Grayscale", command=callbacks['apply_grayscale'], 
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=10, fill=tk.X, padx=10)
        
        tk.Button(basic_tab, text="Edge Detection", command=callbacks['apply_edge_detection'], 
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=5, fill=tk.X, padx=10)
        
        # 2. Blur Slider Group
        blur_frame = tk.LabelFrame(basic_tab, text="Blur Effect", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        blur_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(blur_frame, text="Intensity:", bg='#3c3c3c', fg='#cccccc').pack(anchor=tk.W, padx=5)
        
        # Note: 'command' here updates the label text as you drag
        blur_slider = tk.Scale(
            blur_frame, from_=1, to=51, orient=tk.HORIZONTAL, 
            variable=variables['blur_var'], bg='#3c3c3c', fg='white', 
            troughcolor='#505050', highlightthickness=0,
            command=lambda v: callbacks['update_blur_label']()
        )
        blur_slider.pack(fill=tk.X, padx=5)
        
        # Dynamic label showing current slider value
        variables['blur_label'] = tk.Label(
            blur_frame, text=f"Value: {variables['blur_var'].get()}", 
            bg='#3c3c3c', fg='#cccccc'
        )
        variables['blur_label'].pack()
        
        tk.Button(blur_frame, text="Apply Blur", command=callbacks['apply_blur'], 
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=5, fill=tk.X, padx=5)

    @staticmethod
    def _setup_adjustments_tab(notebook, callbacks, variables):
        """Helper: Populates the 'Adjust' tab (Brightness, Contrast)."""
        adjust_tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(adjust_tab, text='Adjust')
        
        # 1. Brightness Group
        bright_frame = tk.LabelFrame(adjust_tab, text="Brightness", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        bright_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Scale(bright_frame, from_=-100, to=100, orient=tk.HORIZONTAL, variable=variables['brightness_var'],
                 bg='#3c3c3c', fg='white', troughcolor='#505050', highlightthickness=0).pack(fill=tk.X, padx=5)
        
        tk.Button(bright_frame, text="Apply Brightness", command=callbacks['apply_brightness'],
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=5, fill=tk.X, padx=5)
        
        # 2. Contrast Group
        contrast_frame = tk.LabelFrame(adjust_tab, text="Contrast", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        contrast_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Resolution=0.1 allows decimal selection (e.g., 1.5)
        tk.Scale(contrast_frame, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, variable=variables['contrast_var'],
                 bg='#3c3c3c', fg='white', troughcolor='#505050', highlightthickness=0).pack(fill=tk.X, padx=5)
        
        tk.Button(contrast_frame, text="Apply Contrast", command=callbacks['apply_contrast'],
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=5, fill=tk.X, padx=5)

    @staticmethod
    def _setup_transform_tab(notebook, callbacks, variables):
        """Helper: Populates the 'Transform' tab (Rotate, Flip, Resize)."""
        transform_tab = tk.Frame(notebook, bg='#3c3c3c')
        notebook.add(transform_tab, text='Transform')
        
        # 1. Rotation Buttons
        rotate_frame = tk.LabelFrame(transform_tab, text="Rotate", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        rotate_frame.pack(pady=10, padx=10, fill=tk.X)
        
        btn_frame = tk.Frame(rotate_frame, bg='#3c3c3c')
        btn_frame.pack(pady=5, fill=tk.X)
        
        # Loop to create buttons dynamically for 90, 180, 270
        for angle in [90, 180, 270]:
            tk.Button(btn_frame, text=f"{angle}°", command=lambda a=angle: callbacks['rotate_image'](a),
                      bg='#6c757d', fg='black', width=5, relief=tk.FLAT).pack(side=tk.LEFT, padx=3)
        
        # 2. Flip Buttons
        flip_frame = tk.LabelFrame(transform_tab, text="Flip", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        flip_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Button(flip_frame, text="Flip Horizontal", command=lambda: callbacks['flip_image']('horizontal'),
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=2, fill=tk.X, padx=5)
        tk.Button(flip_frame, text="Flip Vertical", command=lambda: callbacks['flip_image']('vertical'),
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=2, fill=tk.X, padx=5)
        
        # 3. Resize Slider
        resize_frame = tk.LabelFrame(transform_tab, text="Resize/Scale", bg='#3c3c3c', fg='white', font=('Segoe UI', 10, 'bold'))
        resize_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Scale from 10% to 200% size
        tk.Scale(resize_frame, from_=10, to=200, orient=tk.HORIZONTAL, variable=variables['scale_var'],
                 bg='#3c3c3c', fg='white', troughcolor='#505050', highlightthickness=0).pack(fill=tk.X, padx=5)
        
        tk.Button(resize_frame, text="Apply Resize", command=callbacks['resize_image'],
                  bg='#007acc', fg='black', relief=tk.FLAT).pack(pady=5, fill=tk.X, padx=5)

    # =========================================================================
    # 5. BOTTOM SECTION: STATUS BAR
    # =========================================================================

    @staticmethod
    def setup_status_bar(root):
        """
        Creates a bar at the bottom to display messages to the user.
        
        Returns:
            tk.Label: The label widget, so logic can update the text later.
        """
        status_bar = tk.Label(
            root, 
            text="Ready - Load an image to start", 
            bd=1, relief=tk.SUNKEN, anchor=tk.W, # sunken effect looks like a status bar
            bg='#007acc', fg='white', font=('Segoe UI', 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        return status_bar