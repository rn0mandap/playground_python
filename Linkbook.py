import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tkinter as tk



class LinkBook:
	def __init__(self, parent, *arg, **kwarg):
		self.parent = parent
		self.parent.title("Linkbook")
		self.parent.geometry("500x300")
		self.parent.attributes("-topmost", True)
		#self.parent.resizable(0, 0)
		self.center(self.parent, 0, -35)
		
		self.selected_browser = "Chrome"
		self.txt_filenames = glob.glob("*.txt")
		self.txt_filenames.sort()
		self.selected_filename = self.txt_filenames[0]
		
		self.prime_frame = tk.Frame(self.parent, highlightthickness=0, bd=1, relief=tk.SOLID)
		self.prime_frame.pack(fill=tk.BOTH, expand=1)
		
		self.side_frame = tk.Frame(self.prime_frame, highlightthickness=0, bd=1, bg="white", relief=tk.SOLID)
		self.side_frame.pack(side=tk.LEFT, fill=tk.Y, expand=0)
		self.main_frame = tk.Frame(self.prime_frame, highlightthickness=0, bd=0, bg="black")
		self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
		
		self.set_listbox_ui(self.side_frame)
		self.set_content_ui(self.main_frame)
		
		for i in range(len(self.txt_filenames)):
			self.listbox.insert(tk.END, self.txt_filenames[i])
			
		self.load_txtfilecontents()

	
	def load_txtfilecontents(self, *arg):
		try:
			index = self.listbox.curselection()[0]
		except:
			index = 0  # none selected
			self.listbox.select_set(0)
		fn = self.txt_filenames[index]
		self.selected_filename = self.txt_filenames[index]
		
		self.filename_display.config(text="{} ({}/{})".format(fn[:-4], index+1, len(self.txt_filenames)))
		
		with open(fn, "r") as txtr:
			buff = txtr.read()
		self.text1.config(state=tk.NORMAL)
		self.text1.delete(0.0, tk.END)
		self.text1.insert(tk.END, buff)
		self.text1.config(state=tk.DISABLED)
		
	
	def toggle_selected_browser(self):
		if self.selected_browser == "Chrome":
			self.selected_browser = "Firefox"
		else:
			self.selected_browser = "Chrome"
		self.toggle_browser.config(text=self.selected_browser)
		
		
	def set_listbox_ui(self, frame):
		w = 15
		self.listbox = tk.Listbox(frame, width=w, selectmode=tk.BROWSE, font="Helvetica 9")
		self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
		self.listbox_scrollbar = tk.Scrollbar(frame, width=12)
		self.listbox_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
		self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)
		self.listbox_scrollbar.config(command=self.listbox.yview)
		self.listbox.bind("<<ListboxSelect>>", self.load_txtfilecontents)
		

	def launch(self):
		self.prime_frame.destroy()
		self.parent.geometry("200x100")
		self.parent.attributes("-topmost", False)
		self.parent.iconify()
		self.launch_frame = tk.Frame(self.parent, highlightthickness=0, bd=1, relief=tk.SOLID)
		self.launch_frame.pack(fill=tk.BOTH, expand=1)
		
		websites = []
		with open(self.selected_filename, "r") as txtr:
			buff = txtr.read()
		websites = buff.split("\n")
		if self.selected_browser == "Chrome":
			options = webdriver.ChromeOptions()
			options.add_argument("--incognito")
			driver = webdriver.Chrome(options=options)
		elif self.selected_browser == "Firefox":
			firefox_profile = webdriver.FirefoxProfile()
			firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
			driver = webdriver.Firefox(firefox_profile=firefox_profile)
		nwebsites = [x.split(" ") for x in websites]
		for i in range(len(websites)):
			try:
				
				if nwebsites[i][0] == "":
					continue  # skip to next
				if i == 0:
					driver.get(nwebsites[i][0])
				else:
					if self.selected_browser == "Chrome":
						driver.execute_script("window.open('{}', 'tab{}');".format(nwebsites[i][0], i))
					elif self.selected_browser == "Firefox":
						driver.execute_script("window.open('');")
						driver.get(nwebsites[i][0])
						# goes to last website in txt file and opens new window
			except:
				continue
		
			
	def set_content_ui(self, frame):
		topframe = tk.Frame(frame, highlightthickness=0, bd=1, bg="white", relief=tk.SOLID)
		bottomframe = tk.Frame(frame, highlightthickness=0, bd=1, bg="white", relief=tk.SOLID)
		topframe.pack(side=tk.TOP, fill=tk.X)
		bottomframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
		# TOP FRAME
		self.filename_display = tk.Label(topframe, text="Filename", bg="white")
		self.filename_display.pack(side=tk.LEFT, padx=1, pady=1)
		self.btn_launch = tk.Button(topframe, text="Launch", bd=1, bg="white", relief=tk.SOLID, command=self.launch)
		self.btn_launch.pack(side=tk.RIGHT, padx=1, pady=1)
		self.toggle_browser = tk.Button(topframe, text=self.selected_browser, bd=1, width=7, bg="white", relief=tk.SOLID, command=self.toggle_selected_browser)
		self.toggle_browser.config(state="disabled")  # firefox not working properly
		self.toggle_browser.pack(side=tk.RIGHT, padx=1, pady=1)
		# BOTTOM FRAME
		self.text1 = tk.Text(bottomframe, padx=5, pady=5, width=5, font="Helvetica 11", bg="white", highlightthickness=0, cursor="arrow", spacing3=5)
		self.text1.pack(side=tk.LEFT, expand=1, fill=tk.BOTH)
		self.text1_scrollbar = tk.Scrollbar(bottomframe, width=15)
		self.text1_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
		self.text1.config(yscrollcommand=self.text1_scrollbar.set)
		self.text1_scrollbar.config(command=self.text1.yview)
		for i in range(42):
			self.text1.insert(tk.END, "HEYEHEY{}\n".format(i))	
		self.text1.config(state=tk.DISABLED)
	
	
	'''
	def set_listbox_ui(self, frame):
		# WHAT I AM TRYING TO DO:
		# Listbox, mouse_wheel moves selection up and down
		# selecting element in line automatically
		def mouse_wheel(event):
			n = -1 if event.delta == 120 else 1  # 120 up, -120 down
			self.listbox.select_set(self.listbox.curselection()[0]+n)
			self.listbox.activate(self.listbox.curselection()[0]+n)
			print("{}, {}".format(self.listbox.curselection()[0]+n, self.listbox.curselection()[0]+n))
			
		#self.listbox = tk.Listbox(frame, selectmode=tk.BROWSE, yscrollcommand=0)
		self.listbox = tk.Listbox(frame, selectmode=tk.BROWSE)
		self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		self.listbox_scrollbar = tk.Scrollbar(frame)
		self.listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		#self.listbox.config(yscrollcommand=self.listbox_scrollbar.set)
		#self.listbox_scrollbar.config(command=self.listbox.yview)
		self.listbox.bind("<MouseWheel>", mouse_wheel)
		
		for i in range(42):
			self.listbox.insert(tk.END, "HEy{}".format(i))
		
		
		self.listbox.select_set(19)
	'''
		
		
		
	def center(self, win, x_add=0, y_add=0):
		win.update_idletasks()
		width = win.winfo_width()
		height = win.winfo_height()
		x = (win.winfo_screenwidth() // 2) - (width // 2)
		y = (win.winfo_screenheight() // 2) - (height //2)
		win.geometry("{}x{}+{}+{}".format(width, height, x+x_add, y+y_add))



if __name__ == "__main__":
	root = tk.Tk()
	app = LinkBook(root)
	root.mainloop()