from kivy.lang import Builder
from kivy.metrics import sp
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
import requests

DAYS = ['Zero', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
TIMES = ['Zero', '8:00 - 8:45', '8:55 - 9:40', '9:50 - 10:35', '10:50 - 11:30', '11:50 - 12:35', '12:45 - 13:30',
         '13:35 - 14:25', '14:30 - 15:20']


class LoginScreen(Screen):
    pass


class RegistrationScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class MDCardNews(MDCard):
    pass


class MDCardSchNumber(MDCard):
    pass


class MDCardSchLesson(MDCard):
    pass


Builder.load_file('kv_files/screens.kv')
sm = ScreenManager()


class LoginApp(MDApp):
    sm = ScreenManager()

    def build(self):
        sm.add_widget(LoginScreen(name='menu'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(MainScreen(name='app'))
        self.url = "https://schoolapp-c99c1-default-rtdb.firebaseio.com/.json"
        self.urlnews = "https://schoolapp-67bbd-default-rtdb.europe-west1.firebasedatabase.app/.json"
        self.urlsch = "https://schledulebase-default-rtdb.europe-west1.firebasedatabase.app/.json"
        sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
        with open('resources/check.txt') as f:
            b = f.read()
            if b == '0':
                return sm
            return self.login()

    def signup(self):
        user = sm.get_screen('registration').ids.getusername.text
        password1 = sm.get_screen('registration').ids.getpassword1.text
        password = "".join([str(ord(i)) for i in list(password1)])
        name = sm.get_screen('registration').ids.getname.text
        surname = sm.get_screen('registration').ids.getsurname.text
        patronymic = sm.get_screen('registration').ids.getpatronymic.text
        sclass = sm.get_screen('registration').ids.getclass.text
        a = sclass
        if not a:
            a = '1000000000000000'
        bukv = a[-1]
        nomer = a[:-1]
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        supported_loginEmail = user.replace('.', '-')
        emails = set()
        for key, value in data.items():
            emails.add(key)
        if len(user.split()) > 1:
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Неверный логин', text='Пожалйста, не используйте пробелы в логине',
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif supported_loginEmail in emails:
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Логин занят',
                                   text='Пожалуйста, используйте другой логин или пройдите регестрацию',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif user.split() == [] or password1.split() == [] or name.split() == [] or surname.split() == [] or patronymic.split() == [] or sclass.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Неверный ввод', text='Пожалуйста, введите верные значения',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif not (bukv.isalpha() and nomer.isdigit()):
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Ошибка класса', text='Неверный формат, введите правильное значение',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif not 1 <= int(nomer) < 12:
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Ошибка класса', text='Неверный диапазон',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif not bukv.lower() in "абвгдклмно":
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Ошибка класса', text='Неверная буква класса',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        elif not (10 <= int(nomer) < 12 and bukv.lower() in "аб"):
            cancel_btn_username_dialogue = MDFlatButton(text='Снова', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Ошибка класса', text='После 9ого класса нет таких букв',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            print(user, password1)
            signup_info = str({
                f'"{user}":{{"Password":"{password}","Username":"{user}","Name":"{name}","Surname":"{surname}","Patronymic":"{patronymic}","Class":"{sclass}"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            to_database = json.loads(signup_info)
            print((to_database))
            with open('resources/check.txt', 'w') as f:
                f.write(f'1,{user},{password}')
            requests.patch(url=self.url, json=to_database)
            self.userclass = sclass
            sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, 'day1', 2))
            sm.get_screen('app').manager.current = 'app'

    auth = 'CSwiRgzsSGde5pwllcXsMzTLuaMxUo5RGafD3I7X'
    authnews = 'Z7raPCgw3vNrXBsMADBfo8hXSWZ4mitTU7STz9M9'
    authsch = 'QWuupfhceIGKPCNtv1CDPJacm6gBrATkdmQ5UbNk'

    def login(self):
        with open('resources/check.txt') as f:
            b = f.read()
            if b[0] == '0':
                user = sm.get_screen('menu').ids.getusername.text
                password = sm.get_screen('menu').ids.getparol.text
                password = "".join([str(ord(i)) for i in list(password)])
            else:
                b = b.split(',')
                user = b[1]
                password = b[2]
        self.login_check = False
        supported_loginEmail = user.replace('.', '-')
        supported_loginPassword = password.replace('.', '-')
        request = requests.get(self.url + '?auth=' + self.auth)
        data = request.json()
        print(data)
        emails = set()
        for key, value in data.items():
            emails.add(key)
        if supported_loginEmail in emails and supported_loginPassword == data[supported_loginEmail]['Password']:
            self.username = data[supported_loginEmail]['Username']
            self.userclass = data[self.username]['Class']
            print(self.userclass)
            self.login_check = True
            if b[0] == '0':
                with open('resources/check.txt', 'w') as f:
                    print(user)
                    print(password)
                    p = f'1,{user},{password}'
                    print(p)
                    f.write(p)

                    sm.get_screen('app').ids.schnav.add_widget(self.makeschledule(self.userclass, 'day1', 2))
                    sm.get_screen('app').manager.current = 'app'
            sm.get_screen('app').ids.schnav.add_widget(self.makeschledule(self.userclass, 'day1', 2))
            return sm.screens[2]
        else:
            sm.get_screen('menu').ids.status.text = 'Неверный логин или пароль'

    def returnt(self):
        sm.get_screen('registration').ids.getusername.text = ''
        sm.get_screen('registration').ids.getpassword1.text = ''
        sm.get_screen('registration').ids.getname.text = ''
        sm.get_screen('registration').ids.getsurname.text = ''
        sm.get_screen('registration').ids.getpatronymic.text = ''
        sm.get_screen('registration').ids.getclass.text = ''
        sm.get_screen('registration').ids.status.text = ''
        sm.get_screen('menu').manager.current = 'menu'

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def get_news(self):
        request = requests.get(self.urlnews + '?auth=' + self.authnews)
        data = request.json()
        news = []
        for key, value in data.items():
            news.append([key, value])
        return news

    def makenews(self):
        layout = GridLayout(size=(Window.width, Window.height), size_hint_x=None, size_hint_y=None, cols=1,
                            row_default_height=sp(180), row_force_default=True, spacing=10)
        layout.bind(minimum_height=layout.setter('height'))
        newslist = self.get_news()
        for i in newslist:
            card = MDCardNews()
            s = str(i[0]) + '\n\n' + str(i[1])
            card.ids.newslabel.text = s
            layout.add_widget(card)
        root = ScrollView(size_hint=(None, 1), size=(Window.width, Window.height),
                          pos_hint={'x': 0.0, 'y': 0.0})
        root.add_widget(layout)
        return root

    def get_sch(self, sclass, day):
        request = requests.get(self.urlsch + '?auth=' + self.authsch)
        data = request.json()
        print(data)
        if sclass in data.keys() and day in data[sclass].keys():
            return data[sclass][day]
        else:
            return ''

    def makeschledule(self, sclass, day, screennum):
        self.daylabel = MDLabel(text=DAYS[int(day[3:])],font_size=sp(53), font_style='Button', pos_hint={'center_y': .95},halign='center')
        # pos = (Window.width // 2.3, Window.height / 2.6)
        sm.screens[screennum].ids.schnav.add_widget(self.daylabel)
        layout = GridLayout(size=(Window.width, Window.height), size_hint_x=1, size_hint_y=None, cols=2,
                            row_default_height=sp(90), row_force_default=True, spacing=10)
        layout.bind(minimum_height=layout.setter('height'))
        schlist = self.get_sch(sclass, day).split(':')
        numb = 1
        for i in schlist:
            cardnum = MDCardSchNumber()
            cardles = MDCardSchLesson()
            cardnum.ids.schnumlabel.text = f'{str(numb)}. {TIMES[numb]}'
            cardles.ids.schlessonlabel.text = i
            layout.add_widget(cardnum)
            layout.add_widget(cardles)
            numb += 1
        root = ScrollView(size_hint=(0.719, 1), size=(Window.width - Window.width / 3, Window.height),
                          pos_hint={'center_x': .5,'center_y': .4})
        root.add_widget(layout)
        self.sch = root, day
        return root

    def arrow_right(self):
        curday = int(self.sch[1][3::])
        if curday == 6:
            curday = 1
        else:
            curday += 1
        sm.screens[2].ids.schnav.remove_widget(self.sch[0])
        sm.screens[2].ids.schnav.remove_widget(self.daylabel)
        sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{curday}', 2))

    def arrow_left(self):
        curday = int(self.sch[1][3::])
        if curday == 1:
            curday = 6
        else:
            curday -= 1
        sm.screens[2].ids.schnav.remove_widget(self.sch[0])
        sm.screens[2].ids.schnav.remove_widget(self.daylabel)
        sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{curday}', 2))


LoginApp().run()