from tkinter import *

if __name__ == "__main__":
    root = Tk()
    root.title("TicTacToe")
    root.resizable(False, False)
    frame_height = 600
    frame_width = frame_height * 2
    # Set the size of the window and center it
    root.geometry(
        f"{frame_width}x{frame_height}+{int((root.winfo_screenwidth() - frame_width) / 2)}+{int((root.winfo_screenheight() - frame_height) / 2)}")
    root.update()
    normal_colors = {"background": "#000000", "letters": "#FFFFFF", "buttons": "#FFFFFF", "field": "#FFFFFF"}
    field_canvas = Canvas(root, bg=normal_colors["background"], height=frame_height, width=int(frame_width / 2))
    field_canvas.place(x=0, y=0)
    specific_ui_canvas = Canvas(root, bg=normal_colors["background"], height=int(frame_height * 0.75),
                                width=int(frame_width / 2))
    specific_ui_canvas.place(x=int(frame_width / 2 + 1), y=0)
    general_ui_canvas = Canvas(root, bg=normal_colors["background"], height=int(frame_height / 4),
                               width=int(frame_width / 2))
    general_ui_canvas.place(x=int(frame_width / 2 + 1), y=int(frame_height * 0.75 + 1))
    root.mainloop()
