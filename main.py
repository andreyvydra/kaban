import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter, QColor, QPixmap

from ui_mw_design import Ui_MainWindow
from ui_task_dialog_design import Ui_Dialog
from ui_show_statistics import Ui_Form
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QDialog, QColorDialog, QVBoxLayout,
                             QLabel, QStyleOption, QStyle, QPushButton,
                             QHBoxLayout, QSizePolicy)

DB_FILE = 'tasks.db'


class KanbanBoard(QMainWindow, Ui_MainWindow):
    """ Класс KanbanBoard отвечает за работу главного окна программы """

    def __init__(self):
        super().__init__()
        self.done = []
        self.todo = []
        self.progress = []

        # Присваиваем MainWindow диалог для добавления задач
        self.dialog = TaskDialog()
        self.dialog.close()

        self.statistics_widget = StatisticsWidget()
        self.statistics_widget.close()

        self.setupUi(self)

        self.dialog.accepted.connect(self.run_addition)
        self.actionAdd_task.triggered.connect(self.run_dialog_task)
        self.actionShow_statistics.triggered.connect(self.run_show_statistics)

        self.con = sqlite3.connect(DB_FILE)
        self.cur = self.con.cursor()
        self.initDb()
        self.load_data()

    def load_data(self):
        """ Подгрузка всех задач из базы данных """

        res = self.get_all_tasks_from_table()
        for info in res:
            task = Task(info[1:], info[0], self)
            self.add_task(task, info[1:])

    def initDb(self):
        """ Создание таблиц в базе данных для, если созданы,
         то просто игнорируем ошибку и идём дальше"""

        try:
            self.create_colors_table()
            self.create_groups_table()
            self.create_tasks_table()
            self.con.commit()
        except sqlite3.OperationalError:
            pass

    def run_show_statistics(self):
        self.statistics_widget.set_data(self)
        self.statistics_widget.exec()

    def run_dialog_task(self):
        self.dialog.exec()

    def add_task(self, task, info):
        """Добавление задачи в layout и список соответствующей группы
        Args:
            task: объект класса Task
            info: list с данными о задаче
        """

        if info[2] == 'to do':
            self.toDoLayout.addWidget(task)
            self.todo.append(task)
        elif info[2] == 'progress':
            self.progressLayout.addWidget(task)
            self.progress.append(task)
        else:
            self.doneLayout.addWidget(task)
            self.done.append(task)

    def run_addition(self):
        """Метод вызываемый нажатием на кнопку в dialog и выполняющий
        весь процесс создания задачи"""

        try:
            info = self.dialog.get_info()
            self.add_task_to_table(info)
            self.make_task(info)
            self.dialog.__init__(*info)
            self.dialog.accepted.connect(self.run_addition)
            self.con.commit()
        except Exception as e:
            print(f'Ошибка добавления задачи {e}')

    def make_task(self, info):
        """ Создание задачи, с последующим добавлением через add_dialog
        Args:
            info: list с данными о задаче
        """

        task_id = self.get_cur_task_id_from_table()
        task = Task(info, task_id, self)
        self.add_task(task, info)

    def connect_to_db(self):
        self.con = sqlite3.connect(DB_FILE)
        self.cur = self.con.cursor()

    def add_task_to_table(self, info):
        """ Добавление задачи в таблицу
        Args:
            info: list с данными о задаче
        """
        color_task = self.get_color(info[4])

        color_text = self.get_color(info[3])

        group = self.get_group_id_from_table(info[2])
        self.cur.execute(f'INSERT INTO tasks("header", "description",' +
                         f' "color_task", "color_text", "column") ' +
                         f'VALUES ("{info[0]}", "{info[1]}",' +
                         f' "{color_task[0]}", "{color_text[0]}",' +
                         f' "{group[0]}")')
        self.con.commit()

    def set_task_to_table(self, task):
        """ Изменение задачи в таблице
        Args:
            task: объект класса Task
        """
        task_color = self.get_color(task.task_color)

        text_color = self.get_color(task.text_color)

        group = self.get_group_id_from_table(task.col)[0]
        self.cur.execute('UPDATE tasks \n' +
                         f'SET header="{task.header}",' +
                         f' description="{task.description}",' +
                         f' color_task="{task_color[0]}",' +
                         f' color_text="{text_color[0]}"' +
                         f'WHERE id="{task.task_id}"').fetchall()
        self.cur.execute('UPDATE tasks \n' +
                         f'SET column="{group}" \n' +
                         f'WHERE id="{task.task_id}"').fetchall()
        self.con.commit()

    def add_color_to_table(self, color):
        """ Добавление в таблицу цвета
        Args:
            color: цвет вида #ffffff
        """

        self.cur.execute('INSERT INTO colors("title")' +
                         f' VALUES ("{color}")').fetchone()
        self.con.commit()

    """ 5 методов для получения информации из базы данных """

    def get_color(self, color):
        cur_color = self.get_color_id_from_table(color)
        if not cur_color:
            self.add_color_to_table(color)
            cur_color = self.get_color_id_from_table(color)
        return cur_color

    def get_color_id_from_table(self, color):
        return self.cur.execute('SELECT id FROM colors \n' +
                                f'WHERE title="{color}"').fetchone()

    def get_group_id_from_table(self, group):
        return self.cur.execute('SELECT id FROM groups \n' +
                                f'WHERE title="{group}"').fetchone()

    def get_cur_task_id_from_table(self):
        return self.cur.execute('SELECT MAX("id") FROM tasks').fetchone()[0]

    def get_all_tasks_from_table(self):
        res = self.cur.execute('''SELECT tasks.id,
                                  tasks.header, 
                                  tasks.description, 
                                  groups.title,
                                  colors.title
                                  FROM tasks
                                  INNER JOIN groups
                                  ON tasks.column = groups.id
                                  INNER JOIN colors
                                  ON tasks.color_text = colors.id
                                  ''').fetchall()
        colors = self.cur.execute("""SELECT colors.title FROM tasks
                                     INNER JOIN colors
                                     WHERE tasks.color_task = colors.id
                                     """).fetchall()
        return [res[i] + colors[i] for i in range(len(res))]

    def delete_task_from_table(self, task):
        self.cur.execute('DELETE from tasks \n' +
                         f'WHERE id = {task.task_id}').fetchall()
        self.con.commit()

    """ 3 метода для инициализации таблиц """

    def create_tasks_table(self):
        self.cur.execute('''CREATE TABLE tasks (
                            id          INTEGER PRIMARY KEY AUTOINCREMENT
                                                UNIQUE
                                                NOT NULL,
                            header      TEXT    NOT NULL,
                            description TEXT,
                            color_task  INTEGER NOT NULL
                                                REFERENCES colors (id),
                            color_text  INTEGER NOT NULL
                                                REFERENCES colors (id),
                            [column]     INTEGER REFERENCES groups (id) 
                                                NOT NULL
                            );''').fetchall()

    def create_colors_table(self):
        self.cur.execute('''CREATE TABLE colors (
                            id    INTEGER PRIMARY KEY AUTOINCREMENT
                                          UNIQUE
                                          NOT NULL,
                            title STRING  NOT NULL
                            );''').fetchall()

    def create_groups_table(self):
        self.cur.execute('''CREATE TABLE groups (
                            id    INTEGER PRIMARY KEY AUTOINCREMENT
                                          UNIQUE
                                          NOT NULL,
                            title STRING  NOT NULL
                            );''').fetchall()
        self.cur.execute('''INSERT INTO groups("title") VALUES ("to do"),
                            ("progress"), ("done")''').fetchall()


