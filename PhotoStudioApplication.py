"""
This program implements a PhotoStudio application using Tkinter and Pillow modules.
"""

#Importing all the necessary modules required 
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance
from PIL.ExifTags import TAGS


# Main Window

#Creating the main window using tkinter
window = Tk()
window.title("PhotoStudio Application")
window.configure(bg='white')
window.geometry("1000x600")

#Creating a left frame to place all the buttons on the left hand side of the window
leftframe = Frame(window, width=400, height=600, bg='lightgrey')
leftframe.pack(side="left", fill="y")

#Creating a canvas which is used to display the images
canvas = Canvas(window, width=750, height=600, bg='white')
canvas.pack(fill="x")


#Declaring the filename and global variables
filename = ""
global originalimage, displayedimage, filteredimage

#Open photo function to open an image and display it on the window
def openphoto():
    """
    Open a photo from the file system and display it on the canvas.
    """
    global originalimage, displayedimage, filterimage, filename

    filename = filedialog.askopenfilename(initialdir="C:/Users/Carol/Desktop/Gallery", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpeg"),("JPG Files", "*.jpg")])

    if filename : #Checking if the filename exists
        originalimage = Image.open(filename)
        requiredwidth = 500
        scale = requiredwidth / originalimage.width
        width = int(originalimage.width * scale)
        height = int(originalimage.height * scale)
        displayedimage = originalimage.resize((width, height), Image.LANCZOS) #Displaying the image after resizing it to fit the tkinter window
        filterimage = displayedimage.copy()  
        canvas.config(width=width, height=height) #Updating the height and width of the canvas to match the dimensions of the displayed image

        displayedimagetk = ImageTk.PhotoImage(displayedimage) #Converting the displayedimage into a Tkinter-compatible format
        canvas.image = displayedimagetk #Assigning the tkinter-compatible image to the attribute to keep a reference
        canvas.create_image(0, 0, image=displayedimagetk, anchor="nw") #Image is displayed on the window anchoring it to the north-west corner

    else :
        messagebox.showerror("Error", "No image opened") #If filename is empty then an error message is displayed


def showphoto():
    """
    Show the currently opened photo in a separate window.
    """
    global filename
    if filename:
        img = Image.open(filename)
        img.show()
    else:
        messagebox.showerror("Error", "No image opened")

#Filters function to add filters onto the image
def filters(filtername):
    """
    Apply different image filters to the displayed image.

    Parameters:
        filtername()= The name of the filter to be applied.

    Filter names:
        - "Black and White"
        - "Blur"
        - "Sharpen"
        - "Brightness"
        - "Darkness"
        - "Sepia"
    """
    global displayedimage, filterimage, filename

    if filename:
        filterimage = displayedimage.copy()

        #Checking the filter selected by the user
        if filtername == "Black and White":
            filterimage = ImageOps.grayscale(filterimage) #Converts the image to grayscale
        elif filtername == "Blur":
            filterimage = filterimage.filter(ImageFilter.BLUR) #Blurs the image
        elif filtername == "Sharpen":
            filterimage = filterimage.filter(ImageFilter.SHARPEN) #Sharpens the image
        elif filtername == "Brightness":
            enhancer = ImageEnhance.Brightness(filterimage) #Creating an ImageEnhance object to adjust brightness
            factor = 1.25 #Defining the factor to increase the brightness 
            filterimage = enhancer.enhance(factor) #Applying the brightness enhancement to the image
        elif filtername == "Darkness":
            enhancer = ImageEnhance.Brightness(filterimage) #Creating an ImageEnhance object to adjust darkness
            factor = 0.5 #Defining the factor to decrease the darkness 
            filterimage = enhancer.enhance(factor) #Applying the darkness enhancement to the image
        elif filtername == "Sepia":
            sepiafilter = [(0.393, 0.769, 0.189), (0.349, 0.686, 0.168), (0.272, 0.534, 0.131)] #Creating a list of tuples for the sepia filter values
            filterimage = filterimage.convert('RGB') #Converting the image into RGB format (incase its not already)
            width, height = filterimage.size #Finding the size of the image
            pixels = filterimage.load() #Loading the pixel values of the image to access individual pixel values of the image
            for x in range(width):
                for y in range(height):
                    r, g, b = pixels[x, y] #Extracting RGB values from the pixels at points x,y

                    #Calculating the new values of the RGB channels using the sepia filter list 
                    newr = int((r * sepiafilter[0][0]) + (g * sepiafilter[0][1]) + (b * sepiafilter[0][2])) 
                    newg = int((r * sepiafilter[1][0]) + (g * sepiafilter[1][1]) + (b * sepiafilter[1][2]))
                    newb = int((r * sepiafilter[2][0]) + (g * sepiafilter[2][1]) + (b * sepiafilter[2][2]))
                    pixels[x, y] = (newr, newg, newb) #Updating the pixel values with the new sepia values
        else:
            messagebox.showerror("Error", "No filter selected!")

        displayedimagetk = ImageTk.PhotoImage(filterimage)
        canvas.image = displayedimagetk
        canvas.create_image(0, 0, image=displayedimagetk, anchor="nw")

    else:
        messagebox.showerror("Error", "No image opened")

#Resize photo function to resize the photo 
def resizephoto():
    """
    Resize the displayed image based on user input.

    Ask the user to enter the new width and height for the image.
    """
    
    global originalimage, displayedimage, filterimage

    if filename:
                
        #Asking the user for the new height and width using a simple dialog box to get integer input
        newwidth = simpledialog.askinteger("Resize", "Enter new width:")
        newheight = simpledialog.askinteger("Resize", "Enter new height:")

        #Clearing the canvas 
        canvas.delete("all")

        if newwidth and newheight:
            displayedimage = originalimage.resize((newwidth, newheight), Image.LANCZOS) #Resizes the original image using the inputs given by the user using the LANCZOS algorithm
            filterimage = displayedimage.copy() #Creating a copy of the displayed image to the filter image so that the image is preserved

            chosenfilter = filtercombobox.get() 
            if chosenfilter != "" :
                filters(chosenfilter)
                
            displayedimagetk = ImageTk.PhotoImage(filterimage) #Converting the displayedimage into a Tkinter-compatible format
            canvas.image = displayedimagetk #Assigning the tkinter-compatible image to the attribute to keep a reference
            canvas.create_image(0, 0, image=displayedimagetk, anchor="nw")
            canvas.config(width=displayedimage.width, height=filterimage.height)

    else:
        messagebox.showerror("Error", "No image opened")

#Function to display the metadata of the function
def metadata():
    """
    Display the metadata information of the currently opened image.

    The metadata includes information such as file name, size, format, mode,
    and EXIF data if available.
    """
    global filename, originalimage, displayedimage

    if filename: #Checks if filename is empty or not

        if displayedimage: #Checks if the displayedimage is empty or not
            #Creating a dictionary to store the data of the image
            metadatadictionary = {
                "Filename": filename,
                "Image Size": displayedimage.size,
                "Image Height": displayedimage.height,
                "Image Width": displayedimage.width,
                "Image Format": displayedimage.format,
                "Image Mode": displayedimage.mode,
            }

            #Retrieving the exif data of the original image 
            exifdata = originalimage.getexif()
            if exifdata: #Checks if there is exifdata available
                for tagid, data in exifdata.items(): #Iterating through the items of the exifdata
                    tag = TAGS.get(tagid, tagid) #Converting the numerical tag into human readable tag
                    if isinstance(data, bytes): #Checks if the data is in a byte string 
                        data = data.decode() #Decoding the byte string into a unicode string
                    metadatadictionary[tag] = data #Storing the tag and its data in the dictionary
            metadata = ""
            for key, value in metadatadictionary.items(): #Iterating through the dictionary
                metadata += f"{key}: {value}\n"
            messagebox.showinfo("Image Metadata", metadata)
        else:
            messagebox.showinfo("Error", "No image")
    else:
        messagebox.showerror("Error", "No image opened")

#Save photo function to save the photo  
def savephoto():
    """
    Save the filtered image to a file on the file system.

    Ask the user to choose a location and provide a file name for the saved image.
    """
    global filename, filterimage
    if filename:
        savefilename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("JPEG Files", ".jpg"), ("PNG Files", ".png")])

        if savefilename: #Checks if the filename is empty or not
            filterimage.save(savefilename) #Saving the image with the name 
            messagebox.showinfo("Save Image", "Image saved successfully.")
        else:
            messagebox.showerror("Save Image", "No image to save.")

"""
All the buttons required for the functions.
""" 
openbutton = ttk.Button(leftframe, text="Open Photo", command=openphoto)
openbutton.pack(pady=10)

showbutton = ttk.Button(leftframe, text="Show Photo", command=showphoto)
showbutton.pack(pady=10)

filtercombobox = ttk.Combobox(leftframe, values=["", "Black and White", "Blur", "Sharpen", "Brightness", "Darkness", "Sepia"])
filtercombobox.pack()

filterbutton = ttk.Button(leftframe, text="Apply Filter", command=lambda: filters(filtercombobox.get()))
filterbutton.pack()

resizebutton = ttk.Button(leftframe, text="Resize Photo", command=resizephoto)
resizebutton.pack(pady=10)

metadatabutton = ttk.Button(leftframe, text="Image Metadata", command=metadata)
metadatabutton.pack(pady=10)

savebutton = ttk.Button(leftframe, text="Save Photo", command=savephoto)
savebutton.pack(pady=10)

window.mainloop()
