from tkinter import *
from tkinter import filedialog
import time

window = Tk()
window.title("The Most Dangerous Writing App")

initial_text = None
timer_id = None
button = None
game_over = False

duration = 5
end_time = time.time() + duration

duration_main = 10
end_time_main = time.time() + duration_main

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

window.geometry(f"{width}x{height}")

canvas = Canvas(window, height=8, bg="black", highlightthickness=0)
canvas.pack(fill="x", side="top")

bar = canvas.create_rectangle(0, 0, 0, 8, fill="green")


top_frame = Frame(window, bg="white")
top_frame.pack(side="top", fill="x")

main_label = Label(top_frame, text="Time Remaining", font=('Arial', 30), bd=0, bg="white", pady=11)
main_label.pack()

text_box = Text(window, font=("Arial", 20), bd=0, highlightthickness=0, padx=100)
text_box.pack(fill="both", expand=True)


def reset_timer(event):
    global end_time, timer_id

    if game_over:
        return

    end_time = time.time() + duration

    # Force immediate redraw to full bar
    width = window.winfo_width()
    canvas.coords(bar, 0, 0, width, 8)
    canvas.itemconfig(bar, fill="green")



def update_bar():
    global timer_id, initial_text, end_time, button, game_over

    if game_over:
        return

    remaining = end_time - time.time()
    progress = max(0, remaining / duration)

    width = window.winfo_width()
    canvas.coords(bar, 0, 0, width * progress, 8)

    if progress < 0.2:
        canvas.itemconfig(bar, fill="red")
    elif progress < 0.5:
        canvas.itemconfig(bar, fill="orange")
    else:
        canvas.itemconfig(bar, fill="green")

    if remaining <= 0:
        current_text = text_box.get("1.0", "end-1c")

        if current_text == initial_text:
            game_over = True
            text_box.delete("1.0", "end")
            text_box.config(bg="#ff4d4f")
            button = Button(window, text="Try Again", command=restart, font=("Arial", 20))
            button.config(bg="black", fg="white", activebackground="red")
            button.place(relx=0.5, rely=0.5, anchor="center")
            text_box.config(state=DISABLED)
            main_label.config(text="You Lost")
            return
        else:
            initial_text = current_text



    timer_id = window.after(50, update_bar)

def update_main_timer():
    global end_time_main, game_over

    if game_over:
        return

    remaining = int(end_time_main - time.time())

    if remaining <= 0:
        end_session()
        return

    mins = remaining // 60
    secs = remaining % 60

    main_label.config(text=f"{mins}:{secs:02d}")

    window.after(1000, update_main_timer)

def end_session():
    global button, game_over

    game_over = True

    main_label.config(text="Now you can save your work!")

    text_box.config(state="normal")

    if button is None:
        button = Button(
            window,
            text="💾 Save your work",
            font=("Arial", 20),
            command=save_text
        )
        button.place(relx=0.9, rely=0.05, anchor="center")
    else:
        button.config(text="💾 Save your work", command=save_text)
def restart():
    global end_time, end_time_main, initial_text, button, game_over

    game_over = False

    text_box.config(state="normal")
    text_box.delete("1.0", "end")
    text_box.config(bg="white")

    main_label.config(text="Time Remaining")

    initial_text = ""
    end_time = time.time() + duration
    end_time_main = time.time() + duration_main

    if button:
        button.destroy()
        button = None

    update_bar()
    update_main_timer()

def save_text():
    content = text_box.get("1.0", "end-1c")
    
    file_path = filedialog.asksaveasfilename(
        initialfile=f"writing_{int(time.time())}.txt",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if file_path:  # user didn't cancel
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        main_label.config(text="✅ Saved!")

text_box.bind("<Key>", reset_timer)

initial_text = text_box.get("1.0", "end-1c")
update_main_timer()
update_bar()

window.mainloop()

