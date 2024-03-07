import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import mysql.connector
import datetime
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox
from tkinter import PhotoImage


class HomePage(tk.Frame):
    def __init__(self, parent, uid):
        self.image_references = []
        tk.Frame.__init__(self, parent)
        parent.geometry("1000x600")
        self.main_dashboard = None
        self.uid = uid
        self.login_time = datetime.datetime.now()

        # Create a connection to the database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1qaz2wsx",
            database="group15"
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(f"SELECT name FROM student WHERE uid={self.uid}")
        self.student_name = self.mycursor.fetchone()[0]

        # Get all the courses a student takes
        self.mycursor.execute(f"SELECT course_id FROM enrolls_in WHERE uid={self.uid}")
        courses = self.mycursor.fetchall()
        self.courses = [course[0] for course in courses]

        self.mycursor.execute(f"SELECT email FROM student WHERE uid={self.uid}")
        self.user_email = self.mycursor.fetchone()[0]
        
        # Get the current day of the week (0 = Monday, 1 = Tuesday, etc.) and current time
        now = datetime.datetime.now()
        current_day = now.weekday()
        current_time = now.time()


        # Function to get the difference in days between two days
        def calculate_days_difference(current_day, class_day):
            return (class_day - current_day) % 7

        # Convert timedelta to time object
        def timedelta_to_time(td):
            return (datetime.datetime.min + td).time()

        # Calculate the nearest upcoming class session from now
        self.nearest_session = None
        self.nearest_session_time = None
        min_days_difference = 7
        for course in self.courses:
            self.mycursor.execute(f"SELECT * FROM class_session WHERE course_id={course}")
            sessions = self.mycursor.fetchall()
            for session in sessions:
                class_day = session[4].upper()
                days = {
                    'MON': 0,
                    'TUE': 1,
                    'WED': 2,
                    'THU': 3,
                    'FRI': 4,
                    'SAT': 5,
                    'SUN': 6
                }
                class_day_num = days[class_day]
                days_difference = calculate_days_difference(current_day, class_day_num)

                session_time = timedelta_to_time(session[1])

                # Check if the class time is in the future
                is_future_class = (days_difference == 0 and session_time > current_time) or days_difference > 0

                if is_future_class and (days_difference < min_days_difference or (days_difference == min_days_difference and session_time > current_time)):
                    self.nearest_session = session
                    self.nearest_session_time = session_time
                    min_days_difference = days_difference

        # Get the upcoming class's name, time, venue (address), zoom link, teacher's message, and course materials
        self.mycursor.execute(f"SELECT course_name, instructor_name, teacher_msg, course_code, course_info FROM course WHERE course_id={self.nearest_session[0]}")
        course_info = self.mycursor.fetchone()

        self.mycursor.execute(f"SELECT material_name, link FROM courseMaterial WHERE course_id={self.nearest_session[0]}")
        self.course_materials = self.mycursor.fetchall()

        # Store the information in variables
        self.upcoming_class_name = course_info[0]
        self.upcoming_class_instructor = course_info[1]
        self.upcoming_class_teacher_msg = course_info[2]
        self.upcoming_class_code = course_info[3]
        self.upcoming_class_info = course_info[4]
        self.upcoming_class_start_time = self.nearest_session[1]
        self.upcoming_class_end_time = self.nearest_session[2]
        self.upcoming_class_date = self.nearest_session[4]
        self.upcoming_class_address = self.nearest_session[3]
        self.upcoming_class_zoom_link = self.nearest_session[5]


        # Sidebar
        sidebar = tk.Frame(self, bg="#6FAE61")
        sidebar.place(relx=0, rely=0, relwidth=0.2, relheight=1)

        # Load HKU logo image
        hku_logo_image = Image.open("image/hku_logo.png")
        # Calculate new dimensions
        hku_logo_new_width = int(parent.winfo_reqwidth()*0.18)
        hku_logo_new_height = int(parent.winfo_reqheight()*0.25)
        # Resize HKU logo
        hku_logo_image = hku_logo_image.resize((hku_logo_new_width, hku_logo_new_height), Image.ANTIALIAS)
        hku_logo_image = ImageTk.PhotoImage(hku_logo_image)
        # HKU logo
        hku_logo = tk.Label(sidebar, image=hku_logo_image, bg="#6FAE61")
        hku_logo.image = hku_logo_image
        hku_logo.place(relx=0, rely=0, relwidth=1, relheight=0.20)

        # Load student profile image
        student_profile_image = Image.open("image/student_profile.png")
        # Calculate new dimensions while maintaining aspect ratio
        student_profile_width, student_profile_height = student_profile_image.size
        student_profile_new_height = int(parent.winfo_reqheight() * 0.2)
        student_profile_new_width = int(student_profile_new_height * (student_profile_width / student_profile_height))
        # Resize student profile image
        student_profile_image = student_profile_image.resize((student_profile_new_width, student_profile_new_height), Image.ANTIALIAS)
        student_profile_image = ImageTk.PhotoImage(student_profile_image)
        # Student profile pic
        student_profile_pic = tk.Button(sidebar, image=student_profile_image, command=self.display_personal_info, bg="white")
        student_profile_pic.image = student_profile_image
        student_profile_pic.place(relx=0.25, rely=0.19, relwidth=0.5, relheight=0.15)

        # Home button
        home_button = tk.Button(sidebar, text="COURSE INFO", command=self.go_to_main_dashboard, bg="#6FAE61", relief="ridge", borderwidth=2)
        home_button.place(relx=0, rely=0.35, relwidth=1, relheight=0.15)

        logout_button = tk.Button(sidebar, text="Logout", command=self.logout, bg="#6FAE61", relief="flat", borderwidth=0)
        logout_button.place(relx=0.5 - 0.5 * 0.5, rely=0.85, relwidth=0.5, relheight=0.05)

        # Schedule button
        schedule_button = tk.Button(sidebar, text="SCHEDULE", command=self.display_schedule, bg="#6FAE61", relief="ridge", borderwidth=2)
        schedule_button.place(relx=0, rely=0.50, relwidth=1, relheight=0.15)

        nearest_class_time = str(self.nearest_session_time)[0:5]
        if (nearest_class_time[0] == '0'):
            nearest_class_hour = int(nearest_class_time[1])
            if (nearest_class_time[3] == '0'):
                nearest_class_minute = int(nearest_class_time[4])
            else:
                nearest_class_minute = int(nearest_class_time[3:5])
            nearest_class_time = nearest_class_hour + nearest_class_minute/60
        # check if there is class within an hour
        current_hour = str(self.login_time)[11:13]
        current_minute = str(self.login_time)[14:16]
        if (current_hour[0] == '0'):
            current_hour = int(current_hour[1])
            if (current_minute[0] == '0'):
                current_minute = int(current_minute[1])
            else:
                current_minute = int(current_minute)
        else:
            current_hour = int(current_hour)
        
        current_time = int(current_hour) + int(current_minute)/60
        
        if (current_time <= nearest_class_time-1 or current_time >= nearest_class_time):
            self.display_schedule()
            #delete the home button
            home_button.destroy()
            #make the schedule button to the original position of home button
            schedule_button.place(relx=0, rely=0.35, relwidth=1, relheight=0.15)
        else:
            # Create the initial main dashboard
            self.go_to_main_dashboard()

    def go_to_main_dashboard(self):
        # Clear the main dashboard
        if self.main_dashboard:
            self.main_dashboard.destroy()

        # Create a new main dashboard
        self.main_dashboard = tk.Frame(self)
        self.main_dashboard.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        # Welcome message
        welcome_frame = tk.Label(self.main_dashboard)
        welcome_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.1)

        welcome_msg = tk.Label(welcome_frame, text=f"Welcome, {self.student_name}! \n Keep fighting!")
        welcome_msg.pack()

        login_time = tk.Label(welcome_frame, text="Login time: " + str(self.login_time))
        
        login_time.pack()

        # Upcoming Class section
        upcoming_class_frame = tk.Frame(self.main_dashboard)
        upcoming_class_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.4)

        upcoming_class_label = tk.Label(upcoming_class_frame, text="Upcoming Class")
        upcoming_class_label.pack()

        class_info = tk.Label(upcoming_class_frame, text=f"{self.upcoming_class_code}: {self.upcoming_class_name}")
        class_info.pack()

        class_time = tk.Label(upcoming_class_frame, text=f"Time: {self.upcoming_class_start_time} - {self.upcoming_class_end_time}")
        class_time.pack()

        class_address = tk.Label(upcoming_class_frame, text=f"Venue: {self.upcoming_class_address}")
        class_address.pack()

        class_address = tk.Label(upcoming_class_frame, text=f"Course Information: {self.upcoming_class_info}", wraplength=400)
        class_address.pack()

        zoom_link_container = tk.Frame(upcoming_class_frame)
        zoom_link_container.pack()

        zoom_link_label = tk.Label(zoom_link_container, text="Zoom link:")
        zoom_link_label.grid(row=0, column=0)

        zoom_link = tk.Label(zoom_link_container, text=self.upcoming_class_zoom_link, fg="blue", cursor="hand2")
        zoom_link.grid(row=0, column=1)
        zoom_link.bind("<Button-1>", lambda e: webbrowser.open(self.upcoming_class_zoom_link))

        teacher_msg = tk.Label(upcoming_class_frame, text=f"Teacher's message: {self.upcoming_class_teacher_msg}")
        teacher_msg.pack()

        # Course material links
        teacher_msg_material_frame = tk.Frame(self.main_dashboard)
        teacher_msg_material_frame.place(relx=0, rely=0.55, relwidth=1, relheight=0.7)

        course_material_label = tk.Label(teacher_msg_material_frame, text="Course Materials:")
        course_material_label.pack()

        # Assuming course materials is a list of tuples (material_name, link)

        # Set a fixed height for the Text widget
        material_links = tk.Text(teacher_msg_material_frame, wrap=tk.WORD, height=30)
        material_links.pack(padx=10, pady=5)

        # Configure and bind tags for clickable links
        material_links.tag_configure('link')
        material_links.tag_bind('link', '<Enter>', lambda e: material_links.config(cursor='hand2'))
        material_links.tag_bind('link', '<Leave>', lambda e: material_links.config(cursor='arrow'))
        original_icon = Image.open("image/pdf_icon.png")
        resized_icon = original_icon.resize((20, 20), Image.ANTIALIAS)

        def make_lambda(link):
            return lambda e: webbrowser.open(link)
       

        for index, (material_name, link) in enumerate(self.course_materials, start=1):
            icon_photoimage = ImageTk.PhotoImage(resized_icon)
            self.image_references.append(icon_photoimage)  # Keep a reference
            material_links.image_create(tk.END, image=icon_photoimage)
            material_links.insert(tk.END, " ") 
            link_tag = f"link{index}"  # Unique tag for each link
            material_links.insert(tk.END, material_name, (link_tag,))
            material_links.insert(tk.END, "\n")
            material_links.insert(tk.END, "\n")

            material_links.tag_configure(link_tag)
            material_links.tag_bind(link_tag, '<Enter>', lambda e: material_links.config(cursor='hand2'))
            material_links.tag_bind(link_tag, '<Leave>', lambda e: material_links.config(cursor='arrow'))
            material_links.tag_bind(link_tag, '<Button-1>', make_lambda(link))

        material_links.config(state=tk.DISABLED)

        # Send email button
        send_email_frame = tk.Frame(self.main_dashboard)
        send_email_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.15)

        send_email_button = tk.Button(send_email_frame, text="Send to my email", command=self.send_email)
        send_email_button.pack()


    def display_personal_info(self):
        # Clear the main dashboard
        if self.main_dashboard:
            self.main_dashboard.destroy()

        # Create a new main dashboard
        self.main_dashboard = tk.Frame(self)
        self.main_dashboard.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)

        # Fetch personal information from the database
        self.mycursor.execute(f"SELECT major, gpa FROM studentList WHERE uid={self.uid}")
        personal_info = self.mycursor.fetchone()
        major, gpa = personal_info

        # Display personal information title
        personal_info_label = tk.Label(self.main_dashboard, text="Personal Information")
        personal_info_label.pack(pady=20)

        # Display student's name, major, and GPA

        name_label = tk.Label(self.main_dashboard, text=f"Name: {self.student_name}")
        name_label.pack(pady=5)

        uid_label = tk.Label(self.main_dashboard, text=f"UID: {self.uid}")
        uid_label.pack(pady=5)

        major_label = tk.Label(self.main_dashboard, text=f"Major: {major}, GPA: {gpa}")
        major_label.pack(pady=5)

        email_label = tk.Label(self.main_dashboard, text=f"Email: {self.user_email}")
        email_label.pack(pady=5)

        # Add some extra padding before the login record section
        separator = tk.Frame(self.main_dashboard, height=50)
        separator.pack()

        # Display login record title
        login_record_label = tk.Label(self.main_dashboard, text="Login Record")
        login_record_label.pack(pady=10)

        # Fetch login records from the database
        self.mycursor.execute(f"SELECT login_time, logout_time, duration FROM login_records WHERE uid={self.uid}")
        login_records = self.mycursor.fetchall()

        # Create table
        table = ttk.Treeview(self.main_dashboard, columns=(1, 2, 3), show='headings')
        table.pack(pady=20)

        # Set column headings
        table.heading(1, text='Login Time')
        table.heading(2, text='Logout Time')
        table.heading(3, text='Duration(min)')

        # Insert data into table
        for login_time, logout_time, duration in login_records:
            table.insert('', 'end', values=(login_time, logout_time, duration))



    def send_email(self):
        # Set up the email
        from_email = "hzyalex217@gmail.com"
        to_email = self.user_email
        subject = "Upcoming class reminder"

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Initialize the body variable
        body = ""

        # Add the information to the email body
        body += f"Upcoming Class: {self.upcoming_class_code}: {self.upcoming_class_name}\n"
        body += f"Time: {self.upcoming_class_start_time} - {self.upcoming_class_end_time}\n"
        body += f"Venue: {self.upcoming_class_address}\n"
        body += f"Zoom link: {self.upcoming_class_zoom_link}\n"
        body += f"Teacher's message: {self.upcoming_class_teacher_msg}\n\n"
        body += "Course Materials:\n"

        for index, (material_name, link) in enumerate(self.course_materials, start=1):
            body += f"{index}. {material_name}: {link}\n"

        msg.attach(MIMEText(body, "plain"))

        # Send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, "iess tole tfwh xewu")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()

        # Show a message after successfully sending the email
        messagebox.showinfo("Email Sent", "Reminder sent, check your inbox!")

    def display_schedule(self):
    # Clear the main dashboard
        if self.main_dashboard:
            self.main_dashboard.destroy()

        # Create a new main dashboard
        self.main_dashboard = tk.Frame(self)
        self.main_dashboard.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        print(self.nearest_session_time)
        # check if there is class within an hour
        nearest_class_time = str(self.nearest_session_time)[0:5]
        if (nearest_class_time[0] == '0'):
            nearest_class_hour = int(nearest_class_time[1])
            if (nearest_class_time[3] == '0'):
                nearest_class_minute = int(nearest_class_time[4])
            else:
                nearest_class_minute = int(nearest_class_time[3:5])
            nearest_class_time = nearest_class_hour + nearest_class_minute/60
        current_hour = str(self.login_time)[11:13]
        current_minute = str(self.login_time)[14:16]
        if (current_hour[0] == '0'):
            current_hour = int(current_hour[1])
            if (current_minute[0] == '0'):
                current_minute = int(current_minute[1])
            else:
                current_minute = int(current_minute)
        else:
            current_hour = int(current_hour)
        
        current_time = int(current_hour) + int(current_minute)/60
        
        if (current_time <= nearest_class_time-1 or current_time >= nearest_class_time):
            welcome_frame = tk.Frame(self.main_dashboard)
            welcome_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.1)  # Ensure this frame has a relative height set

            # Welcome message label
            welcome_msg = tk.Label(welcome_frame, text=f"Welcome, {self.student_name}!")
            welcome_msg.pack()  # Pack or grid inside the welcome_frame

            # Login time label
            login_time = tk.Label(welcome_frame, text=f"Login time: {self.login_time}")
            login_time.pack()  # Pack or grid below the welcome_msg label

        # Display schedule title
        schedule_label = tk.Label(self.main_dashboard, text="Weekly Schedule")
        schedule_label.grid(row=1, column=0, columnspan=5, pady=(100,0))

        # Fetch class sessions from the database
        self.mycursor.execute(f"SELECT course_id FROM enrolls_in WHERE uid={self.uid}")
        courses = self.mycursor.fetchall()
        self.courses = [course[0] for course in courses]

        # Fetch all class sessions for the courses
        all_class_sessions = []
        for course in self.courses:
            self.mycursor.execute(f"SELECT date, start_time, end_time, course_code FROM class_session INNER JOIN course ON class_session.course_id=course.course_id WHERE class_session.course_id={course}")
            sessions = self.mycursor.fetchall()
            for session in sessions:
                all_class_sessions.append((session[0], session[1], session[2], session[3]))

        days = ["MON", "TUE", "WED", "THU", "FRI"]
        times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

        # Create a themed frame for the table
        table_frame = ttk.Frame(self.main_dashboard, padding="10")
        table_frame.grid(row=2, column=0, columnspan=len(days)+1, rowspan=len(times)+1, sticky="nsew")

        # Create the headers for the table
        for i, day in enumerate(days):
            header_label = tk.Label(table_frame, text=day, relief="ridge", padx=10, pady=5)
            header_label.grid(row=0, column=i+1, sticky="nsew")

        for i, time in enumerate(times):
            header_label = tk.Label(table_frame, text=time, relief="ridge", padx=10, pady=5)
            header_label.grid(row=i+1, column=0, sticky="nsew")

        # Fill the table with class sessions
        for session in all_class_sessions:
            day, start_time, end_time, course_code = session
            day_index = days.index(day)
            start_hour = start_time.seconds // 3600
            end_hour = end_time.seconds // 3600
            duration = end_hour - start_hour

            time_index = times.index(f"{start_hour:02d}:00")
            cell_label = tk.Label(table_frame, text=course_code, relief="ridge", padx=10, pady=5, bg="#6FAE61")
            cell_label.grid(row=time_index+1, column=day_index+1, rowspan=duration, sticky="nsew")

        # Configure weights for the table cells
        for i in range(len(days) + 1):
            table_frame.columnconfigure(i, weight=1)
        for i in range(len(times) + 1):
            table_frame.rowconfigure(i, weight=1)
        

    
    def logout(self):
        # Get the current timestamp for logout time
        logout_time = datetime.datetime.now()

        # Calculate the duration
        duration = logout_time - self.login_time

        # Convert duration to total minutes and seconds
        total_seconds = duration.total_seconds()
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        duration_formatted = f"{minutes:02d}:{seconds:02d}"

        # Insert the logout record into the login_records table with duration
        total_minutes = total_seconds / 60
        self.mycursor.execute(f"INSERT INTO login_records (uid, login_time, logout_time, duration) VALUES ({self.uid}, '{self.login_time}', '{logout_time}', {total_minutes})")
        self.mydb.commit()

        # Close the database connection
        self.mydb.close()

        # Quit the application
        self.quit()