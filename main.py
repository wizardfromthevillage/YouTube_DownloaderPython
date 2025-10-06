from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO


temptag = ""  # For download
storage = []  # For video-pics in the tree


def addvideoinlist():
    with YoutubeDL({'quiet': False}) as ytl:
        info = ytl.extract_info(video_url.get(), download=False)
        thumbnail_url = info.get('thumbnail')

        # Collecting video-pic
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img = img.resize((50, 20))
        photo = ImageTk.PhotoImage(img)

        tree.insert("", "end", text=info['title'], image=photo, tags=f"{video_url.get()}")
        storage.append(photo)


root = tk.Tk()
root.title("Youtube Downloader")
root.geometry("600x900")

label = tk.Label(root, text="Вставь ссылку на видео сюда!")
label.pack()

video_url = tk.Entry(root, width=44)
video_url.pack()

button = tk.Button(root, text="Добавить в список", command=addvideoinlist)
button.pack()

treelabel = tk.Label(root, text="Список видео")
treelabel.pack()

tree = ttk.Treeview(root, columns="name", show='tree')
tree.pack()


def on_select(event):
    selected = tree.selection()
    for iid in selected:
        global temptag
        text = tree.item(iid, "text")
        tags = tree.item(iid, "tag")
        print(f"Название: {text}, Ссылка: {tags}")
        temptag = tags


tree.bind("<<TreeviewSelect>>", on_select)

selected_opt = tk.StringVar(value="bestvideo")

radio1 = tk.Radiobutton(root, text="Лучшее качество", variable=selected_opt, value="bestvideo")
radio1.pack()
radio2 = tk.Radiobutton(root, text="Среднее качество", variable=selected_opt, value="normalvideo")
radio2.pack()
radio3 = tk.Radiobutton(root, text="Плохое качество", variable=selected_opt, value="worstvideo")
radio3.pack()


def downloadvideo():
    choice = selected_opt.get()
    if choice == "bestvideo":
        ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'quiet': False,
            'outtmpl': 'downloads/%(title)s.%(format)s'
        }
    elif choice == "normalvideo":
        ydl_opts = {
            'format': 'bestvideo[height<=720]+bestaudio',
            'quiet': False,
            'outtmpl': 'downloads/%(title)s.%(format)s'
        }
    elif choice == "worstvideo":
        ydl_opts = {
            'format': 'worstvideo+worstaudio',
            'quiet': False,
            'outtmpl': 'downloads/%(title)s.%(format)s'
        }
    with YoutubeDL(ydl_opts) as ytl:
        ytl.download(temptag)


button_download = tk.Button(root, text="Скачать выбранный файл", command=downloadvideo)
button_download.pack()

root.mainloop()
