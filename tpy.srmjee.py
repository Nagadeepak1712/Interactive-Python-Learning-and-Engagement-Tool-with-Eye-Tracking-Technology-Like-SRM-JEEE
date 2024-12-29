import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import numpy as np
from PIL import Image, ImageTk
import queue

class IntroWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Welcome")

        # Set up the introduction canvas
        self.canvas = tk.Canvas(master, width=400, height=600, bg='#282c34')
        self.canvas.pack()

        # Introduction text
        self.intro_text = self.canvas.create_text(200, 300, text="Press Enter to Continue", 
                                                  fill='#61dafb', font=("Helvetica", 24))

        # Bind Enter key to continue function
        self.master.bind("<Return>", self.start_quiz)

    def start_quiz(self, event):
        self.master.withdraw()  # Hide the intro window instead of destroying it
        self.open_quiz_window()

    def open_quiz_window(self):
        quiz_window = tk.Toplevel(root)
        quiz_window.geometry("800x600")
        quiz_tool = QuizWindow(quiz_window)

        camera_window = tk.Toplevel(root)
        camera_window.geometry("400x600")
        camera_tool = CameraWindow(camera_window)

class QuizWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Memory Enhancement Tool")

        # Set up grid layout
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Set the portrait canvas for quiz
        self.canvas = tk.Canvas(master, width=800, height=600, bg='#282c34')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Initialize variables
        self.question_index = 0
        self.selected_answer = tk.StringVar()
        self.time_left = 60
        self.score = 0
        self.total_questions = 10  # Total number of questions
        self.questions = self.load_questions()
        self.setup_question()

        # Quit Button
        self.quit_button = tk.Button(master, text="Quit", command=self.quit_app, fg='#ffffff', bg='#ff6f61', font=("Helvetica", 14))
        self.canvas.create_window(400, 550, window=self.quit_button)

    def load_questions(self):
        # Creative and diverse set of questions
        return [
            {"question": "What is the output of `print(2 ** 3)`?", "options": ["6", "8", "9", "10"], "answer": "8"},
            {"question": "Which keyword is used to define a function in Python?", "options": ["func", "function", "define", "def"], "answer": "def"},
            {"question": "What is the data type of `[]` in Python?", "options": ["tuple", "dictionary", "list", "set"], "answer": "list"},
            {"question": "What does the `len()` function do?", "options": ["Returns the length of an object", "Returns the last element", "Returns the type of an object", "Returns a sorted list"], "answer": "Returns the length of an object"},
            {"question": "How do you comment out a line in Python?", "options": ["//", "/* */", "#", "<!-- -->"], "answer": "#"},
            {"question": "What is the output of `print(3 // 2)`?", "options": ["1", "1.5", "2", "0"], "answer": "1"},
            {"question": "Which module in Python is used for generating random numbers?", "options": ["math", "random", "sys", "os"], "answer": "random"},
            {"question": "How do you create a variable with the floating number 2.8?", "options": ["x = 2.8", "x = int(2.8)", "x = str(2.8)", "x = '2.8'"], "answer": "x = 2.8"},
            {"question": "Which operator is used to compare two values?", "options": ["=", "==", "<>", "><"], "answer": "=="},
            {"question": "Which of these data types is immutable?", "options": ["list", "set", "dictionary", "tuple"], "answer": "tuple"},
            {"question": "What will `print('Hello' * 2)` output?", "options": ["Hello Hello", "Hello2", "HelloHello", "Hello, Hello"], "answer": "HelloHello"},
            {"question": "What is the default value of an uninitialized variable in Python?", "options": ["None", "0", "''", "undefined"], "answer": "None"},
            {"question": "What does `list(map(str, [1, 2, 3]))` return?", "options": ["['1', '2', '3']", "[1, 2, 3]", "['1', 2, 3]", "['1', '2', 3]"], "answer": "['1', '2', '3']"},
            {"question": "What is the result of `type([]) == list`?", "options": ["True", "False", "None", "Error"], "answer": "True"},
            {"question": "What is the purpose of the `__init__` method in a class?", "options": ["Initialization", "Destruction", "Inheritance", "Encapsulation"], "answer": "Initialization"},
            {"question": "Which built-in function can be used to read a file line by line?", "options": ["readlines()", "read()", "readfile()", "filelines()"], "answer": "readlines()"}
        ]

    def setup_question(self):
        # Display the question with a colorful label
        question = self.questions[self.question_index]
        self.canvas.delete("all")
        self.question_label = self.canvas.create_text(400, 100, text=question["question"], 
                                                      fill='#61dafb', font=("Helvetica", 16), width=350)

        # Display the answer options as colorful radio buttons
        colors = ['#ff6f61', '#6b5b95', '#88b04b', '#ffcc5c']  # Colorful options
        self.radio_buttons = []
        for i, (option, color) in enumerate(zip(question["options"], colors)):
            radio_button = tk.Radiobutton(self.master, text=option, variable=self.selected_answer, 
                                          value=option, fg=color, bg='#282c34', 
                                          font=("Helvetica", 14), selectcolor='#61dafb')
            self.canvas.create_window(400, 200 + i*50, window=radio_button)
            self.radio_buttons.append(radio_button)

        # Submit button with a bright color
        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_answer, 
                                       fg='#ffffff', bg='#ff6f61', font=("Helvetica", 14))
        self.canvas.create_window(400, 450, window=self.submit_button)

        # Timer display
        self.timer_label = self.canvas.create_text(400, 50, text=f"Time Left: {self.time_left} seconds", 
                                                   fill='#ffffff', font=("Helvetica", 16))
        self.update_timer()

    def check_answer(self):
        correct_answer = self.questions[self.question_index]["answer"]
        user_answer = self.selected_answer.get()

        if user_answer == correct_answer:
            self.score += 1
            messagebox.showinfo("Correct!", "Your answer is correct.")
        else:
            messagebox.showerror("Wrong!", f"The correct answer is: {correct_answer}")

        self.question_index += 1

        if self.question_index < self.total_questions:
            self.setup_question()
            self.time_left = 60
            self.update_timer()
        else:
            self.show_final_result()

    def update_timer(self):
        if self.time_left > 0:
            self.canvas.itemconfig(self.timer_label, text=f"Time Left: {self.time_left} seconds")
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.check_answer()  # Move to the next question or finish

    def show_final_result(self):
        if self.score >= 7:  # Pass mark is 7 out of 10
            messagebox.showinfo("Quiz Completed", f"Congrats, you have passed! Your score is {self.score}/{self.total_questions}.")
        else:
            messagebox.showinfo("Quiz Completed", f"Better luck next time. Your score is {self.score}/{self.total_questions}.")
        self.master.quit()

    def quit_app(self):
        self.master.quit()

class CameraWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera Feed")

        # Set up grid layout
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Set the canvas for camera feed
        self.canvas = tk.Canvas(master, width=400, height=600, bg='black')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Initialize OpenCV variables
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.capture = cv2.VideoCapture(0)
        self.warning_count = 0
        self.max_warnings = 10  # Increase the maximum number of warnings
        self.queue = queue.Queue()

        # Start the camera feed in a separate thread
        self.thread = threading.Thread(target=self.track_eyes)
        self.thread.start()

        # Update camera feed
        self.update_camera_feed()

    def track_eyes(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x + w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)

                if len(eyes) >= 1:
                    # Draw rectangle around the face and eyes
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 0, 0), 2)
                    self.warning_count = 0  # Reset warning count if eyes are detected
                else:
                    # If eyes are not detected, show a warning message
                    if self.warning_count < self.max_warnings:
                        self.warning_count += 1
                        if self.warning_count == self.max_warnings:
                            self.show_warning_popup()

                    elif self.warning_count >= self.max_warnings:
                        self.master.quit()  # Exit the application
                        break

            # Put the frame in the queue for Tkinter to access
            self.queue.put(frame)

    def show_warning_popup(self):
        messagebox.showwarning("WARNING", "Please look at the screen!")

    def update_camera_feed(self):
        if not self.queue.empty():
            frame = self.queue.get()
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

        self.master.after(10, self.update_camera_feed)  # Update every 10 ms

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")
    intro_window = IntroWindow(root)
    root.mainloop()
