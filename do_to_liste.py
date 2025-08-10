
import tkinter as tk

from tkinter import messagebox

import tkinter.font as tkFont 

import os

import time

import pygame

pygame.mixer.init()






class TO_DO:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("To-Do List with Checkboxes")
        self.root.geometry("400x500")
        self.root.configure(bg="white")
        self.root.resizable(0,0)

        self.file_path = r"C:\Users\Utilisateur\Desktop\some project python creative\tasks.txt"

        self.timer_data_file = r"C:\Users\Utilisateur\Desktop\some project python creative\timer_data.txt"
        
        
        self.liste_sound = [r"C:\Users\Utilisateur\Desktop\some project python creative\hello.mp3",
                            r"C:\Users\Utilisateur\Desktop\some project python creative\fuck.mp3",
                            r"C:\Users\Utilisateur\Desktop\some project python creative\good.mp3"]
        self.timer_running = True 
        
        self.time_left = 0
        self.end_time = 0 


        self.Drow()

        self.Add_task()

        self.clean_all()

        self.load_tasks()

        self.check_saved_timer()
        
        
        self.center_window(400,500)

        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

        self.box.bind("<<ListboxSelect>>" ,self.toggle_task_done)
        
        self.box.bind("<BackSpace>" ,self.Remove_task)
        
        self.txt_input.bind('<Return>', lambda event: self.Add_task())
        
        
        self.Mainloop()
        

    def Mainloop(self):
        self.root.mainloop()
        
    def play_sound(self, sound_path):
        try :
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
        except Exception as e:
            print(f'Error playing sound {e}')
            
            
    def center_window(self, width=400, height=500):
     screen_width = self.root.winfo_screenwidth()
     screen_height = self.root.winfo_screenheight()

     x = (screen_width // 2) - (width // 2)
     y = (screen_height // 2) - (height // 2)

     self.root.geometry(f"{width}x{height}+{x}+{y}")
     
     
    def Drow(self):
           
        self.play_sound(self.liste_sound[0])
        self.font = tkFont.Font(family="DS-Digital" , size=20, weight="bold")
         
        self.title = tk.Label(self.root , text="To-Do-Liste" , bg="white",font=self.font)
        self.title.pack(pady=10)
        
        frame = tk.Frame(self.root , bg="white")
        frame.pack(pady=10)
        
        self.txt_input = tk.Entry(frame ,width=25 , font=("Arial" , 12 ))
        self.txt_input.pack(side=tk.LEFT , padx=5)
        

        self.button = tk.Button(frame , text='add',command=self.Add_task )
        self.button.pack(side=tk.LEFT) 

        self.clean_button = tk.Button(frame, text='Clean' , command=self.clean_all)
        self.clean_button.pack(side=tk.LEFT, padx=5) 

        self.timer_button = tk.Button(frame, text='Timer',command=self.open_timer_wid)
        self.timer_button.pack(side=tk.LEFT, padx=5)


        self.box = tk.Listbox(self.root, bg="white", width=50, height=12, font=("DS-Digital", 20), bd=1)
        self.box.pack(padx=10, pady=10)
        
        self.fram_bottom = tk.Frame(self.root , bg="white")
        self.fram_bottom.pack(fill="x" , pady=5)

        content_frame = tk.Frame(self.fram_bottom, bg="white")
        content_frame.pack(fill="x",padx=20)

        self.display = tk.Label(content_frame , text='' , bg="white", fg="red",font=("DS-digital" , 17) )
        self.display.pack(side="left",expand=True , anchor="w")

        self.circle_canvas = tk.Canvas(content_frame, width=20, height=20, bg="white", highlightthickness=0)
        self.circle_canvas.pack(side="left", padx=10)

        self.circle_id = self.circle_canvas.create_oval(2, 2, 18, 18, fill="green")  

 
    def Add_task(self):
        text = self.txt_input.get().strip()
        
        if not text:
            return
        
        self.box.insert(tk.END, text)
        self.txt_input.delete(0,tk.END)
        
        
    def Remove_task(self, event):
        selected_idx = self.box.curselection()
        
        if not selected_idx:
            return 
        
        idx = selected_idx[0]
        self.box.delete(idx)
        
    
    def clean_all(self):
        self.box.delete(0,tk.END)


    def save_tasks(self):
        tasks = self.box.get(0,tk.END)
        with open(self.file_path , "w" , encoding="utf-8") as f:
            for task in tasks:
                f.write(task + "\n")

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path , "r" , encoding="utf-8") as f :
                tasks = f.readlines()
                for task in tasks:
                    task = task.strip()
                    if task:
                        self.box.insert(tk.END , task)


    def toggle_task_done(self , event):
        selected_idx = self.box.curselection()
        if not selected_idx:
            return
        
        idx = selected_idx[0]
        task_text = self.box.get(idx)

        if  task_text.startswith("✓"):
            new_text = task_text[2:]
        
        else:
            new_text = "✓ " + task_text

        self.box.delete(idx)
        self.box.insert(idx ,new_text)

        self.box.selection_set(idx)


    def on_closing(self):
        try:
           self.save_tasks()
        except Exception as e:
            print(f"Error saving tasks:{e}")

        self.root.quit()
        self.root.destroy()

   
    def new_openning_timer(self):
        self.timer_win_two = tk.Toplevel(self.root)
        self.timer_win_two.title("Your time")
        width,height = 300, 80
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()

        x = root_x + root_width 
        y = root_y 

        self.timer_win_two.geometry(f"{width}x{height}+{x}+{y}")
        self.timer_win_two.resizable(0,0)
        self.timer_win_two.config(bg="white")

        self.countdown_label_two = tk.Label(self.timer_win_two, text="", font=("DS-digital", 22), bg="white", fg="blue")
        self.countdown_label_two.pack()
        
        self.frame_two = tk.Frame(self.timer_win_two , bg="white")
        self.frame_two.pack()
        
        self.shot_down_btn = tk.Button(self.frame_two, text="Shot down",command=self.Shot_down_timer_two)
        self.shot_down_btn.pack(side="left", padx=10)
        
        self.stop_btn = tk.Button(self.frame_two, text="Stop", command=self.stop_timer_two)
        self.stop_btn.pack(side="left",pady=5)
        
        self.update_count_two()
        
    def update_count_two(self):
        if self.time_left > 0:
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.countdown_label_two.config(text=f"Time left :{hours:02d}:{minutes:02d}:{seconds:02d}")
 
    def Shot_down_timer_two(self):
        
        self.timer_running = False
        self.time_left = 0 
        
        self.timer_button.config(text="Timer" , command=self.open_timer_wid)
        self.timer_win_two.destroy()
     
    
    def stop_timer_two(self):
        if self.timer_running:
            self.timer_running = False
            self.countdown_label_two.config(fg="red")
            self.stop_btn.config(text="Resume")
            
        else:
            self.timer_running = True
            self.countdown_label_two.config(fg="blue")
            self.stop_btn.config(text="Stop")
            self.background_timer_update()

       
                   
    def open_timer_wid(self):
        self.timer_win = tk.Toplevel(self.root)
        self.timer_win.title("set Timer")
        
        width, height = 300, 150

        
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
    
        x = root_x + root_width + 5
        y = root_y

        self.timer_win.geometry(f"{width}x{height}+{x}+{y}")
        self.timer_win.geometry("300x150")
        self.timer_win.resizable(0,0)
        self.timer_win.config(bg="white")
        
        label = tk.Label(self.timer_win , text="Enter time in houres" , bg="white" , font=("Arial" ,12))
        label.pack(pady=10)

        self.time_entry = tk.Entry(self.timer_win, width=10, font=("Arial", 14))
        self.time_entry.pack(pady=5)
        self.time_entry.focus()

        fram_top = tk.Frame(self.timer_win, bg="white")
        fram_top.pack(pady=10)   
        
        start_btn = tk.Button(fram_top, text="Start", command=self.start_timer)
        start_btn.pack(side=tk.LEFT, padx=10) 

        self.countdown_label = tk.Label(self.timer_win, text="", font=("Arial", 16), bg="white", fg="blue")
        self.countdown_label.pack()
        
        
        self.countdown_label.config(text="")
        self.time_entry.config(state="normal")
        for widget in self.timer_win.winfo_children():
          if isinstance(widget, tk.Button) and widget["text"] == "Start":
            widget.config(state='normal')

        
    def start_timer(self):

        time_str = self.time_entry.get().strip()

        try:
            hours = float(time_str)
            if hours <= 0:
                raise  ValueError
            self.time_left = int(hours * 3600)
        
        except:
            messagebox.showerror("Error" , "Please enter a valid positive number for hours")
            return
        

        end_time = time.time() + self.time_left

        with open(self.timer_data_file, "w") as f:
         f.write(str(end_time))


        self.time_entry.config(state="disabled")

        for widget in self.timer_win.winfo_children():
          if isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
              if isinstance(child, tk.Button) and child["text"] == "Start":
                child.config(state='disabled')


        
        
        self.timer_button.config(text="Your time", command=self.new_openning_timer)
        
        self.timer_running = True
        self.background_timer_update()

        
    
    def background_timer_update(self):
     if self.time_left > 0 and self.timer_running:
        self.time_left -= 1
        
        if hasattr(self, 'countdown_label_two') and self.timer_win_two.winfo_exists():
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.countdown_label_two.config(text=f"Time left :{hours:02d}:{minutes:02d}:{seconds:02d}")

        if hasattr(self, 'countdown_label') and self.timer_win.winfo_exists():
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.countdown_label.config(text=f"Time left :{hours:02d}:{minutes:02d}:{seconds:02d}")

        self.root.after(1000, self.background_timer_update)
     else:
        if self.time_left == 0:
            if os.path.exists(self.timer_data_file):
                os.remove(self.timer_data_file)
            self.check_tasks_done()
            
            if hasattr(self, 'countdown_label') and self.timer_win.winfo_exists():
                self.countdown_label.config(text="")
                
                self.time_entry.config(state="normal")
                for widget in self.timer_win.winfo_children():
                    if isinstance(widget, tk.Button) and widget["text"] == "Start":
                        widget.config(state='normal')
            
            
            
            if hasattr(self, 'timer_win_two') and self.timer_win_two.winfo_exists():
                self.timer_win_two.after(2000, self.timer_win_two.destroy)
                
            if hasattr(self, 'timer_win') and self.timer_win.winfo_exists():
                self.timer_win.after(2000, self.timer_win.destroy)
                
            self.timer_button.config(text="Timer", command=self.open_timer_wid)

    
    
    def update_count(self):
        if self.time_left > 0:
            hours = self.time_left // 3600
            minutes = (self.time_left % 3600) // 60
            seconds = self.time_left % 60
            self.countdown_label.config(text=f"Time left :{hours:02d}:{minutes:02d}:{seconds:02d}")


    def check_tasks_done(self):
        all_done = True
        tasks = self.box.get(0,tk.END)
        for task in tasks:
            if not task.startswith("✓"):
                all_done = False
                break

        if all_done:
            self.circle_canvas.itemconfig(self.circle_id,fill="blue")
            self.display.config(text = "ALL tasks completed!" , fg="blue")
            self.play_sound(self.liste_sound[2])
            
            self.root.after(4000, lambda: self.display.config(text="you can Go now.So let's go", fg="green"))
            self.root.after(6000, lambda: self.circle_canvas.itemconfig(self.circle_id,fill="green"))

        else:
            self.circle_canvas.itemconfig(self.circle_id,fill="red")
            self.display.config(text = "Some tasks are incomplete!" , fg="red")
            self.play_sound(self.liste_sound[1])
            
            self.root.after(6000, lambda: self.display.config(text="you can GO now .So let's go", fg="green"))
            self.root.after(6000, lambda: self.circle_canvas.itemconfig(self.circle_id,fill="green"))


            

     

    def check_saved_timer(self):
        if os.path.exists(self.timer_data_file):
            try:
                with open(self.timer_data_file ,"r") as f:
                    end_time = float(f.read().strip())

                time_left = int(end_time - time.time())

                if time_left > 0:
                    self.timer_button.config(text="Tour Time")
                    self.timer_button.config(command=self.new_openning_timer)
                    self.time_left  = time_left
                    
                    
                    self.timer_running = True
                    self.background_timer_update()
                                    
            except Exception as e:
                print(f"fuck you {e}")
                
    
                
to_do = TO_DO()
