from encoding_module import *
from facial_recognition_module import *
from tkinter import *
import os

class GUI:
    def __init__(self, root, main_class):
        self.main_screen = root
        self.main_class = main_class
        self.initialize_colors()
        self.main_account_screen()
        
    def initialize_colors(self):
        global blue, green, caribbean_current, cambridge_blue, sage, peach_yellow
        blue = "#033F63"
        green = "#157145"
        caribbean_current = "#28666E"
        cambridge_blue = "#7C9885"
        sage = "#B5B682"
        peach_yellow = "#FEDC97"
        
    # Designing Main window
    def main_account_screen(self):        
        self.main_screen.geometry("300x250")
        self.main_screen.title("Account Login")
        Label(text="STUDENT ATTENDANCE LOG", fg="white", bg=blue, width="300", height="2", font=("Calibri", 16, "bold")).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", font=("Calibri", 12), command = self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", font=("Calibri", 12), command = self.register).pack()
        self.main_screen.bind("<Control-w>", self.close_main_window)
        self.main_screen.mainloop()
        
    def close_main_window(self, event=None):
        self.main_screen.destroy()
    
    # Window for registration
    def register(self):
        global register_screen
        register_screen = Toplevel(self.main_screen)
        register_screen.title("Register")
        register_screen.geometry("350x300")
    
        global first_name
        global last_name
        global first_name_entry
        global last_name_entry
        
        first_name = StringVar()
        last_name = StringVar()
    
        Label(register_screen, text="Please enter your details below:", fg="white", bg=blue, width="300", height="2", font=("Calibri", 16, "bold")).pack()
        Label(register_screen, text="").pack()
        first_name_label = Label(register_screen, text="First Name * ", font=("Calibri", 14))
        first_name_label.pack()
        first_name_entry = Entry(register_screen, textvariable=first_name, width=30)
        first_name_entry.pack()
        last_name_label = Label(register_screen, text="Last Name * ", font=("Calibri", 14))
        last_name_label.pack()
        last_name_entry = Entry(register_screen, textvariable=last_name, width=30)
        last_name_entry.pack()
        Label(register_screen, text="").pack()
        Button(register_screen, text="Register", bg=green, fg="white",width="20", height="2", font=("Calibri", 12), command=self.register_user).pack()
        Button(register_screen, text="Back", bg="lightblue", width="13", height="2", font=("Calibri", 10), command=lambda: self.back_button(register_screen)).pack()

    # Implementing event on register button
    def register_user(self):
        first_name_info = first_name.get().upper()
        last_name_info = last_name.get().upper()
        folder_path = f"dataset/{last_name_info}_{first_name_info}"
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            self.student_instance = NewStudent(first_name_info, last_name_info)
            self.encoding_menu()
        
            first_name_entry.delete(0, END)
            last_name_entry.delete(0, END)
            register_screen.destroy()
        else:
            self.user_exists()
            
    # Popup for user already exists msg
    def user_exists(self):
        global user_exists_screen
        user_exists_screen = Toplevel(register_screen)
        user_exists_screen.title("An error occurred")
        user_exists_screen.geometry("350x150")
        Label(user_exists_screen, text="This student already exists in the database.", fg="red", width="300", height="2", font=("Calibri", 13, "bold")).pack()
        Label(user_exists_screen, text="Please log in instead", width="300", height="2", font=("Calibri", 13, "bold")).pack()

        Button(user_exists_screen, text="OK", bg=green, fg="white",width="20", height="2", command=self.delete_user_exists_screen).pack()
            
    def inform_user_no_pics(self):
        global inform_user_no_pics_screen
        inform_user_no_pics_screen = Toplevel(encoding_menu_screen)
        inform_user_no_pics_screen.title("A Gentle Reminder")
        inform_user_no_pics_screen.geometry("300x100")
        Label(inform_user_no_pics_screen, text="You have not submitted any images yet.").pack()
        Button(inform_user_no_pics_screen, text="OK", command=self.delete_inform_user_no_pics).pack()
        
    def encoding_menu(self):
        global encoding_menu_screen
        encoding_menu_screen = Toplevel(self.main_screen)
        encoding_menu_screen.title("New Student Encoding")
        encoding_menu_screen.geometry("500x500")
        
        Label(encoding_menu_screen, text="ENCODING MENU", bg=blue, fg="white", width="300", height="2", font=("calibri", 20)).pack()
        Label(encoding_menu_screen, text="").pack()
        
        Button(encoding_menu_screen, text="Pose for image collection", width=35, height=2, bg=peach_yellow, font=("calibri", 15), command = self.student_instance.save_face_images).pack()
        Button(encoding_menu_screen, text="Manually upload images for encoding", width=35, height=2, bg=sage, font=("calibri", 15), command = self.student_instance.upload_images).pack()
        Button(encoding_menu_screen, text="Crop your images for faster encoding", width=35, height=2, bg=cambridge_blue, font=("calibri", 15), command = lambda: self.crop_images_bttn(encoding_menu_screen)).pack()
        Button(encoding_menu_screen, text="Encode new images", width=35, height=2, bg=caribbean_current, fg="white", font=("calibri", 15), command = lambda: self.encode_new_imgs_bttn(encoding_menu_screen)).pack()
        Button(encoding_menu_screen, text="Back", bg="lightblue", width=15, height=2, font=("Calibri", 12), command=lambda: self.back_button(encoding_menu_screen)).pack()

    def crop_images_bttn(self, screen):
        message = self.student_instance.img_crop_face()
        if message == "":
            self.inform_user_no_pics()
        else:
            self.success(message, screen)
    
    def encode_new_imgs_bttn(self, screen):
        message = self.student_instance.encode_new_images()
        if message == "":
            self.inform_user_no_pics()
        else:
            self.success(message, screen)
        
    # Window for login 
    def login(self):
        global login_screen
        login_screen = Toplevel(self.main_screen)
        login_screen.title("Login")
        login_screen.geometry("500x200")
        Label(login_screen, text="Please look directly into the camera.", font=("calibri", 20)).pack()
        Label(login_screen, text="").pack()
    
        Button(login_screen, text="Ready", width=20, height=2, bg = green, fg = "white", font=("calibri", 15), command = lambda: self.login_trigger(login_screen)).pack()
        Button(login_screen, text="Back", bg="lightblue", width=15, height=2, font=("Calibri", 12), command=lambda: self.back_button(login_screen)).pack()

    def login_trigger(self, screen):
        message = attendance_check()
        self.success(message, screen)
        
    # Poopup for login success
    def success(self, message, screen):
        global login_success_screen
        login_success_screen = Toplevel(screen)
        login_success_screen.title("Success")
        login_success_screen.geometry("600x100")
        Label(login_success_screen, text=message, font=("calibri", 15)).pack()
        Button(login_success_screen, text="OK", width=10, height=2, bg = green, fg = "white", font=("calibri", 10), command=self.delete_login_success).pack()
    
    # Popup for login invalid password
    def password_not_recognised(self):
        global password_not_recog_screen
        password_not_recog_screen = Toplevel(login_screen)
        password_not_recog_screen.title("Success")
        password_not_recog_screen.geometry("150x100")
        Label(password_not_recog_screen, text="Invalid Password ").pack()
        Button(password_not_recog_screen, text="OK", command=self.delete_password_not_recognised).pack()
    
    def back_button(self, current_screen):
        current_screen.destroy()
        
    # Deletion popups
    def delete_login_success(self):
        login_success_screen.destroy()
        
    def delete_inform_user_no_pics(self):
        inform_user_no_pics_screen.destroy()
    
    def delete_password_not_recognised(self):
        password_not_recog_screen.destroy()
    
    def delete_user_exists_screen(self):
        user_exists_screen.destroy()
 
 

 
 
