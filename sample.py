import Tkinter as tk
import subprocess as sub
p = sub.Popen('./script',stdout=sub.PIPE,stderr=sub.PIPE)
output, errors = p.communicate()

root = tk()
text = Text(root)
text.pack()
text.insert(END, output)
root.mainloop()