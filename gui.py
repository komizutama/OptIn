from kivy.app import App
from kivy.core.window import Window
from kivy.uix.video import Video
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
import subprocess
import os
import signal

sound = SoundLoader.load('assets/shotgun.wav')

class OptInApp(App):
    def __init__(self):
        super(OptInApp, self).__init__()
        self.state = 'off_initial'
        self.running_pub = None
    def build(self):
        root = Widget()
        self.root = root
        btn = Button(background_normal=self.filename_for_state(),
            pos=(160, 60),
            size=(500, 500))
        btn.bind(on_press=self.callback)
        self.root.add_widget(btn)
        return self.root
    def callback(self, btn):
        if self.state in ["off_initial", "off"]:
            self.state = "on"
        else:
            self.state = "off"
        btn.background_normal = self.filename_for_state()

        # react: processes
        if self.state == 'on':
            sound.play()
            self.running_pub = subprocess.Popen("python OptIn.py | python publisher.py", shell=True, preexec_fn=os.setsid)
        elif self.running_pub != None:
            os.killpg(os.getpgid(self.running_pub.pid), signal.SIGTERM)
            self.running_pub = None

    def filename_for_state(self):
        if self.state == "off_initial":
            filename = 'assets/off_initial.png'
        elif self.state == "on":
            filename = "assets/on.png"
        else:
            filename = "assets/off.png"
        return filename

if __name__ == '__main__':
    OptInApp().run()
