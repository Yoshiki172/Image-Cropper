# Image Cropper
<img src="https://github.com/user-attachments/assets/161a3237-7d16-4ab5-b249-6b8786ae3dbd" width="150">

Image Cropper is a modern and intuitive graphical user interface (GUI) application for cropping multiple images efficiently. The application is built using Python's Tkinter library along with the ttkbootstrap library for a polished, modern look. It allows users to load, crop, and save images, with the ability to crop multiple images at once while maintaining the same dimensions across all of them.

## Features

- **Load Multiple Images**: Load multiple images at once for processing.
- **Add More Images**: Add more images to the already loaded ones for batch cropping.
- **Crop in Square or Rectangle Mode**: Toggle between free-form rectangle cropping and fixed-size square cropping mode.
- **Next Image Navigation**: Easily navigate between images for cropping.
- **Save Cropped Images**: Save all cropped images to a specified directory.
- **Refresh View**: Reset to the initial image view to start fresh.
- **Modern User Interface**: Built with `ttkbootstrap` for a clean, modern look.
- **Resizable Window**: The application window automatically adjusts based on your screen size.


## Usage

1. **Run the Application**:

   You can run the application with the following command:

   python image_cropper.py


2. **User Interface Overview**:

   - **Load Images**: Click this button to load multiple images into the application.
   - **Add More Images**: Add additional images to the current list of loaded images.
   - **Square Crop Mode**: Toggle between free-form cropping and square cropping mode.
   - **Next Image**: Navigate through the loaded images.
   - **Save Cropped Images**: Save all the cropped images to a selected directory.
   - **Refresh**: Reset the cropping view for the current image.

3. **Cropping**:

   - Click and drag to define a cropping area on the image.
   - Release the mouse button to finalize the cropping region.
   - Use **Square Crop Mode** to enforce a square selection.

## Requirements

- Python 3.x
- Pillow (PIL fork)
- ttkbootstrap
- Tkinter (usually included with Python)

## Screenshot

![[App Screenshot](screenshot.png)](https://github.com/user-attachments/assets/6e768e31-4192-49f0-9168-b67cfd47f2f2)



