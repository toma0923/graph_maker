from kivy.app import App
from kivy.lang.builder import Builder
Builder.load_file('main.kv')
from kivy.core.window import Window
Window.size = (960, 540)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.properties import StringProperty
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import math
import numpy as np
import japanize_kivy

# import os, sys
# from kivy.resources import resource_add_path


SEED = 1
# DEGREE = 20
SPLIT_DISTANCE = 0.1 # 2点のランダム点の距離を0.1の長さに分割する

class MainWidget(Screen):

    line_state = "curve"

    # ボタンクリック時
    def on_click(self, **kwargs):
        self.graph_name_text = self.ids.graph_name.text
        self.x_name_text = self.ids.x_name.text
        self.y_name_text = self.ids.y_name.text
        self.x_value_text = []
        self.y_value_text = []
        for x_text in self.ids.num_x.children:
            self.x_value_text.append(x_text.text)
        for y_text in self.ids.num_y.children:
            self.y_value_text.append(y_text.text)


        self.set_graph()
        if self.check_xy_values():
            self.plot()
            self.manager.current = 'graph_view'

    def set_graph(self):
        self.graph = GraphView(name='graph_view')

        self.graph.ax.set_title(self.graph_name_text)
        self.graph.ax.set_xlabel(self.x_name_text)
        self.graph.ax.set_ylabel(self.y_name_text)

        self.x_values = [self.split_text(x) for x in self.x_value_text]
        self.y_values = [self.split_text(y) for y in self.y_value_text]
        print(self.x_values, self.y_values)

    def plot(self):
        if self.line_state == "curve":
            for x_value, y_value in zip(self.x_values, self.y_values):
                self.plot_curve(x_value, y_value)
        elif self.line_state == "line":
            for x_value, y_value in zip(self.x_values, self.y_values):
                self.plot_line(x_value, y_value)

        self.manager.add_widget(self.graph)

    def plot_split(self, x_val1, x_val2, y_val1, y_val2, x_medium_points, y_medium_points):
        """
        各ランダム点の中間点を生成するメソッド
        (x_val1, y_val1), (x_val2, y_val2): 2点のランダム点
        x_medium_points: 中間点のx座標をすべて格納する配列
        y_medium_points: 中間点のy座標をすべて格納する配列
        """
        # 2点のランダム点の距離を計算
        distance = math.sqrt(math.pow(x_val2 - x_val1, 2) + math.pow(y_val2 - y_val1, 2))
        # 必要な中間点の数を計算
        spl_num = math.floor(distance / SPLIT_DISTANCE)
        # 2点のランダム点を分割する. (x, y)が中間点の座標
        x_ = np.linspace(x_val1 ,x_val2, spl_num)
        y_ = np.linspace(y_val1 ,y_val2, spl_num)
        # 中間点を追加する
        x_medium_points = np.append(x_medium_points, x_)
        y_medium_points = np.append(y_medium_points, y_)
        return x_medium_points, y_medium_points
    
    def plot_curve(self, x_data, y_data):
        """
        近似曲線を描画するメソッド
        """
        np.random.seed(seed=SEED)
        plt.figure(figsize=(8.0, 6.0))

        x = np.array(x_data)
        y = np.array(y_data)
        SIZE = len(x)
        DEGREE = 2 * SIZE
        x_medium_points = np.empty(0) # すべての中間点のx座標を格納するndarray
        y_medium_points = np.empty(0) # すべての中間点のy座標を格納するndarray
        # すべてのランダム点間を分割するループ
        for i in range(SIZE - 1):
            x_medium_points, y_medium_points = self.plot_split(
                x[i], x[i + 1], y[i], y[i + 1], x_medium_points, y_medium_points
            )
        coeff = np.polyfit(x_medium_points, y_medium_points, DEGREE)
        y_polyfit = np.poly1d(coeff)(x_medium_points)

        self.graph.ax.scatter(self.x_values, self.y_values, color='k', marker='o')
        self.graph.ax.plot(x_medium_points, y_polyfit, color='k')

    def plot_line(self, x_data, y_data):
        xnew = np.array(x_data)
        y_array = np.array(y_data)
        # 線型近似
        kijunkeisu, sekisuchikeisu = np.polyfit(xnew, y_array, 1)
        ynew = kijunkeisu*xnew + sekisuchikeisu

        self.graph.ax.scatter(x_data, y_data, color='k')
        self.graph.ax.plot(xnew, ynew, color='k')
          

    def split_text(self, text_list):
        try:
            values = list(map(float, (text_list.split(','))))
        except:
            return False

        return values
    
    def check_xy_values(self):
        """x_valuesとy_valuesが有効な値になっているかチェック"""
        self.reset_text_field()

        if not self.x_values:
            self.ids.x_value.hint_text = "無効な値です"
            return False
        elif not self.y_values:
            self.ids.y_value.hint_text = "無効な値です"
            return False
        elif len(self.x_values) != len(self.y_values):
            self.ids.x_value.hint_text = "x軸とy軸の値の数が一致しません"
            self.ids.y_value.hint_text = "x軸とy軸の値の数が一致しません"
            return False
        
        return True
    
    def reset_text_field(self):
        """無効な入力の時に入力欄をリセットする"""
        self.ids.x_value.text = ""
        self.ids.y_value.text = ""

    def on_press_line_check(self):
        self.ids.curve_check.state = 'normal'
        self.line_state = "line"
        print(self.line_state)

    def on_press_curve_check(self):
        self.ids.line_check.state = 'normal'
        self.line_state = "curve"
        print(self.line_state)

    def on_press_plus(self):
        """グラフの本数を増やす"""
        if len(self.ids.num_x.children) <= 2:
            self.ids.num_x.add_widget(TextInput(hint_text="x軸の値(1,2,3,4,5,... のように入力してください)"))
            self.ids.num_y.add_widget(TextInput(hint_text="y軸の値(1,2,3,4,5,... のように入力してください)"))

    def on_press_minus(self):
        """グラフの本数を減らす"""
        if len(self.ids.num_x.children) >= 2:
            self.ids.num_x.remove_widget(self.ids.num_x.children[0])
            self.ids.num_y.remove_widget(self.ids.num_y.children[0])

    
class GraphView(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.set_graph()

    def set_graph(self):
        self.fig, self.ax = plt.subplots()
        self.ax.grid(True)
        widget = FigureCanvasKivyAgg(self.fig)
        self.ids.graph_layout.add_widget(widget, len(self.children))

        widget.size_hint_x = 0.9

    def save_photo(self):
        self.fig.savefig("graph.png")

class GraphApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainWidget(name='main'))
        # self.sm.add_widget(GraphView(name='graph_view'))
        return self.sm


if __name__ == '__main__':
    # # these lines should be added
    # if hasattr(sys, '_MEIPASS'):
    #     resource_add_path(os.path.join(sys._MEIPASS))
    # ###
    GraphApp().run()