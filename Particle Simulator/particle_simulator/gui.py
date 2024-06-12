from particle_simulator import *
import customtkinter
import tkinter as tk

class GUI:
    def __init__(self, sim, title, gridres):
        self.sim = sim
        self.path = os.path.split(os.path.abspath(__file__))[0]

        self.tk = Tk()
        self.tk.title(title)
        self.tk.resizable(0, 0)
        self.tk.protocol("WM_DELETE_WINDOW", self.destroy)
        self.gui_canvas = Canvas(self.tk, width=self.sim.width + 200, height=self.sim.height + 30)
        self.gui_canvas.pack()
        self.canvas = Canvas(self.tk, width=self.sim.width, height=self.sim.height)
        self.canvas.place(x=0, y=30)

        self.code_window = None
        self.extra_window = None

        self.toolbar = self.gui_canvas.create_rectangle(0, 0, self.sim.width, 30, fill="#2E5984")
        self.gui_canvas.create_line(80, 0, 80, 30, fill='grey30')

        self.play_photo = PhotoImage(file=os.path.join(self.path, 'Assets/play.gif'), master=self.tk).subsample(8, 8)
        self.pause_photo = PhotoImage(file=os.path.join(self.path, 'Assets/pause.gif'), master=self.tk).subsample(7, 7)
        self.pause_button = Button(self.gui_canvas, image=self.play_photo if self.sim.paused else self.pause_photo,
                                   cursor='hand2', border='0', bg='#2E5984', activebackground='#2E5984',
                                   command=self.sim.toggle_paused)
        self.pause_button.place(x=40, y=16, anchor='center')

        x = 125
        self.select_img = PhotoImage(file=os.path.join(self.path, 'Assets/select.gif'), master=self.tk).subsample(57, 57)
        self.select_btn = Button(self.tk, image=self.select_img, cursor='hand2', relief=FLAT,
                                 bg='#2E5984', activebackground='#2E5984',
                                 command=lambda: self.sim.change_mode('SELECT')).place(x=x, y=16, anchor='center')
        self.select_rect = self.gui_canvas.create_rectangle(x - 12, 3, x + 12, 27, outline='blue', state='hidden')

        x = 165
        self.move_img = PhotoImage(file=os.path.join(self.path, 'Assets/move.gif'), master=self.tk).subsample(42, 42)
        self.move_btn = Button(self.tk, image=self.move_img, cursor='hand2', relief=FLAT,
                               bg='#2E5984', activebackground='#2E5984',
                               command=lambda: self.sim.change_mode('MOVE')).place(x=x, y=16, anchor='center')
        self.move_rect = self.gui_canvas.create_rectangle(x - 12, 3, x + 12, 27, outline='blue')

        x = 205
        self.add_img = PhotoImage(file=os.path.join(self.path, 'Assets/add.gif'), master=self.tk).subsample(36, 36)
        self.add_btn = Button(self.tk, image=self.add_img, cursor='hand2', relief=FLAT,
                              bg='#2E5984', activebackground='#2E5984',
                              command=lambda: self.sim.change_mode('ADD'))
        self.add_btn.place(x=x, y=15, anchor='center')
        self.add_rect = self.gui_canvas.create_rectangle(x - 13, 3, x + 11, 27, outline='blue', state='hidden')

        self.tabControl = ttk.Notebook(self.tk)
        
        # layout sidebar-GUI
        self.tabControl = ttk.Notebook(self.tk)
        self.tab1 = ttk.Frame(self.tabControl, relief='flat')
        self.tabControl.add(self.tab1, text='Simulation Settings')
        self.tab2 = ttk.Frame(self.tabControl, relief='flat', width=200, height=self.sim.height + 30)
        self.tabControl.add(self.tab2, text='Particle Settings')
        self.tabControl.place(x=self.sim.width, y=0)

        # Spinbox Styles
        spinbox_bg = '#F0F8FE'
        spinbox_font = ('Verdana', 10)
        border_width = 1
        relief_style = 'flat'

        # Create the canvas with the specified background color
        self.tab1_canvas = Canvas(self.tab1, width=200, height=self.sim.height, bg='#BCD2E8')
        self.tab1_canvas.pack()

        # Gravity
        label = Label(self.tab1, text='Gravity:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=20, anchor='nw')
        
        self.gravity_entry = Spinbox(
                self.tab1,
                width=7,
                from_=0,
                to=10,
                increment=0.1,
                bg=spinbox_bg,
                font=spinbox_font,
                bd=border_width,
                relief=relief_style,
            )
        self.gravity_entry.delete(0, END)
        self.gravity_entry.insert(0, self.sim.g)
        self.gravity_entry.place(x=100, y=20)
        self.create_tooltip(self.gravity_entry, "This is the gravity setting.")

        # Air Resistance
        label = Label(self.tab1, text='Air Resistance:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=55, anchor='nw')

        self.air_res_entry = Spinbox(
                self.tab1, 
                width=7, 
                from_=0, 
                to=1, 
                increment=0.01, 
                bg=spinbox_bg,
                font=spinbox_font,
                bd=border_width,
                relief=relief_style,)
        self.air_res_entry.delete(0, END)
        self.air_res_entry.insert(0, self.sim.air_res)
        self.air_res_entry.place(x=100, y=55)
        self.create_tooltip(self.air_res_entry, "This is the air resistance setting.")

        # Ground Friction
        label = Label(self.tab1, text='Ground Friction:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=85, anchor='nw')
        self.friction_entry = Spinbox(
            self.tab1, 
            width=7, 
            from_=0, to=1, 
            increment=0.01,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.friction_entry.delete(0, END)
        self.friction_entry.insert(0, self.sim.ground_friction)
        self.friction_entry.place(x=100, y=85)
        self.create_tooltip(self.friction_entry, "This is the ground friction setting.")

        # Temperature
        label = Label(self.tab1, text='Temperature (Degree Kelvin):', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=115, anchor='nw')
        self.temp_sc = Scale(self.tab1, from_=0, to=100, orient=HORIZONTAL, resolution=0.1, length=175, width=10,
                             tickinterval=20, fg='black', activebackground='midnight blue', cursor='hand2',  bg='#BCD2E8', borderwidth=0, highlightthickness=0)
        self.temp_sc.set(self.sim.temperature)
        self.temp_sc.place(x=100, y=158, anchor='center')
        self.create_tooltip(self.temp_sc, "Adjust the temperature")

        # Simulation Speed
        label = Label(self.tab1, text='Simulation Speed:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=195, anchor='nw')
        self.speed_sc = Scale(self.tab1, from_=0, to=3, orient=HORIZONTAL, resolution=0.01, length=175, width=10,
                              tickinterval=1, fg='black', activebackground='midnight blue', cursor='hand2', bg='#BCD2E8', borderwidth=0, highlightthickness=0)
        self.speed_sc.set(1)
        self.speed_sc.place(x=100, y=238, anchor='center')
        self.create_tooltip(self.speed_sc, "Adjust simulation speed")

        # Display FPS
        self.show_fps = BooleanVar(self.tk, True)
        self.fps_chk = Checkbutton(self.tab1, text='Display FPS', font=('Verdana', 8), var=self.show_fps, bg='#BCD2E8', activebackground='#BCD2E8')
        self.fps_chk.place(x=10, y=270, anchor='nw')
        self.create_tooltip(self.fps_chk, "Toggle display of frames per second")

        # Display Particles
        self.show_num = BooleanVar(self.tk, True)
        self.num_chk = Checkbutton(self.tab1, text='Display Particles Amount', font=('Verdana', 8), var=self.show_num, bg='#BCD2E8', activebackground='#BCD2E8')
        self.num_chk.place(x=10, y=290, anchor='nw')
        self.create_tooltip(self.num_chk, "Toggle display of particles amount")

        self.tab1_canvas.create_text(100, 335, text='Blocking Edges', font=('Verdana', 9), anchor='center')
        self.tab1_canvas.create_line(10, 345, 190, 345, fill='grey50')

        self.top_bool = BooleanVar(self.tk, True)
        self.top_chk = Checkbutton(self.tab1, text='top', font=('Verdana', 8), var=self.top_bool, bg='#BCD2E8', activebackground='#BCD2E8')
        self.top_chk.place(x=30, y=355, anchor='nw')
        self.create_tooltip(self.top_chk, "Toggle visibility of top edge")

        self.bottom_bool = BooleanVar(self.tk, True)
        self.bottom_chk = Checkbutton(self.tab1, text='bottom', font=('Verdana', 8), var=self.bottom_bool,  bg='#BCD2E8', activebackground='#BCD2E8')
        self.bottom_chk.place(x=110, y=355, anchor='nw')
        self.create_tooltip(self.bottom_chk, "Toggle visibility of bottom edge")

        self.left_bool = BooleanVar(self.tk, True)
        self.left_chk = Checkbutton(self.tab1, text='left', font=('Verdana', 8), var=self.left_bool,  bg='#BCD2E8', activebackground='#BCD2E8')
        self.left_chk.place(x=30, y=375, anchor='nw')
        self.create_tooltip(self.left_chk, "Toggle visibility of left edge")

        self.right_bool = BooleanVar(self.tk, True)
        self.right_chk = Checkbutton(self.tab1, text='right', font=('Verdana', 8), var=self.right_bool,  bg='#BCD2E8', activebackground='#BCD2E8')
        self.right_chk.place(x=110, y=375, anchor='nw')
        self.create_tooltip(self.right_chk, "Toggle visibility of right edge")

        # layout tab2
        self.tab2_canvas = Canvas(self.tab2, width=200, height=self.sim.height, bg='#BCD2E8')
        self.tab2_canvas.pack()

        # Radius
        label = Label(self.tab2, text='Radius:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=20, anchor='nw')
        self.radius_entry = Spinbox(
            self.tab2,
            width=7, 
            from_=1, 
            to=300, 
            increment=1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.radius_entry.delete(0, END)
        self.radius_entry.insert(0, 'scroll')
        self.radius_entry.place(x=100, y=20)
        self.create_tooltip(self.radius_entry, "Adjust particle radius")

        # Color
        label = Label(self.tab2, text='Color:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=55, anchor='nw')
        self.color_var = StringVar(self.tk, 'random')
        self.color_entry = Entry(
                self.tab2, 
                width=6, 
                textvariable=self.color_var, 
                bg=spinbox_bg,
                font=spinbox_font,
                bd=border_width,
                relief=relief_style,)
        self.color_entry.place(x=100, y=55)
        self.color_var.trace("w", self.change_color_entry)

        self.part_color_rect = self.tab2_canvas.create_rectangle(165, 53, 185,73, fill=self.sim.bg_color[1],
                                                                 activeoutline='red', tags="part_color_rect")
        self.tab2_canvas.tag_bind("part_color_rect", "<Button-1>", self.ask_color_entry)
        self.create_tooltip(self.color_entry, "Set particle color")

        # Mass
        label = Label(self.tab2, text='Mass:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=85, anchor='nw')
        self.mass_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0.1, 
            to=100, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.mass_entry.delete(0, END)
        self.mass_entry.insert(0, 1)
        self.mass_entry.place(x=100, y=85)
        self.create_tooltip(self.mass_entry, "Set particle mass")

        # Bounciness
        label = Label(self.tab2, text='Bounciness:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=115, anchor='nw')
        self.bounciness_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0, 
            to=1, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.bounciness_entry.delete(0, END)
        self.bounciness_entry.insert(0, 0.7)
        self.bounciness_entry.place(x=100, y=115)
        self.create_tooltip(self.bounciness_entry, "Set particle bounciness")

        # Velocity
        label = Label(self.tab2, text='Velocity:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=145, anchor='nw')

        label = Label(self.tab2, text='X:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=60, y=145, anchor='nw')
        self.velocity_x_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0, 
            to=1, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.velocity_x_entry.delete(0, END)
        self.velocity_x_entry.insert(0, 0)
        self.velocity_x_entry.place(x=100, y=145)
        self.create_tooltip(self.velocity_x_entry, "Set particle velocity along X axis")

        label = Label(self.tab2, text='Y:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=60, y=167, anchor='nw')
        self.velocity_y_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=-5, 
            to=5, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.velocity_y_entry.delete(0, END)
        self.velocity_y_entry.insert(0, 0)
        self.velocity_y_entry.place(x=100, y=167)
        self.create_tooltip(self.velocity_y_entry, "Set particle velocity along Y axis")

        self.locked_bool = BooleanVar(self.tk, False)
        self.locked_chk = Checkbutton(self.tab2, text='Locked', font=('Verdana', 8), 
                                      var=self.locked_bool, bg='#BCD2E8', activebackground='#BCD2E8' )
        self.locked_chk.place(x=7, y=195, anchor='nw')
        self.create_tooltip(self.locked_chk, "Toggle particle locking")

        self.do_collision_bool = BooleanVar(self.tk, False)
        self.do_collision_chk = Checkbutton(self.tab2, text='Check Collisions', font=('Verdana', 8),
                                            var=self.do_collision_bool, bg='#BCD2E8', activebackground='#BCD2E8')
        self.do_collision_chk.place(x=7, y=215, anchor='nw')
        self.create_tooltip(self.do_collision_chk, "Toggle collision detection for particles")

        # Attraction Radius
        label = Label(self.tab2, text='Attraction Radius:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=255, anchor='nw')
        self.attr_r_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=-1, 
            to=500, 
            increment=1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.attr_r_entry.delete(0, END)
        self.attr_r_entry.insert(0, -1)
        self.attr_r_entry.place(x=100, y=255)
        self.create_tooltip(self.attr_r_entry, "Set attraction radius for particles")

        # Attr-strength
        label = Label(self.tab2, text='Attr-strength:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=285, anchor='nw')
        self.attr_strength_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0, 
            to=50, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.attr_strength_entry.delete(0, END)
        self.attr_strength_entry.insert(0, 0.5)
        self.attr_strength_entry.place(x=100, y=285)
        self.create_tooltip(self.attr_strength_entry, "Set attraction strength for particles")

        # Gravity mode
        self.gravity_mode_bool = BooleanVar(self.tk, False)
        self.gravity_mode_chk = Checkbutton(self.tab2, text='Gravity Mode', font=('Verdana', 7),
                                            var=self.gravity_mode_bool, bg='#BCD2E8', activebackground='#BCD2E8')
        self.gravity_mode_chk.place(x=7, y=305, anchor='nw')
        self.create_tooltip(self.gravity_mode_chk, "Toggle gravity mode")

        # Repulsion Radius
        label = Label(self.tab2, text='Repulsion Rad:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=328, anchor='nw')
        self.repel_r_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0, 
            to=500, 
            increment=1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.repel_r_entry.delete(0, END)
        self.repel_r_entry.insert(0, 10)
        self.repel_r_entry.place(x=100, y=328)
        self.create_tooltip(self.repel_r_entry, "Set repulsion radius")

        # Repel Strength
        label = Label(self.tab2, text='Repel Strength:', font=('Verdana', 8), bg='#BCD2E8')
        label.place(x=7, y=351, anchor='nw')
        self.repel_strength_entry = Spinbox(
            self.tab2, 
            width=7, 
            from_=0, 
            to=50, 
            increment=0.1,
            bg=spinbox_bg,
            font=spinbox_font,
            bd=border_width,
            relief=relief_style,)
        self.repel_strength_entry.delete(0, END)
        self.repel_strength_entry.insert(0, 1)
        self.repel_strength_entry.place(x=100, y=351)
        self.create_tooltip(self.repel_strength_entry, "Set repel strength")

        # Copy set and set all 
        self.copy_selected_btn = Button(self.tab2, text='Copy Selected Settings', bg='light coral',
                                        command=self.sim.copy_from_selected, width=23)
        self.copy_selected_btn.place(x=15, y=self.sim.height - 100)
        self.set_selected_btn = Button(self.tab2, text='Set Settings to Selected', bg='light green', command=self.sim.set_selected)
        self.set_selected_btn.place(x=15, y=self.sim.height - 65)
        self.set_all_btn = Button(self.tab2, text='Set Settings to All', bg='light blue', command=self.sim.set_all)
        self.set_all_btn.place(x=15, y=self.sim.height - 30)

    def create_tooltip(self, widget, text):
        ToolTip(widget, text)
        
    def destroy(self):
        self.tk.destroy()

    def ask_color_entry(self, *event):
        color = colorchooser.askcolor(title="Choose color")
        if color[0] is not None:
            self.color_entry.delete(0, END)
            self.color_entry.insert(0, str([math.floor(x) for x in color[0]]))
            self.tab2_canvas.itemconfig(self.part_color_rect, fill=color[1])

    def change_color_entry(self, *event):
        try:
            color = eval(self.color_var.get())
            self.tab2_canvas.itemconfig(self.part_color_rect, fill='#%02x%02x%02x' % tuple(color))
        except:
            if self.color_var.get() == 'random' or self.color_var.get() == '':
                self.tab2_canvas.itemconfig(self.part_color_rect, fill='#ffffff')

    def update(self):
        if self.code_window is not None:
            self.code_window.tk.update()
        if self.extra_window is not None:
            self.extra_window.update()

        self.tk.update()

    def destroy(self):
        if messagebox.askokcancel("Quit", "Do you want to close the application?"):
            self.sim.running = False
            self.tk.destroy()


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()
