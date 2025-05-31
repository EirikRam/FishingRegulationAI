import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .controller import Controller
from .utils import resource_path

config = {
    "PREDICTION_KEY": "ENTER KEY HERE",
    "PREDICTION_ENDPOINT": "https://fishmodel-prediction.cognitiveservices.azure.com/",
    "PROJECT_ID": "ENTER KEY HERE",
    "PUBLISHED_NAME": "Iteration3",
    "IMG_HEIGHT": 224,
    "IMG_WIDTH": 224,
}

controller = Controller(config)

# GUI Globals
image_path = tk.StringVar()
details_font = None
panel = None
regulations_frame = None
result_label = None
chart_frame = None
landing_frame = None
result_frame = None


def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        image_path.set(file_path)
        display_image(file_path)
        classes, probs = controller.predict(file_path)
        display_results(classes, probs)
        show_result_frame()


def display_image(path):
    img = Image.open(path).resize((300, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img


def display_results(classes, probs):
    text = "Top 3 predictions:\n"
    for i in range(len(classes)):
        text += f"{i + 1}. {classes[i]} (Confidence: {probs[i]:.2f})\n"
    result_label.config(text=text)

    if classes:
        show_regulations(classes[0])
    plot_confidence(classes, probs)


def show_regulations(species):
    for w in regulations_frame.winfo_children():
        w.destroy()
    text = controller.get_regulations_text(species)
    label = tk.Label(regulations_frame, text=text, justify=tk.LEFT, font=details_font, fg="black")
    label.pack(fill=tk.BOTH, expand=True)


def plot_confidence(classes, probs):
    colors = ['blue', 'green', 'orange']
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), subplot_kw=dict(aspect="equal"))

    if len(classes) < 3:
        for i in range(3 - len(classes)):
            fig.delaxes(axes[2 - i])

    for i, (ax, cls, prob) in enumerate(zip(axes, classes, probs)):
        ax.pie([prob, 1 - prob], startangle=90, colors=[colors[i], 'lightgray'],
               wedgeprops=dict(width=0.3, edgecolor='w'), autopct='%1.1f%%', pctdistance=0.85)
        ax.set_title(f"{cls}: {prob * 100:.1f}%")

    fig.suptitle("Confidence Levels", fontsize=16)
    for w in chart_frame.winfo_children():
        w.destroy()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def show_result_frame():
    landing_frame.pack_forget()
    result_frame.pack(fill=tk.BOTH, expand=True)


def show_landing_frame():
    result_frame.pack_forget()
    landing_frame.pack(fill=tk.BOTH, expand=True)


def show_history():
    win = tk.Toplevel(root)
    win.title("Search History")
    text = ""
    for i, (cls, prob, img) in enumerate(controller.search_history):
        text += f"Search {i + 1}:\n  1. {cls} (Confidence: {prob:.2f})\n\n"
    tk.Label(win, text=text, justify=tk.LEFT, font=details_font, fg="black").pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


def show_about():
    win = tk.Toplevel(root)
    win.title("About Me")
    win.geometry("400x450")

    about_text = (
        "This app helps users identify fish species\n"
        "using a custom machine learning model and provides\n"
        "relevant fishing regulations.\n\nCurrent supported fish species:\n\n"
    )
    for species in controller.regulations.keys():
        about_text += f"  - {species}\n"

    footer_text = ("\nFlorida Fishing with AI\nVersion: 1.0\n© 2024 Eric Ramirez\n")

    frame = tk.Frame(win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    tk.Label(frame, text=about_text, justify=tk.LEFT, font=details_font, fg="black").grid(row=0, column=0, sticky='nw', padx=10, pady=10)

    thumb = Image.open(resource_path("assets/FishingAI.webp")).resize((100, 100), Image.LANCZOS)
    thumb = ImageTk.PhotoImage(thumb)
    tk.Label(frame, text=footer_text, justify=tk.LEFT, font=details_font, fg="black").grid(row=2, column=0, sticky='sw', padx=10, pady=10)
    label = tk.Label(frame, image=thumb)
    label.image = thumb
    label.grid(row=2, column=0, sticky='se', padx=10, pady=10)


def run_app():
    global root, details_font, panel, regulations_frame, result_label, chart_frame, landing_frame, result_frame

    root = tk.Tk()
    root.title("Florida Fishing with AI")

    toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
    toolbar.pack(side=tk.TOP, fill=tk.X)
    tk.Button(toolbar, text="Find Fish", command=upload_image).pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="History", command=show_history).pack(side=tk.LEFT, padx=2, pady=2)
    tk.Button(toolbar, text="About Me", command=show_about).pack(side=tk.LEFT, padx=2, pady=2)

    landing_frame = tk.Frame(root)
    landing_frame.pack(fill=tk.BOTH, expand=True)

    img = Image.open(resource_path("assets/Florida_Fishing.webp")).resize((400, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    tk.Label(landing_frame, image=img).pack(pady=10)
    landing_frame.image = img

    tk.Label(landing_frame, text="Welcome to Eric's Fishing Regulation App", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(landing_frame, text="© 2024 Eric's Fishing App", font=("Helvetica", 10)).pack(pady=10)
    tk.Button(landing_frame, text="Find My Fish", command=upload_image).pack(pady=20)

    result_frame = tk.Frame(root)
    image_reg_frame = tk.Frame(result_frame)
    image_reg_frame.pack(side=tk.TOP, padx=10, pady=10)

    panel = tk.Label(image_reg_frame)
    panel.pack(side=tk.LEFT, padx=10, pady=10)

    details_font = tkfont.Font(family="Helvetica", size=10, weight="normal")
    regulations_frame = tk.Frame(image_reg_frame, width=300, height=300, bd=1, relief=tk.SOLID)
    regulations_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    result_label = tk.Label(result_frame, text="", justify=tk.LEFT)
    result_label.pack(side=tk.TOP, padx=10, pady=10)

    chart_frame = tk.Frame(result_frame)
    chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()