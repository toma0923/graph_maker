from kivy.app import App
from kivy.lang.builder import Builder
Builder.load_file('main.kv')
from kivy.core.window import Window
Window.size = (960, 540)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import StringProperty
import matplotlib.pyplot as plt
import matplotlib
import japanize_kivy
import numpy as np


class MainWidget(Screen):
    # TextInputの値取得変数
    graph_name_text = StringProperty()
    x_name_text = StringProperty()
    x_value_text = StringProperty()
    y_name_text = StringProperty()
    y_value_text = StringProperty()

    # ボタンクリック時
    def on_click(self, **kwargs):
        self.graph_name_text = self.ids.graph_name.text
        self.x_name_text = self.ids.x_name.text
        self.x_value_text = self.ids.x_value.text
        self.y_name_text = self.ids.y_name.text
        self.y_value_text = self.ids.y_value.text

        self.set_graph()

    def set_graph(self):
        graph = GraphView(name='graph_view')

        graph.ax.set_title(self.graph_name_text)
        graph.ax.set_xlabel(self.x_name_text)
        graph.ax.set_ylabel(self.y_name_text)

        x_values = self.split_text(self.x_value_text)
        y_values = self.split_text(self.y_value_text)
        graph.ax.plot(x_values, y_values)

        self.manager.add_widget(graph)

    def split_text(self, text_list):
        return list(map(float, (text_list.split(','))))
        
    
class GraphView(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fig, self.ax = plt.subplots()
        x = np.linspace(-4, 4)
        self.ax.grid(True)
        # self.ax.plot(x, np.sin(x), label='sin(x)')
        # self.ax.plot(x, np.cos(x), label='cos(x)')
        # self.ax.legend()
        widget = FigureCanvasKivyAgg(self.fig)
        self.add_widget(widget)


class GraphMakerApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainWidget(name='main'))
        # self.sm.add_widget(GraphView(name='graph_view'))
        return self.sm


if __name__ == '__main__':
    GraphMakerApp().run()