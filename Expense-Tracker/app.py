import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime, timedelta

class ExpenseTrackerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # Custom colors and fonts
        heading_bg = '#2e86c1'  # Light blue
        heading_fg = '#ffffff'  # White
        cell_bg = '#f0f3f4'     # Light grey
        cell_fg = '#000000'     # Black
        font_bold = ('Arial', 12, 'bold')
        
        # Title Label
        title_label = tk.Label(self.root, text="EXPENSE TRACKER", font=('Arial', 20, 'bold'), bg=heading_bg, fg=heading_fg)
        title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)
        
        self.expenses = defaultdict(list)  # Dictionary to store expenses
        
        # Frame for adding expenses
        add_frame = ttk.LabelFrame(self.root, text="Add Expense", padding=(10, 10))
        add_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W+tk.E)
        
        ttk.Label(add_frame, text="Category:", font=font_bold).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.category_entry = ttk.Entry(add_frame, width=20)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Amount (₹):", font=font_bold).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(add_frame, width=20)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Date (dd-mm-yy):", font=font_bold).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.date_entry = ttk.Entry(add_frame, width=20)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Payment Mode:", font=font_bold).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.payment_mode_var = tk.StringVar()
        self.payment_mode_combo = ttk.Combobox(add_frame, textvariable=self.payment_mode_var, width=17,
                                               values=["Cash", "Credit Card", "Debit Card", "Online Transfer"])
        self.payment_mode_combo.grid(row=3, column=1, padx=5, pady=5)
        self.payment_mode_combo.current(0)
        
        add_button = ttk.Button(add_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=4, columnspan=2, padx=5, pady=10)
        
        # Frame for displaying expenses
        display_frame = ttk.LabelFrame(self.root, text="Expenses", padding=(10, 10))
        display_frame.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W+tk.E)
        
        self.expenses_tree = ttk.Treeview(display_frame, columns=("Category", "Amount", "Date", "Mode"), show="headings")
        self.expenses_tree.heading("Category", text="Category", anchor=tk.CENTER)
        self.expenses_tree.heading("Amount", text="Amount (₹)", anchor=tk.CENTER)
        self.expenses_tree.heading("Date", text="Date", anchor=tk.CENTER)
        self.expenses_tree.heading("Mode", text="Mode", anchor=tk.CENTER)
        self.expenses_tree.column("Category", width=150, anchor=tk.CENTER)
        self.expenses_tree.column("Amount", width=100, anchor=tk.CENTER)
        self.expenses_tree.column("Date", width=100, anchor=tk.CENTER)
        self.expenses_tree.column("Mode", width=120, anchor=tk.CENTER)
        self.expenses_tree.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Set style for treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=font_bold, background=heading_bg, foreground=heading_fg)
        style.configure("Treeview", font=('Arial', 10), background=cell_bg, foreground=cell_fg, rowheight=25)
        
        # Frame for displaying graphs
        graph_frame = ttk.LabelFrame(self.root, text="Expense Distribution", padding=(10, 10))
        graph_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Initialize figure and canvas for monthly expenses
        self.monthly_chart = plt.Figure(figsize=(5, 4), dpi=100)
        self.monthly_canvas = FigureCanvasTkAgg(self.monthly_chart, master=graph_frame)
        self.monthly_canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Initialize figure and canvas for weekly expenses
        self.weekly_chart = plt.Figure(figsize=(5, 4), dpi=100)
        self.weekly_canvas = FigureCanvasTkAgg(self.weekly_chart, master=graph_frame)
        self.weekly_canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Initialize figure and canvas for category distribution
        self.category_chart = plt.Figure(figsize=(5, 4), dpi=100)
        self.category_canvas = FigureCanvasTkAgg(self.category_chart, master=graph_frame)
        self.category_canvas.get_tk_widget().grid(row=0, column=2, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Buttons for generating reports
        report_frame = ttk.Frame(self.root)
        report_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        monthly_report_button = ttk.Button(report_frame, text="Generate Monthly Report", command=self.generate_monthly_report)
        monthly_report_button.grid(row=0, column=0, padx=5, pady=5)
        
        weekly_report_button = ttk.Button(report_frame, text="Generate Weekly Report", command=self.generate_weekly_report)
        weekly_report_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.update_display()
        
    def add_expense(self):
        category = self.category_entry.get()
        amount_str = self.amount_entry.get()
        date_str = self.date_entry.get()
        payment_mode = self.payment_mode_var.get()
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than zero.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a number.")
            return
        
        try:
            expense_date = datetime.strptime(date_str, "%d-%m-%y").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use dd-mm-yy.")
            return
        
        if category.strip() == "":
            messagebox.showerror("Error", "Category cannot be empty.")
            return
        
        self.expenses[expense_date].append((category, amount, payment_mode))
        self.update_display()
        self.clear_entries()
        
    def update_display(self):
        # Clear previous plots
        self.monthly_chart.clf()
        self.weekly_chart.clf()
        self.category_chart.clf()
        
        # Clear current treeview
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)
        
        # Populate treeview with updated expenses
        for date, expenses_list in sorted(self.expenses.items()):
            for category, amount, mode in expenses_list:
                self.expenses_tree.insert("", tk.END, values=(category, f"₹ {amount:.2f}", date.strftime("%d-%m-%y"), mode))
        
        # Update monthly chart (histogram)
        monthly_expenses = defaultdict(float)
        current_date = datetime.now().date()
        start_of_month = current_date.replace(day=1)
        
        for date, expenses_list in self.expenses.items():
            if start_of_month <= date <= current_date:
                for _, amount, _ in expenses_list:
                    monthly_expenses[date.strftime("%d-%m-%y")] += amount
        
        if monthly_expenses:
            dates = list(monthly_expenses.keys())
            amounts = list(monthly_expenses.values())
            self.monthly_chart.add_subplot(111).bar(dates, amounts, color='#1f77b4', edgecolor='black')
            self.monthly_chart.suptitle('Monthly Expenses', fontsize=14)
            self.monthly_chart.autofmt_xdate(rotation=45)
        
        self.monthly_canvas.draw()
        
        # Update weekly chart (histogram)
        weekly_expenses = defaultdict(float)
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        for date, expenses_list in self.expenses.items():
            if start_of_week <= date <= end_of_week:
                for _, amount, _ in expenses_list:
                    weekly_expenses[date.strftime("%d-%m-%y")] += amount
        
        if weekly_expenses:
            dates = list(weekly_expenses.keys())
            amounts = list(weekly_expenses.values())
            self.weekly_chart.add_subplot(111).bar(dates, amounts, color='#ff7f0e', edgecolor='black')
            self.weekly_chart.suptitle('Weekly Expenses', fontsize=14)
            self.weekly_chart.autofmt_xdate(rotation=45)
        
        self.weekly_canvas.draw()
        
        # Update category pie chart
        category_expenses = defaultdict(float)
        
        for _, expenses_list in self.expenses.items():
            for category, amount, _ in expenses_list:
                category_expenses[category] += amount
        
        if category_expenses:
            categories = list(category_expenses.keys())
            amounts = list(category_expenses.values())
            self.category_chart.add_subplot(111).pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
            self.category_chart.suptitle('Expense Distribution by Category', fontsize=14)
        
        self.category_canvas.draw()
        
    def clear_entries(self):
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.payment_mode_combo.current(0)
        
    def generate_monthly_report(self):
        current_date = datetime.now().date()
        start_of_month = current_date.replace(day=1)
        monthly_expenses = defaultdict(float)
        
        for date, expenses_list in self.expenses.items():
            if start_of_month <= date <= current_date:
                for _, amount, _ in expenses_list:
                    monthly_expenses[date.strftime("%d-%m-%y")] += amount
        
        if not monthly_expenses:
            messagebox.showinfo("Monthly Report", "No expenses recorded this month.")
            return
        
        dates = list(monthly_expenses.keys())
        amounts = list(monthly_expenses.values())
        
        plt.figure(figsize=(6, 4), dpi=100)
        plt.bar(dates, amounts, color='#1f77b4', edgecolor='black')
        plt.xlabel('Date')
        plt.ylabel('Amount (₹)')
        plt.title('Monthly Expenses')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    def generate_weekly_report(self):
        current_date = datetime.now().date()
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        weekly_expenses = defaultdict(float)
        
        for date, expenses_list in self.expenses.items():
            if start_of_week <= date <= end_of_week:
                for _, amount, _ in expenses_list:
                    weekly_expenses[date.strftime("%d-%m-%y")] += amount
        
        if not weekly_expenses:
            messagebox.showinfo("Weekly Report", "No expenses recorded this week.")
            return
        
        dates = list(weekly_expenses.keys())
        amounts = list(weekly_expenses.values())
        
        plt.figure(figsize=(6, 4), dpi=100)
        plt.bar(dates, amounts, color='#ff7f0e', edgecolor='black')
        plt.xlabel('Date')
        plt.ylabel('Amount (₹)')
        plt.title('Weekly Expenses')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if _name_ == "_main_":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()