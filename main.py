from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp
import json
import os

class ProductWidget(Button):
    product_name = StringProperty('')
    product_price = NumericProperty(0)
    assigned_user = StringProperty('Не занят')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(100)
        self.background_normal = ''
        self.background_color = (0.9, 0.9, 0.9, 1)  # Серый фон
        self.color = (0, 0, 0, 1)  # Чёрный текст
        self.font_size = '16sp'
        self.text_size = (self.width, None)
        self.halign = 'center'
        self.valign = 'middle'
        self.update_text()

    def update_text(self):
        self.text = f"{self.product_name}\nЦена: {self.product_price}\n{self.assigned_user}"

    def on_product_name(self, instance, value):
        self.update_text()

    def on_product_price(self, instance, value):
        self.update_text()

    def on_assigned_user(self, instance, value):
        self.update_text()

    def on_press(self):
        app = App.get_running_app()
        if app.selected_user:
            self.assigned_user = f"User {app.selected_user['id']}"
            app.assign_product_to_user(self.product_name, self.product_price)

class UserWidget(Button):
    user_name = StringProperty('')
    user_total = NumericProperty(0)
    user_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(80)
        self.background_normal = ''
        self.background_color = (0.8, 0.8, 1, 1)  # Голубой фон
        self.color = (0, 0, 0, 1)  # Чёрный текст
        self.font_size = '16sp'
        self.text_size = (self.width, None)
        self.halign = 'center'
        self.valign = 'middle'
        self.update_text()

    def update_text(self):
        self.text = f"ID: {self.user_id}\n{self.user_name}\nСумма: {self.user_total}"

    def on_user_name(self, instance, value):
        self.update_text()

    def on_user_total(self, instance, value):
        self.update_text()

    def on_user_id(self, instance, value):
        self.update_text()

    def on_press(self):
        app = App.get_running_app()
        app.selected_user = {'id': self.user_id, 'name': self.user_name}

class MainApp(App):
    products = ListProperty([
        {'name': 'Товар 1', 'price': 100},
        {'name': 'Товар 2', 'price': 200},
        {'name': 'Товар 3', 'price': 300},
        {'name': 'Товар 4', 'price': 400},
        {'name': 'Товар 5', 'price': 500},
        {'name': 'Товар 6', 'price': 600},
    ])
    
    users = ListProperty([])
    selected_user = None
    
    def build(self):
        self.load_users()
        
        main_layout = BoxLayout(orientation='vertical')
        
        # Products area (top half)
        products_label = Label(text='Товары', size_hint_y=None, height=dp(40))
        products_scroll = ScrollView()
        products_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        products_grid.bind(minimum_height=products_grid.setter('height'))
        
        for product in self.products:
            widget = ProductWidget()
            widget.product_name = product['name']
            widget.product_price = product['price']
            products_grid.add_widget(widget)
        
        products_scroll.add_widget(products_grid)
        
        products_area = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        products_area.add_widget(products_label)
        products_area.add_widget(products_scroll)
        main_layout.add_widget(products_area)
        
        # Users area (bottom half)
        users_label = Label(text='Пользователи', size_hint_y=None, height=dp(40))
        users_scroll = ScrollView()
        self.users_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.users_grid.bind(minimum_height=self.users_grid.setter('height'))
        
        self.update_users_grid()
        
        users_scroll.add_widget(self.users_grid)
        
        users_area = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        users_area.add_widget(users_label)
        users_area.add_widget(users_scroll)
        main_layout.add_widget(users_area)
        
        # Buttons area
        buttons_layout = BoxLayout(size_hint=(1, 0.2), spacing=dp(10), padding=dp(10))
        
        add_user_btn = Button(text='Добавить пользователя')
        add_user_btn.bind(on_press=self.show_add_user_popup)
        
        camera_btn = Button(text='Снимок с камеры')
        camera_btn.bind(on_press=self.take_photo)
        
        buttons_layout.add_widget(add_user_btn)
        buttons_layout.add_widget(camera_btn)
        main_layout.add_widget(buttons_layout)
        
        return main_layout
    
    def update_users_grid(self):
        self.users_grid.clear_widgets()
        for user in self.users:
            widget = UserWidget()
            widget.user_name = user['name']
            widget.user_total = user['total']
            widget.user_id = user['id']
            self.users_grid.add_widget(widget)
    
    def load_users(self):
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                self.users = json.load(f)
    
    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)
    
    def assign_product_to_user(self, product_name, product_price):
        if not self.selected_user:
            return
            
        for user in self.users:
            if user['id'] == self.selected_user['id']:
                user['total'] += product_price
                break
                
        self.save_users()
        self.update_users_grid()
    
    def show_add_user_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        name_input = TextInput(hint_text='Введите имя')
        
        btn_layout = BoxLayout(spacing=dp(10))
        cancel_btn = Button(text='Отмена')
        add_btn = Button(text='Добавить')
        
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(add_btn)
        
        content.add_widget(name_input)
        content.add_widget(btn_layout)
        
        popup = Popup(title='Добавить пользователя', content=content, size_hint=(0.8, 0.4))
        
        def add_user(instance):
            if name_input.text:
                new_id = max([user['id'] for user in self.users], default=0) + 1
                self.users.append({
                    'id': new_id,
                    'name': name_input.text,
                    'total': 0
                })
                self.save_users()
                self.update_users_grid()
                popup.dismiss()
        
        add_btn.bind(on_press=add_user)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        popup.open()
    
    def take_photo(self, instance):
        # Здесь должна быть реализация фото с камеры
        print("Фото с камеры")

if __name__ == '__main__':
    MainApp().run()