from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

ydl_opts = {
    'format': 'best',
    'quiet': False,
    'outtmpl': 'downloads/%(title)s.%(ext)s'
}

root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("600x900")

label = tk.Label(root, text="Привет!")
label.pack()

video_url = tk.Entry(root)
video_url.pack()

storage = []

tree = ttk.Treeview(root, columns=("name"), show='tree')
tree.pack()


def addvideoinlist():
    with YoutubeDL(ydl_opts) as ytl:
        info = ytl.extract_info(video_url.get(), download=False)
        thumbnail_url = info.get('thumbnail')

        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((50, 20))
        photo = ImageTk.PhotoImage(img)

        iid = tree.insert("", "end", text=info['title'], image=photo, tags=f"{video_url.get()}")
        storage.append(photo)


temptag = ""
def on_select(event):
    selected = tree.selection()
    for iid in selected:
        global temptag
        text = tree.item(iid, "text")
        tags = tree.item(iid, "tag")
        print(f"Название: {text}, Ссылка: {tags}")
        temptag = tags



tree.bind("<<TreeviewSelect>>", on_select)


button = tk.Button(root, text="Добавить в список", command=addvideoinlist)
button.pack()

def downloadvideo():
    with YoutubeDL(ydl_opts) as ytl:
        ytl.download(temptag)
    
    

button_download = tk.Button(root, text="Скачать выбранный файл", command=downloadvideo)
button_download.pack()

root.mainloop()