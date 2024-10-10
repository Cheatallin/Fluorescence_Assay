import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import tkinter as tk
from tkinter import filedialog
import os

def process_file(file_path):
    # Load the data from CSV
    data = pd.read_csv(file_path)
    
    # Extract the base name of the file (without directory and extension)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Determine x data based on available columns
    if 'Time_Sec' in data.columns:
        x = data['Time_Sec']
        x_label = 'Time (Seconds)'
    elif 'Wavelength' in data.columns:
        x = data['Wavelength']
        x_label = 'Wavelength (nm)'
    else:
        raise ValueError("CSV file must contain either 'Time_Sec' or 'Wavelength' column.")
    
    # Extract y (Abs) data
    y = data['Fluorescence']

    # Generate smooth trend using spline interpolation
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spl = make_interp_spline(x, y, k=3)  # k=3 for cubic spline
    y_smooth = spl(x_smooth)
    
    # Create the plot with softer colors
    plt.figure(figsize=(12, 8))

    # Plot original data with a soft blue color
    plt.plot(x, y, 'o-', label='Original Data', color='#8cb4d2', markersize=8, linewidth=2)

    # Plot smooth trend line with a soft coral color
    plt.plot(x_smooth, y_smooth, label='Smooth Trend', color='#f3a683', linestyle='--', linewidth=3)

    # Add titles and labels
    plt.title(f'{base_name}', fontsize=16)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel('Fluorescence (unit)', fontsize=14)
    plt.grid(True, color='#e6e6e6', linestyle='--', linewidth=0.5)
    plt.legend(fontsize=12)

    # Customize the plot appearance
    plt.rcParams['axes.facecolor'] = '#f8f8f8'
    plt.rcParams['figure.facecolor'] = 'white'

    # Define the directory to save the graph
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    save_dir = os.path.join(script_dir, "Graph")  # Define the constant path
    os.makedirs(save_dir, exist_ok=True)  # Ensure the directory exists

    # Save the figure as a PNG file in the specified directory
    save_path = os.path.join(save_dir, f'{base_name}.png')
    plt.savefig(save_path)

    # Show the plot
    plt.show()

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        process_file(file_path)

# Create the main window
root = tk.Tk()
root.title("CSV to Graph")

# Create a button to open the file dialog
button = tk.Button(root, text="Open CSV File", command=open_file_dialog)
button.pack(pady=20)

# Run the application
root.mainloop()