# -*- coding: utf-8 -*-
"""
Created on Sun May 23 00:28:46 2021

@author: ntruo
"""



from tkinter import Label, Text, Tk, Canvas, Button
from tkinter import filedialog
from PIL import ImageTk, Image 
import requests
KERAS_REST_API_URL = "http://127.0.0.1:5000/predict"


class MyWindow:
    def __init__(self, window):

        self.window = window
        self.load_btn = Button(window, fg="Green" ,text = "Load Image", command  = self.show_image)
        self.lbl_input = Label(window, text="INPUT")
        self.lbl_img = Label(window)
        self.lbl_input.place(x = 0,y = 100)
        self.lbl_img.place(x = 150,y = 000)
        self.load_btn.place(x = 0,y = 600)
        self.lbl_output = Label(window, text="Prediction", bg="orange", fg="red")
        self.txt_output = Text(window)
        self.lbl_output.place(x = 460,y = 600)
        
        
    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir = "/",
                                              title = "Select a File",
                                              filetypes = (("all files",
                                                            "*.*"),
                                                           ("png files",
                                                            "*.png*"),
                                                           ("jpg files",
                                                            "*.jpg*")))
          
        print(filename)
        return filename

       

    def show_image(self):
        path = self.browseFiles()
        if path != '':
            img = Image.open(path)
            img_resized = img.resize((256*2, 256*2))
            tkimage = ImageTk.PhotoImage(img_resized)
            self.lbl_img.configure(image=tkimage)
            self.lbl_img.image = tkimage
            self.load_api(path)

             
    def load_api(self, path):
        """
        Call API to predcit next word
        """
        files = {
            'input_': open(path, 'rb'),
            'none': 1 
        }

        r = requests.post(KERAS_REST_API_URL, files=files).json()
        self.lbl_output.config(text=r["predictions"])


            
    def load_image(self):
        pass
    
    def command(self):
        pass
   
def main():
    window=Tk()
    mywin=MyWindow(window)
    window.title('Covid-19 prediction')
    window.geometry("850x650")
    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    main()