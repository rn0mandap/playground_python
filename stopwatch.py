import ctypes
import datetime
import tkinter as tk



class Stopwatch:
	def __init__(self, parent, *arg, **kwarg):
		self.parent = parent
		self.parent.title("Stopwatch")
		self.parent.geometry("150x50")
		self.parent.attributes("-topmost", True)
		self.parent.resizable(0, 0)
		self.center(self.parent, 0, -35)
		
		# python 3, minimize console
		ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
		
		self.set_variables()
		self.set_ui()
		
	
	def save2file(self):
		if self.seconds_from_start <= 10:
			return
		try:
			with open(self.filename, "r") as txtr:
				buff = txtr.read()
		except FileNotFoundError:
			buff = ""
		
		tnow = datetime.datetime.now()
		tstart = tnow - datetime.timedelta(seconds=self.seconds_from_start)
		
		data = "{}/{}/{} {}:{}, ".format(tstart.month, tstart.day, tstart.year, tstart.hour, tstart.minute)
		data += "{}/{}/{} {}:{}, ".format(tnow.month, tnow.day, tnow.year, tnow.hour, tnow.minute)
		data += self.seconds2string(self.seconds_from_start)
		
		buff += data + "\n"
		with open(self.filename, "w") as txtw:
			txtw.write(buff)
		
		
	def set_ui(self):
		self.btn_left = tk.Button(self.parent, width=2, relief="flat", bg="cyan", command=self.btn_left_go)
		self.btn_left.pack(side=tk.LEFT, fill=tk.Y, expand=0)
		self.stopwatch_set()
		self.btn_right = tk.Button(self.parent, width=2, relief="flat", bg="cyan", command=self.btn_right_go)
		self.btn_right.pack(side=tk.LEFT, fill=tk.Y, expand=0)
		
	
	def set_variables(self):
		self.filename = "stopwatch_data.txt"
		self.seconds_from_start = 0
		self.stopwatch_paused = True
		self.stopwatch_position = "se"
		self.move_to = {
			"nw": self.move_nw,
			"ne": self.move_ne,
			"sw": self.move_sw,
			"se": self.move_se
		}
		
	
	def btn_left_go(self, *arg):
		y, x = self.stopwatch_position[0], self.stopwatch_position[1]
		
		if y == "n":
			if x == "e":
				x = "w"
			else:
				y = "s"
		
		elif y == "s":
			if x == "e":
				x = "w"
			else:
				y = "n"
		
		self.stopwatch_position = y + x
		self.move_to[self.stopwatch_position]()
		
	
	def btn_right_go(self, *arg):
		y, x = self.stopwatch_position[0], self.stopwatch_position[1]
		
		if y == "n":
			if x == "w":
				x = "e"
			else:
				y = "s"
		
		elif y == "s":
			if x == "w":
				x = "e"
			else:
				y = "n"
		
		self.stopwatch_position = y + x
		self.move_to[self.stopwatch_position]()
	
	
	def stopwatch_set(self, position="se"):
		self.move_to[position]()
		self.stopwatch_position = position
		
		self.stopwatch_frame = tk.Frame(self.parent, highlightthickness=0, bd=0)
		self.stopwatch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		self.stopwatch_display = tk.Button(self.stopwatch_frame, text="00:00", font=("Comic Sans", 16), relief="flat", command=self.pause_resume, bg="white")
		self.stopwatch_display.pack(fill=tk.BOTH, expand=1)
		self.stopwatch_go()
		
	
	def pause_resume(self, *arg):
		if self.stopwatch_paused:
			self.stopwatch_paused = False
		else:
			self.stopwatch_paused = True
			self.save2file()
			self.seconds_from_start = 0
	
	
	def stopwatch_go(self, *arg):
		n = 0 if self.stopwatch_paused else 1
		self.seconds_from_start += n
		self.stopwatch_display.configure(text=self.seconds2string(self.seconds_from_start))
		self.parent.after(1000, self.stopwatch_go)
		
	
	def seconds2string(self, seconds, shorten=True, *arg):
		h = str(seconds // 3600)
		m = str((seconds % 3600) // 60)
		s = str(seconds % 60)
		h = "0"+h if len(h) == 1 else h
		m = "0"+m if len(m) == 1 else m
		s = "0"+s if len(s) == 1 else s
		txt = "{}:{}:{}".format(h, m, s)
		if seconds // 3600 <= 0 and shorten:
			txt = "{}:{}".format(m, s)
		return txt
	
	
	def move_nw(self): self.parent.geometry("+0+5")
	def move_ne(self): self.parent.geometry("-0+5")
	def move_sw(self): self.parent.geometry("+0-40")
	def move_se(self): self.parent.geometry("-0-40")
	
	
	def center(self, win, x_add=0, y_add=0):
		win.update_idletasks()
		width = win.winfo_width()
		height = win.winfo_height()
		x = (win.winfo_screenwidth() // 2) - (width // 2)
		y = (win.winfo_screenheight() // 2) - (height //2)
		win.geometry("{}x{}+{}+{}".format(width, height, x+x_add, y+y_add))



if __name__ == "__main__":
	root = tk.Tk()
	app = Stopwatch(root)
	root.mainloop()