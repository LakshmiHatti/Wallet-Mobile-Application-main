from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from login import LoginScreen
from signin import SignInScreen
from signup import SignUpScreen
from kivymd.uix.snackbar import Snackbar
import re
import sqlite3
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
Builder.load_string(
    """
<ScreenManagement>:
    LoginScreen:
        name: 'login'
        manager: root
    SignInScreen:
        name: 'signin'
        manager: root
    SignUpScreen:
        name: 'signup'
        manager: root

    """
)

class ScreenManagement(ScreenManager):
    def signup(self):
        current_screen = self.current_screen
        gmail = current_screen.ids.gmail.text
        username = current_screen.ids.username.text
        password = current_screen.ids.password.text
        phone_no = current_screen.ids.phone_no.text
        aadhar_card = current_screen.ids.aadhar_card.text
        pan_card = current_screen.ids.pan_card.text
        address = current_screen.ids.address.text

        try:
            # Database Connection
            conn = sqlite3.connect('wallet_app.db')
            cursor = conn.cursor()
            # Inserting data into DataSbase
            sql=('INSERT INTO login(gmail,username,password,phone,adhaar,pan,address) VALUES (?,?,?,?,?,?,?);')
            mydata=(gmail,username,password,phone_no,aadhar_card,pan_card,address)
            cursor.execute(sql,mydata)
            # cheking for duplicate values
            # Check for duplicate usernames and phones
            cursor.execute('''
                SELECT gmail, username, COUNT(*)
                FROM login
                GROUP BY gmail,username
                HAVING COUNT(*) > 1
            ''')

            duplicate_records = cursor.fetchall()

            if duplicate_records:
                Snackbar(text="Username/Gmail Already exists").open()
                for gmail,username, count in duplicate_records:
                    print(f"Username: {username}, gmail: {gmail} - Count: {count}")
            else:
                print("No duplicate records found.")
        except Exception as e :
            print(e)
        conn.commit()
        conn.close()

        if ( not gmail or not username
                or not password or not phone_no
                or not aadhar_card or not pan_card or not address):
            Snackbar(text="All fields are mandatory. Please fill in all the required fields.").open()
            return

        if not self.is_valid_aadhar(aadhar_card):
            Snackbar(
                text="Invalid Aadhar card number. Aadhar card should be 12 digits long and contain only numeric characters.").open()
            return

        if not self.is_valid_phone(phone_no):
            Snackbar(
                text="Invalid phone number. Phone number should be 10 digits long and start with 6, 7, 8, or 9.").open()
            return

        if not self.is_valid_pan(pan_card):
            Snackbar(
                text="Invalid PAN card number. PAN card should start with 5 characters (A-Z), followed by 4 numbers, and ending with 1 character (A-Z).").open()
            return

        # Add your sign-up logic here
        print("Signing up...")
        print(f"Gmail: {gmail}, Username: {username}, Password: {password}, "
              f"Phone Number: {phone_no}, Aadhar Card: {aadhar_card}, PAN Card: {pan_card}, "
              f"Address: {address}")

    def is_valid_phone(self, phone):
        if len(phone) == 10 and phone[0] in ['6', '7', '8', '9']:
            return True
        return False

    def is_valid_aadhar(self, aadhar):
        if len(aadhar) == 12 and aadhar.isdigit():
            return True
        return False


    def is_valid_pan(self, pan):
        if len(pan) == 10 or len(pan) == 11 and pan[:5].isalpha() and pan[5:9].isdigit() and pan[9:10].isdigit() or pan[9:12].isalpha()  :
            return True
        return False



    # ...

    def sign_in(self, input_text, password):
        # ... (rest of your code)

        if input_text == '' or password == '':
            # Show popup for required fields
            self.show_popup("All Fields are Required")
        else:
            try:
                conn = sqlite3.connect('wallet_app.db')
                cursor = conn.cursor()
            except:
                # Show popup for connection error
                self.show_popup("Something Went Wrong")
                return

            sql = "SELECT * FROM login WHERE (username=? or phone=? or gmail=?) AND password=?"
            data = (input_text, input_text, input_text, password)
            cursor.execute(sql, data)
            row = cursor.fetchone()

            if row is None:
                # Show popup for invalid user
                self.show_popup("Invalid User")
            else:
                # Show popup for successful login
                self.show_popup("Login Successful")

            conn.commit()
            conn.close()

        # ... (rest of your code)

    def show_popup(self, text):
        dialog = MDDialog(
            title="Alert",
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                    #pos_hint = {"center_x": 0.5, "center_y": 0.5}
        )
            ]
        )
        dialog.open()



class WalletApp(MDApp):
    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    WalletApp().run()
