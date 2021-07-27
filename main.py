"""An image watermarking desktop app"""

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps

FONT = "Courier"
GREY = "#545454"
WHITE = "#ffffff"

# NOTE: Change this path to find your photo directory - set as "/" to start from home dir
SOURCE_DIRECTORY = "../Pictures"

# NOTE: TO CUSTOMISE THIS APP WITH YOU OWN LOGO: all you need to do is save your logo to this
# project directory and then change the below text to the name of your logo (can be png or jpg).
# (The app is currently configured for square shaped logos, the size ratio can be altered in the add_watermark function)
LOGO = "logo.png"


class WaterMarker(Tk):
    def __init__(self):
        super(WaterMarker, self).__init__()
        self.title("WaterMarker")

        corner_icon = PhotoImage(file="logo.png")
        self.iconphoto(True, corner_icon)

        self.canvas = Canvas(width=800, height=600, bg=WHITE, highlightthickness=0)
        self.canvas.grid(columnspan=4, rowspan=6)

        self.message_text = Label(text="", font=(FONT, 16), fg=GREY, bg=WHITE)

        self.logo = Image.open(LOGO).convert("RGBA")

        self.start_text = Label(text="If so, please select the image you \nwould like to WaterMark!",
                                font=(FONT, 16), fg=GREY, bg=WHITE)

        self.find_img_btn = Button(text="Select Image", bg=GREY, fg=WHITE, font=(FONT, 18), command=self.find_img)
        self.add_wtrmrk_btn = Button(text="Add Logo", bg=GREY, fg=WHITE, font=(FONT, 18), command=self.add_watermark)
        self.save_final_btn = Button(text="Save Image", bg=GREY, fg=WHITE, font=(FONT, 18), command=self.save)
        self.go_again_btn = Button(text="Go Again", bg=GREY, fg=WHITE, font=(FONT, 18), command=self.find_img)

        self.radio_state = IntVar()
        self.position = (0, 0)

        self.top_left_btn = Radiobutton(text="Top Left", value=1, variable=self.radio_state,
                                        command=self.set_logo_position, fg=GREY, bg=WHITE, font=(FONT, 14))
        self.top_right_btn = Radiobutton(text="Top Right", value=2, variable=self.radio_state,
                                         command=self.set_logo_position, fg=GREY, bg=WHITE, font=(FONT, 14))
        self.bottom_left_btn = Radiobutton(text="Bottom Left", value=3, variable=self.radio_state,
                                           command=self.set_logo_position, fg=GREY, bg=WHITE, font=(FONT, 14))
        self.bottom_right_btn = Radiobutton(text="Bottom Right", value=4, variable=self.radio_state,
                                            command=self.set_logo_position, fg=GREY, bg=WHITE, font=(FONT, 14))

        self.show_logo = None
        self.filename = None
        self.img = None
        self.img_label = None
        self.wm_logo = None
        self.final_img = None

        self.start()

    def start(self):
        self.message_text.config(text="Welcome to WaterMarker!\n\nWould you like to add this logo to an image?\n"
                                      "(If not see the NOTE in main.py)")
        self.message_text.grid(row=1, column=0, columnspan=4)

        # Display logo to be added as the watermark to any images
        logo_big = self.logo.resize((170, 170))
        logo_tk = ImageTk.PhotoImage(logo_big)
        self.show_logo = Label(image=logo_tk, bg=WHITE)
        self.show_logo.image = logo_tk
        self.show_logo.grid(row=2, column=1, columnspan=2)

        self.start_text.grid(row=3, column=0, columnspan=4)

        self.find_img_btn.grid(row=4, column=1, columnspan=2)

    def find_img(self):
        self.start_text.grid_forget()
        self.message_text.config(text="Find your image...", )

        self.filename = filedialog.askopenfilename(initialdir=SOURCE_DIRECTORY, title="Select A File",
                                                   filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))

        if self.filename:

            self.img = Image.open(self.filename).convert("RGBA")

            # Keeps correct orientation of image
            self.img = ImageOps.exif_transpose(self.img)

            # Display selected image
            show_img = self.img.resize((400, 400))
            photo = ImageTk.PhotoImage(show_img)
            self.img_label = Label(image=photo)
            self.img_label.image = photo

            self.show_logo.grid_forget()
            self.img_label.grid(row=2, column=1, columnspan=2)

            self.find_img_btn.grid(row=4, column=1, columnspan=1)
            self.add_wtrmrk_btn.grid(row=4, column=2, columnspan=1)

        else:
            self.find_img_btn.grid(row=4, column=1, columnspan=2)

        self.go_again_btn.grid_forget()

    def set_logo_position(self):
        selected_position = self.radio_state.get()
        if selected_position == 1:
            # top left
            self.position = (0, 0)
        elif selected_position == 2:
            # top right
            self.position = (self.img.size[0] - self.wm_logo.size[0], 0)
        elif selected_position == 3:
            # bottom left
            self.position = (0, self.img.size[1] - self.wm_logo.size[1])
        else:
            # bottom right
            self.position = (self.img.size[0] - self.wm_logo.size[0], self.img.size[1] - self.wm_logo.size[1])
        self.add_watermark()

    def add_watermark(self):
        self.message_text.config(text="Does this look ok?\n"
                                      "(Any distortion here will not\nbe reflected in the saved image).")

        # Watermark size relative to image
        # proportional to shorter side of the image (this is for a square logo)
        if self.img.size[0] <= self.img.size[1]:
            resize = round(self.img.size[0] * 0.2)
        else:
            resize = round(self.img.size[1] * 0.2)
        self.wm_logo = self.logo.resize((resize, resize))

        # Radio buttons for choosing logo location
        self.top_left_btn.grid(row=3, column=0)
        self.top_right_btn.grid(row=3, column=1)
        self.bottom_left_btn.grid(row=3, column=2)
        self.bottom_right_btn.grid(row=3, column=3)

        # Create watermarked image (logo on top of image)
        self.final_img = Image.new('RGBA', self.img.size, (0, 0, 0, 0))
        self.final_img.paste(self.img, (0, 0))
        self.final_img.paste(self.wm_logo, self.position, mask=self.wm_logo)

        final_img_show = self.final_img
        final_img_show = final_img_show.resize((400, 400))

        # Display final image (might be distorted but saved version will not be)
        watermarked = ImageTk.PhotoImage(final_img_show)

        self.img_label = None
        self.img_label = Label(image=watermarked)
        self.img_label.image = watermarked
        self.img_label.grid(row=2, column=1, columnspan=2)

        self.add_wtrmrk_btn.grid_forget()
        self.save_final_btn.grid(row=4, column=2, columnspan=1)

    def save(self):

        self.top_left_btn.grid_forget()
        self.top_right_btn.grid_forget()
        self.bottom_left_btn.grid_forget()
        self.bottom_right_btn.grid_forget()

        self.find_img_btn.grid_forget()
        self.save_final_btn.grid_forget()
        self.go_again_btn.grid(row=4, column=1, columnspan=2)

        # Save watermarked image
        final_img_save = self.final_img.convert("RGB")
        final_img_name = self.filename[:-4] + "_watermark.jpg"
        final_img_save.save(final_img_name)

        self.message_text.config(text=f"Image saved as: \n{final_img_name}\n\n"
                                      f"Do you want to watermark another image?")


water_marker = WaterMarker()
water_marker.mainloop()
