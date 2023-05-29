import tkinter as tk
from tkinter import messagebox
import mysql.connector as m
from PIL import ImageTk, Image

# Connect to MySQL server
mydb = m.connect(host="localhost", user="root", password="Dhobekar123#")

# Create a new database
cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS hotel")
cursor.execute("USE hotel")

# Create a new table to store guest information
cursor.execute("CREATE TABLE IF NOT EXISTS guest1 ("
               "ID INT AUTO_INCREMENT PRIMARY KEY,"
               "Name VARCHAR(100) NOT NULL,"
               "Address VARCHAR(100),"
               "Phone VARCHAR(20),"
               "Checkin DATE,"
               "Checkout DATE)")

# Function to add a new guest
def add_guest():
    def save_guest():
        name = name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        checkin = checkin_entry.get()
        checkout = checkout_entry.get()

        if name and address and phone and checkin and checkout:
            query = "INSERT INTO guest1 (Name, Address, Phone, Checkin, Checkout) VALUES (%s, %s, %s, %s, %s)"
            values = (name, address, phone, checkin, checkout)
            cursor.execute(query, values)
            mydb.commit()
            messagebox.showinfo("Success", "Guest added successfully.")
            guest_window.destroy()
        else:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields.")

    guest_window = tk.Toplevel(window)
    guest_window.title("Add New Guest")

    name_label = tk.Label(guest_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(guest_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    address_label = tk.Label(guest_window, text="Address:")
    address_label.grid(row=1, column=0, padx=10, pady=5)
    address_entry = tk.Entry(guest_window)
    address_entry.grid(row=1, column=1, padx=10, pady=5)

    phone_label = tk.Label(guest_window, text="Phone:")
    phone_label.grid(row=2, column=0, padx=10, pady=5)
    phone_entry = tk.Entry(guest_window)
    phone_entry.grid(row=2, column=1, padx=10, pady=5)

    checkin_label = tk.Label(guest_window, text="Check-in Date:")
    checkin_label.grid(row=3, column=0, padx=10, pady=5)
    checkin_entry = tk.Entry(guest_window)
    checkin_entry.grid(row=3, column=1, padx=10, pady=5)

    checkout_label = tk.Label(guest_window, text="Check-out Date:")
    checkout_label.grid(row=4, column=0, padx=10, pady=5)
    checkout_entry = tk.Entry(guest_window)
    checkout_entry.grid(row=4, column=1, padx=10, pady=5)

    save_button = tk.Button(guest_window, text="Save", command=save_guest)
    save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10,)

# Function to view guest information
def view_guests():
    cursor.execute("SELECT * FROM guest1")
    result = cursor.fetchall()
    
    if result:
        guest_info = ""
        for row in result:
            guest_info += f"ID: {row[0]}\n"
            guest_info += f"Name: {row[1]}\n"
            guest_info += f"Address: {row[2]}\n"
            guest_info += f"Phone: {row[3]}\n"
            guest_info += f"Check-in Date: {row[4]}\n"
            guest_info += f"Check-out Date: {row[5]}\n\n"
        messagebox.showinfo("Guest Information", guest_info)
    else:
        messagebox.showinfo("Guest Information", "No guests found.")

# Function to check out a guest
def checkout_guest():
    def confirm_checkout():
        guest_id = guest_id_entry.get()
        if guest_id:
            cursor.execute(f"SELECT * FROM guest1 WHERE ID={guest_id}")
            guest = cursor.fetchone()

            if guest:
                checkin_date = guest[4]
                checkout_date = guest[5]
                num_nights = (checkout_date - checkin_date).days
                room_rate = 6000  # Assumed room rate of 6000 per night
                bill = num_nights * room_rate

                cursor.execute(f"DELETE FROM guest1 WHERE ID={guest_id}")
                mydb.commit()

                messagebox.showinfo("Checkout", f"Guest {guest[1]} has checked out. Their bill is {bill}.")
                checkout_window.destroy()
            else:
                messagebox.showwarning("Invalid ID", "Guest not found.")
        else:
            messagebox.showwarning("Invalid ID", "Please enter a valid guest ID.")

    checkout_window = tk.Toplevel(window)
    checkout_window.title("Check-out Guest")

    guest_id_label = tk.Label(checkout_window, text="Guest ID:")
    guest_id_label.grid(row=0, column=0, padx=10, pady=5)
    guest_id_entry = tk.Entry(checkout_window)
    guest_id_entry.grid(row=0, column=1, padx=10, pady=5)

    confirm_button = tk.Button(checkout_window, text="Confirm", command=confirm_checkout)
    confirm_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Function to exit the program
def exit_program():
    window.destroy()

# Create the main application window
window = tk.Tk()
window.title("Hotel Management System")


##############


# # Load the background image
bg_image = ImageTk.PhotoImage(Image.open("hotel1.jpg"))

#Create a label with the background image

background_label = tk.Label(window, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Increase the size of the main window
window.geometry("600x400")

# Create the menu frame
menu_frame = tk.Frame(window)
menu_frame.pack(pady=160)

input_tital=tk.Label(window,text="HOTEL MANAGEMENT SYSTEM",bg="red",font=("times",25))
input_tital.place(x=14,y=15)

# Add buttons to the menu frame
add_button = tk.Button(menu_frame, text="Add Guest", font=("arial,20"), command=add_guest, bg="green", fg="white")
add_button.grid(row=0, column=0, padx=10)

view_button = tk.Button(menu_frame, text="View Guests", font=("arial,20"), command=view_guests, bg="blue", fg="white")
view_button.grid(row=0, column=1, padx=10)

checkout_button = tk.Button(menu_frame, text="Checkout Guest", font=("arial,20"), command=checkout_guest, bg="red", fg="white")
checkout_button.grid(row=0, column=2, padx=10)

exit_button = tk.Button(menu_frame, text="Exit", font=("arial,20"), command=exit_program, bg="gray", fg="white")
exit_button.grid(row=0, column=3, padx=10)

# Run the main application window
window.mainloop()
