import ctypes
import datetime
import tkinter as tk



class LinkPaster:
	def __init__(self, parent, *arg, **kwarg):
		self.parent = parent
		self.parent.title("LinkPaster")
		self.parent.geometry("400x300")
		self.parent.attributes("-topmost", True)
		self.parent.geometry("-0+27")
		
		# python 3, minimize console
		ctypes.windll.user32.ShowWindow(
			ctypes.windll.kernel32.GetConsoleWindow(), 6)
			
		self.mainframe = tk.Frame(self.parent, highlightthickness=0, bd=1,
			relief=tk.SOLID)
		self.mainframe.pack(fill=tk.BOTH, expand=1)
		
		#self.filename = self.time_now()+".txt"
		self.filename = self.time_now()
		self.cd_activated = False
		
		self.set_ui()
		self.reset_filename()
		
		
	def set_ui(self):
		# top frame
		self.top_frame = tk.Frame(self.mainframe, highlightthickness=0, bd=1,
			bg="white", relief=tk.SOLID)
		self.top_frame.pack(fill=tk.X, expand=0)
		self.btn1 = tk.Button(self.top_frame, text="Filename: ", command=self.reset_filename,
			bd=1, relief=tk.SOLID, bg="white")
		self.btn1.pack(side=tk.LEFT, padx=3, pady=3)
		
		self.entry1 = tk.Entry(self.top_frame, bg="light blue", width=17, bd=1, relief=tk.SOLID)
		self.entry1.pack(side=tk.LEFT, pady=2, ipadx=2, ipady=2)
		
		self.btn2 = tk.Button(self.top_frame, text="Paste", 
			command=lambda:self.text1.insert(tk.END, self.parent.clipboard_get()+"\n"),
			bd=1, relief=tk.SOLID, bg="white")
		self.btn2.pack(side=tk.LEFT, padx=3, pady=3)
		
		self.btn3 = tk.Button(self.top_frame, text="Save", command=self.save_file,
			bd=1, relief=tk.SOLID, bg="white", width=7)
		self.btn3.pack(side=tk.RIGHT, padx=3, pady=3)
		
		# bottom frame
		self.bot_frame = tk.Frame(self.mainframe, highlightthickness=0, bd=1,
			bg="blue", relief=tk.SOLID)
		self.bot_frame.pack(fill=tk.BOTH, expand=1)
		
		self.text1 = tk.Text(self.bot_frame, padx=5, pady=5, width=5,
			font="Helvetica 11", bg="white", highlightthickness=0, spacing3=5,
			cursor="arrow")
		self.text1.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
		
		self.text1_scrollbar = tk.Scrollbar(self.bot_frame, width=15)
		self.text1_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
		
		self.text1.config(yscrollcommand=self.text1_scrollbar.set)
		self.text1_scrollbar.config(command=self.text1.yview)
		
		
	def save_file(self, *arg):
		if not self.cd_activated:
			data = self.text1.get(0.0, tk.END)
			if data == "" or data == "\n":
				return
			print(len(data))
			self.filename = self.entry1.get()
			with open(self.filename+".txt", "w") as txtw:
				txtw.write(data)
			self.cd_activated = True
			self.btn3.configure(text="Saving...")
			self.entry1.configure(state=tk.DISABLED)
			self.btn1.configure(state=tk.DISABLED)
			self.btn2.configure(state=tk.DISABLED)
			self.btn3.configure(state=tk.DISABLED)
			self.text1.configure(state=tk.DISABLED)
			self.parent.after(1000, self.deactivate_cd)
			

	def deactivate_cd(self, *arg):
		self.cd_activated = False
		self.entry1.configure(state=tk.NORMAL)
		self.btn1.configure(state=tk.NORMAL)
		self.btn2.configure(state=tk.NORMAL)
		self.btn3.configure(state=tk.NORMAL)
		self.text1.configure(state=tk.NORMAL)
		self.btn3.configure(text="Save")
		
		
	def reset_filename(self, *arg):
		self.entry1.delete(0, tk.END)
		self.entry1.insert(tk.END, self.filename)
		

	def center(self, win, x_add=0, y_add=0):
		win.update_idletasks()
		width = win.winfo_width()
		height = win.winfo_height()
		x = (win.winfo_screenwidth() // 2) - (width // 2)
		y = (win.winfo_screenheight() // 2) - (height //2)
		win.geometry("{}x{}+{}+{}".format(width, height, x+x_add, y+y_add))
		
	
	def time_now(self):
		tnow = datetime.datetime.now()
		tvalues = [tnow.year, tnow.month, tnow.day, tnow.hour, tnow.minute]
		stv = [str(x) for x in tvalues]
		nstv = ["0"+x if len(x) == 1 else x for x in stv]
		data = "{}{}{}_{}{}".format(nstv[0], nstv[1], nstv[2], nstv[3], nstv[4])
		return data
		
		

if __name__ == "__main__":
	root = tk.Tk()
	app = LinkPaster(root)
	root.mainloop()			