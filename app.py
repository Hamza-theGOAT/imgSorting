import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
import threading

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ImageViewer:
    def __init__(self):
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Image Viewer")
        self.root.geometry("1000x700")

        # Variables to store images and current selection
        self.imageFiles = []
        self.currentIndex = 0
        self.thumbnailButtons = []
        self.currentFolder = ""

        # Supported image formats
        self.supportedFormats = (
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

        self.createWidgets()

    def createWidgets(self):
        """Create all the GUI elements"""

        # Main container frame
        mainFrame = ctk.CTkFrame(self.root)
        mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top section - Browse button and folder info
        topFrame = ctk.CTkFrame(mainFrame)
        topFrame.pack(fill="x", padx=10, pady=(10, 5))

        self.browseBtn = ctk.CTkButton(
            topFrame,
            text="📁 Browse Folder",
            command=self.browseFolder,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=150
        )
        self.browseBtn.pack(side="left", padx=10, pady=10)

        # Image count label
        self.countLabel = ctk.CTkLabel(
            topFrame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.countLabel.pack(side="right", padx=10, pady=10)

        # Main image display area
        self.imageFrame = ctk.CTkFrame(mainFrame)
        self.imageFrame.pack(fill="both", expand=True, padx=10, pady=5)

        # Large image preview label
        self.imageLabel = ctk.CTkLabel(
            self.imageFrame,
            text="Select a folder to view images",
            font=ctk.CTkFont(size=16)
        )
        self.imageLabel.pack(expand=True, fill="both", padx=20, pady=20)

        # Scrollable frame for thumbnails
        self.thumbnailFrame = ctk.CTkFrame(mainFrame)
        self.thumbnailFrame.pack(fill="x", padx=10, pady=(5, 10), ipady=10)

        # Scrollable frame for thumbnails
        self.thumbnailScroll = ctk.CTkScrollableFrame(
            self.thumbnailFrame,
            orientation="horizontal",
            height=80
        )
        self.thumbnailScroll.pack(fill="x", padx=10, pady=10)

    def browseFolder():
        pass

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == '__main__':
    app = ImageViewer()
    app.run()
