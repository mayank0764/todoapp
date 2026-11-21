import json
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class TodoApp(App):
    def build(self):
        self.title = "To-Do List"
        self.file = os.path.join(self.user_data_dir, "tasks.json")
        self.tasks = self.load_tasks()

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        top = BoxLayout(size_hint_y=None, height=120, spacing=10)
        self.input = TextInput(hint_text="Enter task", multiline=False)
        add_btn = Button(text="Add", size_hint_x=0.3)
        add_btn.bind(on_press=self.add_task)
        top.add_widget(self.input)
        top.add_widget(add_btn)

        scroll = ScrollView()
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=8)
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        scroll.add_widget(self.list_box)

        root.add_widget(top)
        root.add_widget(scroll)
        self.refresh()
        return root

    def load_tasks(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(self.file, "w") as f:
            json.dump(self.tasks, f)

    def add_task(self, instance):
        title = self.input.text.strip()
        if title:
            self.tasks.append({"title": title, "done": False})
            self.input.text = ""
            self.save_tasks()
            self.refresh()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.refresh()

    def delete_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()
        self.refresh()

    def refresh(self):
        self.list_box.clear_widgets()
        for i, t in enumerate(self.tasks):
            row = BoxLayout(size_hint_y=None, height=120, spacing=10)
            mark = "[x] " if t["done"] else "[ ] "
            label = Label(text=mark + t["title"])
            done_btn = Button(text="Done", size_hint_x=0.25)
            done_btn.bind(on_press=lambda x, i=i: self.toggle_task(i))
            del_btn = Button(text="Delete", size_hint_x=0.25)
            del_btn.bind(on_press=lambda x, i=i: self.delete_task(i))
            row.add_widget(label)
            row.add_widget(done_btn)
            row.add_widget(del_btn)
            self.list_box.add_widget(row)


TodoApp().run()
