import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
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

        # Get pathz dict and folder options
        self.pathz, self.optFolders = self.getPathz()
        self.defaultOpt = ctk.StringVar(value=self.optFolders[0])

        # Text styles dict
        self.textStyles = {
            "header": ctk.CTkFont(size=16, weight="bold", family="Monaco"),
            "button": ctk.CTkFont(size=14, weight="bold", family="Monaco"),
            "normal": ctk.CTkFont(size=12, family="Courier"),
            "small": ctk.CTkFont(size=10, family="Courier")
        }

        self.createWidgets()

    def createWidgets(self):
        """Create all the GUI elements"""

        # Main container frame
        mainFrame = ctk.CTkFrame(self.root)
        mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Top section - Browse button and folder info
        topFrame = ctk.CTkFrame(mainFrame)
        topFrame.pack(fill="x", padx=10, pady=(10, 5))

        # Top left section - For browser and other utilities
        topLeftFrame = ctk.CTkFrame(topFrame)
        topLeftFrame.pack(side="left", fill="both",
                          expand=True, padx=5, pady=(5, 2.5))

        self.browseBtn = ctk.CTkButton(
            topLeftFrame,
            text="📁 Browse Folder",
            command=self.browseFolder,
            font=self.textStyles["button"],
            height=40,
            width=150
        )
        self.browseBtn.pack(side="left", padx=10, pady=10)

        # Dropdown menu for folders
        self.optionDropdown = ctk.CTkComboBox(
            topLeftFrame,
            values=self.optFolders,
            variable=self.defaultOpt,
            command=self.onDropSelection,
            font=self.textStyles["normal"],
            height=40,
            width=140,
            justify="center"
        )
        self.optionDropdown.pack(side="left", padx=(10, 10), pady=10)

        # Top right section - For folder name and other stats
        topRightFrame = ctk.CTkFrame(topFrame)
        topRightFrame.pack(side="right", fill="y", padx=5, pady=(5, 2.5))
        topRightFrame.configure(width=280)

        # Folder path label
        self.folderLabel = ctk.CTkLabel(
            topRightFrame,
            text="No folder selected",
            font=self.textStyles["normal"]
        )
        self.folderLabel.pack(side="left", padx=(20, 10), pady=10)

        # Image count label
        self.countLabel = ctk.CTkLabel(
            topRightFrame,
            text="",
            font=self.textStyles["normal"]
        )
        self.countLabel.pack(side="right", padx=10, pady=10)

        # Main image display area
        self.imageFrame = ctk.CTkFrame(mainFrame)
        self.imageFrame.pack(fill="both", expand=True, padx=10, pady=5)

        # Large image preview label
        self.imageLabel = ctk.CTkLabel(
            self.imageFrame,
            text="Select a folder to view images",
            font=self.textStyles["header"]
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

    def browseFolder(self):
        """Open folder dialog and load images"""
        folderPath = filedialog.askdirectory(title="Select Image Folder")

        if folderPath:
            self.currentFolder = folderPath
            self.folderLabel.configure(
                text=f"Folder: {os.path.basename(folderPath)}")

            # Load images in a separate thread to prevent GUI freezing
            threading.Thread(target=self.loadImages, daemon=True).start()

            # Show loading message
            self.imageLabel.configure(text="Loading images...")
            self.countLabel.configure(text="Loading...")

    def loadImages(self):
        """Load all images from the selected folder"""
        allFiles = os.listdir(self.currentFolder)
        self.imageFiles = [
            f for f in allFiles
            if f.lower().endswith(self.supportedFormats)
        ]

        if not self.imageFiles:
            self.root.after(0, lambda: self.showNoImages())
            return

        # Sort files naturally
        self.imageFiles.sort()

        # Update UI in main thread
        self.root.after(0, lambda: self.updateUIafterLoading())

    def updateUIafterLoading(self):
        """Update the UI after images are loaded"""
        self.countLabel.configure(text=f"{len(self.imageFiles)} images")
        self.currentIndex = 0
        self.createThumbnails()
        self.displayCurrentImage()

    def showNoImages(self):
        """Show message when no images found"""
        self.imageLabel.configure(text="No images found in selected folder")
        self.countLabel.configure(text="0 images")
        # Clear thumbnails
        for widget in self.thumbnailScroll.winfo_children():
            widget.destroy()
        self.thumbnailButtons.clear()

    def createThumbnails(self):
        """Create thumbnail buttons in the filmstrip"""
        # Clear existing thumbnails
        for widget in self.thumbnailScroll.winfo_children():
            widget.destroy()
        self.thumbnailButtons.clear()

        # Create thumbnail for each image
        for i, filename in enumerate(self.imageFiles):
            # Load and resize image for thumbnail
            imagePath = os.path.join(self.currentFolder, filename)
            image = Image.open(imagePath)

            # Create thumbnail button
            image.thumbnail((60, 60), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(
                light_image=image, dark_image=image, size=(60, 60)
            )

            # Create thumbnaul button
            thumbBtn = ctk.CTkButton(
                self.thumbnailScroll,
                image=photo,
                text="",
                width=70,
                height=70,
                command=lambda idx=i: self.selectImage(idx)
            )
            thumbBtn.pack(side="left", padx=2, pady=2)

            # Store reference to prevent garbage collection
            thumbBtn.image = photo
            self.thumbnailButtons.append(thumbBtn)

        # Hightlight first thumbnail
        if self.thumbnailButtons:
            self.highlightThumbnail(0)

    def selectImage(self, index):
        """Select and display image at given index"""
        if 0 <= index < len(self.imageFiles):
            self.currentIndex = index
            self.displayCurrentImage()
            self.highlightThumbnail(index)

    def highlightThumbnail(self, index):
        """Highlight the selected thumbnail"""
        # Reset all thumbnails to normal
        for btn in self.thumbnailButtons:
            btn.configure(
                border_width=2,
                border_color="gray10",
                fg_color=("gray10", "gray10")
            )

        # Highlight selected thumbnail
        if 0 <= index < len(self.thumbnailButtons):
            self.thumbnailButtons[index].configure(
                border_width=3,
                border_color="blue",
                fg_color=("lightblue", "darkblue")
            )

    def displayCurrentImage(self):
        """Display the currently selected image in large preview"""
        if not self.imageFiles:
            return

        # Load current image
        currentFile = self.imageFiles[self.currentIndex]
        imagePath = os.path.join(self.currentFolder, currentFile)

        # Open and resize image to fit display area
        image = Image.open(imagePath)

        # Calculate size to fit in display area (max 600x400)
        maxWidth, maxHeight = 600, 400
        image.thumbnail((maxWidth, maxHeight), Image.Resampling.LANCZOS)

        # Convert to PhotoImage and display
        photo = ctk.CTkImage(
            light_image=image, dark_image=image, size=image.size
        )
        self.imageLabel.configure(image=photo, text="")
        self.imageLabel.image = photo

        # Update window title with filename
        self.root.title(f"Image Viewer - {currentFile}")
        self.currentFile = currentFile

    def getPathz(self):
        with open('paths.json', 'r', encoding='utf-8') as j:
            pathz = json.load(j)
        folders = [p for p in pathz.keys()]

        return pathz, folders

    def onDropSelection(self, selectedValue):
        """Handle dropdown selection changes"""
        self.defaultOpt.set(selectedValue)
        print(f"Moving {self.currentFile} to {selectedValue}")
        # curList = self.pathz[selectedValue]['images']
        if self.currentFile not in self.pathz[selectedValue]['images']:
            self.pathz[selectedValue]['images'].append(self.currentFile)
        # self.pathz[selectedValue]['images'] = curList
        with open('paths.json', 'w', encoding='utf-8') as j:
            json.dump(self.pathz, j, indent=4, ensure_ascii=False)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


if __name__ == '__main__':
    app = ImageViewer()
    app.run()
