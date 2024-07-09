from chatos import ChatSerial
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatSerial(root)
    root.mainloop()