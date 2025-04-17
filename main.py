from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from plyer import camera
import os
from kivy.core.window import Window

from android.permissions import request_permissions, Permission
request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])


KV = '''
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDFloatLayout:
        md_bg_color: [1, 1, 1, 1]
        MDIconButton:
            icon: "camera"
            pos_hint: {"center_x": 0.2, "center_y": 0.5}
            user_font_size: "64sp"
            theme_text_color: "Custom"
            text_color: [0, 0, 0, 1]
            on_release: root.capture_image()
'''


class MainScreen(Screen):
    def capture_image(self):
        try:
            save_path = os.path.join(os.getcwd(), "photo.jpg")
            
            # Делаем снимок
            camera.take_picture(
                filename=save_path,
                on_complete=self.on_camera_success
            )
        except Exception as e:
            print(f"error: {e}")

    def on_camera_success(self, filename):
        print(f"save foto {filename}")


class CameraApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


if __name__ == "__main__":
    CameraApp().run()