# HIT137 – Assignment 3

## Image Processing Desktop Application (Updated)

### Overview

This assignment requires the development of a **desktop-based image processing application** that demonstrates your understanding of **Object-Oriented Programming (OOP)** concepts, **Graphical User Interface (GUI)** development using **Tkinter**, and **digital image processing** using **OpenCV (cv2)**. The application should allow users to load, manipulate, and save images through an intuitive and well-structured interface.

The focus of this assignment is on clean software design, correct use of OOP principles, and the effective integration of GUI components with image processing functionality.

---

### Functional Requirements

## 1. Object-Oriented Programming (OOP)

The application must be structured using **a minimum of three well-defined classes**. The design should clearly demonstrate the following OOP principles:

* **Encapsulation** – Class attributes should be protected and accessed through methods where appropriate
* **Constructors** – Each class should use constructors to initialise required data
* **Methods** – Classes should contain meaningful methods that perform specific tasks
* **Class Interaction** – Classes must collaborate with one another to achieve application functionality (e.g., GUI interacting with image processor)

Example class responsibilities may include:

* Image processing operations
* GUI management and event handling
* File handling and application state management

---

## 2. Image Processing Using OpenCV

The application must implement the following image processing features using the **OpenCV library**:

* **Grayscale Conversion** – Convert a colour image to grayscale
* **Blur Effect** – Apply Gaussian blur with user-adjustable intensity
* **Edge Detection** – Detect edges using the Canny edge detection algorithm
* **Brightness Adjustment** – Allow users to increase or decrease image brightness
* **Contrast Adjustment** – Enable contrast modification through a slider or control
* **Image Rotation** – Rotate the image by 90°, 180°, or 270°
* **Image Flip** – Flip the image horizontally or vertically
* **Resize / Scale** – Allow users to resize the image by specifying scale factors or dimensions

All transformations should be applied to the currently displayed image and reflected immediately in the GUI.

---

## 3. Graphical User Interface (Tkinter)

You are free to design the layout and appearance of the GUI, provided it clearly supports all required features and ensures good usability.

### Required GUI Elements

* **Main Window**

  * Appropriately sized window
  * Meaningful application title

* **Menu Bar**

  * **File Menu**: Open, Save, Save As, Exit
  * **Edit Menu**: Undo, Redo

* **Image Display Area**

  * Canvas or Label widget to display the current image

* **Control Panel**

  * Buttons, sliders, or a sidebar to apply image effects and transformations
  * At least **one slider** for adjustable effects (e.g., blur, brightness, or contrast)

* **Status Bar**

  * Displays useful information such as:

    * Current filename
    * Image dimensions
    * Processing status messages

---

## 4. Required Application Functionality

The application must also include the following features:

* File dialogs for opening and saving images
* Support for common image formats (**JPG, PNG, BMP**)
* Error handling using message boxes (e.g., invalid file, no image loaded)
* Confirmation dialogs for critical actions (e.g., exiting without saving)
* Undo and Redo functionality for image operations

---

### Expected Outcome

By completing this assignment, you will demonstrate:

* Practical understanding of OOP design in Python
* Ability to build a functional desktop application using Tkinter
* Competency in applying image processing techniques with OpenCV
* Clean, readable, and well-documented code following professional standards

---

**End of Assignment Specification**
