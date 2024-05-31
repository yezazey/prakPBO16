from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QTextEdit
from PySide6.QtGui import QFont
import mysql.connector

class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Masukkan detail Anda:")
        self.label.setFont(QFont('Arial'))

        self.name_textbox = QLineEdit()
        self.name_textbox.setFont(QFont('Arial'))
        self.name_textbox.setPlaceholderText("Nama")

        self.nim_textbox = QLineEdit()
        self.nim_textbox.setFont(QFont('Arial'))
        self.nim_textbox.setPlaceholderText("NIM")

        self.hobby_textbox = QLineEdit()
        self.hobby_textbox.setFont(QFont('Arial'))
        self.hobby_textbox.setPlaceholderText("Hobi")

        self.button = QPushButton("Kirim")
        self.button.setFont(QFont('Arial'))

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont('Arial'))

        self.display_button = QPushButton("Tampil")
        self.display_button.setFont(QFont('Arial'))

        self.data_display = QTextEdit()
        self.data_display.setFont(QFont('Arial'))
        self.data_display.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.name_textbox)
        self.layout.addWidget(self.nim_textbox)
        self.layout.addWidget(self.hobby_textbox)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.reset_button)
        self.layout.addWidget(self.display_button)
        self.layout.addWidget(self.data_display)

        self.button.clicked.connect(self.greet)
        self.reset_button.clicked.connect(self.reset)
        self.display_button.clicked.connect(self.display_data)

        self.button.setStyleSheet("background-color: #82E0AA;")
        self.reset_button.setStyleSheet("background-color: #E9F5AA;")
        self.display_button.setStyleSheet("background-color: #ADD8E6;")

    def greet(self):
        name = self.name_textbox.text()
        nim = self.nim_textbox.text()
        hobby = self.hobby_textbox.text()

        if not name and not nim and not hobby:
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi!")
        elif not name:
            QMessageBox.warning(self, "Peringatan", "Nama Belum diisi!")
        elif not nim:
            QMessageBox.warning(self, "Peringatan", "Nim Belum diisi!")
        else:
            try:
                int(nim)
            except ValueError:
                QMessageBox.warning(self, "Peringatan", "Nim harus berupa angka")
                return

        if not hobby:
            QMessageBox.warning(self, "Peringatan", "Hobby Belum diisi!")
        else:
            self.label.setText(f"Halo, {name}!\nNIM Anda adalah {nim}\ndan hobi Anda adalah {hobby}.")
            self.save_to_db(name, nim, hobby)

    def save_to_db(self, name, nim, hobby):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='trisakti23',
                user='root',
                password=''
            )

            cursor = connection.cursor()
            check_query = "SELECT * FROM users WHERE name = %s OR nim = %s"
            cursor.execute(check_query, (name, nim))
            result = cursor.fetchone()

            if result:
                QMessageBox.warning(self, "Peringatan", "Nama atau NIM sudah ada!")
            else:
                insert_query = """INSERT INTO users (name, nim, hobby) VALUES (%s, %s, %s)"""
                record = (name, nim, hobby)
                cursor.execute(insert_query, record)
                connection.commit()
                QMessageBox.information(self, "Sukses", "Data berhasil disimpan ke database!")

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data ke database: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def reset(self):
        self.name_textbox.clear()
        self.nim_textbox.clear()
        self.hobby_textbox.clear()
        self.label.setText("Masukkan detail Anda:")

    def display_data(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='trisakti23',
                user='root',
                password=''
            )

            cursor = connection.cursor()
            select_query = "SELECT name, nim, hobby FROM users"
            cursor.execute(select_query)
            records = cursor.fetchall()
            
            display_text = "Data Users:\n" + "="*30 + "\n"
            for row in records:
                display_text += f"Nama: {row[0]}\nNIM: {row[1]}\nHobi: {row[2]}\n" + "="*30 + "\n"

            self.data_display.setPlainText(display_text)
        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Error", f"Gagal mengambil data dari database: {error}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikasi Input Detail")
        
        self.widget = CustomWidget()
        self.setCentralWidget(self.widget)
        

app = QApplication([])
window = MainWindow()
window.show()
app.exec_()
