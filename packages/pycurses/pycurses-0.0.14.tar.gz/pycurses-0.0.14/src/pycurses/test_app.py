from pycurses.window import Window
from pycurses.layout import Layout
from pycurses.mainwindow import MainWindow
from pycurses.list_view import ListView

class TestWindow(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TestApp(MainWindow):

    def __init__(self):
        super().__init__([])
        self.base_layout = Layout(colors=self.colors, defaultchar='.', defaultattr=0)
        self.left = Window(colors=self.colors, defaultchar='L', defaultattr=0)
        self.left.set_name('Left Window')
        self.right_layout = Layout(horizontal=False, colors=self.colors, defaultchar='.', defaultattr=0)
        self.right_layout.set_name('Right Layout')
        self.right = Window(colors=self.colors, defaultchar='.', defaultattr=0)
        self.right.set_min_height(8)
        self.right.set_name('Right Top')

        self.right_bottom  = ListView(headers=['word', 'another', 'third', 'a', 'b'], colors=self.colors, defaultchar='*', defaultattr=0)
        self.right_bottom.set_name('Right Bottom')

        self.right_layout.add_child(self.right, weight=2)
        self.right_layout.add_child(self.right_bottom, weight=5)
        self.base_layout.add_child(self.left, weight=2)
        self.base_layout.add_child(self.right_layout, weight=1)
        self.add_child(self.base_layout)
        self.set_title('VQC')


if __name__ == '__main__':
    TestApp().loop()
