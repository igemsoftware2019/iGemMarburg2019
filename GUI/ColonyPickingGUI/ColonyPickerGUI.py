from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from PIL import *
from threading import Thread
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.graphics.svg import Svg

from operator import add

import os
import socket
import ssl
import pickle


host_addr = '10.10.197.166'
host_port = 2973
server_sni_hostname = 'OT-2'
server_cert = 'OT-2/server.crt'
client_cert = 'OT-2/client.crt'
client_key = 'OT-2/client.key'


stp_sz = 0
cps = [0, 0, 150]

Builder.load_file('GUI.kv')


class Root(TabbedPanel):
    mnager = ObjectProperty(None)

    def switch_to(self, header):
        self.manager.current = header.screen
        self.current_tab.state = 'normal'
        header.state= 'down'
        self._current_tab = header

    def OnSliderValueChange(self, value):
        print(self)
        print(value)
    
    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            #self.text_input.text = stream.read()
            print(path)
        self.dismiss_popup()
    
    def connect_ot2(self):
        global conn
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
        context.load_cert_chain(certfile=client_cert, keyfile=client_key)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
        conn.connect((host_addr, host_port))
        print("SSL established. Peer: {}".format(conn.getpeercert()))
        
        ot2_data = pickle.dumps([[['point', 4], ['opentrons_96_tiprack_10ul', 1]],[(0,0,150)]])
        conn.sendall(ot2_data)
        #conn.close()

    def calibrating_ot2(self, button):
        global cps
        global stp_sz
        global conn

        if button.text == 'X+':
            new_cps = map(add, [stp_sz, 0, 0], cps)
        if button.text == 'X-':
            new_cps = map(add, [-stp_sz, 0, 0], cps)
        if button.text == 'Y+':
            new_cps = map(add, [0, stp_sz, 0], cps)
        if button.text == 'Y-':
            new_cps = map(add, [0, -stp_sz, 0], cps)
        if button.text == 'Z+':
            new_cps = map(add, [0, 0, stp_sz], cps)
        if button.text == 'Z-':    
            new_cps = map(add, [0, 0, -stp_sz], cps)
        
        cps = list(new_cps)
        print(cps)
        calib_data = pickle.dumps([[], [tuple(cps)]])

        '''context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
        context.load_cert_chain(certfile=client_cert, keyfile=client_key)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
        conn.connect((host_addr, host_port))
        print("SSL established. Peer: {}".format(conn.getpeercert()))'''

        conn.send(calib_data)    
        #conn.close()

    def disconnect_ot2(self):
        global conn
        print('Disconnecting')
        conn.close()

    def set_step_size(self, togglebutton):
        print(togglebutton.state, togglebutton.text)
        global stp_sz

        if togglebutton.text == '0.1':
            self.ids.stp_adj2.state='normal' 
            self.ids.stp_adj3.state='normal' 
            #self.ids.stp_adj1.state='down' 
            stp_sz = 0.1   
        if togglebutton.text == '1.0':
            self.ids.stp_adj1.state='normal' 
            self.ids.stp_adj3.state='normal'
            #self.ids.stp_adj2.state='down'
            stp_sz = 1
        if togglebutton.text == '10':
            self.ids.stp_adj1.state='normal'
            self.ids.stp_adj2.state='normal'
            #self.ids.stp_adj3.state='down' 
            stp_sz = 10
        return None



class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)



class MainApp(App):
    title = 'Colony Picker GUI'
    def build(self):
        #return RootWidget()
        return Root()
    def on_pause(self):
        return True

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
#Factory.register('MyPopup', cls=MyPopup)

if __name__ == '__main__':
    MainApp().run()