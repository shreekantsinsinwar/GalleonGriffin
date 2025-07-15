import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

DATA_FILE = "vault_data.json"

class GalleonGriffin:
    def __init__(self, root):
        self.root = root
        self.root.title("GalleonGriffin - Wizarding Expense Tracker")
        self.root.geometry("700x500")
        self.root.configure(bg="#7f0909")  # Gryffindor red

        self.expenses = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        title = tk.Label(self.root, text="GalleonGriffin - Expense Ledger", font=("Georgia", 20, "bold"), fg="gold", bg="#7f0909")
        title.pack(pady=10)

        form = tk.Frame(self.root, bg="#7f0909")
        form.pack(pady=5)

        tk.Label(form, text="Item:", bg="#7f0909", fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.item_entry = tk.Entry(form)
        self.item_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Amount (⚡ Galleons):", bg="#7f0909", fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Category:", bg="#7f0909", fg="white").grid(row=2, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(form)
        self.category_entry.grid(row=2, column=1, padx=5)

        add_btn = tk.Button(self.root, text="Add to Gringotts", command=self.add_expense, bg="gold", fg="black", width=20)
        add_btn.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Item", "Amount", "Category", "Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        action_frame = tk.Frame(self.root, bg="#7f0909")
        action_frame.pack(pady=5)

        chart_btn = tk.Button(action_frame, text="Reveal the Vaults", command=self.show_chart, bg="gold", width=20)
        chart_btn.grid(row=0, column=0, padx=10)

        delete_btn = tk.Button(action_frame, text="Obliviate Entry", command=self.delete_selected, bg="black", fg="white", width=20)
        delete_btn.grid(row=0, column=1, padx=10)

    def add_expense(self):
        item = self.item_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        if not item or not amount or not category:
            messagebox.showwarning("Incomplete", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid", "Amount must be a number!")
            return

        entry = (item, amount, category, date)
        self.expenses.append(entry)
        self.tree.insert("", tk.END, values=entry)
        self.save_data()

        self.item_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an entry to Obliviate!")
            return

        for sel in selected:
            values = self.tree.item(sel, "values")
            self.tree.delete(sel)
            self.expenses = [exp for exp in self.expenses if exp != tuple(values)]

        self.save_data()

    def show_chart(self):
        if not self.expenses:
            messagebox.showinfo("Empty Vault", "No expenses to reveal yet!")
            return

        categories = {}
        for _, amount, category, _ in self.expenses:
            categories[category] = categories.get(category, 0) + float(amount)

        labels = list(categories.keys())
        sizes = list(categories.values())

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=plt.cm.tab20.colors)
        plt.title("🪙 Vault Distribution - Category Wise")
        plt.show()

    def save_data(self):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.expenses, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save vault: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.expenses = json.load(f)
                for entry in self.expenses:
                    self.tree.insert("", tk.END, values=entry)
            except Exception as e:
                messagebox.showwarning("Warning", f"Could not load vault data: {e}")

# ---------------- Launch ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GalleonGriffin(root)
    root.mainloop()
