import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class SalesVisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Data Visualization Dashboard")
        self.df = pd.read_csv("data/train.csv")
        self.preprocess_data()
        self.create_widgets()
        
    def preprocess_data(self):
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(inplace=True)
        self.df["Order Date"] = pd.to_datetime(self.df["Order Date"], format="%d/%m/%Y")
        self.df["Ship Date"] = pd.to_datetime(self.df["Ship Date"], format="%d/%m/%Y")
        self.df["Postal Code"] = self.df["Postal Code"].fillna(50840)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Visualization buttons
        buttons = [
            ("Ship Mode Distribution", self.show_ship_mode),
            ("Segment Distribution", self.show_segment),
            ("Sales by State", self.show_state_sales),
            ("Sub-Category Distribution", self.show_subcategory),
            ("Category Sales", self.show_category_sales)
        ]

        for i, (text, cmd) in enumerate(buttons):
            ttk.Button(main_frame, text=text, command=cmd).grid(
                row=i, column=0, padx=10, pady=5, sticky="nsew"
            )

    def create_plot_window(self, title):
        window = tk.Toplevel(self.root)
        window.title(title)
        return window

    def show_ship_mode(self):
        window = self.create_plot_window("Ship Mode Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='Ship Mode', data=self.df, ax=ax, palette='coolwarm')
        ax.set_title("Ship Mode Distribution")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_segment(self):
        window = self.create_plot_window("Segment Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.countplot(x='Segment', data=self.df, ax=ax, palette='Set2')
        ax.set_title('Segment Distribution')
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_state_sales(self):
        window = self.create_plot_window("Sales by State")
        fig, ax = plt.subplots(figsize=(10, 6))
        self.df.groupby("State")["Sales"].sum().sort_values().plot.bar(ax=ax)
        ax.set_title("Sales by State")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_subcategory(self):
        window = self.create_plot_window("Sub-Category Distribution")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.countplot(x='Sub-Category', data=self.df, ax=ax, palette='Paired')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_title("Sub-Category Distribution")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def show_category_sales(self):
        window = self.create_plot_window("Category Sales")
        fig, ax = plt.subplots(figsize=(8, 8))
        self.df.groupby("Category")["Sales"].sum().plot.pie(
            autopct='%1.1f%%', ax=ax, startangle=90
        )
        ax.set_title("Sales by Category")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesVisualizationApp(root)
    root.mainloop()