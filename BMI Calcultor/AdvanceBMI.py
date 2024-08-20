import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import sqlite3
import datetime

conn1 = sqlite3.connect('bmi_data.db')
c = conn1.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_data 
             (id INTEGER PRIMARY KEY, date TEXT, name TEXT, weight REAL, height REAL, bmi REAL, category TEXT)''')

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = weight / (height ** 2)
        category = categorize_bmi(bmi)
        bmi_label.config(text=f"BMI: {bmi:.2f} ({category})")
   
        save_data(name_entry.get(), weight, height, bmi, category)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight and height.")

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(name, weight, height, bmi, category):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_data (date, name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?, ?)",
              (date, name, weight, height, bmi, category))
    conn1.commit()

def visualize_data():
    c.execute("SELECT date, bmi FROM bmi_data WHERE name = ?", (name_entry.get(),))
    data = c.fetchall()
    
    if data:
        dates = [datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in data]
        bmis = [row[1] for row in data]
        plt.plot(dates, bmis, marker='o')
        plt.title("BMI Trends Over Time")
        plt.xlabel("Date")
        plt.ylabel("BMI")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No historical data found for this user.")

root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Weight (kg)").grid(row=1, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Height (m)").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

bmi_label = tk.Label(root, text="BMI: ")
bmi_label.grid(row=3, column=0, columnspan=2)

tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="View Trends", command=visualize_data).grid(row=5, column=0, columnspan=2)

root.mainloop()

conn1.close()
