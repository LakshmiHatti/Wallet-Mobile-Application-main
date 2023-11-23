from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivymd.uix.button import MDFloatingActionButton
Window.size = (300, 500)
Builder.load_file("signin.kv")

class SignInScreen(Screen):
    def go_back(self):
        self.manager.current = 'login'


class WalletApp(MDApp):
    def build(self):
        print("Building walletApp")
        return Builder.load_file("signin.kv")


if __name__ == "__main__":
    WalletApp().run()
