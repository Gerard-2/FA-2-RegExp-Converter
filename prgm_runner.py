from GUI import *

MASTER_WIDTH = 500
MASTER_HEIGHT = 300

root = tk.Tk()
root.title("FA To Regular Expression Converter")

width = root.winfo_screenwidth()
height = root.winfo_screenheight()

x_corner = (width / 2) - (MASTER_WIDTH / 2)
y_corner = (height / 2) - (MASTER_HEIGHT / 2)

root.geometry(str(MASTER_WIDTH) + "x" + str(MASTER_HEIGHT) + "+" + str(x_corner) + "+" + str(y_corner))

app = RIJK_App(root, MASTER_WIDTH, MASTER_HEIGHT)

root.mainloop()