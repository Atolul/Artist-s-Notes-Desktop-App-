from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os
import shutil
import uuid

window = Tk()
window.geometry("700x400")
window.title("Artist's Notes")
window.config(background="#3b3b3b")

DATA_FILE = "data.json"
IMAGE_FOLDER = "data/images"

os.makedirs(IMAGE_FOLDER, exist_ok=True)

image_count = 0
image_entries = []


# ---------Upload button-----------
button_frame = tk.Frame(window, bg="#3b3b3b")
button_frame.pack(fill="x", pady=10)

#-------Scrollable area-----------
scroll_frame = tk.Frame(window, bg= "#3b3b3b")
scroll_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(scroll_frame,bg="#3b3b3b",highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

image_frame = tk.Frame(canvas, bg="#3b3b3b")

canvas_window = canvas.create_window((350,0), window=image_frame, anchor="n")

#--------------------------------------

def display_item(image_path, description_text=""):
     #Create new label for this image
            global image_count

            original_image = Image.open(image_path)

            #Create thumbnail
            display_image = original_image.copy()
            display_image.thumbnail((300,300))

            photo = ImageTk.PhotoImage(display_image)
    
            row = image_count // 2
            column = image_count % 2
    
             #Create a frame for description
            item_frame = tk.Frame(image_frame, bg="#3b3b3b")
            item_frame.grid(row=row, column=column, padx=5, pady=5)

    
            #Image
            image_label = tk.Label(item_frame, image=photo, bg="#797979")
            image_label.pack()
    
            # keep it alive
            image_label.image = photo
    
            
    
            image_label.bind("<Button-1>", lambda event, img=original_image: expand_image(img))
    
            description_frame = tk.Frame(item_frame, bg="#797979")
            description_frame.pack(pady=(5,0))
    
            #Description
            description = tk.Text(description_frame, width=35, height=4, wrap="word", bg="gray")
            description_scrollbar = tk.Scrollbar(description_frame, command=description.yview)
    
            description.configure(yscrollcommand=description_scrollbar.set)
            description.pack(side="left")
            description_scrollbar.pack(side="right", fill="y")
    
            description.insert(1.0, description_text)
    
            image_count +=1

            image_entries.append({
                 "image_path": image_path,
                 "description_widget": description
            })

    
            #Automatically scroll down after upload
            canvas.update_idletasks()
            canvas.yview_moveto(1.0)


def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

image_frame.bind("<Configure>", update_scrollregion)

def mouse_scroll(event):
    canvas.yview_scroll(-1*(event.delta//120), "units")

canvas.bind_all("<MouseWheel>",mouse_scroll)

#-------------------------------

image_count = 0

image_entries = []

#-----Expand image func---------
def expand_image(original_image):
    #create a new window
    expanded_window = tk.Toplevel(window)
    expanded_window.title("Image")

    #Get original image dimensions
    width, height = original_image.size

    #Make the window the same size as image
    expanded_window.geometry(f"{width}x{height}")

    expanded_photo = ImageTk.PhotoImage(original_image)

    image_label = tk.Label(expanded_window, image=expanded_photo, bg="#3b3b3b", cursor="hand2")
    image_label.pack()

    image_label.image = expanded_photo

   # expanded_window.maxsize(1000,1000)


def add_image():
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif")
        ]
    )

    if file_path:

        extension = os.path.splitext(file_path)[1]
        image_name = f"{uuid.uuid4()}{extension}"

        saved_path = os.path.join(IMAGE_FOLDER, image_name)
        shutil.copy2(file_path, saved_path)

        display_item(saved_path)

def save_data():
     data = []

     for entry in image_entries:
          description_text = entry["description_widget"].get("1.0","end-1c")
          data.append({
               "image_path":entry["image_path"],
               "description": description_text
          })

     with open(DATA_FILE, "w", encoding="utf-8") as file:
          json.dump(data, file, indent=4, ensure_ascii=False)

     print("Saved successfully!")

save_button = tk.Button(button_frame, text="Save", command=save_data)
save_button.pack(side="left",padx=10)

def load_data():
     if not os.path.exists(DATA_FILE):
          return
     with open(DATA_FILE, "r", encoding="utf-8") as file:
          data = json.load(file)

     for entry in data:
          image_path = entry["image_path"]
          description = entry["description"]

          if os.path.exists(image_path):
               display_item(image_path, description)

def close_app():
     save_data()
     window.destroy()

window.protocol("DELETE_WINDOW", close_app)

add_button = tk.Button(
    window,
    text="Upload Image",
    command=add_image
)
add_button.pack(pady=20)

load_data()

window.mainloop()