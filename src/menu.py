from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import *
from tkinter.font import *
import configparser
from tkinter import messagebox

class InvalidConfigFile(Exception):
	pass

class MainMenuBar(Menu):
	def __init__(self, root, main_app):
		Menu.__init__(self, root)

		self.root = root
		self.file = Menu(self, tearoff=0)
		self.add_cascade(label="File", menu=self.file)
		self.populate_file_menu()

		self.help = Menu(self, tearoff=0)
		self.add_cascade(label="Help", menu=self.help)
		self.populate_help_menu()
		self.main_app = main_app

	def populate_file_menu(self):
		self.file.add_command(label="Clear Devices", command=self.clear_devices)
		self.file.add_command(label="Save Config", command=self.save_config)
		self.file.add_command(label="Open Config", command=self.open_config)
		self.file.add_command(label="Exit", command=lambda:self.root.destroy())

	def populate_help_menu(self):
		self.help.add_command(label="About", command=self.display_about_box)

	def display_about_box(self):
		about = AboutBox(self.root)
		pass	
	def refresh_main_app(self):
		self.main_app.selected_device = 0
		self.main_app.refresh_devices()
		self.main_app.refresh_device_switcher()
		self.main_app.refresh_start_stopper()
		self.main_app.refresh_input_device_chooser()
		

	def clear_devices(self):
		self.main_app.init_devices()
		self.refresh_main_app()

	def read_config_file(self, file):
		config = configparser.ConfigParser()
		config.read(file)

		if int(config["info"]["output_device_count"]) == 0:
			raise InvalidConfigFile

		self.main_app.input_device = config["info"]["input_device"]
		for i in range(0, int(config["info"]["output_device_count"]) ):
			self.main_app.output_devices[i] = config["output_devices"][str(i)]
		print(self.main_app.output_devices)
		self.refresh_main_app()
		file.close()

	def save_config(self):
		save = asksaveasfile(initialfile = 'config.ini', defaultextension=".ini",filetypes=[("All Files","*.*"),("Config files","*.ini")])
		if save != "":
			config = configparser.ConfigParser()
			config["info"]= {
			"input_device": self.main_app.input_device,
			"output_device_count": len(self.main_app.output_devices)
			}
			config["output_devices"] = {}
			for i, dev in enumerate(self.main_app.output_devices):
				config["output_devices"][str(i)] = str(dev)

			config.write(save)
			save.close()

	def open_config(self):
		file = askopenfilename()
		if file != "":
			try:
				self.read_config_file(file)
			except Exception as exc:
				messagebox.showerror("Error", "There was an error while reading the config file")

class AboutBox(Toplevel):
	def __init__(self, root):
		Toplevel.__init__(self, root)
		self.geometry("500x100")
		self.title("About GroupListen")

		program_name = Label(self, text="GroupListen", font=Font(size=20))
		about_text = Label(self, text="Divert audio from one audio device to another on multiple devices at the same time.")
		close_button = Button(self, text="Close", command=lambda:self.destroy())

		program_name.pack()
		about_text.pack()
		close_button.pack()
