import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from PIL import Image, ImageTk
import json
import os
from datetime import datetime

DATA_FILE = "mandoubeen_data.json"

class Mandoub:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.orders = []

    def add_order(self, value, location, date):
        self.orders.append({"value": value, "location": location, "date": date})

    def total_orders_value(self):
        return sum(order["value"] for order in self.orders)

    def total_orders_count(self):
        return len(self.orders)

class DataManager:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                # Convert old format to new format if needed
                converted_data = {}
                for name, value in data.items():
                    if isinstance(value, list) and len(value) >= 2:
                        converted_data[name] = [value[0], value[1]]
                    else:
                        converted_data[name] = ["", []]
                return converted_data
        return {}

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

class MandoubApp:
    def __init__(self, root):
        self.root = root
        self.data_manager = DataManager(DATA_FILE)
        self.mandoubeen = self.data_manager.data
        self.setup_ui()
        self.setup_background()

    def setup_background(self):
        try:
            # تحقق من وجود الملف أولاً
            image_path = "C:\\Users\\ahmed\\Downloads\\WhatsApp_Image_2025-03-20_at_7.47.21_PM__1_-removebg-preview.png"
            if not os.path.exists(image_path):
                raise FileNotFoundError("لم يتم العثور على الصورة في المسار المحدد")
            
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((400, 400), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            
            self.bg_label = tk.Label(self.root, image=self.bg_photo, bg="white")
            self.bg_label.place(relx=0.5, rely=0.6, anchor="center")
        except Exception as e:
            print(f"خطأ في تحميل صورة الخلفية: {e}")
            error_label = tk.Label(self.root, text="صورة الخلفية غير متوفرة", 
                                font=("Arial", 12), bg="white", fg="red")
            error_label.place(relx=0.5, rely=0.6, anchor="center")

    def setup_ui(self):
        self.root.title("واجهة المندوبين")
        self.root.geometry("1500x700")
        self.root.configure(bg="white")

        # إطار لعناصر التحكم العلوية
        top_frame = tk.Frame(self.root, bg="white")
        top_frame.pack(side="top", fill="x", padx=20, pady=20)

        # إضافة عنوان أو شعار إذا لزم الأمر
        title_label = tk.Label(top_frame, text="", 
                             font=("Arial", 18, "bold"), bg="white", fg="black")
        title_label.pack(side="top", pady=10)

        # إطار جديد للأزرار السفلية
        bottom_frame = tk.Frame(self.root, bg="white")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)

        # زر الرجاله في الأسفل
        men_button = tk.Button(bottom_frame, text="مناديب", font=("Arial", 14, "bold"), 
                             bg="lightgray", fg="black", width=20, height=2,
                             command=lambda: self.open_new_window("مناديب"))
        men_button.pack(side="bottom", pady=10)

    def open_new_window(self, title):
        new_window = tk.Toplevel(self.root)
        new_window.title(title)
        new_window.geometry("1500x700")
        new_window.configure(bg="white")
        new_window.grab_set()
        new_window.resizable(True, True)

        title_label = tk.Label(new_window, text=title, font=("Arial", 18, "bold"), 
                             bg="white", fg="black")
        title_label.pack(pady=20)

        if title == "الرجاله":
            frame_container = tk.Frame(new_window, bg="white")
            frame_container.pack(pady=10, fill="both", expand=True)

            canvas = tk.Canvas(frame_container, bg="white")
            scrollbar = ttk.Scrollbar(frame_container, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="white")

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.order_display_frame = scrollable_frame

            def update_mandoub_display():
                for widget in self.order_display_frame.winfo_children():
                    widget.destroy()

                for name, data in self.mandoubeen.items():
                    if not isinstance(data, list) or len(data) < 2:
                        self.mandoubeen[name] = ["", []]
                        data = self.mandoubeen[name]
                    
                    number, orders = data[0], data[1]
                    mandoub_instance = Mandoub(name, number)
                    for order in orders:
                        mandoub_instance.add_order(order["value"], order["location"], order["date"])
                    
                    total_orders_value = mandoub_instance.total_orders_value()
                    total_orders_count = mandoub_instance.total_orders_count()

                    row_frame = tk.Frame(self.order_display_frame, bg="white")
                    row_frame.pack(pady=5, fill="x")

                    value_label = tk.Label(row_frame, text=f"💰 {total_orders_value} جنيه", 
                                         font=("Arial", 12), bg="lightgreen", fg="black", 
                                         width=20, height=2)
                    value_label.pack(side="left", padx=5)

                    count_label = tk.Label(row_frame, text=f"عدد الأوردرات: {total_orders_count}", 
                                         font=("Arial", 12), bg="lightblue", fg="black", 
                                         width=20, height=2)
                    count_label.pack(side="left", padx=5)

                    mandoub_label = tk.Label(row_frame, text=f"{name} ({number})", 
                                           font=("Arial", 12), bg="lightgray",
                                           fg="black", width=30, height=2)
                    mandoub_label.pack(side="left", padx=10)

                    view_orders_button = tk.Button(row_frame, text="📦 عرض الأوردرات", 
                                                 font=("Arial", 10), bg="orange",
                                                 fg="white", width=30, height=2,
                                                 command=lambda n=name: view_orders(n))
                    view_orders_button.pack(side="left", padx=5)

                    add_order_button = tk.Button(row_frame, text="+ أضف أوردر", 
                                               font=("Arial", 10), bg="green",
                                               fg="white", width=30, height=2, 
                                               command=lambda n=name: add_order(n))
                    add_order_button.pack(side="left", padx=5)

                    delete_button = tk.Button(row_frame, text="X", bg="red", 
                                            fg="white", font=("Arial", 10, "bold"),
                                            width=5, height=2, 
                                            command=lambda n=name: confirm_delete(n))
                    delete_button.pack(side="left", padx=5)

            def add_mandoub():
                name = simpledialog.askstring("إدخال اسم", "أدخل اسم المندوب:", parent=new_window)
                if not name:
                    return
                number = simpledialog.askstring("إدخال رقم", f"أدخل رقم {name}:", parent=new_window)
                if not number:
                    return

                self.mandoubeen[name] = [number, []]
                self.data_manager.data = self.mandoubeen
                self.data_manager.save_data()
                update_mandoub_display()

            def add_order(mandoub_name):
                try:
                    order_value = simpledialog.askinteger("إدخال قيمة الأوردر", 
                                                         f"أدخل قيمة الأوردر لمندوب {mandoub_name}:",
                                                         parent=new_window)
                    if order_value is None or order_value < 0:
                        messagebox.showerror("خطأ", "يجب إدخال قيمة صحيحة للأوردر.")
                        return
                except Exception as e:
                    messagebox.showerror("خطأ", f"حدث خطأ: {str(e)}")
                    return

                order_location = simpledialog.askstring("إدخال موقع الأوردر",
                                                      f"أدخل موقع الأوردر لمندوب {mandoub_name}:", 
                                                      parent=new_window)
                if not order_location:
                    return

                order_date = datetime.now().strftime('%Y-%m-%d')
                self.mandoubeen[mandoub_name][1].append(
                    {"value": order_value, "location": order_location, "date": order_date})
                self.data_manager.data = self.mandoubeen
                self.data_manager.save_data()
                update_mandoub_display()

            def confirm_delete(mandoub_name):
                result = messagebox.askyesno("تأكيد الحذف", 
                                           f"هل أنت متأكد من حذف {mandoub_name}؟", 
                                           parent=new_window)
                if result:
                    remove_mandoub(mandoub_name)

            def remove_mandoub(mandoub_name):
                if mandoub_name in self.mandoubeen:
                    del self.mandoubeen[mandoub_name]
                    self.data_manager.data = self.mandoubeen
                    self.data_manager.save_data()
                    update_mandoub_display()

            def view_orders(mandoub_name):
                orders_window = tk.Toplevel(new_window)
                orders_window.title(f"أوردرات {mandoub_name}")
                orders_window.geometry("500x500")
                orders_window.configure(bg="white")

                tk.Label(orders_window, text=f"أوردرات {mandoub_name}:", 
                       font=("Arial", 14, "bold"), bg="white").pack(pady=10)

                total_value = 0
                order_labels = []

                if mandoub_name in self.mandoubeen and len(self.mandoubeen[mandoub_name]) > 1 and self.mandoubeen[mandoub_name][1]:
                    for index, order in enumerate(self.mandoubeen[mandoub_name][1]):
                        order_frame = tk.Frame(orders_window, bg="white")
                        order_frame.pack(fill="x", padx=10, pady=5)

                        order_label = tk.Label(order_frame, 
                                             text=f"- {order['value']} جنيه ({order['location']})",
                                             font=("Arial", 12), bg="white")
                        order_label.pack(side="left", padx=10)
                        order_labels.append(order_label)

                        edit_button = tk.Button(order_frame, text="تعديل", 
                                              bg="yellow", fg="black", 
                                              font=("Arial", 10), width=6,
                                              command=lambda n=mandoub_name, i=index, 
                                              label=order_label: edit_order(n, i, label, orders_window))
                        edit_button.pack(side="right", padx=5)

                        delete_button = tk.Button(order_frame, text="X", 
                                                 bg="red", fg="white",
                                                 font=("Arial", 10, "bold"), 
                                                 width=3, height=1,
                                                 command=lambda n=mandoub_name, i=index,
                                                 orders_window=orders_window: delete_order(n, i, orders_window))
                        delete_button.pack(side="right", padx=5)

                        total_value += order["value"]

                    total_label = tk.Label(orders_window, 
                                         text=f"💰 إجمالي الأوردرات: {total_value} جنيه", 
                                         font=("Arial", 14, "bold"), 
                                         bg="white", fg="green")
                    total_label.pack(pady=10)
                else:
                    tk.Label(orders_window, text="لا توجد أوردرات حتى الآن.", 
                            font=("Arial", 12), bg="white", fg="gray").pack(pady=20)

                def edit_order(mandoub_name, order_index, label, orders_window):
                    if (mandoub_name in self.mandoubeen and 
                        len(self.mandoubeen[mandoub_name]) > 1 and 
                        order_index < len(self.mandoubeen[mandoub_name][1])):
                        order = self.mandoubeen[mandoub_name][1][order_index]

                        new_value = simpledialog.askinteger("تعديل قيمة الأوردر",
                                                           f"أدخل القيمة الجديدة للأوردر ({order['location']}):",
                                                           initialvalue=order['value'])
                        
                        new_location = simpledialog.askstring("تعديل مكان الأوردر",
                                                            f"أدخل الموقع الجديد للأوردر:",
                                                            initialvalue=order['location'])

                        if new_value is not None and new_location:
                            order['value'] = new_value
                            order['location'] = new_location
                            self.data_manager.data = self.mandoubeen
                            self.data_manager.save_data()
                            label.config(text=f"- {new_value} جنيه ({new_location})")
                            update_mandoub_display()
                            new_total = sum(o['value'] for o in self.mandoubeen[mandoub_name][1])
                            total_label.config(text=f"💰 إجمالي الأوردرات: {new_total} جنيه")

                def delete_order(mandoub_name, order_index, orders_window):
                    if (mandoub_name in self.mandoubeen and 
                        len(self.mandoubeen[mandoub_name]) > 1 and 
                        order_index < len(self.mandoubeen[mandoub_name][1])):
                        del self.mandoubeen[mandoub_name][1][order_index]
                        self.data_manager.data = self.mandoubeen
                        self.data_manager.save_data()
                        update_mandoub_display()
                        orders_window.destroy()
                        view_orders(mandoub_name)

            def clear_all_orders():
                result = messagebox.askyesno("تأكيد المسح", 
                                            "هل أنت متأكد من مسح جميع الأوردرات؟", 
                                            parent=new_window)
                if result:
                    for mandoub in self.mandoubeen.keys():
                        if len(self.mandoubeen[mandoub]) > 1:
                            self.mandoubeen[mandoub][1] = []
                    self.data_manager.data = self.mandoubeen
                    self.data_manager.save_data()
                    update_mandoub_display()

            button_bar = tk.Frame(new_window, bg="white")
            button_bar.pack(side="bottom", pady=10)

            add_mandoub_button = tk.Button(button_bar, text="+ اضافه مندوب", 
                                         font=("Arial", 14, "bold"), bg="blue",
                                         fg="white", command=add_mandoub)
            add_mandoub_button.pack(side="left", padx=10)

            clear_orders_button = tk.Button(button_bar, text="🗑️ مسح الأوردرات", 
                                          font=("Arial", 14, "bold"), bg="red", 
                                          fg="white", command=clear_all_orders)
            clear_orders_button.pack(side="left", padx=10)

            update_mandoub_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = MandoubApp(root)
    root.mainloop()
