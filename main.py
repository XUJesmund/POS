def launch_pos():
    print('POS System is running...')

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QScrollArea, QFrame,
    QLineEdit, QMessageBox, QGroupBox, QComboBox, QListWidget, QGridLayout, QDialog, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from datetime import datetime


class Product:
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def __hash__(self):
        return hash((self.name, self.price, self.category))

    def __eq__(self, other):
        return (isinstance(other, Product) and
                self.name == other.name and
                self.price == other.price and
                self.category == other.category)


class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add_item(self, product, quantity=1):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            product = list(self.items.keys())[index]
            self.items[product] -= 1
            if self.items[product] <= 0:
                del self.items[product]

    def delete_item(self, index):
        if 0 <= index < len(self.items):
            product = list(self.items.keys())[index]
            del self.items[product]

    def update_item_quantity(self, index, new_quantity):
        if 0 <= index < len(self.items):
            product = list(self.items.keys())[index]
            if new_quantity <= 0:
                del self.items[product]
            else:
                self.items[product] = new_quantity

    def total_price(self):
        return sum(product.price * qty for product, qty in self.items.items())

    def clear_cart(self):
        self.items.clear()


class ProductCard(QFrame):
    def __init__(self, product, parent=None):
        super().__init__()
        self.product = product
        self.parent = parent
        self.setFixedSize(150, 150)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #007359;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label = QLabel()
        image_label.setFixedSize(80, 80)
        image_label.setStyleSheet("border-radius: 10px; border: 1px solid #007359;")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_filename = f"images/{self.product.name.lower().replace(' ', '_')}.png"
        pixmap = QPixmap(self.image_filename)

        if not pixmap.isNull():
            image_label.setPixmap(pixmap.scaled(image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            print(f"Image not found: {self.image_filename}")
            image_label.setText("No Image")

        label = QLabel(f"{product.name}\n₱{product.price:.2f}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: black; font-weight: bold;")

        layout.addWidget(image_label)
        layout.addWidget(label)
        self.setLayout(layout)
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        try:
            self.parent.select_product(self.product)
        except Exception as e:
            print("Error selecting product:", e)
        event.accept()


class POSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System - 7/11 Style")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #007350;
                color: black;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #007359;
                margin-top: 10px;
                color: #007359;
            }
            QGroupBox::title {
                subline-control-position: top center;
                padding: 5px;
                color: #C90000;
                background-color: #007359;
            }
        """)

        self.category_combo = QComboBox()
        self.cart_list = QListWidget()
        self.total_label = QLabel("Total: ₱0.00")
        self.quantity_input = QLineEdit()
        self.qty_update_input = QLineEdit()
        self.inventory = self.create_sample_inventory()
        self.cart = ShoppingCart()
        self.selected_product = None
        self.receipt_history = []
        self.receipt_history_window = None

        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)

        self.init_ui()

    def create_sample_inventory(self):
        return [
            Product("Coca-Cola", 25.00, "Drinks"),
            Product("Pepsi", 22.00, "Drinks"),
            Product("Sprite", 25.00, "Drinks"),
            Product("Iced Tea", 20.50, "Drinks"),
            Product("Orange Juice", 20.50, "Drinks"),
            Product("Water Bottle", 15.00, "Drinks"),
            Product("Toothbrush", 30.00, "Personal Care"),
            Product("Toothpaste", 45.00, "Personal Care"),
            Product("Shampoo", 109.50, "Personal Care"),
            Product("Soap", 29.00, "Personal Care"),
            Product("Deodorant", 129.50, "Personal Care"),
            Product("Razor", 49.00, "Personal Care"),
            Product("Eggs", 60.00, "Groceries"),
            Product("Bread", 68.00, "Groceries"),
            Product("Milk", 89.00, "Groceries"),
            Product("Cheese", 104.25, "Groceries"),
            Product("Tomato", 45.00, "Groceries"),
            Product("Potato", 55.00, "Groceries"),
            Product("Chips", 64.30, "Snacks & Candies"),
            Product("Chocolate Bar", 75.00, "Snacks & Candies"),
            Product("Gummy Bears", 40.00, "Snacks & Candies"),
            Product("Popcorn", 80.50, "Snacks & Candies"),
            Product("Crackers", 15.00, "Snacks & Candies"),
            Product("Nuts", 30.00, "Snacks & Candies"),
            Product("Facial Cleanser", 126.50, "Skincare"),
            Product("Moisturizer", 150.00, "Skincare"),
            Product("Sunscreen", 189.30, "Skincare"),
            Product("Toner", 199.50, "Skincare"),
            Product("Serum", 210.00, "Skincare"),
            Product("Face Mask", 174.90, "Skincare"),
        ]

    def init_ui(self):
        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        top_bar = QHBoxLayout()

        view_history_btn = QPushButton("📜 View Receipt History")
        view_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #007359;
                color: white;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #002419;
            }
        """)
        view_history_btn.clicked.connect(self.open_receipt_history_window)
        top_bar.addWidget(view_history_btn)
        top_bar.addStretch()
        left_panel.addLayout(top_bar)

        self.category_combo.addItems([
            "All",
            "Drinks",
            "Personal Care",
            "Groceries",
            "Snacks & Candies",
            "Skincare"
        ])
        self.category_combo.setItemText(0, "Browse All Categories")
        self.category_combo.currentIndexChanged.connect(self.update_product_grid)
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #014f37;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)

        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
        """)

        left_panel.addWidget(QLabel("Select Category:"))
        left_panel.addWidget(self.category_combo)
        left_panel.addWidget(QLabel("Products:"))
        left_panel.addWidget(self.scroll_area)

        self.quantity_input.setPlaceholderText("Enter quantity")
        self.quantity_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #002419;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        add_button = QPushButton("Add to Cart")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #014f37;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #002419;
            }
        """)
        add_button.clicked.connect(self.add_to_cart_with_quantity)

        left_panel.addWidget(QLabel("Quantity:"))
        left_panel.addWidget(self.quantity_input)
        left_panel.addWidget(add_button)

        cart_group = QGroupBox()  # Removed title "Shopping Cart"
        cart_group.setStyleSheet("background-color: #014f37; border: 2px solid #007359; border-radius: 8px;")
        cart_layout = QVBoxLayout()

        self.cart_list.itemDoubleClicked.connect(self.remove_from_cart)
        self.cart_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: black;
                border: 1px solid #002419;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Changed label text color to white
        self.items_label = QLabel("Shopping Cart:")
        self.items_label.setStyleSheet("color: white; font-weight: bold;")
        cart_layout.addWidget(self.items_label)
        cart_layout.addWidget(self.cart_list)

        self.qty_update_input.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #014f37;
                border-radius: 5px;
                font-size: 14px;
            }
        """)

        # Changed label text color to white
        self.edit_qty_label = QLabel("Edit Quantity:")
        self.edit_qty_label.setStyleSheet("color: white; font-weight: bold;")
        cart_layout.addWidget(self.edit_qty_label)
        cart_layout.addWidget(self.qty_update_input)

        btn_layout = QHBoxLayout()
        delete_btn = QPushButton("Delete Item")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #014f37;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: ##002419;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_item)

        update_btn = QPushButton("Update Quantity")
        update_btn.setStyleSheet("""
            QPushButton {
                background-color: #014f37;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #002419;
            }
        """)
        update_btn.clicked.connect(self.update_selected_item_quantity)

        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(update_btn)
        cart_layout.addLayout(btn_layout)

        total_checkout_layout = QHBoxLayout()
        self.total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        checkout_btn = QPushButton("Checkout")
        checkout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #014f37;
                border: 2px solid #014f37;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #002419;
            }
        """)
        checkout_btn.clicked.connect(self.checkout)
        total_checkout_layout.addWidget(self.total_label, stretch=1)
        total_checkout_layout.addWidget(checkout_btn)
        cart_layout.addLayout(total_checkout_layout)

        cart_group.setLayout(cart_layout)
        main_layout.addLayout(left_panel, 4)
        main_layout.addWidget(cart_group, 3)

        self.setLayout(main_layout)
        self.update_product_grid()

    def select_product(self, product):
        self.selected_product = product
        self.quantity_input.setFocus()

    def update_product_grid(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        selected_category = self.category_combo.currentText().replace("Browse All Categories", "All")
        filtered_products = self.inventory
        if selected_category != "All":
            filtered_products = [p for p in self.inventory if p.category == selected_category]

        row = 0
        col = 0
        for product in filtered_products:
            card = ProductCard(product, parent=self)
            self.grid_layout.addWidget(card, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        self.scroll_content.adjustSize()

    def add_to_cart_with_quantity(self):
        if not hasattr(self, 'selected_product') or self.selected_product is None:
            QMessageBox.warning(self, "No Product Selected", "Please click a product card first.")
            return
        quantity_text = self.quantity_input.text()
        if not quantity_text.isdigit() or int(quantity_text) <= 0:
            QMessageBox.warning(self, "Invalid Quantity", "Please enter a valid positive number.")
            return
        quantity = int(quantity_text)
        self.cart.add_item(self.selected_product, quantity)
        self.update_cart_display()
        self.quantity_input.clear()
        self.selected_product = None

    def remove_from_cart(self, item):
        row = self.cart_list.row(item)
        self.cart.remove_item(row)
        self.update_cart_display()

    def delete_selected_item(self):
        selected = self.cart_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item to delete.")
            return
        self.cart.delete_item(selected)
        self.update_cart_display()

    def update_selected_item_quantity(self):
        selected = self.cart_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item to update.")
            return
        qty_text = self.qty_update_input.text()
        if not qty_text.isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid quantity.")
            return
        new_qty = int(qty_text)
        self.cart.update_item_quantity(selected, new_qty)
        self.update_cart_display()
        self.qty_update_input.clear()

    def update_cart_display(self):
        self.cart_list.clear()
        for product, qty in self.cart.items.items():
            total_price = product.price * qty
            self.cart_list.addItem(f"{product.name} x{qty} - ₱{total_price:.2f}")
        self.total_label.setText(f"Total: ₱{self.cart.total_price():.2f}")

    def checkout(self):
        if not self.cart.items:
            QMessageBox.warning(self, "Empty Cart", "Your cart is empty!")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt = f"Receipt Time: {now}\n"
        receipt += "=" * 30 + "\n"
        receipt += "{:<15} {:<5}  {}\n".format("Item", "Qty", "Total")
        receipt += "-" * 30 + "\n"

        for product, qty in self.cart.items.items():
            total_price = product.price * qty
            receipt += "{:<15} x{:<4} ₱{:.2f}\n".format(product.name[:15], qty, total_price)

        receipt += "-" * 30 + "\n"
        receipt += "Grand Total:     ₱{:.2f}\n".format(self.cart.total_price())
        receipt += "=" * 30 + "\n"
        receipt += "Thank you for shopping!\nCome again soon!"

        dialog = QDialog(self)
        dialog.setWindowTitle("Receipt")
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(receipt)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        dialog.resize(500, 400)
        dialog.exec()

        self.receipt_history.append(receipt)
        try:
            with open("receipt_history.txt", "a", encoding="utf-8") as file:
                file.write(receipt + "\n\n" + "=" * 40 + "\n\n")
        except Exception as e:
            QMessageBox.critical(self, "File Error", f"Failed to save receipt:\n{e}")

        self.cart.clear_cart()
        self.update_cart_display()

    def open_receipt_history_window(self):
        if not self.receipt_history:
            QMessageBox.information(self, "No Receipts", "No receipts have been generated yet.")
            return
        if self.receipt_history_window is None:
            self.receipt_history_window = ReceiptHistoryWindow(self.receipt_history)
        else:
            self.receipt_history_window.update_receipts(self.receipt_history)

        self.receipt_history_window.show()
        self.receipt_history_window.raise_()
        self.receipt_history_window.activateWindow()


class ReceiptHistoryWindow(QWidget):
    def __init__(self, receipts):
        super().__init__()
        self.setWindowTitle("Receipt History")
        self.setGeometry(100, 100, 600, 400)
        self.receipts = receipts
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.receipt_list = QListWidget()
        self.receipt_list.itemDoubleClicked.connect(self.show_receipt_details)
        layout.addWidget(QLabel("Saved Receipts:"))
        layout.addWidget(self.receipt_list)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        self.setLayout(layout)
        self.populate_list()

    def populate_list(self):
        self.receipt_list.clear()
        if not self.receipts:
            self.receipt_list.addItem("No receipts yet.")
        else:
            for i, receipt in enumerate(self.receipts):
                lines = receipt.split("\n")[:9]
                display_text = "\n".join(lines)
                self.receipt_list.addItem(display_text)

    def update_receipts(self, receipts):
        self.receipts = receipts
        self.populate_list()

    def show_receipt_details(self, item):
        index = self.receipt_list.row(item)
        selected_receipt = self.receipts[index]
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Receipt #{index + 1}")
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(selected_receipt)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        dialog.resize(500, 400)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSApp()
    window.show()
    sys.exit(app.exec())
