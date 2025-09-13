import os
import shutil
import sys
from datetime import datetime
from PySide6.QtCore import QDate, Qt, QAbstractTableModel, QTimer
from PySide6.QtGui import QColor, QPixmap, QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout, \
    QMessageBox, QInputDialog, QLabel, QTableView, QSpacerItem, QSizePolicy, QDialog, QLineEdit
import pandas as pd
import sqlite3
import numpy as np
import ctypes
from ctypes import wintypes
from dotenv import load_dotenv


class FileBrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        copyright_symbol = '\u00A9'
        self.setWindowTitle("ASC606 & IFRS15 Revenue System by Chipmunk Robotics " + copyright_symbol + "2024")
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))

        # Set fixed window size
        self.setFixedSize(800, 800)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # add a title for the entire application
        image_label = QLabel()
        pixmap = QPixmap('ops/reserved/pic/Chipmunk Title.png')
        pixmap = pixmap.scaledToWidth(300, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        main_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Create a vertical layout for the button layouts
        button_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.setSpacing(10)

        # add accessory layouts after the buttons
        # Add a vertical spacer item to the layout
        spacer = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)
        # Labels for links
        link_label = QLabel(
            '<a style="color:dark blue;font-family:Times New Roman;font-size:12px;text-decoration:none;" href="https://www.ChipmunkRPA.com/">Visit Chipmunk Robotics Website</a>')
        link_label.setOpenExternalLinks(True)  # open the link in a web browser
        link_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(link_label)
        # Label for links
        link_label = QLabel(
            '<a style="color:dark blue;font-family:Times New Roman;font-size:12px;text-decoration:none;" href="https://www.chipmunkrpa.com/erev">Learn More About eRev</a>')
        link_label.setOpenExternalLinks(True)  # open the link in a web browser
        link_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(link_label)
        # Label for copyright
        copyright = QLabel(f"© {2024} Chipmunk Robotics")
        copyright.setStyleSheet("color: dark blue;")
        copyright.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(copyright)

        # set font sizes for all labels
        font = QFont()
        font.setPointSize(20)  # Set the font size to 20
        font.setFamily("Times New Roman")  # Set the font family to Arial

        # Create a title layout for the first row of buttons
        button_layout1_title = QHBoxLayout()
        button_layout.addLayout(button_layout1_title)

        # Create a title label in button_layout_title
        self.label1 = QLabel("<b>Contract Operations<b>")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFixedHeight(50)
        self.label1.setFont(font)
        button_layout1_title.addWidget(self.label1)

        # Create a horizontal layout for the first row of buttons
        button_layout1 = QHBoxLayout()
        button_layout.addLayout(button_layout1)

        # set button style
        button_stylesheet = """
                QPushButton {
                    background-color: rgba(255, 255, 255, 150);font-size: 14px; font-family: Times New Roman;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 255, 150);font-size: 14px; font-family: Times New Roman;
                }
            """

        # Create buttons
        self.button1 = QPushButton("Load SSPs")
        self.button1.setFixedHeight(50)
        # Set a stylesheet for the button to make it transparent and define hover effect
        self.button1.setStyleSheet(button_stylesheet)
        button_layout1.addWidget(self.button1)

        self.button2 = QPushButton("Load Contracts")
        self.button2.setFixedHeight(50)
        self.button2.setStyleSheet(button_stylesheet)
        button_layout1.addWidget(self.button2)

        self.button3 = QPushButton("Load Delivery and Billing")
        self.button3.setFixedHeight(50)
        self.button3.setStyleSheet(button_stylesheet)
        button_layout1.addWidget(self.button3)

        # Create a title layout for the second row of buttons
        button_layout2_title = QHBoxLayout()
        button_layout.addLayout(button_layout2_title)

        # Create a title label in button_layout_title
        self.label2 = QLabel("<b>Mod Operations<b>")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFixedHeight(50)
        self.label2.setFont(font)
        button_layout2_title.addWidget(self.label2)

        # Create a horizontal layout for the 2nd row of buttons
        button_layout2 = QHBoxLayout()
        button_layout.addLayout(button_layout2)

        self.button4 = QPushButton("Prospective Contract Mod")
        self.button4.setFixedHeight(50)
        self.button4.setStyleSheet(button_stylesheet)
        button_layout2.addWidget(self.button4)

        self.button5 = QPushButton("Retrospective Contract Mod")
        self.button5.setFixedHeight(50)
        self.button5.setStyleSheet(button_stylesheet)
        button_layout2.addWidget(self.button5)

        self.button5_1 = QPushButton("POB Specific VC")
        self.button5_1.setFixedHeight(50)
        self.button5_1.setStyleSheet(button_stylesheet)
        button_layout2.addWidget(self.button5_1)

        # Create a title layout for the fourth row of buttons
        button_layout4_title = QHBoxLayout()
        button_layout.addLayout(button_layout4_title)

        # Create a title label in button_layout_title
        self.label4 = QLabel("<b>Journals and Reporting<b>")
        self.label4.setAlignment(Qt.AlignCenter)
        self.label4.setFixedHeight(50)
        self.label4.setFont(font)
        button_layout4_title.addWidget(self.label4)

        # Create a horizontal layout for the third row of buttons
        button_layout4 = QHBoxLayout()
        button_layout.addLayout(button_layout4)

        # Create buttons
        self.button9 = QPushButton("Revenue Journal Entries")
        self.button9.setFixedHeight(50)
        self.button9.setStyleSheet(button_stylesheet)
        button_layout4.addWidget(self.button9)

        self.button10 = QPushButton("Contract History")
        self.button10.setFixedHeight(50)
        self.button10.setStyleSheet(button_stylesheet)
        button_layout4.addWidget(self.button10)

        self.button11 = QPushButton("Latest Contract Status")
        self.button11.setFixedHeight(50)
        self.button11.setStyleSheet(button_stylesheet)
        button_layout4.addWidget(self.button11)

        # Create a title layout for the third row of buttons
        button_layout3_title = QHBoxLayout()
        button_layout.addLayout(button_layout3_title)

        # Create a title label in button_layout_title
        self.label3 = QLabel("<b>Premium Database Functions<b>")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFixedHeight(50)
        self.label3.setFont(font)
        button_layout3_title.addWidget(self.label3)

        # Create a horizontal layout for the third row of buttons
        button_layout3 = QHBoxLayout()
        button_layout.addLayout(button_layout3)

        # Create buttons
        self.button6 = QPushButton("Backup Database")
        self.button6.setFixedHeight(50)
        self.button6.setStyleSheet(button_stylesheet)
        button_layout3.addWidget(self.button6)

        self.button7 = QPushButton("Restore from Backup")
        self.button7.setFixedHeight(50)
        self.button7.setStyleSheet(button_stylesheet)
        button_layout3.addWidget(self.button7)

        self.button8 = QPushButton("!Reset Database Completely!")
        self.button8.setFixedHeight(50)
        self.button8.setStyleSheet(button_stylesheet)
        button_layout3.addWidget(self.button8)

        self.button8_1 = QPushButton("Append from Another")
        self.button8_1.setFixedHeight(50)
        self.button8_1.setStyleSheet(button_stylesheet)
        button_layout3.addWidget(self.button8_1)

        self.button8_2 = QPushButton("Purge Contracts")
        self.button8_2.setFixedHeight(50)
        self.button8_2.setStyleSheet(button_stylesheet)
        button_layout3.addWidget(self.button8_2)

        # Set spacing between the layouts to 0
        button_layout1.setSpacing(20)
        button_layout2.setSpacing(20)
        button_layout3.setSpacing(20)
        button_layout4.setSpacing(20)
        main_layout.setSpacing(20)

        # Set margins to 0 for both layouts
        # main_layout.setContentsMargins(0, 0, 0, 0)
        button_layout1.setContentsMargins(10, 0, 10, 0)
        button_layout2.setContentsMargins(10, 0, 10, 0)
        button_layout3.setContentsMargins(10, 0, 10, 0)
        button_layout4.setContentsMargins(10, 0, 10, 0)

        # Connect button clicks to file browsing
        self.button1.clicked.connect(lambda: self.browse_file_SSPs())
        self.button2.clicked.connect(lambda: self.browse_file_Contracts())
        self.button3.clicked.connect(lambda: self.browse_file_Deliveries())
        self.button4.clicked.connect(lambda: self.browse_file_ProsMod())
        self.button5.clicked.connect(lambda: self.browse_file_RetroMod())
        self.button5_1.clicked.connect(lambda: self.browse_file_POB_specific_VC())
        self.button6.clicked.connect(lambda: self.db_backup())
        self.button7.clicked.connect(lambda: self.db_restore())
        self.button8.clicked.connect(lambda: self.db_reset())
        self.button8_1.clicked.connect(lambda: self.db_another())
        self.button8_2.clicked.connect(lambda: self.db_purge_contract())
        self.button9.clicked.connect(lambda: self.show_custom_dialog())
        self.button10.clicked.connect(lambda: self.show_contract_dialog())
        self.button11.clicked.connect(lambda: self.show_latest_contract_dialog())

        # set app background
        image_label = QLabel(self)
        pixmap_background = QPixmap('ops/reserved/pic/background.jpg')
        image_label.setPixmap(QPixmap('ops/reserved/pic/background.jpg'))
        pixmap_background = pixmap_background.scaled(1000, 800)
        image_label.setPixmap(pixmap_background)
        image_label.setGeometry(0, 0, 1000, 800)
        image_label.setScaledContents(True)
        image_label.lower()

        # Load computer names from spreadsheet
        self.license_key = self.load_license_key()

        try:
            if not (self.license_key[2] == "r" and self.license_key[5] == "s" and self.license_key[9] == "y" and
                    self.license_key[15] == "s"):
                self.show_notification_and_disable()
        except:
            self.show_notification_and_disable()

    def load_license_key(self):
        # Load computer names from the password-protected spreadsheet
        load_dotenv()
        chipmunk_key = os.getenv('Chipmunk_License_Key')
        if not chipmunk_key:
            dialog = LicenseKeyDialog()
            dialog.exec()
            load_dotenv()
            chipmunk_key = os.getenv('Chipmunk_License_Key')
            return chipmunk_key
        else:
            return chipmunk_key

    def show_notification_and_disable(self):
        msg = QMessageBox()
        # Set the icon for the QMessageBox window
        msg.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Notice for the Premium Database Functions")
        msg.setText(
            "Premium license key is not found. \nIf required, contact support for assistance support@chipmunkrpa.com\n\nNormal ASC606 Functions are still free to use.")
        msg.exec()
        self.button6.setEnabled(False)
        self.button7.setEnabled(False)
        self.button8.setEnabled(False)
        self.button8_1.setEnabled(False)
        self.button8_2.setEnabled(False)

    def db_backup(self):
        try:
            shutil.copyfile('ops/libnew/libwarm/db/ASC606.db', 'ops/libnew/libwarm/db/backup db/ASC606.db')

            # method to encrypt windows files
            def encrypt_file(file_path):
                # Load the Advapi32 library
                advapi32 = ctypes.WinDLL('Advapi32')

                # Define the required data types
                LPWSTR = wintypes.LPWSTR
                BOOL = wintypes.BOOL

                # Declare the EncryptFile function
                EncryptFile = advapi32.EncryptFileW
                EncryptFile.argtypes = (LPWSTR,)
                EncryptFile.restype = BOOL

                # Convert the file path to a wide character string
                wide_path = ctypes.create_unicode_buffer(file_path)

                # Encrypt the file
                result = EncryptFile(wide_path)

                if not result:
                    raise ctypes.WinError()

            try:
                encrypt_file('ops/libnew/libwarm/db/backup db/ASC606.db')
            except:
                pass

            QMessageBox.information(self, "ASC606 database backup", "ASC606 Database has been successfully backed up.")

        except Exception as e:
            QMessageBox.critical(self, "Error Notification", str(e))

    def db_restore(self):
        try:
            # Remove the current database file
            try:
                os.remove('ops/libnew/libwarm/db/ASC606.db')
            except FileNotFoundError:
                pass

            # Restore the database from the backup
            shutil.copyfile('ops/libnew/libwarm/db/backup db/ASC606.db', 'ops/libnew/libwarm/db/ASC606.db')

            # method to encrypt windows files
            def encrypt_file(file_path):
                # Load the Advapi32 library
                advapi32 = ctypes.WinDLL('Advapi32')

                # Define the required data types
                LPWSTR = wintypes.LPWSTR
                BOOL = wintypes.BOOL

                # Declare the EncryptFile function
                EncryptFile = advapi32.EncryptFileW
                EncryptFile.argtypes = (LPWSTR,)
                EncryptFile.restype = BOOL

                # Convert the file path to a wide character string
                wide_path = ctypes.create_unicode_buffer(file_path)

                # Encrypt the file
                result = EncryptFile(wide_path)

                if not result:
                    raise ctypes.WinError()

            try:
                encrypt_file('ops/libnew/libwarm/db/ASC606.db')
            except:
                pass

            QMessageBox.information(self, "ASC606 database restore",
                                    "ASC606 Database has been restored using the backup file.")

        except Exception as e:
            QMessageBox.critical(self, "Error Notification", str(e))

    def db_reset(self):
        try:
            # only continue when the user confirms yes
            reply = QMessageBox.question(self, "Confirmation",
                                         f"Do you want to proceed wiping out the current database?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Connect to the SQLite database
                conn = sqlite3.connect("ops/libnew/libwarm/db/ASC606.db")
                cursor = conn.cursor()
                # Get the names of all tables in the database
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                # Drop each table in the database
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                # Commit the changes and close the connection
                conn.commit()
                conn.close()
                QMessageBox.information(self, "ASC606 database reset", "ASC606 Database has been wiped out and reset!")

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def db_another(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        try:
            if file_path:
                # Connect to the source database
                source_conn = sqlite3.connect(file_path)
                source_cursor = source_conn.cursor()

                # Connect to the destination database
                destination_conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                destination_cursor = destination_conn.cursor()

                # Retrieve data from the source table
                source_cursor.execute('''SELECT * FROM "Contract_Live"''')
                data = source_cursor.fetchall()

                # Generate placeholders for the insert statement
                placeholders = ', '.join(['?'] * len(data[0]))

                # Insert data into the destination table
                destination_cursor.executemany(f'''INSERT INTO "Contract_Live" VALUES ({placeholders})''', data)

                # Commit the transaction
                destination_conn.commit()

                # Close the cursors and connections
                source_cursor.close()
                source_conn.close()
                destination_cursor.close()
                destination_conn.close()

                # method to encrypt windows files
                def encrypt_file(file_path):
                    # Load the Advapi32 library
                    advapi32 = ctypes.WinDLL('Advapi32')

                    # Define the required data types
                    LPWSTR = wintypes.LPWSTR
                    BOOL = wintypes.BOOL

                    # Declare the EncryptFile function
                    EncryptFile = advapi32.EncryptFileW
                    EncryptFile.argtypes = (LPWSTR,)
                    EncryptFile.restype = BOOL

                    # Convert the file path to a wide character string
                    wide_path = ctypes.create_unicode_buffer(file_path)

                    # Encrypt the file
                    result = EncryptFile(wide_path)

                    if not result:
                        raise ctypes.WinError()

                try:
                    encrypt_file('ops/libnew/libwarm/db/ASC606.db')
                except:
                    pass

                QMessageBox.information(self, "ASC606 database appended",
                                        "ASC606 Database has been appended with the new dataset from the database selected!")

        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                source_conn.close()
                destination_conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def db_purge_contract(self):
        try:
            input_text, ok = QInputDialog.getText(self, "Start Date Input",
                                                  f"Enter the start date of the date range to purge the revenue contract history (YYYY-MM-DD):")
            if ok:
                qdate_start = QDate.fromString(input_text, "yyyy-MM-dd")
                if not qdate_start.isValid():
                    QMessageBox.warning(self, "Invalid Date",
                                        "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                else:
                    input_text, ok = QInputDialog.getText(self, "Date Input",
                                                          f"Enter the end date of the date range to purge the revenue contract history (YYYY-MM-DD):")
                    if ok:
                        qdate_end = QDate.fromString(input_text, "yyyy-MM-dd")
                        if not qdate_end.isValid():
                            QMessageBox.warning(self, "Invalid Date",
                                                "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                        else:
                            contract_name, ok = QInputDialog.getText(self, "Enter contract unique name",
                                                                     f"Please enter the specific contract unique name to purge the revenue history:")
                            # Define the datetime period
                            start_date = datetime.combine(qdate_start.toPython(), datetime.min.time())
                            end_date = datetime.combine(qdate_end.toPython(), datetime.min.time())
                            # execute the deletion
                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            # Create a cursor object to interact with the database
                            cursor = conn.cursor()
                            query_purge_contract = f'''
                                DELETE FROM "Contract_Live" 
                                WHERE "Contract Unique Name" = "{contract_name}" AND "Current Period" BETWEEN "{start_date}" AND "{end_date}"
                                '''
                            # Execute the query and create a DataFrame
                            cursor.execute(query_purge_contract)

                            # Commit the changes to the database
                            conn.commit()

                            # Close the cursor and the database connection
                            cursor.close()
                            conn.close()

                            msg = QMessageBox()
                            # Set the icon for the QMessageBox window
                            msg.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
                            msg.setIcon(QMessageBox.Information)
                            msg.setWindowTitle("Contract Records Purged")
                            msg.setText(
                                "The contract records within the periods selected are successfully purged from the database.")
                            msg.exec()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_SSPs(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        try:
            # Operation
            if file_path:
                df = pd.read_excel(file_path)
                db_file = "ops/libnew/libwarm/db/ASC606.db"
                # build validation here:
                expected_titles = ['SKU Unique ID', 'SKU Name', 'Distinct or Nondistinct', 'SKU Unit List Price',
                                   'ASC 606 Stratification', 'Midpoint Discount Percentage', 'SSP Range Method (+-)',
                                   'SSP Version', 'Revenue Account']  # Specify the expected column titles
                actual_titles = df.columns.tolist()  # Get the actual column titles as a list
                missing_titles = [title for title in expected_titles if title not in actual_titles]
                extra_titles = [title for title in actual_titles if title not in expected_titles]
                numbers_to_validate = ['SKU Unit List Price', 'Midpoint Discount Percentage',
                                       'SSP Range Method (+-)']  # Specify the columns to validate as numbers
                # error handling the missing and extra fields
                if missing_titles or extra_titles:
                    QMessageBox.information(self, "File Upload Error",
                                            "Error: The Excel file has incorrect or missing column titles.")
                    if missing_titles:
                        QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                    if extra_titles:
                        QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                else:
                    # Additional error handling or validation logic can be implemented here
                    stop_process = False  # Flag variable to control the loop
                    for column in numbers_to_validate:
                        if stop_process:
                            break  # Exit the loop if the flag is set to True
                        try:
                            pd.to_numeric(df[column], errors='raise')
                        except (ValueError, TypeError):
                            QMessageBox.information(self, "Format Error",
                                                    f"Error: The column '{column}' should contain numeric values.")
                            stop_process = True  # Set the flag to True to skip the remaining iterations
                    if not stop_process:
                        # Proceed with further processing of the data
                        # convert versioning to text type
                        df['SSP Version'] = df['SSP Version'].astype(str)
                        # continue
                        conn = sqlite3.connect(db_file)
                        df.to_sql("SKU_SSP", conn, if_exists="replace", index=False)
                        # close the db connection
                        conn.close()

                        # method to encrypt windows files
                        def encrypt_file(file_path):
                            # Load the Advapi32 library
                            advapi32 = ctypes.WinDLL('Advapi32')

                            # Define the required data types
                            LPWSTR = wintypes.LPWSTR
                            BOOL = wintypes.BOOL

                            # Declare the EncryptFile function
                            EncryptFile = advapi32.EncryptFileW
                            EncryptFile.argtypes = (LPWSTR,)
                            EncryptFile.restype = BOOL

                            # Convert the file path to a wide character string
                            wide_path = ctypes.create_unicode_buffer(file_path)

                            # Encrypt the file
                            result = EncryptFile(wide_path)

                            if not result:
                                raise ctypes.WinError()

                        try:
                            encrypt_file(db_file)
                        except:
                            pass

                        QMessageBox.information(self, "SSPs are set up",
                                                "All company SSPs for the uploaded file are set up. To add or update, re-upload SSPs to refresh.")

        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_Contracts(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        try:
            if file_path:
                # Operation
                df_contract = pd.read_excel(file_path)
                # build validation here:
                expected_titles = ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'POB Start Date',
                                   'POB End Date',
                                   'ASC 606 Stratification', 'Original POB Total Selling Price',
                                   'Original POB Total Qty', 'Selling Entity',
                                   'SSP Version', 'Deferred Revenue Account', 'Unbilled A/R Account',
                                   'Current Period', 'Memo 1', 'Memo 2', 'Memo 3']  # Specify the expected column titles
                actual_titles = df_contract.columns.tolist()  # Get the actual column titles as a list
                missing_titles = [title for title in expected_titles if title not in actual_titles]
                extra_titles = [title for title in actual_titles if title not in expected_titles]
                numbers_to_validate = ['Original POB Total Selling Price',
                                       'Original POB Total Qty']  # Specify the columns to validate as numbers
                # error handling the missing and extra fields
                if missing_titles or extra_titles:
                    QMessageBox.information(self, "File Upload Error",
                                            "Error: The Excel file has incorrect or missing column titles.")
                    if missing_titles:
                        QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                    if extra_titles:
                        QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                else:
                    # Additional error handling or validation logic can be implemented here
                    stop_process = False  # Flag variable to control the loop
                    for column in numbers_to_validate:
                        if stop_process:
                            break  # Exit the loop if the flag is set to True
                        try:
                            pd.to_numeric(df_contract[column], errors='raise')
                        except (ValueError, TypeError):
                            QMessageBox.information(self, "Format Error",
                                                    f"Error: The column '{column}' should contain numeric values.")
                            stop_process = True  # Set the flag to True to skip the remaining iterations
                    if not stop_process:
                        # Proceed with further processing of the data
                        # convert versioning to text type
                        df_contract['SSP Version'] = df_contract['SSP Version'].astype(str)
                        # continue
                        # load SSPs into df_SSP
                        conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                        query = f'''
                           SELECT *
                           FROM "SKU_SSP"
                           '''
                        # Execute the query and create a DataFrame
                        df_SSP = pd.read_sql_query(query, conn)
                        conn.close()

                        # merge two dataframes by left join
                        merged_df = pd.merge(df_contract, df_SSP,
                                             on=['SKU Name', 'ASC 606 Stratification', 'SSP Version'],
                                             how='left', indicator=True, suffixes=('', '_right_table'))

                        # calculate SSP ranges
                        merged_df['Original SSP - Midpoint'] = merged_df['Original POB Total Qty'] * merged_df[
                            'SKU Unit List Price'] * (1 - merged_df['Midpoint Discount Percentage'])
                        merged_df['Original SSP - Higher'] = merged_df['Original POB Total Qty'] * merged_df[
                            'SKU Unit List Price'] * (1 - merged_df['Midpoint Discount Percentage']) * (
                                                                     1 + merged_df['SSP Range Method (+-)'])
                        merged_df['Original SSP - Lower'] = merged_df['Original POB Total Qty'] * merged_df[
                            'SKU Unit List Price'] * (1 - merged_df['Midpoint Discount Percentage']) * (
                                                                    1 - merged_df['SSP Range Method (+-)'])

                        # determine the original SSP
                        def compare_columns(row):
                            if row['Original POB Total Selling Price'] > row['Original SSP - Higher']:
                                return row['Original SSP - Higher']
                            elif row['Original POB Total Selling Price'] < row['Original SSP - Lower']:
                                return row['Original SSP - Lower']
                            else:
                                return row['Original POB Total Selling Price']

                        merged_df['Original Extended SSP'] = merged_df.apply(compare_columns, axis=1)

                        # perform the initial allocation
                        # get the total contract price
                        merged_df['Original Total Contract Price'] = merged_df.groupby('Contract Unique Name')[
                            'Original POB Total Selling Price'].transform('sum')
                        # get the total contract SSP
                        merged_df['Original Total Contract SSP'] = merged_df.groupby('Contract Unique Name')[
                            'Original Extended SSP'].transform('sum')
                        # get allocation for each POB
                        merged_df['Original Allocation'] = merged_df['Original Extended SSP'] / merged_df[
                            'Original Total Contract SSP'] * merged_df['Original Total Contract Price']
                        # get unit SSP
                        merged_df['Original Unit SSP'] = merged_df['Original Extended SSP'] / merged_df[
                            'Original POB Total Qty']
                        # get unit Rev Rec
                        merged_df['Original Unit Rev Rec'] = merged_df['Original Allocation'] / merged_df[
                            'Original POB Total Qty']

                        # populate the previous and current fields - everything should be the same with the initial contract
                        merged_df['Previous Period'] = pd.NaT
                        merged_df['Previous Remaining Qty'] = merged_df['Original POB Total Qty']
                        merged_df['Previous Remaining SSP'] = merged_df['Original Extended SSP']
                        merged_df['Previous Remaining Allocation'] = merged_df['Original Allocation']
                        merged_df['Previous Remaining Billing'] = merged_df['Original POB Total Selling Price']
                        merged_df['Previous Unit SSP'] = merged_df['Original Unit SSP']
                        merged_df['Previous Remaining Unit Rev Rec'] = merged_df['Original Unit Rev Rec']
                        merged_df['Previous Delivery - Cumulative'] = 0
                        merged_df['Previous Rev Rec - Cumulative'] = 0
                        merged_df['Previous Pre-ASC606 Revenue (Net Design Only) - Cumulative'] = 0
                        merged_df['Previous Billing - Cumulative'] = 0
                        merged_df['Previous Cumulative Catchup - Cumulative - Disclosure Only'] = 0
                        merged_df['Previous SSP Delivered - Cumulative'] = 0
                        merged_df['Previous Contract Position - POB'] = 0
                        merged_df['Previous Contract Position - Contract Level'] = 0
                        merged_df['Previous Reclass to UAR'] = 0
                        merged_df['Current Remaining Qty'] = merged_df['Original POB Total Qty']
                        merged_df['Current Remaining SSP'] = merged_df['Original Extended SSP']
                        merged_df['Current Remaining Allocation'] = merged_df['Original Allocation']
                        merged_df['Current Remaining Billing'] = merged_df['Original POB Total Selling Price']
                        merged_df['Current Unit SSP'] = merged_df['Original Unit SSP']
                        merged_df['Current Remaining Unit Rev Rec'] = merged_df['Original Unit Rev Rec']
                        merged_df['Current Delivery'] = 0
                        merged_df['Current Rev Rec'] = 0
                        merged_df['Current Pre-ASC606 Revenue (Net Design Only)'] = 0
                        merged_df['Current Billing'] = 0
                        merged_df['Current Cumulative Catchup - Disclosure Only'] = 0
                        merged_df['Current SSP Delivered'] = 0
                        merged_df['Current Delivery - Cumulative'] = 0
                        merged_df['Current Rev Rec - Cumulative'] = 0
                        merged_df['Current Pre-ASC606 Revenue (Net Design Only) - Cumulative'] = 0
                        merged_df['Current Billing - Cumulative'] = 0
                        merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = 0
                        merged_df['Current SSP Delivered - Cumulative'] = 0
                        merged_df['Current Contract Position - POB'] = 0
                        merged_df['Current Contract Position - Contract Level'] = 0
                        merged_df['Current Reclass to UAR'] = 0
                        merged_df['Processing Time Log'] = pd.Timestamp.now()
                        merged_df['Record Unique ID without time'] = merged_df['Contract Unique Name'] + " " + \
                                                                     merged_df[
                                                                         'POB Unique ID'] + " " + merged_df['SKU Name']
                        merged_df['Record Unique ID'] = merged_df['Processing Time Log'].astype(str) + " " + merged_df[
                            'Contract Unique Name'] + " " + merged_df['POB Unique ID'] + " " + merged_df['SKU Name']

                        # error handling when the upload contract POBs doesn't match to any SKU
                        unmerged_left = merged_df.loc[merged_df['_merge'] == 'left_only', merged_df.columns]
                        if unmerged_left.empty:
                            # QMessageBox.information(self, "Contract Setup", "All POBs are successfully found and matched with SSPs! Setting up the contract table now.")
                            pass
                        else:
                            UnmatchedPOB = ",".join(unmerged_left["SKU Name"].tolist())
                            QMessageBox.information(self, "Contract Error",
                                                    f"Those POBs below are not matched with a SKU within the SKU databse. Re-upload the file after fixes! \n '{UnmatchedPOB}'")
                            raise Exception("The process is stopped for users to fix the file")

                        # remove those unused columns
                        merged_df = merged_df.drop(
                            columns=[col for col in merged_df.columns if col.endswith(('_right_table'))])
                        merged_df = merged_df.drop(
                            columns=[col for col in merged_df.columns if col.endswith(('_merge'))])

                        # Sort the DataFrame based on 'Record Unique ID without time'
                        merged_df = merged_df.sort_values('Record Unique ID without time')

                        # check in incremental data if table exists; if not create the table
                        conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                        cur = conn.cursor()
                        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Contract_Live'")
                        table_exists = bool(cur.fetchone())
                        # Close the cursor and connection
                        cur.close()
                        conn.close()
                        # insert incremental if exists
                        if table_exists:
                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            # query = f'''
                            #   SELECT *
                            #   FROM "Contract_Live"
                            #   '''
                            # Execute the query and create a DataFrame
                            # df_contract_live = pd.read_sql_query(query, conn)
                            # conn.close()
                            # Filter the pandas DataFrame to include only incremental data
                            # incremental_data = merged_df[
                            #    ~merged_df['Record Unique ID'].isin(df_contract_live['Record Unique ID'])]
                            # Insert the incremental data into the SQL table
                            # conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            merged_df.to_sql("Contract_Live", conn, if_exists="append", index=False)
                            conn.close()
                        else:
                            # create Contract_Live table
                            conn = sqlite3.connect("ops/libnew/libwarm/db/ASC606.db")
                            merged_df.to_sql("Contract_Live", conn, if_exists="replace", index=False)
                            conn.close()

                        QMessageBox.information(self, "Contracts are set up",
                                                "All contracts(s) within the uploaded file are successfully set up!")
        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_Deliveries(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        try:
            if file_path:
                input_text, ok = QInputDialog.getText(self, "Date Input",
                                                      f"Enter current period in this format (YYYY-MM-DD) for delivery/billing upload:")
                if ok:
                    qdate = QDate.fromString(input_text, "yyyy-MM-dd")
                    if not qdate.isValid():
                        QMessageBox.warning(self, "Invalid Date",
                                            "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                    else:
                        # message = f"The following date is set for the current delivery/billing: {qdate.toString('yyyy-MM-dd')}"
                        # QMessageBox.information(self, "Date Selected", message)
                        # Operation
                        df_progress = pd.read_excel(file_path)
                        # build validation here:
                        # insert Current Pre-ASC606 Revenue (Net Design Only)
                        expected_titles = ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'Current Delivery',
                                           'Current Billing', 'Current Pre-ASC606 Revenue (Net Design Only)', 'Memo 1',
                                           'Memo 2', 'Memo 3']  # Specify the expected column titles
                        actual_titles = df_progress.columns.tolist()  # Get the actual column titles as a list
                        missing_titles = [title for title in expected_titles if title not in actual_titles]
                        extra_titles = [title for title in actual_titles if title not in expected_titles]
                        numbers_to_validate = ['Current Delivery',
                                               'Current Billing',
                                               'Current Pre-ASC606 Revenue (Net Design Only)']  # Specify the columns to validate as numbers
                        # error handling the missing and extra fields
                        if missing_titles or extra_titles:
                            QMessageBox.information(self, "File Upload Error",
                                                    "Error: The Excel file has incorrect or missing column titles.")
                            if missing_titles:
                                QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                            if extra_titles:
                                QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                        else:
                            # Additional error handling or validation logic can be implemented here
                            stop_process = False  # Flag variable to control the loop
                            for column in numbers_to_validate:
                                if stop_process:
                                    break  # Exit the loop if the flag is set to True
                                try:
                                    pd.to_numeric(df_progress[column], errors='raise')
                                    if df_progress[column].isna().any():
                                        QMessageBox.information(self, "Format Error",
                                                                f"Error: The column '{column}' should contain numeric values.")
                                        stop_process = True  # Set the flag to True to skip the remaining iterations
                                except (ValueError, TypeError):
                                    QMessageBox.information(self, "Format Error",
                                                            f"Error: The column '{column}' should contain numeric values.")
                                    stop_process = True  # Set the flag to True to skip the remaining iterations
                            if not stop_process:
                                # Proceed with further processing of the data
                                conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                query = '''
                                    SELECT t1.*
                                    FROM Contract_Live t1
                                    JOIN (
                                            SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                            FROM Contract_Live
                                            GROUP BY "Record Unique ID without time"
                                    ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                    '''
                                # Execute the query and create a DataFrame
                                df_contract_live = pd.read_sql_query(query, conn)
                                conn.close()

                                # Convert the Timestamp field to datetime
                                df_contract_live['Processing Time Log'] = pd.to_datetime(
                                    df_contract_live['Processing Time Log'])

                                # Retrieve the latest records for each unique ID
                                df_contract_live_latest = df_contract_live.loc[
                                    df_contract_live.groupby('Record Unique ID without time')[
                                        'Processing Time Log'].idxmax()]

                                # Sort the DataFrame based on 'Record Unique ID without time'
                                df_contract_live_latest = df_contract_live_latest.sort_values(
                                    'Record Unique ID without time')

                                # group deliveries and billings if multiple records exist for the same SKU within the same contract
                                df_progress = df_progress.groupby(
                                    ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'Memo 1', 'Memo 2',
                                     'Memo 3'])[
                                    ['Current Delivery', 'Current Billing',
                                     'Current Pre-ASC606 Revenue (Net Design Only)']].sum().reset_index()

                                # print(df_progress)

                                # concat to create a unique ID for the later join
                                df_progress['Record Unique ID without time'] = df_progress[
                                                                                   'Contract Unique Name'] + " " + \
                                                                               df_progress['POB Unique ID'] + " " + \
                                                                               df_progress[
                                                                                   'SKU Name']

                                # Sort the DataFrame based on 'Record Unique ID without time'
                                df_progress = df_progress.sort_values('Record Unique ID without time')

                                # Perform outer join and show unmatched records from the progress table
                                merged = pd.merge(df_contract_live_latest, df_progress,
                                                  on='Record Unique ID without time',
                                                  how='outer', indicator=True, suffixes=('', '_progress'))

                                # error handling when the upload doesn't match to any POB
                                unmerged_right = merged.loc[merged['_merge'] == 'right_only', merged.columns]

                                if not unmerged_right.empty:
                                    list_error = unmerged_right.index.tolist()
                                    error_position = [x + 1 for x in list_error]
                                    failed_list_str = [str(x) for x in error_position]
                                    failed_list = ",".join(failed_list_str)
                                    QMessageBox.information(self, "Delivery/Billing load failed",
                                                            f"Below deliveries are not found with a match in contracts. Re-upload the file after fixes! \nFile position(s): \n{failed_list}")
                                    raise Exception("The process is stopped for users to fix the file")

                                else:
                                    # check post join df
                                    # print(merged_df)
                                    # create a list to only show the contracts with activities
                                    result_contract_mod_unique_name = merged.loc[
                                        merged['Current Delivery_progress'].notna() & merged[
                                            'Current Billing_progress'].notna() & merged[
                                            'Current Pre-ASC606 Revenue (Net Design Only)'].notna(), 'Contract Unique Name']
                                    result_contract_mod_unique_name_list = result_contract_mod_unique_name.tolist()

                                    # Filter and replace the original DataFrame based on the list
                                    merged = merged.loc[
                                        merged['Contract Unique Name'].isin(result_contract_mod_unique_name_list)]

                                    # Compare values between two columns
                                    merged['Flag_Qty'] = merged['Current Remaining Qty'] < merged[
                                        'Current Delivery_progress']
                                    merged['Flag_Billing'] = merged[merged["ASC 606 Stratification"] != "VC"][
                                                                 'Current Remaining Billing'] < \
                                                             merged[merged["ASC 606 Stratification"] != "VC"][
                                                                 'Current Billing_progress']
                                    # Check if any True value exists in 'Flag' column
                                    # print(merged['Flag_Qty'])
                                    # print(merged['Flag_Billing'])
                                    has_true_qty = merged['Flag_Qty'].any()
                                    has_true_billing = merged['Flag_Billing'].any()

                                    if has_true_qty or has_true_billing:
                                        QMessageBox.information(self, "Delivery/Billing load failed",
                                                                "Qty or billing loaded are greater than the remaining of the POBs. Check your uploads please.")
                                        raise Exception("The process is stopped for users to fix the file")

                                    else:
                                        # drop the flags
                                        merged = merged.drop(columns=['Flag_Qty', 'Flag_Billing'])
                                        # update the previous delivery info. before bringing the new deliveries
                                        merged["Previous Remaining Qty"] = merged["Current Remaining Qty"].fillna(0)
                                        merged["Previous Remaining SSP"] = merged["Current Remaining SSP"].fillna(0)
                                        merged["Previous Remaining Allocation"] = merged[
                                            "Current Remaining Allocation"].fillna(0)
                                        merged["Previous Remaining Billing"] = merged[
                                            "Current Remaining Billing"].fillna(0)
                                        merged["Previous Unit SSP"] = merged["Current Unit SSP"].fillna(0)
                                        merged["Previous Remaining Unit Rev Rec"] = merged[
                                            "Current Remaining Unit Rev Rec"].fillna(
                                            0)
                                        merged["Previous Delivery - Cumulative"] = merged[
                                            "Current Delivery - Cumulative"].fillna(0)
                                        merged["Previous Rev Rec - Cumulative"] = merged[
                                            "Current Rev Rec - Cumulative"].fillna(0)

                                        # insert Current Pre-ASC606 Revenue (Net Design Only)
                                        merged["Previous Pre-ASC606 Revenue (Net Design Only) - Cumulative"] = merged[
                                            "Current Pre-ASC606 Revenue (Net Design Only) - Cumulative"].fillna(0)
                                        merged["Previous Billing - Cumulative"] = merged[
                                            "Current Billing - Cumulative"].fillna(0)
                                        merged['Previous Cumulative Catchup - Cumulative - Disclosure Only'] = merged[
                                            'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                        merged['Previous SSP Delivered - Cumulative'] = merged[
                                            'Current SSP Delivered - Cumulative'].fillna(0)
                                        merged["Previous Contract Position - POB"] = merged[
                                            "Current Contract Position - POB"].fillna(0)
                                        merged["Previous Contract Position - Contract Level"] = merged[
                                            "Current Contract Position - Contract Level"].fillna(0)
                                        merged["Previous Reclass to UAR"] = merged["Current Reclass to UAR"].fillna(0)
                                        merged['Previous Period'] = merged['Current Period']
                                        # load the progress qty and bills to the existing dataframe and update the current fields
                                        merged["Current Delivery"] = merged["Current Delivery_progress"].fillna(0)
                                        merged["Current Billing"] = merged["Current Billing_progress"].fillna(0)
                                        # print(merged["Memo 1"])
                                        # print(merged["Memo 1_progress"])
                                        merged["Memo 1"] = merged["Memo 1_progress"].fillna(merged["Memo 1"])
                                        merged["Memo 2"] = merged["Memo 2_progress"].fillna(merged["Memo 2"])
                                        merged["Memo 3"] = merged["Memo 3_progress"].fillna(merged["Memo 3"])

                                        # insert Current Pre-ASC606 Revenue (Net Design Only)
                                        merged["Current Pre-ASC606 Revenue (Net Design Only)"] = merged[
                                            "Current Pre-ASC606 Revenue (Net Design Only)_progress"].fillna(0)

                                        merged['Current Cumulative Catchup - Disclosure Only'] = 0
                                        # ask for an input of the current period
                                        merged['Current Period'] = datetime.combine(qdate.toPython(),
                                                                                    datetime.min.time())
                                        # continue updating the current fields
                                        merged["Current Rev Rec"] = merged["Current Delivery"].fillna(0) * merged[
                                            "Current Remaining Unit Rev Rec"].fillna(0)
                                        merged['Current SSP Delivered'] = merged["Current Delivery"].fillna(0) * merged[
                                            "Current Unit SSP"].fillna(0)
                                        merged["Current Remaining Qty"] = merged["Current Remaining Qty"].fillna(0) - \
                                                                          merged["Current Delivery"].fillna(0)
                                        merged["Current Remaining SSP"] = merged["Current Remaining SSP"].fillna(0) - \
                                                                          merged["Current Delivery"].fillna(0) * merged[
                                                                              "Current Unit SSP"].fillna(0)
                                        merged["Current Remaining Allocation"] = merged[
                                                                                     "Current Remaining Allocation"].fillna(
                                            0) - merged["Current Rev Rec"].fillna(0)
                                        merged["Current Remaining Billing"] = merged[
                                                                                  "Current Remaining Billing"].fillna(
                                            0) - merged["Current Billing"].fillna(0)

                                        # fill NaN with zero (when fully delivered)
                                        merged["Current Unit SSP"] = (
                                                merged["Current Remaining SSP"].fillna(0) / merged[
                                            "Current Remaining Qty"].fillna(0)).fillna(0)
                                        merged["Current Remaining Unit Rev Rec"] = (merged[
                                                                                        "Current Remaining Allocation"].fillna(
                                            0) / merged["Current Remaining Qty"].fillna(0)).fillna(0)

                                        # continue calculating the rest current fields
                                        merged["Current Delivery - Cumulative"] = merged[
                                                                                      "Previous Delivery - Cumulative"].fillna(
                                            0) + merged["Current Delivery"].fillna(0)
                                        merged["Current Rev Rec - Cumulative"] = merged[
                                                                                     "Previous Rev Rec - Cumulative"].fillna(
                                            0) + merged["Current Rev Rec"].fillna(0)
                                        merged["Current Billing - Cumulative"] = merged[
                                                                                     "Previous Billing - Cumulative"].fillna(
                                            0) + merged["Current Billing"].fillna(0)
                                        # insert Current Pre-ASC606 Revenue (Net Design Only)
                                        merged["Current Pre-ASC606 Revenue (Net Design Only) - Cumulative"] = merged[
                                                                                                                  "Previous Pre-ASC606 Revenue (Net Design Only) - Cumulative"].fillna(
                                            0) + merged["Current Pre-ASC606 Revenue (Net Design Only)"].fillna(0)

                                        merged['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged[
                                                                                                                  'Previous Cumulative Catchup - Cumulative - Disclosure Only'].fillna(
                                            0) + merged['Current Cumulative Catchup - Disclosure Only'].fillna(0)
                                        merged['Current SSP Delivered - Cumulative'] = merged[
                                                                                           "Previous SSP Delivered - Cumulative"].fillna(
                                            0) + merged["Current SSP Delivered"].fillna(0)
                                        merged["Current Contract Position - POB"] = merged[
                                                                                        "Current Billing - Cumulative"].fillna(
                                            0) - merged["Current Rev Rec - Cumulative"].fillna(0)
                                        merged["Current Contract Position - Contract Level"] = \
                                            merged.groupby('Contract Unique Name')[
                                                'Current Contract Position - POB'].transform(
                                                'sum')
                                        # need to use loc to build conditional logics to populate this
                                        merged["Current Reclass to UAR"] = np.where(
                                            merged['Current Contract Position - Contract Level'] < 0,
                                            -merged['Current Contract Position - Contract Level'] /
                                            merged.groupby('Contract Unique Name')[
                                                'Current SSP Delivered - Cumulative'].transform(
                                                'sum') * merged['Current SSP Delivered - Cumulative'], 0)
                                        # override VC line's reclass to UAR to zero as this is not a true POB
                                        merged.loc[
                                            merged["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                        # remove the progress table's duplicate data
                                        merged = merged.drop(
                                            columns=[col for col in merged.columns if col.endswith(('_progress'))])
                                        merged = merged.drop(
                                            columns=[col for col in merged.columns if col.endswith(('_merge'))])

                                        # add another validation to make sure the current delivery if negative,
                                        # doesn't cause the total delivery cumulative to be negative
                                        # print((merged["Current Delivery - Cumulative"] < 0).any())
                                        # print((merged["Current Billing - Cumulative"] < 0).any())
                                        # print((merged[merged["Current Billing - Cumulative"] < 0]["ASC 606 Stratification"] != "VC").all())

                                        if (merged["Current Remaining Qty"] < 0).any() or (
                                                merged[merged["ASC 606 Stratification"] != "VC"][
                                                    'Current Remaining Billing'] < 0).any():
                                            QMessageBox.information(self, "Delivery/Billing load failed",
                                                                    "Qty returned or refund are greater than previous total delivery or total amount previously paid by the customer causing the total qty delivered or total billing to date to be negative. Check your uploads please.")
                                            raise Exception("The process is stopped for users to fix the file")

                                        else:
                                            # update the records timestamp
                                            merged['Processing Time Log'] = pd.Timestamp.now()
                                            merged['Record Unique ID without time'] = merged[
                                                                                          'Contract Unique Name'] + " " + \
                                                                                      merged['POB Unique ID'] + " " + \
                                                                                      merged[
                                                                                          'SKU Name']
                                            merged['Record Unique ID'] = merged['Processing Time Log'].astype(
                                                str) + " " + \
                                                                         merged['Contract Unique Name'] + " " + merged[
                                                                             'POB Unique ID'] + " " + merged['SKU Name']

                                            # Sort the DataFrame based on 'Record Unique ID without time'
                                            merged = merged.sort_values('Record Unique ID without time')

                                            # check in incremental data if table exists; if not create the table
                                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            cur = conn.cursor()
                                            cur.execute(
                                                "SELECT name FROM sqlite_master WHERE type='table' AND name='Contract_Live'")
                                            table_exists = bool(cur.fetchone())
                                            # Close the cursor and connection
                                            cur.close()
                                            conn.close()
                                            # insert incremental if exists
                                            if table_exists:
                                                conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                                # query = f'''
                                                #    SELECT *
                                                #    FROM "Contract_Live"
                                                #    '''
                                                # Execute the query and create a DataFrame
                                                # df_contract_live = pd.read_sql_query(query, conn)
                                                # conn.close()
                                                # Filter the pandas DataFrame to include only incremental data
                                                # incremental_data = merged[
                                                #    ~merged['Record Unique ID'].isin(
                                                #        df_contract_live['Record Unique ID'])]
                                                # Insert the incremental data into the SQL table
                                                # conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                                # incremental_data.to_sql("Contract_Live", conn, if_exists="append",
                                                #                        index=False)
                                                # '''
                                                merged.to_sql("Contract_Live", conn, if_exists="append", index=False)
                                                conn.close()
                                                QMessageBox.information(self, "Rev Rec Success",
                                                                        "Rev Rec has been processed with uploaded deliveries and/or billings for the current date :)")
                                            else:
                                                # create Contract_Live table
                                                raise Exception("No contract table is found!")
        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_ProsMod(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        try:
            if file_path:
                input_text, ok = QInputDialog.getText(self, "Date Input",
                                                      f"Enter the prospective contract mod date in this format (YYYY-MM-DD):")
                if ok:
                    qdate = QDate.fromString(input_text, "yyyy-MM-dd")
                    if not qdate.isValid():
                        QMessageBox.warning(self, "Invalid Date",
                                            "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                    else:
                        # message = f"The following date is set for the prospective contract modification: {qdate.toString('yyyy-MM-dd')}"
                        # QMessageBox.information(self, "Date Selected", message)
                        # Operation
                        df_prospective_changes = pd.read_excel(file_path)
                        # build validation here:
                        expected_titles = ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'Mod Start Date',
                                           'Mod End Date', 'ASC 606 Stratification', 'Mod Billing', 'Mod Qty',
                                           'Selling Entity', 'Deferred Revenue Account',
                                           'Unbilled A/R Account', 'SSP Version', 'Memo 1', 'Memo 2',
                                           'Memo 3']  # Specify the expected column titles
                        actual_titles = df_prospective_changes.columns.tolist()  # Get the actual column titles as a list
                        missing_titles = [title for title in expected_titles if title not in actual_titles]
                        extra_titles = [title for title in actual_titles if title not in expected_titles]
                        numbers_to_validate = ['Mod Billing',
                                               'Mod Qty']  # Specify the columns to validate as numbers
                        # error handling the missing and extra fields
                        if missing_titles or extra_titles:
                            QMessageBox.information(self, "File Upload Error",
                                                    "Error: The Excel file has incorrect or missing column titles.")
                            if missing_titles:
                                QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                            if extra_titles:
                                QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                        else:
                            # Additional error handling or validation logic can be implemented here
                            stop_process = False  # Flag variable to control the loop
                            for column in numbers_to_validate:
                                if stop_process:
                                    break  # Exit the loop if the flag is set to True
                                try:
                                    pd.to_numeric(df_prospective_changes[column], errors='raise')

                                    # check pd to numeric values
                                    # print(df_retrospective_changes[column])
                                    if df_prospective_changes[column].isna().any():
                                        QMessageBox.information(self, "Format Error",
                                                                f"Error: The column '{column}' should contain numeric values.")
                                        stop_process = True  # Set the flag to True to skip the remaining iterations
                                except (ValueError, TypeError):
                                    QMessageBox.information(self, "Format Error",
                                                            f"Error: The column '{column}' should contain numeric values.")
                                    stop_process = True  # Set the flag to True to skip the remaining iterations
                            if not stop_process:
                                conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                query_existing_contract = '''
                                    SELECT t1.*
                                    FROM Contract_Live t1
                                    JOIN (
                                        SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                        FROM Contract_Live
                                        GROUP BY "Record Unique ID without time"
                                    ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                '''
                                query_SSP = '''
                                    SELECT * FROM "SKU_SSP"
                                '''
                                # Execute the query and create a DataFrame
                                df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                                df_SSP_table = pd.read_sql_query(query_SSP, conn)
                                conn.close()

                                # convert SSP versioning to text type for joining and ask for a contract mod date as the new current date
                                mod_date = datetime.combine(qdate.toPython(), datetime.min.time())
                                df_prospective_changes['Current Period'] = mod_date
                                df_prospective_changes['SSP Version'] = df_prospective_changes['SSP Version'].astype(
                                    str)
                                df_prospective_changes['Contract Unique Name'] = df_prospective_changes[
                                    'Contract Unique Name'].astype(str)
                                df_prospective_changes['POB Unique ID'] = df_prospective_changes[
                                    'POB Unique ID'].astype(
                                    str)

                                # Perform left join on specified columns; keep the duplicate columns from the left table

                                # merge two dataframes by left join
                                df_prospective_changes_SSP = pd.merge(df_prospective_changes, df_SSP_table,
                                                                      on=['SKU Name', 'ASC 606 Stratification',
                                                                          'SSP Version'], how='left',
                                                                      indicator=True, suffixes=('', '_right_table'))

                                # error handling when the upload contract POBs doesn't match to any SKU
                                df_prospective_changes_SSP_left = df_prospective_changes_SSP.loc[
                                    df_prospective_changes_SSP[
                                        '_merge'] == 'left_only', df_prospective_changes_SSP.columns]

                                if not df_prospective_changes_SSP_left.empty:

                                    failed_list = ",".join(df_prospective_changes_SSP_left["SKU Name"].tolist())
                                    QMessageBox.information(self, "Mod Upload Failed",
                                                            f"Some Mod POBs are not matched with the existing SSP databse. Re-upload the file after fixes! \nPOB with issues: \n{failed_list}")
                                    raise Exception("The process is stopped for users to fix the file")

                                else:
                                    # Drop duplicate and unused _merged columns
                                    df_prospective_changes_SSP = df_prospective_changes_SSP.drop(
                                        columns=[col for col in df_prospective_changes_SSP.columns if
                                                 col.endswith(('_right_table'))])
                                    df_prospective_changes_SSP = df_prospective_changes_SSP.drop(
                                        columns=[col for col in df_prospective_changes_SSP.columns if
                                                 col.endswith(('_merge'))])

                                    # calculate SSP ranges for the prospective changes
                                    df_prospective_changes_SSP['Mod Midpoint SSP'] = df_prospective_changes_SSP[
                                                                                         'Mod Qty'] * \
                                                                                     df_prospective_changes_SSP[
                                                                                         'SKU Unit List Price'] * (
                                                                                             1 -
                                                                                             df_prospective_changes_SSP[
                                                                                                 'Midpoint Discount Percentage'])
                                    df_prospective_changes_SSP['Mod Lower_End SSP'] = df_prospective_changes_SSP[
                                                                                          'Mod Qty'] * \
                                                                                      df_prospective_changes_SSP[
                                                                                          'SKU Unit List Price'] * (
                                                                                              1 -
                                                                                              df_prospective_changes_SSP[
                                                                                                  'Midpoint Discount Percentage']) * (
                                                                                              1 -
                                                                                              df_prospective_changes_SSP[
                                                                                                  'SSP Range Method (+-)'])
                                    df_prospective_changes_SSP['Mod Higher_End SSP'] = df_prospective_changes_SSP[
                                                                                           'Mod Qty'] * \
                                                                                       df_prospective_changes_SSP[
                                                                                           'SKU Unit List Price'] * (
                                                                                               1 -
                                                                                               df_prospective_changes_SSP[
                                                                                                   'Midpoint Discount Percentage']) * (
                                                                                               1 +
                                                                                               df_prospective_changes_SSP[
                                                                                                   'SSP Range Method (+-)'])

                                    def compare_columns(row):
                                        if row['Mod Qty'] > 0:
                                            if row['Mod Billing'] > row['Mod Higher_End SSP']:
                                                return row['Mod Higher_End SSP']
                                            elif row['Mod Billing'] < row['Mod Lower_End SSP']:
                                                return row['Mod Lower_End SSP']
                                            else:
                                                return row['Mod Billing']
                                        else:
                                            if row['Mod Billing'] < row['Mod Higher_End SSP']:
                                                return row['Mod Higher_End SSP']
                                            elif row['Mod Billing'] > row['Mod Lower_End SSP']:
                                                return row['Mod Lower_End SSP']
                                            else:
                                                return row['Mod Billing']

                                    df_prospective_changes_SSP['Mod SSP Changes'] = df_prospective_changes_SSP.apply(
                                        compare_columns, axis=1)

                                    df_prospective_changes_SSP['Record Unique ID without time'] = \
                                        df_prospective_changes_SSP[
                                            'Contract Unique Name'] + " " + \
                                        df_prospective_changes_SSP[
                                            'POB Unique ID'] + " " + \
                                        df_prospective_changes_SSP[
                                            'SKU Name']

                                    # Retrieve the latest records for each unique ID
                                    # Convert the Timestamp field to datetime
                                    df_existing_contract['Processing Time Log'] = pd.to_datetime(
                                        df_existing_contract['Processing Time Log'])
                                    df_contract_live_latest = df_existing_contract.loc[
                                        df_existing_contract.groupby('Record Unique ID without time')[
                                            'Processing Time Log'].idxmax()]

                                    # Outer join the Contract_Live table's latest records and the prospective changes with SSP
                                    merged_df = df_contract_live_latest.merge(df_prospective_changes_SSP,
                                                                              on='Record Unique ID without time',
                                                                              how='outer', suffixes=('', '_new'))
                                    # check post join df
                                    # print(merged_df)
                                    # create a list to only show the contracts with mods
                                    result_contract_mod_unique_name = merged_df.loc[
                                        merged_df['Mod Qty'].notna() & merged_df[
                                            'Mod Billing'].notna(), 'Contract Unique Name']
                                    result_contract_mod_unique_name_list = result_contract_mod_unique_name.tolist()

                                    # Filter and replace the original DataFrame based on the list
                                    merged_df = merged_df.loc[
                                        merged_df['Contract Unique Name'].isin(result_contract_mod_unique_name_list)]

                                    # fill in the joined df
                                    merged_df['Contract Unique Name'] = merged_df['Contract Unique Name'].fillna(
                                        merged_df['Contract Unique Name_new'])
                                    merged_df['POB Unique ID'] = merged_df['POB Unique ID'].fillna(
                                        merged_df['POB Unique ID_new'])
                                    merged_df['SKU Name'] = merged_df['SKU Name'].fillna(merged_df['SKU Name_new'])
                                    # update the memo for the contract mods
                                    merged_df['Memo 1'] = merged_df['Memo 1_new'].fillna(merged_df['Memo 1'])
                                    merged_df['Memo 2'] = merged_df['Memo 2_new'].fillna(merged_df['Memo 2'])
                                    merged_df['Memo 3'] = merged_df['Memo 3_new'].fillna(merged_df['Memo 3'])
                                    # update the dates with mod dates
                                    merged_df['Mod Start Date'] = merged_df['Mod Start Date'].fillna(
                                        merged_df['POB Start Date'])
                                    merged_df['POB Start Date'] = merged_df['Mod Start Date']
                                    merged_df['Mod End Date'] = merged_df['Mod End Date'].fillna(
                                        merged_df['POB End Date'])
                                    merged_df['POB End Date'] = merged_df['Mod End Date']
                                    merged_df = merged_df.drop(columns=['Mod Start Date', 'Mod End Date'])

                                    # continue fill in the joined df
                                    merged_df['ASC 606 Stratification'] = merged_df['ASC 606 Stratification'].fillna(
                                        merged_df['ASC 606 Stratification_new'])
                                    merged_df['Selling Entity'] = merged_df['Selling Entity'].fillna(
                                        merged_df['Selling Entity_new'])
                                    merged_df['SSP Version'] = merged_df['SSP Version'].fillna(
                                        merged_df['SSP Version_new'])
                                    merged_df['Deferred Revenue Account'] = merged_df[
                                        'Deferred Revenue Account'].fillna(
                                        merged_df['Deferred Revenue Account_new'])
                                    merged_df['Unbilled A/R Account'] = merged_df[
                                        'Unbilled A/R Account'].fillna(
                                        merged_df['Unbilled A/R Account_new'])
                                    merged_df['Previous Period'] = merged_df['Current Period']
                                    merged_df['Current Period'] = mod_date
                                    merged_df['SKU Unique ID'] = merged_df['SKU Unique ID'].fillna(
                                        merged_df['SKU Unique ID_new'])
                                    merged_df['Distinct or Nondistinct'] = merged_df['Distinct or Nondistinct'].fillna(
                                        merged_df['Distinct or Nondistinct_new'])
                                    merged_df['SKU Unit List Price'] = merged_df['SKU Unit List Price'].fillna(
                                        merged_df['SKU Unit List Price_new'])
                                    merged_df['Midpoint Discount Percentage'] = merged_df[
                                        'Midpoint Discount Percentage'].fillna(
                                        merged_df['Midpoint Discount Percentage_new'])
                                    merged_df['SSP Range Method (+-)'] = merged_df['SSP Range Method (+-)'].fillna(
                                        merged_df['SSP Range Method (+-)_new'])
                                    merged_df['Revenue Account'] = merged_df['Revenue Account'].fillna(
                                        merged_df['Revenue Account_new'])

                                    # update previous fields
                                    merged_df['Previous Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0)
                                    merged_df['Previous Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0)
                                    merged_df['Previous Remaining Allocation'] = merged_df[
                                        'Current Remaining Allocation'].fillna(0)
                                    merged_df['Previous Remaining Billing'] = merged_df[
                                        'Current Remaining Billing'].fillna(0)
                                    merged_df['Previous Unit SSP'] = merged_df['Current Unit SSP'].fillna(0)
                                    merged_df['Previous Remaining Unit Rev Rec'] = merged_df[
                                        'Current Remaining Unit Rev Rec'].fillna(0)
                                    merged_df['Previous Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Previous Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Previous Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Previous Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Previous SSP Delivered - Cumulative'] = merged_df[
                                        'Current SSP Delivered - Cumulative'].fillna(0)
                                    merged_df['Previous Contract Position - POB'] = merged_df[
                                        'Current Contract Position - POB'].fillna(0)
                                    merged_df['Previous Contract Position - Contract Level'] = merged_df[
                                        'Current Contract Position - Contract Level'].fillna(0)
                                    merged_df["Previous Reclass to UAR"] = merged_df["Current Reclass to UAR"].fillna(0)

                                    # update current fields
                                    merged_df['Current Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0) + \
                                                                         merged_df['Mod Qty'].fillna(0)
                                    merged_df['Current Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0) + \
                                                                         merged_df[
                                                                             'Mod SSP Changes'].fillna(0)
                                    # in case the remaining SSP is reduced to below zero, make the zero as the minimum
                                    merged_df.loc[merged_df['Current Remaining SSP'] < 0, "Current Remaining SSP"] = 0

                                    merged_df['Current Remaining Allocation'] = (
                                            (merged_df.groupby('Contract Unique Name')[
                                                 'Current Remaining Allocation'].transform(
                                                'sum') + merged_df.groupby('Contract Unique Name')[
                                                 'Mod Billing'].transform('sum')) / \
                                            merged_df.groupby('Contract Unique Name')[
                                                'Current Remaining SSP'].transform('sum') * \
                                            merged_df['Current Remaining SSP']).fillna(0)
                                    merged_df['Current Remaining Billing'] = merged_df[
                                                                                 'Current Remaining Billing'].fillna(
                                        0) + \
                                                                             merged_df[
                                                                                 'Mod Billing'].fillna(0)
                                    merged_df['Current Unit SSP'] = (
                                            merged_df['Current Remaining SSP'].fillna(0) / merged_df[
                                        'Current Remaining Qty'].fillna(0)).fillna(0)
                                    merged_df['Current Remaining Unit Rev Rec'] = (merged_df[
                                                                                       'Current Remaining Allocation'].fillna(
                                        0) / merged_df[
                                                                                       'Current Remaining Qty'].fillna(
                                        0)).fillna(0)
                                    merged_df['Current Delivery'] = 0
                                    merged_df['Current Rev Rec'] = 0
                                    merged_df['Current Billing'] = 0
                                    merged_df['Current SSP Delivered'] = 0
                                    merged_df['Current Cumulative Catchup - Disclosure Only'] = 0
                                    merged_df['Current Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Current Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Current Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Current SSP Delivered - Cumulative'] = merged_df[
                                        'Current SSP Delivered - Cumulative'].fillna(0)
                                    merged_df['Current Contract Position - POB'] = merged_df[
                                                                                       'Current Billing - Cumulative'].fillna(
                                        0) - merged_df[
                                                                                       'Current Rev Rec - Cumulative'].fillna(
                                        0)
                                    merged_df["Current Contract Position - Contract Level"] = \
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    merged_df["Current Reclass to UAR"] = np.where(
                                        merged_df['Current Contract Position - Contract Level'] < 0,
                                        -merged_df['Current Contract Position - Contract Level'] /
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * merged_df['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    merged_df.loc[
                                        merged_df["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # update the records timestamp
                                    merged_df['Processing Time Log'] = pd.Timestamp.now()
                                    merged_df['Record Unique ID'] = merged_df['Processing Time Log'].astype(str) + " " + \
                                                                    merged_df[
                                                                        'Contract Unique Name'] + " " + merged_df[
                                                                        'POB Unique ID'] + " " + merged_df['SKU Name']

                                    # Drop unused _new columns
                                    merged_df = merged_df.drop(
                                        columns=[col for col in merged_df.columns if col.endswith(('_new'))])
                                    merged_df = merged_df.drop(
                                        columns=['Mod Billing', 'Mod Qty', 'Mod Midpoint SSP', 'Mod Lower_End SSP',
                                                 'Mod Higher_End SSP',
                                                 'Mod SSP Changes'])

                                    # Sort the DataFrame based on 'Record Unique ID without time'
                                    merged_df = merged_df.sort_values('Record Unique ID without time')

                                    # Filter the DataFrame based on the 'Distinct' column
                                    df_distinct = merged_df[merged_df['Distinct or Nondistinct'] == "Distinct"].copy()
                                    df_nondistinct = merged_df[
                                        merged_df['Distinct or Nondistinct'] == "Nondistinct"].copy()

                                    # calculate the cumulative catch-up for Nondistinct POBs
                                    df_nondistinct['Current Rev Rec - Cumulative Should Be'] = (df_nondistinct[
                                                                                                    'Current Delivery - Cumulative'] / (
                                                                                                        df_nondistinct[
                                                                                                            'Current Delivery - Cumulative'] +
                                                                                                        df_nondistinct[
                                                                                                            'Current Remaining Qty']) * (
                                                                                                        df_nondistinct[
                                                                                                            'Current Rev Rec - Cumulative'] +
                                                                                                        df_nondistinct[
                                                                                                            'Current Remaining Allocation'])).fillna(
                                        0)
                                    df_nondistinct['Current Cumulative Catchup - Disclosure Only'] = df_nondistinct[
                                                                                                         'Current Rev Rec - Cumulative Should Be'] - \
                                                                                                     df_nondistinct[
                                                                                                         'Current Rev Rec - Cumulative']
                                    df_nondistinct['Current Cumulative Catchup - Cumulative - Disclosure Only'] = \
                                        df_nondistinct['Current Cumulative Catchup - Cumulative - Disclosure Only'] + \
                                        df_nondistinct['Current Cumulative Catchup - Disclosure Only']
                                    # next step: add the 'current cumulative catch up' to Contract_Live
                                    df_nondistinct['Current Rev Rec'] = df_nondistinct[
                                        'Current Cumulative Catchup - Disclosure Only']
                                    df_nondistinct['Current Rev Rec - Cumulative'] = df_nondistinct[
                                                                                         'Current Rev Rec - Cumulative'].fillna(
                                        0) + df_nondistinct['Current Rev Rec']
                                    df_nondistinct['Current Remaining Allocation'] = df_nondistinct[
                                                                                         'Current Remaining Allocation'] - \
                                                                                     df_nondistinct['Current Rev Rec']
                                    df_nondistinct['Current Remaining Unit Rev Rec'] = (df_nondistinct[
                                                                                            'Current Remaining Allocation'].fillna(
                                        0) / df_nondistinct[
                                                                                            'Current Remaining Qty'].fillna(
                                        0)).fillna(0)
                                    df_nondistinct['Current Contract Position - POB'] = df_nondistinct[
                                                                                            'Current Billing - Cumulative'].fillna(
                                        0) - df_nondistinct[
                                                                                            'Current Rev Rec - Cumulative'].fillna(
                                        0)

                                    # the recalculation below is not complete and will be overwritten by the complete contract level recalculation later
                                    df_nondistinct["Current Contract Position - Contract Level"] = \
                                        df_nondistinct.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    df_nondistinct["Current Reclass to UAR"] = np.where(
                                        df_nondistinct['Current Contract Position - Contract Level'] < 0,
                                        -df_nondistinct['Current Contract Position - Contract Level'] /
                                        df_nondistinct.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * df_nondistinct['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    df_nondistinct.loc[
                                        df_nondistinct["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # drop the nondistinct POB's 'Current Rev Rec - Cumulative Should Be'
                                    df_nondistinct = df_nondistinct.drop(
                                        columns='Current Rev Rec - Cumulative Should Be')

                                    # Concatenate the two DataFrames vertically
                                    prospective_completed_df = pd.concat([df_distinct, df_nondistinct],
                                                                         ignore_index=True)
                                    # reset contract level position after the nondistinct's refresh
                                    prospective_completed_df["Current Contract Position - Contract Level"] = \
                                        prospective_completed_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    prospective_completed_df["Current Reclass to UAR"] = np.where(
                                        prospective_completed_df['Current Contract Position - Contract Level'] < 0,
                                        -prospective_completed_df['Current Contract Position - Contract Level'] /
                                        prospective_completed_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * prospective_completed_df['Current SSP Delivered - Cumulative'], 0)
                                    # Sort the DataFrame based on 'Record Unique ID without time'
                                    prospective_completed_df = prospective_completed_df.sort_values(
                                        'Record Unique ID without time')

                                    # add another validation to make sure the current delivery if negative,
                                    # doesn't cause the total delivery cumulative to be negative

                                    if (prospective_completed_df["Current Remaining Qty"] < 0).any() or (
                                            prospective_completed_df[
                                                prospective_completed_df["ASC 606 Stratification"] != "VC"][
                                                'Current Remaining Billing'] < 0).any():
                                        QMessageBox.information(self, "Mod Failed",
                                                                "Qty or Price modified cannot reduce the remaining qty or remaining billing to negative. Check your uploads please.")
                                        raise Exception("The process is stopped for users to fix the file")

                                    else:
                                        # check in incremental data if table exists; if not create the table
                                        conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                        cur = conn.cursor()
                                        cur.execute(
                                            "SELECT name FROM sqlite_master WHERE type='table' AND name='Contract_Live'")
                                        table_exists = bool(cur.fetchone())
                                        # Close the cursor and connection
                                        cur.close()
                                        conn.close()
                                        # insert incremental if exists
                                        if table_exists:
                                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # query = f'''
                                            #    SELECT *
                                            #    FROM "Contract_Live"
                                            #    '''
                                            # Execute the query and create a DataFrame
                                            # df_contract_live = pd.read_sql_query(query, conn)
                                            # conn.close()
                                            # Filter the pandas DataFrame to include only incremental data
                                            # incremental_data = prospective_completed_df[
                                            #    ~prospective_completed_df['Record Unique ID'].isin(
                                            #        df_contract_live['Record Unique ID'])]
                                            # Insert the incremental data into the SQL table
                                            # conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # incremental_data.to_sql("Contract_Live", conn, if_exists="append",
                                            #                        index=False)
                                            prospective_completed_df.to_sql("Contract_Live", conn, if_exists="append",
                                                                            index=False)
                                            conn.close()
                                            QMessageBox.information(self, "Mod Success",
                                                                    "Prospective Mod has been processed with uploaded modifications for the current date :)")
                                        else:
                                            # create Contract_Live table
                                            raise Exception("No contract table is found!")
        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_RetroMod(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        try:
            if file_path:
                input_text, ok = QInputDialog.getText(self, "Date Input",
                                                      f"Enter the retrospective contract mod date in this format (YYYY-MM-DD):")
                if ok:
                    qdate = QDate.fromString(input_text, "yyyy-MM-dd")
                    if not qdate.isValid():
                        QMessageBox.warning(self, "Invalid Date",
                                            "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                    else:
                        # message = f"The following date is set for the retrospective contract modification: {qdate.toString('yyyy-MM-dd')}"
                        # QMessageBox.information(self, "Date Selected", message)
                        # Operation
                        df_retrospective_changes = pd.read_excel(file_path)
                        # build validation here:
                        expected_titles = ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'Mod Start Date',
                                           'Mod End Date', 'ASC 606 Stratification', 'Mod Billing', 'Mod Qty',
                                           'Selling Entity', 'Deferred Revenue Account',
                                           'Unbilled A/R Account', 'SSP Version', 'Memo 1', 'Memo 2',
                                           'Memo 3']  # Specify the expected column titles
                        actual_titles = df_retrospective_changes.columns.tolist()  # Get the actual column titles as a list
                        missing_titles = [title for title in expected_titles if title not in actual_titles]
                        extra_titles = [title for title in actual_titles if title not in expected_titles]
                        numbers_to_validate = ['Mod Billing',
                                               'Mod Qty']  # Specify the columns to validate as numbers
                        # error handling the missing and extra fields
                        if missing_titles or extra_titles:
                            QMessageBox.information(self, "File Upload Error",
                                                    "Error: The Excel file has incorrect or missing column titles.")
                            if missing_titles:
                                QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                            if extra_titles:
                                QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                        else:
                            # Additional error handling or validation logic can be implemented here
                            stop_process = False  # Flag variable to control the loop
                            for column in numbers_to_validate:
                                if stop_process:
                                    break  # Exit the loop if the flag is set to True
                                try:
                                    pd.to_numeric(df_retrospective_changes[column], errors='raise')
                                    # check pd to numeric values
                                    # print(df_retrospective_changes[column])
                                    if df_retrospective_changes[column].isna().any():
                                        QMessageBox.information(self, "Format Error",
                                                                f"Error: The column '{column}' should contain numeric values.")
                                        stop_process = True  # Set the flag to True to skip the remaining iterations
                                except (ValueError, TypeError):
                                    QMessageBox.information(self, "Format Error",
                                                            f"Error: The column '{column}' should contain numeric values.")
                                    stop_process = True  # Set the flag to True to skip the remaining iterations
                            if not stop_process:
                                conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                query_existing_contract = '''
                                    SELECT t1.*
                                    FROM Contract_Live t1
                                    JOIN (
                                        SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                        FROM Contract_Live
                                        GROUP BY "Record Unique ID without time"
                                    ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                '''
                                query_SSP = '''
                                    SELECT * FROM "SKU_SSP"
                                    '''
                                # Execute the query and create a DataFrame
                                df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                                df_SSP_table = pd.read_sql_query(query_SSP, conn)
                                conn.close()

                                # convert SSP versioning to text type for joining and ask for a contract mod date as the new current date
                                mod_date = datetime.combine(qdate.toPython(), datetime.min.time())
                                df_retrospective_changes['Current Period'] = mod_date
                                df_retrospective_changes['SSP Version'] = df_retrospective_changes[
                                    'SSP Version'].astype(
                                    str)
                                df_retrospective_changes['Contract Unique Name'] = df_retrospective_changes[
                                    'Contract Unique Name'].astype(str)
                                df_retrospective_changes['POB Unique ID'] = df_retrospective_changes[
                                    'POB Unique ID'].astype(str)

                                # Perform left join on specified columns; keep the duplicate columns from the left table

                                # merge two dataframes by left join
                                df_retrospective_changes_SSP = pd.merge(df_retrospective_changes, df_SSP_table,
                                                                        on=['SKU Name', 'ASC 606 Stratification',
                                                                            'SSP Version'], how='left',
                                                                        indicator=True, suffixes=('', '_right_table'))

                                # error handling when the upload contract POBs doesn't match to any SKU
                                df_retrospective_changes_left = df_retrospective_changes_SSP.loc[
                                    df_retrospective_changes_SSP[
                                        '_merge'] == 'left_only', df_retrospective_changes_SSP.columns]

                                if not df_retrospective_changes_left.empty:

                                    failed_list = ",".join(df_retrospective_changes_left["SKU Name"].tolist())
                                    QMessageBox.information(self, "Mod Upload Failed",
                                                            f"Some Mod POBs are not matched with the existing SSP databse. Re-upload the file after fixes! \nPOB with issues: \n{failed_list}")
                                    raise Exception("The process is stopped for users to fix the file")

                                else:
                                    # Drop duplicate and unused _merged columns
                                    df_retrospective_changes_SSP = df_retrospective_changes_SSP.drop(
                                        columns=[col for col in df_retrospective_changes_SSP.columns if
                                                 col.endswith(('_right_table'))])
                                    df_retrospective_changes_SSP = df_retrospective_changes_SSP.drop(
                                        columns=[col for col in df_retrospective_changes_SSP.columns if
                                                 col.endswith(('_merge'))])

                                    # calculate SSP ranges for the retrospective changes
                                    df_retrospective_changes_SSP['Mod Midpoint SSP'] = df_retrospective_changes_SSP[
                                                                                           'Mod Qty'] * \
                                                                                       df_retrospective_changes_SSP[
                                                                                           'SKU Unit List Price'] * (1 -
                                                                                                                     df_retrospective_changes_SSP[
                                                                                                                         'Midpoint Discount Percentage'])
                                    df_retrospective_changes_SSP['Mod Lower_End SSP'] = df_retrospective_changes_SSP[
                                                                                            'Mod Qty'] * \
                                                                                        df_retrospective_changes_SSP[
                                                                                            'SKU Unit List Price'] * (
                                                                                                1 -
                                                                                                df_retrospective_changes_SSP[
                                                                                                    'Midpoint Discount Percentage']) * (
                                                                                                1 -
                                                                                                df_retrospective_changes_SSP[
                                                                                                    'SSP Range Method (+-)'])
                                    df_retrospective_changes_SSP['Mod Higher_End SSP'] = df_retrospective_changes_SSP[
                                                                                             'Mod Qty'] * \
                                                                                         df_retrospective_changes_SSP[
                                                                                             'SKU Unit List Price'] * (
                                                                                                 1 -
                                                                                                 df_retrospective_changes_SSP[
                                                                                                     'Midpoint Discount Percentage']) * (
                                                                                                 1 +
                                                                                                 df_retrospective_changes_SSP[
                                                                                                     'SSP Range Method (+-)'])

                                    def compare_columns(row):
                                        if row['Mod Qty'] > 0:
                                            if row['Mod Billing'] > row['Mod Higher_End SSP']:
                                                return row['Mod Higher_End SSP']
                                            elif row['Mod Billing'] < row['Mod Lower_End SSP']:
                                                return row['Mod Lower_End SSP']
                                            else:
                                                return row['Mod Billing']
                                        else:
                                            if row['Mod Billing'] < row['Mod Higher_End SSP']:
                                                return row['Mod Higher_End SSP']
                                            elif row['Mod Billing'] > row['Mod Lower_End SSP']:
                                                return row['Mod Lower_End SSP']
                                            else:
                                                return row['Mod Billing']

                                    df_retrospective_changes_SSP[
                                        'Mod SSP Changes'] = df_retrospective_changes_SSP.apply(
                                        compare_columns, axis=1)

                                    df_retrospective_changes_SSP['Record Unique ID without time'] = \
                                        df_retrospective_changes_SSP[
                                            'Contract Unique Name'] + " " + \
                                        df_retrospective_changes_SSP['POB Unique ID'] + " " + \
                                        df_retrospective_changes_SSP['SKU Name']

                                    # Retrieve the latest records for each unique ID
                                    # Convert the Timestamp field to datetime
                                    df_existing_contract['Processing Time Log'] = pd.to_datetime(
                                        df_existing_contract['Processing Time Log'])
                                    df_contract_live_latest = df_existing_contract.loc[
                                        df_existing_contract.groupby('Record Unique ID without time')[
                                            'Processing Time Log'].idxmax()]

                                    # Outer join the Contract_Live table's latest records and the retrospective changes with SSP
                                    merged_df = df_contract_live_latest.merge(df_retrospective_changes_SSP,
                                                                              on='Record Unique ID without time',
                                                                              how='outer', suffixes=('', '_new'))

                                    # check post join df
                                    # print(merged_df)
                                    # create a list to only show the contracts with mods
                                    result_contract_mod_unique_name = merged_df.loc[
                                        merged_df['Mod Qty'].notna() & merged_df[
                                            'Mod Billing'].notna(), 'Contract Unique Name']
                                    result_contract_mod_unique_name_list = result_contract_mod_unique_name.tolist()

                                    # Filter and replace the original DataFrame based on the list
                                    merged_df = merged_df.loc[
                                        merged_df['Contract Unique Name'].isin(result_contract_mod_unique_name_list)]

                                    # fill in the joined df
                                    merged_df['Contract Unique Name'] = merged_df['Contract Unique Name'].fillna(
                                        merged_df['Contract Unique Name_new'])
                                    merged_df['POB Unique ID'] = merged_df['POB Unique ID'].fillna(
                                        merged_df['POB Unique ID_new'])
                                    merged_df['SKU Name'] = merged_df['SKU Name'].fillna(merged_df['SKU Name_new'])
                                    # update the memo for the contract mods
                                    merged_df['Memo 1'] = merged_df['Memo 1_new'].fillna(merged_df['Memo 1'])
                                    merged_df['Memo 2'] = merged_df['Memo 2_new'].fillna(merged_df['Memo 2'])
                                    merged_df['Memo 3'] = merged_df['Memo 3_new'].fillna(merged_df['Memo 3'])
                                    # update the dates with mod dates
                                    merged_df['Mod Start Date'] = merged_df['Mod Start Date'].fillna(
                                        merged_df['POB Start Date'])
                                    merged_df['POB Start Date'] = merged_df['Mod Start Date']
                                    merged_df['Mod End Date'] = merged_df['Mod End Date'].fillna(
                                        merged_df['POB End Date'])
                                    merged_df['POB End Date'] = merged_df['Mod End Date']
                                    merged_df = merged_df.drop(columns=['Mod Start Date', 'Mod End Date'])

                                    # continue fill in the joined df
                                    merged_df['ASC 606 Stratification'] = merged_df['ASC 606 Stratification'].fillna(
                                        merged_df['ASC 606 Stratification_new'])
                                    merged_df['Selling Entity'] = merged_df['Selling Entity'].fillna(
                                        merged_df['Selling Entity_new'])
                                    merged_df['SSP Version'] = merged_df['SSP Version'].fillna(
                                        merged_df['SSP Version_new'])
                                    merged_df['Deferred Revenue Account'] = merged_df[
                                        'Deferred Revenue Account'].fillna(
                                        merged_df['Deferred Revenue Account_new'])
                                    merged_df['Unbilled A/R Account'] = merged_df[
                                        'Unbilled A/R Account'].fillna(
                                        merged_df['Unbilled A/R Account_new'])
                                    merged_df['Previous Period'] = merged_df['Current Period']
                                    merged_df['Current Period'] = mod_date
                                    merged_df['SKU Unique ID'] = merged_df['SKU Unique ID'].fillna(
                                        merged_df['SKU Unique ID_new'])
                                    merged_df['Distinct or Nondistinct'] = merged_df['Distinct or Nondistinct'].fillna(
                                        merged_df['Distinct or Nondistinct_new'])
                                    merged_df['SKU Unit List Price'] = merged_df['SKU Unit List Price'].fillna(
                                        merged_df['SKU Unit List Price_new'])
                                    merged_df['Midpoint Discount Percentage'] = merged_df[
                                        'Midpoint Discount Percentage'].fillna(
                                        merged_df['Midpoint Discount Percentage_new'])
                                    merged_df['SSP Range Method (+-)'] = merged_df['SSP Range Method (+-)'].fillna(
                                        merged_df['SSP Range Method (+-)_new'])
                                    merged_df['Revenue Account'] = merged_df['Revenue Account'].fillna(
                                        merged_df['Revenue Account_new'])

                                    # update previous fields
                                    merged_df['Previous Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0)
                                    merged_df['Previous Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0)
                                    merged_df['Previous Remaining Allocation'] = merged_df[
                                        'Current Remaining Allocation'].fillna(0)
                                    merged_df['Previous Remaining Billing'] = merged_df[
                                        'Current Remaining Billing'].fillna(0)
                                    merged_df['Previous Unit SSP'] = merged_df['Current Unit SSP'].fillna(0)
                                    merged_df['Previous Remaining Unit Rev Rec'] = merged_df[
                                        'Current Remaining Unit Rev Rec'].fillna(0)
                                    merged_df['Previous Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Previous Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Previous Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Previous Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Previous SSP Delivered - Cumulative'] = merged_df[
                                        'Current SSP Delivered - Cumulative'].fillna(0)
                                    merged_df['Previous Contract Position - POB'] = merged_df[
                                        'Current Contract Position - POB'].fillna(0)
                                    merged_df['Previous Contract Position - Contract Level'] = merged_df[
                                        'Current Contract Position - Contract Level'].fillna(0)
                                    merged_df["Previous Reclass to UAR"] = merged_df["Current Reclass to UAR"].fillna(0)

                                    # update current fields
                                    merged_df['Current Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0) + \
                                                                         merged_df['Mod Qty'].fillna(0)
                                    merged_df['Current Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0) + \
                                                                         merged_df[
                                                                             'Mod SSP Changes'].fillna(0)
                                    # in case the remaining SSP is reduced to below zero, make the zero as the minimum
                                    merged_df.loc[merged_df['Current Remaining SSP'] < 0, "Current Remaining SSP"] = 0

                                    # calculate current remaining allocation based on SSP undelivered after the entire retrospective re-allocation based on the total SSPs
                                    merged_df['Current Remaining Allocation'] = ((merged_df.groupby(
                                        'Contract Unique Name')[
                                                                                      'Current Remaining Allocation'].transform(
                                        'sum') + merged_df.groupby('Contract Unique Name')[
                                                                                      'Mod Billing'].transform('sum') +
                                                                                  merged_df.groupby(
                                                                                      'Contract Unique Name')[
                                                                                      'Current Rev Rec - Cumulative'].transform(
                                                                                      'sum')) / (merged_df.groupby(
                                        'Contract Unique Name')['Current Remaining SSP'].transform('sum') +
                                                                                                 merged_df.groupby(
                                                                                                     'Contract Unique Name')[
                                                                                                     'Previous SSP Delivered - Cumulative'].transform(
                                                                                                     'sum')) * (
                                                                                         merged_df[
                                                                                             'Current Remaining SSP'] +
                                                                                         merged_df[
                                                                                             'Previous SSP Delivered - Cumulative'])).fillna(
                                        0) - merged_df['Previous Rev Rec - Cumulative']

                                    merged_df['Current Remaining Billing'] = merged_df[
                                                                                 'Current Remaining Billing'].fillna(
                                        0) + \
                                                                             merged_df[
                                                                                 'Mod Billing'].fillna(0)
                                    merged_df['Current Unit SSP'] = (
                                            merged_df['Current Remaining SSP'].fillna(0) / merged_df[
                                        'Current Remaining Qty'].fillna(0)).fillna(0)
                                    merged_df['Current Remaining Unit Rev Rec'] = (merged_df[
                                                                                       'Current Remaining Allocation'].fillna(
                                        0) / merged_df[
                                                                                       'Current Remaining Qty'].fillna(
                                        0)).fillna(0)
                                    merged_df['Current Delivery'] = 0
                                    merged_df['Current Rev Rec'] = 0
                                    merged_df['Current Billing'] = 0
                                    merged_df['Current Cumulative Catchup - Disclosure Only'] = 0
                                    merged_df['Current Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Current Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Current Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Current Contract Position - POB'] = merged_df[
                                                                                       'Current Billing - Cumulative'].fillna(
                                        0) - merged_df[
                                                                                       'Current Rev Rec - Cumulative'].fillna(
                                        0)
                                    merged_df["Current Contract Position - Contract Level"] = \
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    merged_df["Current Reclass to UAR"] = np.where(
                                        merged_df['Current Contract Position - Contract Level'] < 0,
                                        -merged_df['Current Contract Position - Contract Level'] /
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * merged_df['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    merged_df.loc[
                                        merged_df["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # update the records timestamp
                                    merged_df['Processing Time Log'] = pd.Timestamp.now()
                                    merged_df['Record Unique ID'] = merged_df['Processing Time Log'].astype(str) + " " + \
                                                                    merged_df[
                                                                        'Contract Unique Name'] + " " + merged_df[
                                                                        'POB Unique ID'] + " " + merged_df['SKU Name']

                                    # Drop unused _new columns
                                    merged_df = merged_df.drop(
                                        columns=[col for col in merged_df.columns if col.endswith(('_new'))])
                                    merged_df = merged_df.drop(
                                        columns=['Mod Billing', 'Mod Qty', 'Mod Midpoint SSP', 'Mod Lower_End SSP',
                                                 'Mod Higher_End SSP',
                                                 'Mod SSP Changes'])

                                    # calculate the cumulative catch-up for the retrospective changes
                                    # merged_df['Current Rev Rec - Cumulative Should Be'] = (merged_df[
                                    #                                                          'Current Remaining Allocation'] / \
                                    #                                                      merged_df['Current Remaining SSP'] * \
                                    #                                                      merged_df[
                                    #                                                          'Previous SSP Delivered - Cumulative']).fillna(0)
                                    # print(merged_df['Current Rev Rec - Cumulative Should Be'])

                                    # re-write merged_df['Current Rev Rec - Cumulative Should Be'] with the total allocation and total SSPs
                                    merged_df['Current Rev Rec - Cumulative Should Be'] = (
                                            (merged_df['Current Remaining Allocation'] + merged_df[
                                                'Current Rev Rec - Cumulative']) / (
                                                    merged_df['Current Remaining SSP'] + merged_df[
                                                'Previous SSP Delivered - Cumulative']) * merged_df[
                                                'Previous SSP Delivered - Cumulative']).fillna(0)

                                    merged_df['Current Cumulative Catchup - Disclosure Only'] = merged_df[
                                                                                                    'Current Rev Rec - Cumulative Should Be'] - \
                                                                                                merged_df[
                                                                                                    'Current Rev Rec - Cumulative']
                                    merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                                                                                                 'Current Cumulative Catchup - Cumulative - Disclosure Only'] + \
                                                                                                             merged_df[
                                                                                                                 'Current Cumulative Catchup - Disclosure Only']
                                    # next step: add the 'current cumulative catch up' to Contract_Live
                                    merged_df['Current Rev Rec'] = merged_df[
                                        'Current Cumulative Catchup - Disclosure Only'].fillna(0)
                                    merged_df['Current Rev Rec - Cumulative'] = merged_df[
                                                                                    'Current Rev Rec - Cumulative'].fillna(
                                        0) + \
                                                                                merged_df['Current Rev Rec']

                                    # print(merged_df['Current Cumulative Catchup - Disclosure Only'])
                                    # update current remaining allocation after the cumulative catchup
                                    merged_df['Current Remaining Allocation'] = (
                                            merged_df['Current Remaining Allocation'] - merged_df[
                                        'Current Rev Rec']).fillna(0)

                                    merged_df['Current Remaining Unit Rev Rec'] = (merged_df[
                                                                                       'Current Remaining Allocation'].fillna(
                                        0) / \
                                                                                   merged_df[
                                                                                       'Current Remaining Qty'].fillna(
                                                                                       0)).fillna(0)
                                    merged_df['Current Contract Position - POB'] = merged_df[
                                                                                       'Current Billing - Cumulative'].fillna(
                                        0) - \
                                                                                   merged_df[
                                                                                       'Current Rev Rec - Cumulative'].fillna(
                                                                                       0)
                                    merged_df["Current Contract Position - Contract Level"] = \
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    merged_df["Current Reclass to UAR"] = np.where(
                                        merged_df['Current Contract Position - Contract Level'] < 0,
                                        -merged_df['Current Contract Position - Contract Level'] /
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * merged_df['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    merged_df.loc[
                                        merged_df["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # drop the nondistinct POB's 'Current Rev Rec - Cumulative Should Be'
                                    merged_df = merged_df.drop(columns='Current Rev Rec - Cumulative Should Be')

                                    # Sort the DataFrame based on 'Record Unique ID without time'
                                    merged_df = merged_df.sort_values('Record Unique ID without time')

                                    # add another validation to make sure the current delivery if negative,
                                    # doesn't cause the total delivery cumulative to be negative

                                    if (merged_df["Current Remaining Qty"] < 0).any() or (
                                            merged_df[merged_df["ASC 606 Stratification"] != "VC"][
                                                'Current Remaining Billing'] < 0).any():
                                        QMessageBox.information(self, "Mod Failed",
                                                                "Qty or Price modified cannot reduce the remaining qty or remaining billing to negative. Check your uploads please.")
                                        raise Exception("The process is stopped for users to fix the file")

                                    else:
                                        # check in incremental data if table exists; if not create the table
                                        conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                        cur = conn.cursor()
                                        cur.execute(
                                            "SELECT name FROM sqlite_master WHERE type='table' AND name='Contract_Live'")
                                        table_exists = bool(cur.fetchone())
                                        # Close the cursor and connection
                                        cur.close()
                                        conn.close()
                                        # insert incremental if exists
                                        if table_exists:
                                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # query = f'''
                                            #    SELECT *
                                            #    FROM "Contract_Live"
                                            #    '''
                                            # Execute the query and create a DataFrame
                                            # df_contract_live = pd.read_sql_query(query, conn)
                                            # conn.close()
                                            # Filter the pandas DataFrame to include only incremental data
                                            # incremental_data = merged_df[
                                            #    ~merged_df['Record Unique ID'].isin(
                                            #        df_contract_live['Record Unique ID'])]
                                            # Insert the incremental data into the SQL table
                                            # conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # incremental_data.to_sql("Contract_Live", conn, if_exists="append",
                                            #                        index=False)
                                            merged_df.to_sql("Contract_Live", conn, if_exists="append", index=False)
                                            conn.close()
                                            QMessageBox.information(self, "Mod Success",
                                                                    "Retrospective Mod has been processed with uploaded modifications for the current date :)")
                                        else:
                                            # create Contract_Live table
                                            raise Exception("No contract table is found!")
        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def browse_file_POB_specific_VC(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        try:
            if file_path:
                input_text, ok = QInputDialog.getText(self, "Date Input",
                                                      f"Enter the retrospective contract mod date in this format (YYYY-MM-DD):")
                if ok:
                    qdate = QDate.fromString(input_text, "yyyy-MM-dd")
                    if not qdate.isValid():
                        QMessageBox.warning(self, "Invalid Date",
                                            "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                    else:
                        # message = f"The following date is set for the retrospective contract modification: {qdate.toString('yyyy-MM-dd')}"
                        # QMessageBox.information(self, "Date Selected", message)
                        # Operation
                        df_retrospective_changes = pd.read_excel(file_path)
                        # build validation here:
                        expected_titles = ['Contract Unique Name', 'POB Unique ID', 'SKU Name', 'Mod Start Date',
                                           'Mod End Date', 'ASC 606 Stratification', 'Mod Billing', 'Mod Qty',
                                           'Selling Entity', 'Deferred Revenue Account',
                                           'Unbilled A/R Account', 'SSP Version', 'Memo 1', 'Memo 2',
                                           'Memo 3']  # Specify the expected column titles
                        actual_titles = df_retrospective_changes.columns.tolist()  # Get the actual column titles as a list
                        missing_titles = [title for title in expected_titles if title not in actual_titles]
                        extra_titles = [title for title in actual_titles if title not in expected_titles]
                        numbers_to_validate = ['Mod Billing',
                                               'Mod Qty']  # Specify the columns to validate as numbers
                        # error handling the missing and extra fields
                        if missing_titles or extra_titles:
                            QMessageBox.information(self, "File Upload Error",
                                                    "Error: The Excel file has incorrect or missing column titles.")
                            if missing_titles:
                                QMessageBox.information(self, "Missing fields:", ", ".join(missing_titles))
                            if extra_titles:
                                QMessageBox.information(self, "Extra fields:", ", ".join(extra_titles))
                        else:
                            # Additional error handling or validation logic can be implemented here
                            stop_process = False  # Flag variable to control the loop
                            for column in numbers_to_validate:
                                if stop_process:
                                    break  # Exit the loop if the flag is set to True
                                try:
                                    pd.to_numeric(df_retrospective_changes[column], errors='raise')
                                    # check pd to numeric values
                                    # print(df_retrospective_changes[column])
                                    if df_retrospective_changes[column].isna().any():
                                        QMessageBox.information(self, "Format Error",
                                                                f"Error: The column '{column}' should contain numeric values.")
                                        stop_process = True  # Set the flag to True to skip the remaining iterations
                                except (ValueError, TypeError):
                                    QMessageBox.information(self, "Format Error",
                                                            f"Error: The column '{column}' should contain numeric values.")
                                    stop_process = True  # Set the flag to True to skip the remaining iterations
                            if not stop_process:
                                conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                query_existing_contract = '''
                                    SELECT t1.*
                                    FROM Contract_Live t1
                                    JOIN (
                                        SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                        FROM Contract_Live
                                        GROUP BY "Record Unique ID without time"
                                    ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                '''
                                query_SSP = '''
                                    SELECT * FROM "SKU_SSP"
                                    '''
                                # Execute the query and create a DataFrame
                                df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                                df_SSP_table = pd.read_sql_query(query_SSP, conn)
                                conn.close()

                                # convert SSP versioning to text type for joining and ask for a contract mod date as the new current date
                                mod_date = datetime.combine(qdate.toPython(), datetime.min.time())
                                df_retrospective_changes['Current Period'] = mod_date
                                df_retrospective_changes['SSP Version'] = df_retrospective_changes[
                                    'SSP Version'].astype(
                                    str)
                                df_retrospective_changes['Contract Unique Name'] = df_retrospective_changes[
                                    'Contract Unique Name'].astype(str)
                                df_retrospective_changes['POB Unique ID'] = df_retrospective_changes[
                                    'POB Unique ID'].astype(str)

                                # Perform left join on specified columns; keep the duplicate columns from the left table

                                # merge two dataframes by left join
                                df_retrospective_changes_SSP = pd.merge(df_retrospective_changes, df_SSP_table,
                                                                        on=['SKU Name', 'ASC 606 Stratification',
                                                                            'SSP Version'], how='left',
                                                                        indicator=True, suffixes=('', '_right_table'))

                                # error handling when the upload contract POBs doesn't match to any SKU
                                df_retrospective_changes_left = df_retrospective_changes_SSP.loc[
                                    df_retrospective_changes_SSP[
                                        '_merge'] == 'left_only', df_retrospective_changes_SSP.columns]

                                if not df_retrospective_changes_left.empty:

                                    failed_list = ",".join(df_retrospective_changes_left["SKU Name"].tolist())
                                    QMessageBox.information(self, "Mod Upload Failed",
                                                            f"Some Mod POBs are not matched with the existing SSP databse. Re-upload the file after fixes! \nPOB with issues: \n{failed_list}")
                                    raise Exception("The process is stopped for users to fix the file")

                                else:
                                    # Drop duplicate and unused _merged columns
                                    df_retrospective_changes_SSP = df_retrospective_changes_SSP.drop(
                                        columns=[col for col in df_retrospective_changes_SSP.columns if
                                                 col.endswith(('_right_table'))])
                                    df_retrospective_changes_SSP = df_retrospective_changes_SSP.drop(
                                        columns=[col for col in df_retrospective_changes_SSP.columns if
                                                 col.endswith(('_merge'))])

                                    df_retrospective_changes_SSP[
                                        'Mod SSP Changes'] = 0

                                    df_retrospective_changes_SSP['Record Unique ID without time'] = \
                                        df_retrospective_changes_SSP[
                                            'Contract Unique Name'] + " " + \
                                        df_retrospective_changes_SSP['POB Unique ID'] + " " + \
                                        df_retrospective_changes_SSP['SKU Name']

                                    # Retrieve the latest records for each unique ID
                                    # Convert the Timestamp field to datetime
                                    df_existing_contract['Processing Time Log'] = pd.to_datetime(
                                        df_existing_contract['Processing Time Log'])
                                    df_contract_live_latest = df_existing_contract.loc[
                                        df_existing_contract.groupby('Record Unique ID without time')[
                                            'Processing Time Log'].idxmax()]

                                    # Outer join the Contract_Live table's latest records and the retrospective changes with SSP
                                    merged_df = df_contract_live_latest.merge(df_retrospective_changes_SSP,
                                                                              on='Record Unique ID without time',
                                                                              how='outer', suffixes=('', '_new'))

                                    # check post join df
                                    # print(merged_df)
                                    # create a list to only show the contracts with mods
                                    result_contract_mod_unique_name = merged_df.loc[
                                        merged_df['Mod Qty'].notna() & merged_df[
                                            'Mod Billing'].notna(), 'Contract Unique Name']
                                    result_contract_mod_unique_name_list = result_contract_mod_unique_name.tolist()

                                    # Filter and replace the original DataFrame based on the list
                                    merged_df = merged_df.loc[
                                        merged_df['Contract Unique Name'].isin(result_contract_mod_unique_name_list)]

                                    # fill in the joined df
                                    merged_df['Contract Unique Name'] = merged_df['Contract Unique Name'].fillna(
                                        merged_df['Contract Unique Name_new'])
                                    merged_df['POB Unique ID'] = merged_df['POB Unique ID'].fillna(
                                        merged_df['POB Unique ID_new'])
                                    merged_df['SKU Name'] = merged_df['SKU Name'].fillna(merged_df['SKU Name_new'])

                                    # update the memo for the contract mods
                                    merged_df['Memo 1'] = merged_df['Memo 1_new'].fillna(merged_df['Memo 1'])
                                    merged_df['Memo 2'] = merged_df['Memo 2_new'].fillna(merged_df['Memo 2'])
                                    merged_df['Memo 3'] = merged_df['Memo 3_new'].fillna(merged_df['Memo 3'])

                                    # update the dates with mod dates
                                    merged_df['Mod Start Date'] = merged_df['Mod Start Date'].fillna(
                                        merged_df['POB Start Date'])
                                    merged_df['POB Start Date'] = merged_df['Mod Start Date']
                                    merged_df['Mod End Date'] = merged_df['Mod End Date'].fillna(
                                        merged_df['POB End Date'])
                                    merged_df['POB End Date'] = merged_df['Mod End Date']
                                    merged_df = merged_df.drop(columns=['Mod Start Date', 'Mod End Date'])

                                    # continue fill in the joined df
                                    merged_df['ASC 606 Stratification'] = merged_df['ASC 606 Stratification'].fillna(
                                        merged_df['ASC 606 Stratification_new'])
                                    merged_df['Selling Entity'] = merged_df['Selling Entity'].fillna(
                                        merged_df['Selling Entity_new'])
                                    merged_df['SSP Version'] = merged_df['SSP Version'].fillna(
                                        merged_df['SSP Version_new'])
                                    merged_df['Deferred Revenue Account'] = merged_df[
                                        'Deferred Revenue Account'].fillna(
                                        merged_df['Deferred Revenue Account_new'])
                                    merged_df['Unbilled A/R Account'] = merged_df[
                                        'Unbilled A/R Account'].fillna(
                                        merged_df['Unbilled A/R Account_new'])
                                    merged_df['Previous Period'] = merged_df['Current Period']
                                    merged_df['Current Period'] = mod_date
                                    merged_df['SKU Unique ID'] = merged_df['SKU Unique ID'].fillna(
                                        merged_df['SKU Unique ID_new'])
                                    merged_df['Distinct or Nondistinct'] = merged_df['Distinct or Nondistinct'].fillna(
                                        merged_df['Distinct or Nondistinct_new'])
                                    merged_df['SKU Unit List Price'] = merged_df['SKU Unit List Price'].fillna(
                                        merged_df['SKU Unit List Price_new'])
                                    merged_df['Midpoint Discount Percentage'] = merged_df[
                                        'Midpoint Discount Percentage'].fillna(
                                        merged_df['Midpoint Discount Percentage_new'])
                                    merged_df['SSP Range Method (+-)'] = merged_df['SSP Range Method (+-)'].fillna(
                                        merged_df['SSP Range Method (+-)_new'])
                                    merged_df['Revenue Account'] = merged_df['Revenue Account'].fillna(
                                        merged_df['Revenue Account_new'])

                                    # update previous fields
                                    merged_df['Previous Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0)
                                    merged_df['Previous Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0)
                                    merged_df['Previous Remaining Allocation'] = merged_df[
                                        'Current Remaining Allocation'].fillna(0)
                                    merged_df['Previous Remaining Billing'] = merged_df[
                                        'Current Remaining Billing'].fillna(0)
                                    merged_df['Previous Unit SSP'] = merged_df['Current Unit SSP'].fillna(0)
                                    merged_df['Previous Remaining Unit Rev Rec'] = merged_df[
                                        'Current Remaining Unit Rev Rec'].fillna(0)
                                    merged_df['Previous Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Previous Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Previous Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Previous Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Previous SSP Delivered - Cumulative'] = merged_df[
                                        'Current SSP Delivered - Cumulative'].fillna(0)
                                    merged_df['Previous Contract Position - POB'] = merged_df[
                                        'Current Contract Position - POB'].fillna(0)
                                    merged_df['Previous Contract Position - Contract Level'] = merged_df[
                                        'Current Contract Position - Contract Level'].fillna(0)
                                    merged_df["Previous Reclass to UAR"] = merged_df["Current Reclass to UAR"].fillna(0)

                                    # update current fields
                                    merged_df['Current Remaining Qty'] = merged_df['Current Remaining Qty'].fillna(0) + \
                                                                         merged_df['Mod Qty'].fillna(0)
                                    merged_df['Current Remaining SSP'] = merged_df['Current Remaining SSP'].fillna(0) + \
                                                                         merged_df[
                                                                             'Mod SSP Changes'].fillna(0)
                                    # in case the remaining SSP is reduced to below zero, make the zero as the minimum
                                    merged_df.loc[merged_df['Current Remaining SSP'] < 0, "Current Remaining SSP"] = 0

                                    # calculate current remaining allocation based on SSP undelivered after the entire retrospective re-allocation based on the total SSPs
                                    merged_df['Current Remaining Allocation'] = merged_df[
                                                                                    'Current Remaining Allocation'].fillna(
                                        0) + merged_df[
                                                                                    'Mod Billing'].fillna(0)

                                    merged_df['Current Remaining Billing'] = merged_df[
                                                                                 'Current Remaining Billing'].fillna(
                                        0) + merged_df[
                                                                                 'Mod Billing'].fillna(0)
                                    merged_df['Current Unit SSP'] = (
                                            merged_df['Current Remaining SSP'].fillna(0) / merged_df[
                                        'Current Remaining Qty'].fillna(0)).fillna(0)
                                    merged_df['Current Remaining Unit Rev Rec'] = (
                                            merged_df['Current Remaining Allocation'].fillna(0) / merged_df[
                                        'Current Remaining Qty'].fillna(
                                        0)).fillna(0)
                                    merged_df['Current Delivery'] = 0
                                    merged_df['Current Rev Rec'] = 0
                                    merged_df['Current Billing'] = 0
                                    merged_df['Current Cumulative Catchup - Disclosure Only'] = 0
                                    merged_df['Current Delivery - Cumulative'] = merged_df[
                                        'Current Delivery - Cumulative'].fillna(0)
                                    merged_df['Current Rev Rec - Cumulative'] = merged_df[
                                        'Current Rev Rec - Cumulative'].fillna(0)
                                    merged_df['Current Billing - Cumulative'] = merged_df[
                                        'Current Billing - Cumulative'].fillna(0)
                                    merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                        'Current Cumulative Catchup - Cumulative - Disclosure Only'].fillna(0)
                                    merged_df['Current Contract Position - POB'] = merged_df[
                                                                                       'Current Billing - Cumulative'].fillna(
                                        0) - merged_df[
                                                                                       'Current Rev Rec - Cumulative'].fillna(
                                        0)
                                    merged_df["Current Contract Position - Contract Level"] = \
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    merged_df["Current Reclass to UAR"] = np.where(
                                        merged_df['Current Contract Position - Contract Level'] < 0,
                                        -merged_df['Current Contract Position - Contract Level'] /
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * merged_df['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    merged_df.loc[
                                        merged_df["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # update the records timestamp
                                    merged_df['Processing Time Log'] = pd.Timestamp.now()
                                    merged_df['Record Unique ID'] = merged_df['Processing Time Log'].astype(str) + " " + \
                                                                    merged_df[
                                                                        'Contract Unique Name'] + " " + merged_df[
                                                                        'POB Unique ID'] + " " + merged_df['SKU Name']

                                    # Drop unused _new columns
                                    merged_df = merged_df.drop(
                                        columns=[col for col in merged_df.columns if col.endswith(('_new'))])
                                    merged_df = merged_df.drop(
                                        columns=['Mod Billing', 'Mod Qty', 'Mod SSP Changes'])

                                    # re-write merged_df['Current Rev Rec - Cumulative Should Be'] with the total allocation and total SSPs
                                    merged_df['Current Rev Rec - Cumulative Should Be'] = (
                                            (merged_df['Current Remaining Allocation'] + merged_df[
                                                'Current Rev Rec - Cumulative']) / (
                                                    merged_df['Current Remaining SSP'] + merged_df[
                                                'Previous SSP Delivered - Cumulative']) * merged_df[
                                                'Previous SSP Delivered - Cumulative']).fillna(0)

                                    merged_df['Current Cumulative Catchup - Disclosure Only'] = merged_df[
                                                                                                    'Current Rev Rec - Cumulative Should Be'] - \
                                                                                                merged_df[
                                                                                                    'Current Rev Rec - Cumulative']
                                    merged_df['Current Cumulative Catchup - Cumulative - Disclosure Only'] = merged_df[
                                                                                                                 'Current Cumulative Catchup - Cumulative - Disclosure Only'] + \
                                                                                                             merged_df[
                                                                                                                 'Current Cumulative Catchup - Disclosure Only']
                                    # next step: add the 'current cumulative catch up' to Contract_Live
                                    merged_df['Current Rev Rec'] = merged_df[
                                        'Current Cumulative Catchup - Disclosure Only'].fillna(0)
                                    merged_df['Current Rev Rec - Cumulative'] = merged_df[
                                                                                    'Current Rev Rec - Cumulative'].fillna(
                                        0) + merged_df['Current Rev Rec']

                                    # print(merged_df['Current Cumulative Catchup - Disclosure Only'])
                                    # update current remaining allocation after the cumulative catchup
                                    merged_df['Current Remaining Allocation'] = (
                                            merged_df['Current Remaining Allocation'] - merged_df[
                                        'Current Rev Rec']).fillna(0)

                                    merged_df['Current Remaining Unit Rev Rec'] = (merged_df[
                                                                                       'Current Remaining Allocation'].fillna(
                                        0) / \
                                                                                   merged_df[
                                                                                       'Current Remaining Qty'].fillna(
                                                                                       0)).fillna(0)
                                    merged_df['Current Contract Position - POB'] = merged_df[
                                                                                       'Current Billing - Cumulative'].fillna(
                                        0) - \
                                                                                   merged_df[
                                                                                       'Current Rev Rec - Cumulative'].fillna(
                                                                                       0)
                                    merged_df["Current Contract Position - Contract Level"] = \
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current Contract Position - POB'].transform('sum')
                                    merged_df["Current Reclass to UAR"] = np.where(
                                        merged_df['Current Contract Position - Contract Level'] < 0,
                                        -merged_df['Current Contract Position - Contract Level'] /
                                        merged_df.groupby('Contract Unique Name')[
                                            'Current SSP Delivered - Cumulative'].transform(
                                            'sum') * merged_df['Current SSP Delivered - Cumulative'], 0)
                                    # override VC line's reclass to UAR to zero as this is not a true POB
                                    merged_df.loc[
                                        merged_df["ASC 606 Stratification"] == "VC", "Current Reclass to UAR"] = 0

                                    # drop the nondistinct POB's 'Current Rev Rec - Cumulative Should Be'
                                    merged_df = merged_df.drop(columns='Current Rev Rec - Cumulative Should Be')

                                    # Sort the DataFrame based on 'Record Unique ID without time'
                                    merged_df = merged_df.sort_values('Record Unique ID without time')

                                    # add another validation to make sure the current delivery if negative,
                                    # doesn't cause the total delivery cumulative to be negative

                                    if (merged_df["Current Remaining Qty"] < 0).any() or (
                                            merged_df[merged_df["ASC 606 Stratification"] != "VC"][
                                                'Current Remaining Billing'] < 0).any():
                                        QMessageBox.information(self, "Mod Failed",
                                                                "Qty or Price modified cannot reduce the remaining qty or remaining billing to negative. Check your uploads please.")
                                        raise Exception("The process is stopped for users to fix the file")

                                    else:
                                        # check in incremental data if table exists; if not create the table
                                        conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                        cur = conn.cursor()
                                        cur.execute(
                                            "SELECT name FROM sqlite_master WHERE type='table' AND name='Contract_Live'")
                                        table_exists = bool(cur.fetchone())
                                        # Close the cursor and connection
                                        cur.close()
                                        conn.close()
                                        # insert incremental if exists
                                        if table_exists:
                                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # query = f'''
                                            #    SELECT *
                                            #    FROM "Contract_Live"
                                            #    '''
                                            # Execute the query and create a DataFrame
                                            # df_contract_live = pd.read_sql_query(query, conn)
                                            # conn.close()
                                            # Filter the pandas DataFrame to include only incremental data
                                            # incremental_data = merged_df[
                                            #    ~merged_df['Record Unique ID'].isin(
                                            #        df_contract_live['Record Unique ID'])]
                                            # Insert the incremental data into the SQL table
                                            # conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                                            # incremental_data.to_sql("Contract_Live", conn, if_exists="append",
                                            #                        index=False)
                                            merged_df.to_sql("Contract_Live", conn, if_exists="append", index=False)
                                            conn.close()
                                            QMessageBox.information(self, "POB Specific VC Successfully Applied!",
                                                                    "POB Specific VC has been processed retrospectively for the current date :)")
                                        else:
                                            # create Contract_Live table
                                            raise Exception("No contract table is found!")
        except TypeError:  # Skip TypeError when the user cancels the file selection
            pass
        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def journal_entries(self):
        try:
            input_text, ok = QInputDialog.getText(self, "Start Date Input",
                                                  f"Enter the start date of the date range to retrieve the revenue journal entries (YYYY-MM-DD):")
            if ok:
                qdate_start = QDate.fromString(input_text, "yyyy-MM-dd")
                if not qdate_start.isValid():
                    QMessageBox.warning(self, "Invalid Date",
                                        "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                else:
                    input_text, ok = QInputDialog.getText(self, "Date Input",
                                                          f"Enter the end date of the date range to retrieve the revenue journal entries (YYYY-MM-DD):")
                    if ok:
                        qdate_end = QDate.fromString(input_text, "yyyy-MM-dd")
                        if not qdate_end.isValid():
                            QMessageBox.warning(self, "Invalid Date",
                                                "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                        else:
                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            query_existing_contract = '''
                                SELECT * FROM "Contract_Live"
                                '''
                            # Execute the query and create a DataFrame
                            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                            conn.close()

                            # Define the datetime period
                            start_date = datetime.combine(qdate_start.toPython(), datetime.min.time())
                            end_date = datetime.combine(qdate_end.toPython(), datetime.min.time())

                            # Converting the dataframe current period to datetime
                            df_existing_contract['Current Period'] = pd.to_datetime(
                                df_existing_contract['Current Period'])
                            # Filter the DataFrame within the datetime period
                            filtered_df = df_existing_contract[
                                (df_existing_contract['Current Period'] >= start_date) & (
                                        df_existing_contract['Current Period'] <= end_date)].copy()

                            # create df for revenue entries
                            journal_entries_deferred = pd.DataFrame()
                            journal_entries_revenue = pd.DataFrame()

                            # create df for reversing reclass UAR entries
                            journal_entries_deferred_reversing = pd.DataFrame()
                            journal_entries_UAR_reversing = pd.DataFrame()

                            # create df for reclass entries
                            journal_entries_deferred_reclass = pd.DataFrame()
                            journal_entries_UAR_reclass = pd.DataFrame()

                            # create a journal df to store all the JEs
                            journal_entries_completed = pd.DataFrame()

                            # populate JEs based on the dates selected
                            journal_entries_deferred['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred['Amount'] = filtered_df['Current Rev Rec'].round(4)
                            # journal_entries_deferred['Memo'] = "Record deferred revenue reduction for current period rev rec"

                            journal_entries_revenue['Record Unique ID without time'] = filtered_df[
                                'Record Unique ID without time']
                            journal_entries_revenue['Current Period'] = filtered_df['Current Period']
                            journal_entries_revenue['Account'] = filtered_df['Revenue Account']
                            journal_entries_revenue['Amount'] = 0 - filtered_df['Current Rev Rec'].round(4)
                            # journal_entries_revenue['Memo'] = "Record current period rev rec"

                            journal_entries_deferred_reversing['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred_reversing['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred_reversing['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred_reversing['Amount'] = filtered_df['Previous Reclass to UAR'].round(
                                4)
                            # journal_entries_deferred_reversing['Memo'] = "Reverse previous reclass from deferred revenue to UAR if applicable"

                            journal_entries_UAR_reversing['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_UAR_reversing['Current Period'] = filtered_df['Current Period']
                            journal_entries_UAR_reversing['Account'] = filtered_df['Unbilled A/R Account']
                            journal_entries_UAR_reversing['Amount'] = 0 - filtered_df['Previous Reclass to UAR'].round(
                                4)
                            # journal_entries_UAR_reversing['Memo'] = "Reverse previous reclass from deferred revenue to UAR if applicable"

                            journal_entries_deferred_reclass['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred_reclass['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred_reclass['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred_reclass['Amount'] = 0 - filtered_df[
                                'Current Reclass to UAR'].round(4)
                            # journal_entries_deferred_reclass['Memo'] = "Reclass from deferred revenue to UAR for the current period if applicable"

                            journal_entries_UAR_reclass['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_UAR_reclass['Current Period'] = filtered_df['Current Period']
                            journal_entries_UAR_reclass['Account'] = filtered_df['Unbilled A/R Account']
                            journal_entries_UAR_reclass['Amount'] = filtered_df['Current Reclass to UAR'].round(4)
                            # journal_entries_UAR_reclass['Memo'] = "Reclass from deferred revenue to UAR for the current period if applicable"

                            journal_entries_completed = pd.concat(
                                [journal_entries_deferred, journal_entries_revenue, journal_entries_deferred_reversing,
                                 journal_entries_UAR_reversing, journal_entries_deferred_reclass,
                                 journal_entries_UAR_reclass], ignore_index=True)
                            journal_entries_nonZero = journal_entries_completed[
                                journal_entries_completed['Amount'].round(2) != 0].copy()

                            # group all amounts in the same account of the same period
                            consolidated_df = \
                                journal_entries_nonZero.groupby(['Record Unique ID without time', 'Account'])[
                                    'Amount'].sum().reset_index()
                            consolidated_df_nonZero = consolidated_df[consolidated_df['Amount'].round(2) != 0].copy()
                            consolidated_df_nonZero['Amount'] = consolidated_df_nonZero['Amount'].round(2)

                            # Export DataFrame to Excel
                            consolidated_df_nonZero.to_excel(
                                f'Revenue JE Summary between {qdate_start.toPython()} and {qdate_end.toPython()}.xlsx',
                                index=False)

                            # Create a pop-up window
                            self.sender().parent().close()  # Close the dialog
                            self.journal_window = DataFramePopup(consolidated_df_nonZero)
                            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def contract_history(self):
        try:
            input_text, ok = QInputDialog.getText(self, "Start Date Input",
                                                  f"Enter the start date of the date range to retrieve the revenue contract history (YYYY-MM-DD):")
            if ok:
                qdate_start = QDate.fromString(input_text, "yyyy-MM-dd")
                if not qdate_start.isValid():
                    QMessageBox.warning(self, "Invalid Date",
                                        "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                else:
                    input_text, ok = QInputDialog.getText(self, "Date Input",
                                                          f"Enter the end date of the date range to retrieve the revenue contract history (YYYY-MM-DD):")
                    if ok:
                        qdate_end = QDate.fromString(input_text, "yyyy-MM-dd")
                        if not qdate_end.isValid():
                            QMessageBox.warning(self, "Invalid Date",
                                                "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                        else:
                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            query_existing_contract = '''
                                SELECT * FROM "Contract_Live"
                                '''
                            # Execute the query and create a DataFrame
                            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                            conn.close()

                            # Define the datetime period
                            start_date = datetime.combine(qdate_start.toPython(), datetime.min.time())
                            end_date = datetime.combine(qdate_end.toPython(), datetime.min.time())

                            # Converting the dataframe current period to datetime
                            df_existing_contract['Current Period'] = pd.to_datetime(
                                df_existing_contract['Current Period'])
                            # Filter the DataFrame within the datetime period
                            filtered_df = df_existing_contract[
                                (df_existing_contract['Current Period'] >= start_date) & (
                                        df_existing_contract['Current Period'] <= end_date)].copy()

                            # Export DataFrame to Excel
                            filtered_df.to_excel(
                                f'Contract History between {qdate_start.toPython()} and {qdate_end.toPython()}.xlsx',
                                index=False)

                            # Create a pop-up window
                            self.sender().parent().close()  # Close the dialog
                            self.journal_window = DataFramePopup(filtered_df)
                            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def specific_contract_history(self):
        try:
            input_text, ok = QInputDialog.getText(self, "Start Date Input",
                                                  f"Enter the start date of the date range to retrieve the revenue contract history (YYYY-MM-DD):")
            if ok:
                qdate_start = QDate.fromString(input_text, "yyyy-MM-dd")
                if not qdate_start.isValid():
                    QMessageBox.warning(self, "Invalid Date",
                                        "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                else:
                    input_text, ok = QInputDialog.getText(self, "Date Input",
                                                          f"Enter the end date of the date range to retrieve the revenue contract history (YYYY-MM-DD):")
                    if ok:
                        qdate_end = QDate.fromString(input_text, "yyyy-MM-dd")
                        if not qdate_end.isValid():
                            QMessageBox.warning(self, "Invalid Date",
                                                "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                        else:
                            contract_name, ok = QInputDialog.getText(self, "Enter contract unique name",
                                                                     f"Please enter the specific contract unique name to retrieve the revenue history:")

                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            query_existing_contract = f'''
                                SELECT * FROM "Contract_Live"
                                WHERE "Contract Unique Name" = "{contract_name}"
                                '''
                            # Execute the query and create a DataFrame
                            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                            conn.close()

                            # Define the datetime period
                            start_date = datetime.combine(qdate_start.toPython(), datetime.min.time())
                            end_date = datetime.combine(qdate_end.toPython(), datetime.min.time())

                            # Converting the dataframe current period to datetime
                            df_existing_contract['Current Period'] = pd.to_datetime(
                                df_existing_contract['Current Period'])
                            # Filter the DataFrame within the datetime period
                            filtered_df = df_existing_contract[
                                (df_existing_contract['Current Period'] >= start_date) & (
                                        df_existing_contract['Current Period'] <= end_date)].copy()

                            # Export DataFrame to Excel
                            filtered_df.to_excel(
                                f'{contract_name} History between {qdate_start.toPython()} and {qdate_end.toPython()}.xlsx',
                                index=False)

                            # Create a pop-up window
                            self.sender().parent().close()  # Close the dialog
                            self.journal_window = DataFramePopup(filtered_df)
                            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def latest_contracts(self):
        try:
            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
            query_existing_contract = '''
                                SELECT t1.*
                                FROM Contract_Live t1
                                JOIN (
                                        SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                        FROM Contract_Live
                                        GROUP BY "Record Unique ID without time"
                                ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                '''
            # Execute the query and create a DataFrame
            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
            conn.close()

            # Convert the Timestamp field to datetime
            df_existing_contract['Processing Time Log'] = pd.to_datetime(df_existing_contract['Processing Time Log'])
            df_contract_live_latest = df_existing_contract.loc[
                df_existing_contract.groupby('Record Unique ID without time')['Processing Time Log'].idxmax()]

            # Export DataFrame to Excel
            df_contract_live_latest.to_excel('Latest Contract Details.xlsx')

            # Create a pop-up window
            self.sender().parent().close()  # Close the dialog
            self.journal_window = DataFramePopup(df_contract_live_latest)
            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def specific_latest_contracts(self):
        try:

            contract_name, ok = QInputDialog.getText(self, "Enter contract unique name",
                                                     f"Please enter the specific contract unique name to retrieve the latest contract version:")

            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
            query_existing_contract = f'''
                                SELECT t1.*
                                FROM Contract_Live t1
                                JOIN (
                                        SELECT "Record Unique ID without time", MAX("Processing Time Log") AS max_timestamp
                                        FROM Contract_Live
                                        WHERE "Contract Unique Name" = "{contract_name}"
                                        GROUP BY "Record Unique ID without time"
                                ) t2 ON t1."Record Unique ID without time" = t2."Record Unique ID without time" AND t1."Processing Time Log" = t2.max_timestamp;
                                '''

            # Execute the query and create a DataFrame
            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
            conn.close()

            # Convert the Timestamp field to datetime
            df_existing_contract['Processing Time Log'] = pd.to_datetime(df_existing_contract['Processing Time Log'])
            df_contract_live_latest = df_existing_contract.loc[
                df_existing_contract.groupby('Record Unique ID without time')['Processing Time Log'].idxmax()]

            # Export DataFrame to Excel
            df_contract_live_latest.to_excel(f'{contract_name} Latest Contract Details.xlsx')

            # Create a pop-up window
            self.sender().parent().close()  # Close the dialog
            self.journal_window = DataFramePopup(df_contract_live_latest)
            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def journal_entries_delta(self):
        try:
            input_text, ok = QInputDialog.getText(self, "Start Date Input",
                                                  f"Enter the start date of the date range to retrieve the revenue journal entries (YYYY-MM-DD):")
            if ok:
                qdate_start = QDate.fromString(input_text, "yyyy-MM-dd")
                if not qdate_start.isValid():
                    QMessageBox.warning(self, "Invalid Date",
                                        "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                else:
                    input_text, ok = QInputDialog.getText(self, "Date Input",
                                                          f"Enter the end date of the date range to retrieve the revenue journal entries (YYYY-MM-DD):")
                    if ok:
                        qdate_end = QDate.fromString(input_text, "yyyy-MM-dd")
                        if not qdate_end.isValid():
                            QMessageBox.warning(self, "Invalid Date",
                                                "Invalid date format. Please enter a valid date in the format 'YYYY-MM-DD'.")
                        else:
                            conn = sqlite3.connect('ops/libnew/libwarm/db/ASC606.db')
                            query_existing_contract = '''
                                SELECT * FROM "Contract_Live"
                                '''
                            # Execute the query and create a DataFrame
                            df_existing_contract = pd.read_sql_query(query_existing_contract, conn)
                            conn.close()

                            # Define the datetime period
                            start_date = datetime.combine(qdate_start.toPython(), datetime.min.time())
                            end_date = datetime.combine(qdate_end.toPython(), datetime.min.time())

                            # Converting the dataframe current period to datetime
                            df_existing_contract['Current Period'] = pd.to_datetime(
                                df_existing_contract['Current Period'])
                            # Filter the DataFrame within the datetime period
                            filtered_df = df_existing_contract[
                                (df_existing_contract['Current Period'] >= start_date) & (
                                        df_existing_contract['Current Period'] <= end_date)].copy()

                            # create df for revenue entries
                            journal_entries_deferred = pd.DataFrame()
                            journal_entries_revenue = pd.DataFrame()

                            # create df for reversing reclass UAR entries
                            journal_entries_deferred_reversing = pd.DataFrame()
                            journal_entries_UAR_reversing = pd.DataFrame()

                            # create df for reclass entries
                            journal_entries_deferred_reclass = pd.DataFrame()
                            journal_entries_UAR_reclass = pd.DataFrame()

                            # create df for delta entries
                            journal_entries_revenue_delta = pd.DataFrame()
                            journal_entries_deferred_delta = pd.DataFrame()

                            # create a journal df to store all the JEs
                            journal_entries_completed = pd.DataFrame()

                            # populate JEs based on the dates selected
                            journal_entries_deferred['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred['Amount'] = filtered_df['Current Rev Rec'].round(4)
                            # journal_entries_deferred['Memo'] = "Record deferred revenue reduction for current period rev rec"

                            journal_entries_revenue['Record Unique ID without time'] = filtered_df[
                                'Record Unique ID without time']
                            journal_entries_revenue['Current Period'] = filtered_df['Current Period']
                            journal_entries_revenue['Account'] = filtered_df['Revenue Account']
                            journal_entries_revenue['Amount'] = 0 - filtered_df['Current Rev Rec'].round(4)
                            # journal_entries_revenue['Memo'] = "Record current period rev rec"

                            journal_entries_deferred_reversing['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred_reversing['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred_reversing['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred_reversing['Amount'] = filtered_df['Previous Reclass to UAR'].round(
                                4)
                            # journal_entries_deferred_reversing['Memo'] = "Reverse previous reclass from deferred revenue to UAR if applicable"

                            journal_entries_UAR_reversing['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_UAR_reversing['Current Period'] = filtered_df['Current Period']
                            journal_entries_UAR_reversing['Account'] = filtered_df['Unbilled A/R Account']
                            journal_entries_UAR_reversing['Amount'] = 0 - filtered_df['Previous Reclass to UAR'].round(
                                4)
                            # journal_entries_UAR_reversing['Memo'] = "Reverse previous reclass from deferred revenue to UAR if applicable"

                            journal_entries_deferred_reclass['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred_reclass['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred_reclass['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred_reclass['Amount'] = 0 - filtered_df[
                                'Current Reclass to UAR'].round(4)
                            # journal_entries_deferred_reclass['Memo'] = "Reclass from deferred revenue to UAR for the current period if applicable"

                            journal_entries_UAR_reclass['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_UAR_reclass['Current Period'] = filtered_df['Current Period']
                            journal_entries_UAR_reclass['Account'] = filtered_df['Unbilled A/R Account']
                            journal_entries_UAR_reclass['Amount'] = filtered_df['Current Reclass to UAR'].round(4)
                            # journal_entries_UAR_reclass['Memo'] = "Reclass from deferred revenue to UAR for the current period if applicable"

                            # Debit revenue = billing/Current Pre-ASC606 Revenue (Net Design Only) to create the delta entry on the revenue side
                            journal_entries_revenue_delta['Record Unique ID without time'] = filtered_df[
                                'Record Unique ID without time']
                            journal_entries_revenue_delta['Current Period'] = filtered_df['Current Period']
                            journal_entries_revenue_delta['Account'] = filtered_df['Revenue Account']
                            journal_entries_revenue_delta['Amount'] = filtered_df[
                                'Current Pre-ASC606 Revenue (Net Design Only)'].round(4)

                            # Cr. Deferred Revenue = billing/Current Pre-ASC606 Revenue (Net Design Only) to create the delta entry on the revenue side
                            journal_entries_deferred_delta['Record Unique ID without time'] = filtered_df[
                                'Contract Unique Name']
                            journal_entries_deferred_delta['Current Period'] = filtered_df['Current Period']
                            journal_entries_deferred_delta['Account'] = filtered_df['Deferred Revenue Account']
                            journal_entries_deferred_delta['Amount'] = 0 - filtered_df[
                                'Current Pre-ASC606 Revenue (Net Design Only)'].round(4)

                            journal_entries_completed = pd.concat(
                                [journal_entries_deferred, journal_entries_revenue, journal_entries_deferred_reversing,
                                 journal_entries_UAR_reversing, journal_entries_deferred_reclass,
                                 journal_entries_UAR_reclass, journal_entries_revenue_delta,
                                 journal_entries_deferred_delta], ignore_index=True)
                            journal_entries_nonZero = journal_entries_completed[
                                journal_entries_completed['Amount'].round(2) != 0].copy()

                            # group all amounts in the same account of the same period
                            consolidated_df = \
                                journal_entries_nonZero.groupby(['Record Unique ID without time', 'Account'])[
                                    'Amount'].sum().reset_index()
                            consolidated_df_nonZero = consolidated_df[consolidated_df['Amount'].round(2) != 0].copy()
                            consolidated_df_nonZero['Amount'] = consolidated_df_nonZero['Amount'].round(2)

                            # Export DataFrame to Excel
                            consolidated_df_nonZero.to_excel(
                                f'Revenue Adj. Summary between {qdate_start.toPython()} and {qdate_end.toPython()}.xlsx',
                                index=False)

                            # Create a pop-up window
                            self.sender().parent().close()  # Close the dialog
                            self.journal_window = DataFramePopup(consolidated_df_nonZero)
                            self.journal_window.show()

        except Exception as e:
            try:
                conn.close()
            except:
                pass
            QMessageBox.critical(self, "Error Notification", str(e))

    def show_custom_dialog(self):
        dialog = CustomDialog(self)
        dialog.exec()

    def show_contract_dialog(self):
        dialog = ContractDialog(self)
        dialog.exec()

    def show_latest_contract_dialog(self):
        dialog = LatestContractDialog(self)
        dialog.exec()


class DataFramePopup(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()
        self.setWindowTitle("Summary")
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
        self.resize(800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        table_view = QTableView(self)
        table_view.setSortingEnabled(False)  # Disable sorting to keep column title frozen
        table_model = DataFrameTableModel(dataframe)
        table_view.setModel(table_model)

        main_layout.addWidget(table_view)

        QMessageBox.information(self, "File Saved",
                                "Details are exported to an Excel within the folder :)")


class DataFrameTableModel(QAbstractTableModel):
    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe

    def rowCount(self, parent):
        return len(self.dataframe)

    def columnCount(self, parent):
        return len(self.dataframe.columns)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.dataframe.iloc[index.row(), index.column()])

        if role == Qt.BackgroundRole and index.row() == 0:
            # Color the first row (column title) with a different background color
            return QColor(240, 240, 240)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.dataframe.columns[section])
            if orientation == Qt.Vertical:
                return str(self.dataframe.index[section])

        return None


class ShutdownNotifier:
    def __init__(self, shutdown_datetime):
        self.shutdown_datetime = shutdown_datetime
        # Start a QTimer to check the current time periodically
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.timer.start(60000)  # Check every second (adjust as needed)

    def check_time(self):
        current_datetime = datetime.now()
        if current_datetime >= self.shutdown_datetime:
            self.timer.stop()
            self.show_notification()
            self.shutdown()

    def show_notification(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("End of Life Notification")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(
            "The software end of life period has been reached. The application will now shut down. Please download the latest version.")
        msg_box.exec()

    def shutdown(self):
        # Quit the application
        QApplication.quit()


# class for the revenue JE pop-up window
class CustomDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose A Revenue Journal Entry Option")
        self.resize(300, 80)
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))

        layout = QVBoxLayout(self)

        # Add buttons for user's choices
        button1 = QPushButton("Gross Revenue JEs", self)
        button2 = QPushButton("Revenue Adjustment JEs", self)

        layout.addWidget(button1)
        layout.addWidget(button2)

        # Connect button clicks to custom signals
        button1.clicked.connect(self.parent().journal_entries)
        button2.clicked.connect(self.parent().journal_entries_delta)


# class for the contract history pop-up window
class ContractDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose A Contract History Option")
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
        self.resize(300, 80)

        layout = QVBoxLayout(self)

        # Add buttons for user's choices
        button1 = QPushButton("Check All Contract History", self)
        button2 = QPushButton("Check Specific Contract", self)

        layout.addWidget(button1)
        layout.addWidget(button2)

        # Connect button clicks to custom signals
        button1.clicked.connect(self.parent().contract_history)
        button2.clicked.connect(self.parent().specific_contract_history)


# class for the latest contract history pop-up window
class LatestContractDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose A Latest Contract Option")
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
        self.resize(300, 80)

        layout = QVBoxLayout(self)

        # Add buttons for user's choices
        button1 = QPushButton("Check All Latest Contract", self)
        button2 = QPushButton("Check Specific Latest Contract", self)

        layout.addWidget(button1)
        layout.addWidget(button2)

        # Connect button clicks to custom signals
        button1.clicked.connect(self.parent().latest_contracts)
        button2.clicked.connect(self.parent().specific_latest_contracts)


# license key management
class LicenseKeyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chipmunk_License_Key Input")
        self.setWindowIcon(QIcon('ops/reserved/pic/Chipmunk.ico'))
        self.setFixedSize(500, 100)
        layout = QVBoxLayout()

        self.label = QLabel("Enter your Chipmunk Premium License Key or enter anything to use the free version:")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.api_key_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_license_key)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_license_key(self):
        api_key = self.api_key_input.text()
        if api_key:
            with open(".env", "w") as f:
                f.write(f"Chipmunk_License_Key={api_key}\n")
            QMessageBox.information(self, "Success", "Chipmunk_License_Key saved successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Chipmunk_License_Key cannot be empty.")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = FileBrowserWindow()
    window.show()

    # Specify the shutdown time
    shutdown_time = datetime(2025, 12, 31, 23, 59)
    notifier = ShutdownNotifier(shutdown_time)

    sys.exit(app.exec())