class Task(QWidget):
    """ Класс Task - виджет, который служит отображением задачи
    для пользователя, а также хранит и обрабатывает собственную
    информацию. """

    def __init__(self, info, task_id, mw):
        super().__init__()

        # Сдоздание атрибута mw для сохранения MainWindow для последующего
        # вызова методов и переменных этого класса
        self.mw = mw

        self.task_id = task_id
        self.header = info[0]
        self.description = info[1]
        self.col = info[2]
        self.text_color = info[3]
        self.task_color = info[4]

        # Сразу добавим vertical layout в наш виджет
        self.setLayout(QVBoxLayout())
        self.installEventFilter(self)

        self.initUi()

        # Создадим диалог для нашего виджета
        self.init_dialog()

    def init_dialog(self):
        self.dialog = TaskDialog(self.header, self.description, self.col,
                                 self.text_color, self.task_color, True)
        self.dialog.close()

        self.dialog.accepted.connect(self.update_task)
        self.dialog.del_button.clicked.connect(self.delete_task_from_group)

    def initUi(self):
        """Удаление всех вложенных виджетов в vertical layout для
        того, чтобы легче добавить изменения текста и цвета задачи """

        while self.layout().count():
            child = self.layout().takeAt(0)
            if isinstance(child, QHBoxLayout):
                while child.count():
                    child.takeAt(0).widget().deleteLater()
                child.deleteLater()
            else:
                child.widget().deleteLater()

        self.set_header()
        self.set_desc()
        self.set_change_group_buttons()
        self.set_sizes()
        self.set_bg_style()

    def set_header(self):
        header = QLabel(self.header)
        header.adjustSize()
        header.setFont(QFont('Arial', 18, 2, False))
        header.setStyleSheet(f'color: {self.text_color}')
        header.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.layout().addWidget(header)

    def set_desc(self):
        desc = QLabel(self.description)
        desc.adjustSize()
        desc.setStyleSheet(f'color: {self.text_color}')
        desc.setFont(QFont('Arial', 10, 2, False))
        desc.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.layout().addWidget(desc)

    def set_change_group_buttons(self):
        horizontal_layout = QHBoxLayout()
        self.left_button = ChangeGroupButton('<')
        self.right_button = ChangeGroupButton('>')
        self.left_button.clicked.connect(self.click_change_group_button)
        self.right_button.clicked.connect(self.click_change_group_button)
        horizontal_layout.addWidget(self.left_button, 1)
        horizontal_layout.addWidget(self.right_button, 1)
        self.layout().addLayout(horizontal_layout)

    def set_sizes(self):
        self.setMinimumHeight(275)
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)
        self.setMaximumHeight(400)

    def click_change_group_button(self):
        if self.sender().text() == '>':
            if self.col == 'to do':
                self.dialog.progressButton.setChecked(True)
            elif self.col == 'progress':
                self.dialog.doneButton.setChecked(True)
        else:
            if self.col == 'done':
                self.dialog.progressButton.setChecked(True)
            elif self.col == 'progress':
                self.dialog.todoButton.setChecked(True)
        self.update_task()

    def set_bg_style(self):
        color = self.task_color
        self.setStyleSheet(f'background-color: {color};'
                           f'border-radius: 50px;'
                           'margin: 5px;')

    def update_task(self):
        """ Обновление всей информации после диалога с юзером """

        try:
            info = self.dialog.get_info()
            self.header = info[0]
            self.description = info[1]
            self.text_color = info[3]
            self.task_color = info[4]

            if self.col != info[2]:
                self.col = info[2]
                self.delete_task_from_group()
                self.mw.add_task(self, info)
                self.mw.set_task_to_table(self)

            self.initUi()
            self.init_dialog()
        except Exception as e:
            print(f'Ошибка обновления задачи {e}')

    def delete_task_from_group(self):
        """ Удаление задачи из группы """

        if self in self.mw.done:
            del self.mw.done[self.mw.done.index(self)]
            self.mw.doneLayout.removeWidget(self)
        elif self in self.mw.progress:
            del self.mw.progress[self.mw.progress.index(self)]
            self.mw.progressLayout.removeWidget(self)
        else:
            del self.mw.todo[self.mw.todo.index(self)]
            self.mw.toDoLayout.removeWidget(self)

        if isinstance(self.sender(), QPushButton) and \
                not self.sender().text() in ['<', '>']:
            self.dialog.close()
            self.deleteLater()
            self.mw.delete_task_from_table(self)

    def mousePressEvent(self, event):
        self.dialog.exec()

    def eventFilter(self, QObject, QEvent):
        """ Метод переопределён для корректной работы
         кнопок в виджете
         Args:
             QObject: объект принимающий event
             QEvent: событие
         Returns:
             True или рекурсия до True
         """

        if QEvent.type() == QEvent.Enter:
            if not self.right_button.isVisible() or \
                    not self.left_button.isVisible():
                if self.col != 'done':
                    self.right_button.change_visible()
                if self.col != 'to do':
                    self.left_button.change_visible()
            return True
        elif QEvent.type() == QEvent.Leave:
            if self.right_button.isVisible() or \
                    self.left_button.isVisible():
                if self.col != 'done':
                    self.right_button.change_visible()
                if self.col != 'to do':
                    self.left_button.change_visible()
            return True
        return super(Task, self).eventFilter(QObject, QEvent)

    def paintEvent(self, event):
        """ Метод переопределён для корректной работы стилей
        для класса Task, унаследованного от QWidget
        Args:
            event: событие
        """

        opt = QStyleOption()
        opt.initFrom(self)
        qp = QPainter(self)
        style = self.style()
        style.drawPrimitive(QStyle.PE_Widget, opt, qp, self)


