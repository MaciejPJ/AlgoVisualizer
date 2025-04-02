# Sorting Algorithms Visualizer

This project provides a visualization of various sorting algorithms using a graphical user interface built with PyQt5. The application displays the step-by-step process of selected sorting algorithms and highlights the elements being processed with different colors.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Customization and Extension](#customization-and-extension)

## Features

- **Real-Time Visualization:** Watch sorting algorithms in action with live animations.
- **Multiple Algorithms Supported:** Visualizes BubbleSort, QuickSort, SelectionSort, and InsertionSort. (More algorithms can be easily added.)
- **Interactive Controls:** Start, Pause, and Reset buttons allow you to control the animation.
- **Adjustable Animation Speed:** Use the slider to modify the speed of the animation.
- **Responsive Design:** Automatically adjusts the visualization based on the window size.

## Requirements

- Python 3.x
- [PyQt5](https://pypi.org/project/PyQt5/)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MaciejPJ/AlgoVisualizer
2. **Create and activate a virtual environment - optional but recommended**
3. **Install the required libraries (requirements.txt)**
   ```bash
   pip install -r requirements.txt

## Usage

Run the application using the following command:
```bash
python main.py
```
Once launched, the application window will allow you to select a sorting algorithm, adjust the animation speed, and observe the sorting process in real time.

## Project structure

- **requirements.txt** – Contains a list of required packages (e.g., PyQt5).
- **src/main.py** – The main entry point of the application.
- **src/main_window.py** - The file responsible for window app behaviour and layout.
- **src/sorting.py** – Implements various sorting algorithms (BubbleSort, QuickSort, etc.).
- **src/styles.qss** – Defines the styling for the application’s GUI.

## Customization and Extension

- **Adding New Algorithms:**
To add a new sorting algorithm, implement its function in **sorting.py** and include its name in the **QComboBox** list in **mainwindow.py**.
- **Modifying the UI Styles:**
Edit the **styles.qss** file to customize the appearance of the application.
- **Animation Configuration:**
You can change parameters such as the number of elements **(SAMPLES)** and the animation interval (**INTERVAL_TIME**) directly in the code to suit your needs.
- **Colours changing:**
You can change the colours in the **main_window.py** file  
