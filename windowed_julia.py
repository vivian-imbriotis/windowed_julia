import random
import numpy as np
import numpy.ma as ma
from math import pi
from cmath import exp
import os, requests, json
import tkinter as tk
from PIL import Image, ImageTk

WIDTH,HEIGHT = 500,500
ITERS = 20
VIEW = 2
RSHIFT = 2


rgb565 = lambda r,g,b:(
                        (((31*(r+4))//255)<<11)|
                       (((63*(g+2))//255)<< 5)|
                       ((31*(b+4))//255))


def fast_julia(f):
    real_part = np.linspace(-VIEW,VIEW,WIDTH)
    imag_part = np.linspace(-VIEW,VIEW,HEIGHT)
    real_part,imag_part = np.meshgrid(real_part,imag_part)
    state = real_part + 1j*imag_part
    result = np.zeros((HEIGHT,WIDTH),dtype="int")
    for i in range(10):
        state = f(state)
        res = np.heaviside(np.abs(state) - 2,1)
        result += res.astype("int")
        state = ma.masked_array(state,res)
    return result

def fast_julia_exp(f):
    real_part = np.linspace(RSHIFT-VIEW,RSHIFT+VIEW,WIDTH)
    imag_part = np.linspace(-VIEW,VIEW,HEIGHT)
    real_part,imag_part = np.meshgrid(real_part,imag_part)
    state = real_part + 1j*imag_part
    result = np.zeros((HEIGHT,WIDTH),dtype="int")
    for i in range(10):
        state = f(state)
        res = np.heaviside(np.real(state) - 50,1)
        result += res.astype("int")
        state = ma.masked_array(state,res)
    return result
        
def rand_pallet():
    data = '{"model":"default"}'
    response = requests.post('http://colormind.io/api/', data=data)
    if response.status_code != requests.codes.ok:
        raise Exception("Error from colormind lookup")
    pallet = []
    for col in response.json()['result']:
##        pallet.append(rgb565(*col))
        pallet.append(col)
    return pallet


class Window():
    def __init__(self):
        self.master = tk.Tk()
        self.w = tk.Canvas(self.master, width = WIDTH,height=HEIGHT)
        self.w.pack()
    def loop_quadratic(self):  
        modulus = random.uniform(0.4,1.4)
        color = np.asarray(rand_pallet())
        for i in range(ITERS+1):
            j = fast_julia(lambda x:(x*x)+ modulus*exp((0+1j)*i*pi*2/ITERS))
            f = np.vectorize(color.__getitem__,signature = "()->(n)")
            self.img = np.asarray(f(np.mod(j,color.shape[0]))).astype("uint8")
            self.master.update()
            self.master.update_idletasks()
            image = Image.fromarray(self.img)
            self.photo = ImageTk.PhotoImage(image=image)
            self.w.create_image(0,0,anchor='nw',image=self.photo)
            self.w.pack()
            self.master.update()
            self.master.update_idletasks()
    def loop_exp(self):
        modulus = random.uniform(0.9,1.1)
        color = np.asarray(rand_pallet())
        for i in range(ITERS+1):
            j = fast_julia_exp(lambda x:np.exp(x)*modulus*exp(2*pi*1j*i/ITERS))
            f = np.vectorize(color.__getitem__,signature = "()->(n)")
            self.img = np.asarray(f(np.mod(j,color.shape[0]))).astype("uint8")
            self.master.update()
            self.master.update_idletasks()
            image = Image.fromarray(self.img)
            image.save("%d.jpeg"%i,"JPEG")
            self.photo = ImageTk.PhotoImage(image=image)
            self.w.create_image(0,0,anchor='nw',image=self.photo)
            self.w.pack()
            self.master.update()
            self.master.update_idletasks()

my_window = Window()
while True:
    my_window.loop_exp()










