from kivy.lang import Builder
from kivy.metrics import sp
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
import requests
import datetime
import ast
import threading

from kivymd.uix.tab import MDTabsBase

DAYS = ['Zero', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
TIMES = ['Zero', '8:00 - 8:45', '8:55 - 9:40', '9:50 - 10:35', '10:50 - 11:30', '11:50 - 12:35', '12:45 - 13:30',
         '13:35 - 14:25', '14:30 - 15:20']
TIMES_SATURDAY = ['Zero', '8:00 - 8:40', '8:45 - 9:25', '9:30 - 10:10', '10:20 - 11:00', '11:10 - 11:50',
                  '12:00 - 12:40',
                  '12:45 - 13:25']
seckey = "6061799"


# class RusTab(MDFloatLayout, MDTabsBase):
#     '''Class implementing content for a tab.'''
#     pass
#
# class MathTab(MDFloatLayout, MDTabsBase):
#     '''Class implementing content for a tab.'''
#     pass

class LoginScreen(Screen):
    pass


class RegistrationScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class MDCardNews(MDCard):
    pass


class ErrorCard(MDCard):
    pass


class MDEmilNewsCard(MDCard):
    pass


class MDCardSchNumber(MDCard):
    pass


class MDCardSchLesson(MDCard):
    pass


class MDNewsMak(ScrollView):
    pass


class AccountSettings(MDCard):
    pass


Builder.load_file('kv_files/screens.kv')
sm = ScreenManager()


class LoginApp(MDApp):
    sm = ScreenManager()

    def build(self):
        sm.add_widget(LoginScreen(name='menu'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(MainScreen(name='app'))
        # sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
        self.authorise = False
        self.initial = 0
        self.now_pad = "Новости"
        self.first_zapusk = True
        with open('resources/bd_date.txt', encoding="utf-8") as f:
            b = f.readlines()
            self.url = b[0][:-1]
            print(self.url)
            self.urlnews = b[1][:-1]
            self.urlsch = b[2][:-1]
            self.auth = b[3][:-1]
            self.authnews = b[4][:-1]
            self.authsch = b[5][:-1]
            print(self.authsch)
        request = requests.get(self.urlsch + '?auth=' + self.authsch)
        print(self.urlsch + '?auth=' + self.authsch)
        self.weekday = datetime.datetime.today().weekday() + 1
        self.time = str(datetime.datetime.today().time()).split(':')
        print(self.time)
        if self.weekday == 7:
            self.weekday = 1
        else:
            if self.time[0] > '19':
                self.weekday += 1
                if self.weekday == 7:
                    self.weekday = 1
        self.school_data = request.json()
        self.fonter = 18

        with open('resources/check.txt', encoding="utf-8") as f:
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
        elif sclass != seckey:
            if not (bukv.isalpha() and nomer.isdigit()):
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
                self.username = user
                signup_info = str({
                    f'"{user}":{{"Password":"{password}","Username":"{user}","Name":"{name}","Surname":"{surname}","Patronymic":"{patronymic}","Class":"{sclass}"}}'})
                signup_info = signup_info.replace(".", "-")
                signup_info = signup_info.replace("\'", "")
                to_database = json.loads(signup_info)
                # self.user_info = {user: [password, user, name, surname, patronymic, sclass]}
                self.user_info = signup_info
                print((to_database))
                with open('resources/check.txt', 'w', encoding="utf-8") as f:
                    f.write(f'1,{user},{password},{int(self.fonter)}')
                self.authorise = True
                requests.patch(url=self.url, json=to_database)
                self.userclass = sclass
                sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
                sm.screens[2].ids.getfont.text = str(int(self.fonter))
                if sclass == seckey:
                    self.upgrade_news()
                else:
                    sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{self.weekday}', 2))
                sm.get_screen('app').manager.current = 'app'
        else:
            self.password = password
            signup_info = str({
                f'"{user}":{{"Password":"{password}","Username":"{user}","Name":"{name}","Surname":"{surname}","Patronymic":"{patronymic}","Class":"{sclass}"}}'})
            signup_info = signup_info.replace(".", "-")
            signup_info = signup_info.replace("\'", "")
            self.user_info = signup_info
            to_database = json.loads(signup_info)
            print((to_database))
            with open('resources/check.txt', 'w', encoding="utf-8") as f:
                f.write(f'1,{user},{password},{int(self.fonter)}')
            requests.patch(url=self.url, json=to_database)
            self.userclass = sclass
            sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
            sm.screens[2].ids.getfont.text = str(int(self.fonter))
            if sclass == seckey:
                self.type = 1
                self.upgrade_news()
            else:
                self.type = 0
                sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{self.weekday}', 2))
            sm.get_screen('app').manager.current = 'app'

    def login(self):
        with open('resources/check.txt', encoding="utf-8") as f:
            b = f.read()
            if b[0] == '0':
                user = sm.get_screen('menu').ids.getusername.text
                password = sm.get_screen('menu').ids.getparol.text
                password = "".join([str(ord(i)) for i in list(password)])
            else:
                b = b.split(',')
                user = b[1]
                password = b[2]
                self.fonter = int(b[3])
        self.login_check = False
        # sm.get_screen('app').ids.tabs.add_widget(RusTab(title=f"Русский язык"))
        # sm.get_screen('app').ids.tabs.add_widget(MathTab(title=f"Математика"))
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
            self.password = supported_loginPassword
            self.user_info = data[supported_loginEmail]
            print(self.userclass)
            self.login_check = True
            if b[0] == '0':
                with open('resources/check.txt', 'w', encoding="utf-8") as f:
                    print(user)
                    print(password)
                    p = f'1,{user},{password},{int(self.fonter)}'
                    print(p)
                    f.write(p)
                    sm.get_screen('app').manager.current = 'app'
            self.authorise = True
            sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
            sm.screens[2].ids.getfont.text = str(int(self.fonter))
            if self.userclass == seckey:
                self.type = 1
                self.upgrade_news()
            else:
                self.type = 0
                sm.get_screen('app').ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{self.weekday}', 2))
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
            key = key.replace("$", ".")
            key = key.replace("PROCENT", "%")
            try:
                value = value.replace("$", ".")
            except AttributeError:
                you = []
                for zet, ix in value.items():
                    you.append(ix)
                you[1] = you[1].replace("$", ".")
                value = "[color=#A9A9A9]" + you[0] + "[/color]" + "\n" + you[1]
            news.append([key, value])
        self.news_data = news, data
        return news

    def makenews(self):
        root = MDNewsMak()
        if self.first_zapusk:
            newslist = self.get_news()
            self.first_zapusk = False
        else:
            newslist = self.news_data[0]
        for i in range(len(newslist)):
            if 'http' in newslist[i][1]:
                m = newslist[i][1].split()
                for j in range(len(m)):
                    if m[j].startswith('http'):
                        m[j] = f'[color=#353e96][u][ref="{m[j]}"]{m[j]}[/ref][/u][/color]'
                        newslist[i][1] = ' '.join(m)
                        break
        self.news_col = len(newslist)
        numb = 1
        for i in newslist:
            s = f'''[size={int(sp(self.fonter))}][b]{i[0]}[/b]
{i[1]}'''

            exec(f"root.ids.label{numb}.text = '''{s}'''")

            numb += 1

        for i in range(len(newslist) + 1, 11):
            exec(f"root.ids.card{i}.size_hint = (1, 0)")
        # root.ids.card5.md_bg_color = get_color_from_hex("#AAAAAA")
        self.news_up = root
        return root

    def get_sch(self, sclass, day):
        data = self.school_data
        if sclass in data.keys() and day in data[sclass].keys():
            return data[sclass][day]
        else:
            return ''

    def makeschledule(self, sclass, day, screennum):
        self.daylabel = MDLabel(text=DAYS[int(day[3:])], font_size=sp(53), font_style='Button',
                                pos_hint={'center_y': .95}, halign='center')
        # pos = (Window.width // 2.3, Window.height / 2.6)
        sm.screens[screennum].ids.schnav.add_widget(self.daylabel)
        layout = MDGridLayout(size=(Window.width, Window.height), size_hint_x=1, size_hint_y=None, cols=2,
                              row_default_height=sp(90), row_force_default=True, spacing=10)
        layout.bind(minimum_height=layout.setter('height'))
        schlist = self.get_sch(sclass, day).split(':')
        numb = 1
        for i in schlist:
            cardnum = MDCardSchNumber()
            cardnum.ids.schnumlabel.font_size = sp(self.fonter + 2)
            cardles = MDCardSchLesson()
            if day != 'day6':
                cardnum.ids.schnumlabel.text = f'{str(numb)}. {TIMES[numb]}'
            else:
                cardnum.ids.schnumlabel.text = f'{str(numb)}. {TIMES_SATURDAY[numb]}'
            cardles.ids.schlessonlabel.font_size = sp(self.fonter)
            cardles.ids.schlessonlabel.text = i
            layout.add_widget(cardnum)
            layout.add_widget(cardles)
            numb += 1
        root = ScrollView(size_hint=(0.719, 1), size=(Window.width - Window.width / 3, Window.height),
                          pos_hint={'center_x': .5, 'center_y': .4})
        root.add_widget(layout)
        self.sch = root, day, self.daylabel, layout
        return root

    def arrow_right(self):
        t1 = threading.Thread(target=self.update_news())
        curday = int(self.sch[1][3::])
        if curday == 6:
            curday = 1
        else:
            curday += 1
        sm.screens[2].ids.schnav.remove_widget(self.sch[0])
        sm.screens[2].ids.schnav.remove_widget(self.daylabel)
        t2 = threading.Thread(
            target=sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{curday}', 2)))
        t2.start(), t1.start()
        t2.join(), t1.join()

    def arrow_left(self):
        t1 = threading.Thread(target=self.update_news())
        curday = int(self.sch[1][3::])
        if curday == 1:
            curday = 6
        else:
            curday -= 1
        sm.screens[2].ids.schnav.remove_widget(self.sch[0])
        sm.screens[2].ids.schnav.remove_widget(self.daylabel)
        t2 = threading.Thread(
            target=sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{curday}', 2)))
        t2.start(), t1.start()
        t2.join(), t1.join()

    def getfontbut(self):
        if str(sm.screens[2].ids.getfont.text).isdigit():
            self.fonter = int(sm.screens[2].ids.getfont.text)
            with open('resources/check.txt', encoding="utf-8") as f:
                b = f.read()
                a = b.split(",")
                a[-1] = str(self.fonter)
                s = ",".join(a)
                print(s)
            with open('resources/check.txt', 'w', encoding="utf-8") as f:
                f.write(f'{s}')
            sm.get_screen('app').ids.newsnav.remove_widget(self.news_up)
            sm.screens[2].ids.schnav.remove_widget(self.sch[0])
            sm.screens[2].ids.schnav.remove_widget(self.daylabel)
            sm.screens[2].ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{self.weekday}', 2))
            sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
        else:
            sm.screens[2].ids.getfont.text = str(self.fonter)

    def exits(self):
        LoginApp().stop()

    def exit_acc(self):
        with open('resources/check.txt', 'w', encoding="utf-8") as f:
            f.write("0")
        LoginApp().stop()

    def update_news(self, r=True):
        if r == True:
            # Однопоточный:
            sm.get_screen('app').ids.newsnav.remove_widget(self.news_up)
            self.get_news()
            sm.get_screen('app').ids.newsnav.add_widget(self.makenews())
        elif r == "Нажал на расписание":
            pass

    def upgrade_news(self):
        sm.screens[2].ids.rb.size_hint = (0.00001, 0.00001)
        sm.screens[2].ids.lb.size_hint = (0.00001, 0.000001)
        sm.screens[2].ids.schnav.text = "Добавить Новость"
        self.cardnews = MDEmilNewsCard()
        sm.screens[2].ids.schnav.add_widget(self.cardnews)

    def get_upgrade_news(self):
        zagolovok = self.cardnews.ids.get_zag.text
        text_news = self.cardnews.ids.get_text.text
        k = text_news.count('http')
        if k <= 1:

            signup_info = {
                f'{zagolovok}': f'{text_news}'}
            to_database = ast.literal_eval(json.dumps(signup_info))
            print(to_database)
            self.cardnews.ids.get_zag.text = ''

            c = requests.patch(url=self.urlnews, json=to_database)
            print(c, c.reason)
            self.update_news()
        else:
            cancel_btn_username_dialogue = MDFlatButton(text='Ок', on_release=self.close_username_dialog)

            self.dialog = MDDialog(title='Ошибка', text='В тексте новости пока что доступна только 1 ссылка.',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()

    def delite_news(self, nomber):
        if self.password == "69109105108":
            self.nomber = nomber
            cancel_btn_username_dialogue_yes = MDFlatButton(text='Удалить', on_release=self.delite_news_1)
            cancel_btn_username_dialogue = MDFlatButton(text='Отмена', on_release=self.close_username_dialog)
            cancel_btn_username_dialogue_redaction = MDFlatButton(text='Изменить', on_release=self.redactor_news)

            self.dialog = MDDialog(title='Править новость', text='Вы уверены?',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue, cancel_btn_username_dialogue_yes,
                                            cancel_btn_username_dialogue_redaction])
            self.dialog.open()

    def delite_news_1(self, inst):
        nomber = self.nomber
        s = self.news_data[0][nomber - 1][0]
        s = s.replace("%", "PROCENT")
        s = s.replace("\'", "")
        s = s.replace(".", "$")
        s = s.replace(" ", "%20")

        response = requests.delete(f"{self.urlnews[:-5] + s + '.json' + '?auth=' + self.authnews}")
        print(response.json())

        self.update_news()
        self.dialog.dismiss()

    def update_sch(self):
        if self.type == 0:
            sm.get_screen('app').ids.schnav.remove_widget(self.sch[3])
            sm.get_screen('app').ids.schnav.remove_widget(self.sch[0])
            sm.get_screen('app').ids.schnav.remove_widget(self.sch[2])
            sm.get_screen('app').ids.schnav.add_widget(self.makeschledule(self.userclass, f'day{self.weekday}', 2))

        self.dialog.dismiss()

    def delite_acc(self, x):
        cancel_btn_username_dialogue = MDFlatButton(text='Нет', on_release=self.close_username_dialog)
        if x == "acc":
            cancel_btn_username_dialogue_yes = MDFlatButton(text='Да', on_release=self.delite_acc_1)
            self.dialog = MDDialog(title='Перейти в настройки аккаунта?', text='Вы уверены?',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue, cancel_btn_username_dialogue_yes])
        else:
            cancel_btn_username_dialogue_yes = MDFlatButton(text='Да', on_release=self.delite_acc_2)
            self.dialog = MDDialog(title='Удалить аккаунт?', text='Вы уверены?',
                                   size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue, cancel_btn_username_dialogue_yes])
        self.dialog.open()

    def delite_acc_1(self, inst):
        self.accountset = AccountSettings()
        self.basetools = sm.get_screen('app').ids.settools
        sm.get_screen('app').ids.settoll.remove_widget(sm.get_screen('app').ids.settools)
        sm.get_screen('app').ids.settoll.add_widget(self.accountset)
        self.user_info = dict(self.user_info)
        self.accountset.ids.getusername_1.text = self.user_info['Name']
        # response = requests.delete(f"{self.url[:-5] + self.username + '.json' + '?auth=' + self.auth}")
        # print(response.json())
        self.dialog.dismiss()
        # self.exit_acc()

    def delite_acc_2(self, inst):
        response = requests.delete(f"{self.url[:-5] + self.username + '.json' + '?auth=' + self.auth}")
        print(response.json())
        self.dialog.dismiss()
        self.exit_acc()

    def now_pad_move(self, zet):
        self.now_pad = zet

    def redactor_news(self, inst):
        nomber = self.nomber
        s = self.news_data[0][nomber - 1][0]
        s_2 = self.news_data[0][nomber - 1][1]
        s_2 = s_2.split()
        for i in s_2:
            w = i.split('[')
            for j in w:
                if j.startswith("ref="):
                    q = j[j.index('ref=') + 5:j.index(']') - 1]
                    break
        for i in range(len(s_2)):
            if '[ref=' in s_2[i]:
                s_2[i] = q
                break
        s_2 = ' '.join(s_2)
        self.cardnews.ids.get_zag.text = s
        self.cardnews.ids.get_text.text = s_2
        sm.get_screen('app').ids.botnav.switch_tab("screen 2")
        self.dialog.dismiss()

    def openlink(self, id):
        import webbrowser
        text = self.news_data[0][id - 1][1]
        m = text.split('[')
        for i in m:
            if i.startswith('ref='):
                link = i[i.index('ref=') + 5:-1]
                link = link.split("']")
                webbrowser.open(link[0])
                break

    def reborned(self):
        print(self.user_info)
        print(self.accountset.ids)
        user = self.accountset.ids.getusername_1.text
        old_password = self.accountset.ids.old_password.text
        old_password = "".join([str(ord(i)) for i in list(old_password)])
        new_password = self.accountset.ids.new_password.text
        new_password = "".join([str(ord(i)) for i in list(new_password)])
        if old_password != "":
            if old_password == self.user_info['Password']:
                username = self.user_info['Username']
                surname = self.user_info['Surname']
                patronymic = self.user_info['Patronymic']
                sclass = self.user_info['Class']
                self.user_info['Password'] = new_password
                signup_info = str({
                    f'"{username}":{{"Password":"{new_password}","Username":"{username}","Name":"{user}","Surname":"{surname}","Patronymic":"{patronymic}","Class":"{sclass}"}}'})
                signup_info = signup_info.replace(".", "-")
                signup_info = signup_info.replace("\'", "")
                to_database = json.loads(signup_info)
                print((to_database))
                requests.patch(url=self.url, json=to_database)
            else:
                self.accountset.ids.error.text = "Неправильный пароль"


    def back_to_settings(self):
        sm.get_screen('app').ids.settoll.remove_widget(self.accountset)
        sm.get_screen('app').ids.settoll.add_widget(self.basetools)


LoginApp().run()