class ChangeGroupButton(QPushButton):
    """Кнопка для виджета задачи"""

    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setAutoFillBackground(True)
        self.installEventFilter(self)
        self.setFont(QFont('Arial', 19, 2, False))
        self.setVisible(False)
        self.setStyleSheet('QPushButton {'
                           'border-radius: 50px;'
                           'border: none;'
                           '}'
                           'QPushButton:pressed {'
                           f'color: #222222;'
                           '}')

    def change_visible(self):
        self.setVisible(not self.isVisible())


class StatisticsWidget(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_data(self, mw):
        """ Обновление данных для виджета
        Args:
            mw: MainWindow
        """
        fsum = len(mw.todo) + len(mw.progress) + len(mw.done)
        self.quantity.setText(str(fsum))
        self.todo.setText(str(len(mw.todo)))
        self.progress.setText(str(len(mw.progress)))
        self.done.setText(str(len(mw.done)))
        if len(mw.done):
            percent_done = (len(mw.done) / fsum) * 100
        else:
            percent_done = 0
        self.percentDone.setText(str(round(percent_done)) + '%')
        if percent_done < 30:
            self.status.setText('Вам нужно поднажать!')
            self.pixmap = QPixmap('img/bronze_medal.png')
        elif percent_done < 60:
            self.status.setText('У вас хорошая продуктивность!')
            self.pixmap = QPixmap('img/silver_medal.png')
        else:
            self.status.setText('Вы настоящий трудоголик!')
            self.pixmap = QPixmap('img/gold_medal.png')
        self.medal.setPixmap(self.pixmap)


class TaskDialog(QDialog, Ui_Dialog):
    def __init__(self, header=None, desc=None, col=None,
                 text_color='#000000', task_color='#ffaa00',
                 del_button=False):
        super().__init__()
        self.current_text_color = text_color
        self.current_task_color = task_color

        self.text_color = text_color
        self.task_color = task_color
        self.header_t = header
        self.description_t = desc
        self.col = col

        self.setupUi(self)
        self.initUi()

        self.buttonBox.accepted.disconnect()
        self.buttonBox.accepted.connect(self.check_info)
        self.buttonBox.rejected.connect(self.close)
        self.textColorButton.clicked.connect(self.text_color_dialog)
        self.taskColorButton.clicked.connect(self.task_color_dialog)

        self.set_bg_colors_to_widgets()

        if del_button:
            self.init_del_button()

    def initUi(self):
        """Заполнение всей информации о задаче для того, чтобы
        пользователь мог её видеть"""

        text = self.header_t
        if text is None:
            text = 'Новая задача'
        self.header.setText(text)
        self.description.setPlainText(self.description_t)

        if self.col is not None:
            if self.col == 'to do':
                self.todoButton.setChecked(True)
            elif self.col == 'progress':
                self.progressButton.setChecked(True)
            else:
                self.doneButton.setChecked(True)

    def set_bg_color_to_widget(self, color, widget):
        widget.setStyleSheet(f'background-color: {color}')

    def set_bg_colors_to_widgets(self):
        self.set_bg_color_to_widget(self.text_color, self.widgetColorText)
        self.set_bg_color_to_widget(self.task_color, self.widgetColorTask)

    def init_del_button(self):
        del_button = QPushButton()
        del_button.setText('Удалить задачу')
        self.del_button = del_button
        self.del_button.setStyleSheet('background-color: #777777;'
                                      'color: #ffffff;')
        self.gridLayout.addWidget(del_button, 6, 1, 1, 4)

    def closeEvent(self, QCloseEvent):
        self.initUi()
        self.set_bg_colors_to_widgets()
        self.reject()

    def check_info(self):
        """Проверка информации для того, чтобы при нажатии
        в диалоге на 'ok' сохранилась корректная информация,
        а если присутствуют ошибки при вводе, то не сохранять и
        предупредить пользователя о данном"""

        try:
            self.get_info()
            self.set_bg_colors_to_widgets()
            self.accept()
            self.del_error_msg()
        except:
            self.set_error_msg()
            print('Ошибка проверки информации')

    def set_error_msg(self):
        self.err_msg.setText('Неверный ввод')

    def del_error_msg(self):
        self.err_msg.setText('')

    """ последующие 2 функции для выбора цвета и
    сохранения результата в атрибут """

    def text_color_dialog(self):
        text_color = QColor(self.current_text_color)
        dialog = QColorDialog()
        if text_color is None:
            text_color = Qt.White
        dialog.setCustomColor(0, text_color)
        color = dialog.getColor()
        if color.isValid():
            self.current_text_color = color.name()
            self.set_bg_color_to_widget(self.current_text_color,
                                        self.widgetColorText)

    def task_color_dialog(self):
        task_color = QColor(self.current_task_color)
        dialog = QColorDialog()
        if task_color is None:
            task_color = Qt.white
        dialog.setCustomColor(0, task_color)
        color = dialog.getColor()
        if color.isValid():
            self.current_task_color = color.name()
            self.set_bg_color_to_widget(self.current_task_color,
                                        self.widgetColorTask)

    def get_info(self):
        """ Сбор и возврат информации или вызов ошибки
        Returns:
            list, состоящий из информации о задаче
        """

        header = self.header.text()
        desc = self.description.toPlainText()
        if header == '':
            raise Exception
        if self.current_task_color is None or self.current_text_color is None:
            raise Exception
        if self.doneButton.isChecked():
            col = 'done'
        elif self.todoButton.isChecked():
            col = 'to do'
        elif self.progressButton.isChecked():
            col = 'progress'
        else:
            raise Exception
        return [header, '\n'.join(desc.split('\n')[:7]), col,
                self.current_text_color, self.current_task_color]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kb = KanbanBoard()
    kb.show()
    sys.exit(app.exec())
