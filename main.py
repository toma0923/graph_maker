from kivy.app import App
from kivy.lang.builder import Builder
Builder.load_file('main.kv')
from kivy.core.window import Window
Window.size = (960, 540)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import matplotlib
import japanize_kivy
import numpy as np


class MainWidget(Screen):
    pass

    
class GraphView(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        fig, ax = plt.subplots()
        x = np.linspace(-4, 4)
        ax.set_xlabel('X label')
        ax.set_ylabel('Y label')
        ax.set_title('Trigonometric functions')
        ax.grid(True)
        ax.plot(x, np.sin(x), label='sin(x)')
        ax.plot(x, np.cos(x), label='cos(x)')
        ax.legend()
        widget = FigureCanvasKivyAgg(fig)
        self.add_widget(widget)


class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainWidget(name='main'))
        self.sm.add_widget(GraphView(name='graph_view'))
        return self.sm


if __name__ == '__main__':
    MyApp().run()