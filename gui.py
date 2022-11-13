from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# from ctypes import windll
import sounddevice as sd
import glist
from menu import MainMenuBar

DEVICE_LIMIT = 5


class Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Group Listen")
        self.geometry("640x150")

#        windll.shcore.SetProcessDpiAwareness(1)
        
        self.top_bar = TopBar(self)
        self.top_bar.grid(sticky="ew")

        self.main_app = MainApp(self)
        self.main_app.grid(row=1, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

        menu_bar = MainMenuBar(self, self.main_app)
        self.config(menu=menu_bar)

    def run_app(self):
        self.mainloop()

class TopBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        label = Label(self, text="Group Listen")
        label.grid(row=1, column=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

class MainApp(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.duplicating = False

        self.init_devices()

        self.draw_input_device_chooser()
        self.draw_device_switcher()
        self.draw_device_properties()
        self.draw_start_stopper()

    # Clear device list and input device
    def init_devices(self):
        self.all_devices = sd.query_devices()
        self.all_device_names = []
        for i in self.all_devices:
            self.all_device_names.append(i["name"])

        self.input_device = -1

        self.selected_device = 0
        try:
            del self.output_devices
        except:
            pass
        self.output_devices = [-1]

    # Called there is an error while duplicating audio
    def error_callback(self, traceback):
        messagebox.showerror("ERROR", "TRACEBACK: {0}".format(traceback))
        self.stop()

    # Called when start button pressed
    def start(self):
        self.duplicating = True
        
        self.refresh_device_switcher()
        self.refresh_start_stopper()
        self.refresh_input_device_chooser()

        self.sound_duplicator = glist.SoundDuplicator(self.input_device, tuple(self.output_devices), self.error_callback)
        self.sound_duplicator.start_duplication()
        
    # Called when stop button pressed
    def stop(self):
        self.duplicating = False
        
        self.refresh_device_switcher()
        self.refresh_start_stopper()
        self.refresh_input_device_chooser()

        self.sound_duplicator.kill_threads()
        del self.sound_duplicator

    # Called when - button pressed
    def add_device(self):
        if len(self.output_devices) < 5:
            self.output_devices.append(-1)
            print(self.output_devices)
            self.refresh_device_switcher()

        else:
            messagebox.showerror("Error", "You have reached the device limit.")
    # Called when + button pressed
    def remove_device(self):
        if len(self.output_devices) != 1:
            del self.output_devices[self.selected_device]
            self.selected_device = 0
            self.refresh_device_switcher()

        else:
            messagebox.showerror("Error", "There is only 1 device left, this is the minimum")
    
    # Called when > button pressed
    def next_device(self):
        self.selected_device += 1
        self.refresh_device_switcher()
        self.refresh_device_properties()

    # Called when < button pressed
    def previous_device(self):
        self.selected_device -= 1
        self.refresh_device_switcher()
        self.refresh_device_properties()

    # frame with navigation buttons (<>)
    # TODO: Split into own class
    def refresh_device_switcher(self):
        self.remove_device_switcher()
        self.draw_device_switcher()

    def remove_device_switcher(self):
        self.device_switcher.destroy()
    
    def draw_device_switcher(self):
        self.device_switcher = Frame(self)

        next_button = ttk.Button(self.device_switcher, text=">", command=self.next_device)
        if self.selected_device + 1 == len(self.output_devices):
            next_button["state"] = "disabled"
            
        previous_button = ttk.Button(self.device_switcher, text="<", command=self.previous_device)
        if self.selected_device == 0:
            previous_button["state"] = "disabled"

        plus_button = ttk.Button(self.device_switcher, text="+", command=self.add_device)
        minus_button = ttk.Button(self.device_switcher, text="-", command=self.remove_device)

        device_count_text = "[{}], total: [{}]".format(self.selected_device + 1, len(self.output_devices))
        device_count_label = ttk.Label(self.device_switcher, text=device_count_text)

        previous_button.grid(row=0, column=0, sticky="w")
        minus_button.grid(row=0, column=1, sticky="w")

        device_count_label.grid(row=0, column=2)
        self.device_switcher.grid_columnconfigure(2, weight=1)

        plus_button.grid(row=0, column=3, sticky="e")
        next_button.grid(row=0, column=4, sticky="e")

        self.device_switcher.grid(row=1, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

    def refresh_device_properties(self):
        self.device_properties.destroy()
        self.draw_device_properties()

    def refresh_devices(self):
        self.all_devices = sd.query_devices()
        self.all_device_names = []
        for i in self.all_devices:
            self.all_device_names.append(i["name"])

        self.refresh_device_properties()
        self.refresh_input_device_chooser()

    def draw_device_properties(self):
        self.device_properties = ttk.Frame(self)
        self.device_properties["borderwidth"] = 2

        device_picker_label = ttk.Label(self.device_properties, text="Device: ")
        device_picker = ttk.Combobox(self.device_properties)
        device_picker["value"] = self.all_device_names

        if self.output_devices[self.selected_device] != -1:
            device_picker.current(self.output_devices[self.selected_device])

        device_picker.bind("<<ComboboxSelected>>", self.select_output_device)

        refresh_button = ttk.Button(self.device_properties, text="Refresh", command=self.refresh_devices)

        blocksize_changer_label = ttk.Label(self.device_properties, text="Blocksize: ")
        blocksize_entry = ttk.Entry(self.device_properties)
        blocksize_reset = Button(self.device_properties, text="reset")

        device_picker_label.grid(row=0, column=0, sticky="w")
        device_picker.grid(row=0, column=1, sticky="ew")
        refresh_button.grid(row=0, column=2, sticky="w")

        self.device_properties.grid_columnconfigure(1, weight=1)

        self.device_properties.grid(row=2, column=0, sticky="ew")

    def select_output_device(self, event):
        self.output_devices[self.selected_device] = event.widget.current()

    def refresh_start_stopper(self):
        self.start_stopper.destroy()
        self.draw_start_stopper()

    def draw_start_stopper(self):
        self.start_stopper = Frame(self)

        start_button = ttk.Button(self.start_stopper, text="Start", command=self.start)
        stop_button = ttk.Button(self.start_stopper, text="Stop", command=self.stop)

        if self.duplicating == True:
            start_button["state"] = DISABLED
            stop_button["state"] = NORMAL
        else:
            start_button["state"] = NORMAL
            stop_button["state"] = DISABLED


        start_button.grid(column=1, row=0, sticky="e")
        stop_button.grid(column=2, row=0, sticky="w")

        self.start_stopper.grid_columnconfigure(0, weight = 1)
        self.start_stopper.grid_columnconfigure(3, weight = 1)

        self.start_stopper.grid(row=3, column=0, sticky="ew",)

    def select_input_device(self, event):
        self.input_device = event.widget.current()
        print(self.input_device)

    def refresh_input_device_chooser(self):
        self.input_dev_chooser_frame.destroy()
        self.draw_input_device_chooser()

    def draw_input_device_chooser(self):
        self.input_dev_chooser_frame = ttk.Frame(self)
  
        input_chooser_label = ttk.Label(self.input_dev_chooser_frame, text="Input Device: ")
        input_device_chooser = ttk.Combobox(self.input_dev_chooser_frame)
                                            
        input_device_chooser["value"] = self.all_device_names
        if self.input_device != -1:
            input_device_chooser.current(self.input_device)

        input_device_chooser.bind("<<ComboboxSelected>>", self.select_input_device)

        refresh_button = ttk.Button(self.input_dev_chooser_frame, text="Refresh", command=self.refresh_devices)

        input_chooser_label.grid(row=0, column=0, sticky="w")
        input_device_chooser.grid(row=0, column=1, sticky="ew")
        refresh_button.grid(row=0, column=2, sticky="w")
        self.input_dev_chooser_frame.grid_columnconfigure(1, weight=1)

        self.input_dev_chooser_frame.grid(row=0, column=0, sticky="ew")

if __name__ == "__main__":
    root = Window()
    root.run_app()
