#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Author: Ruben Dorado
Last modified: October 2016
"""

from Tkinter import Tk, Frame, Text, Scrollbar, StringVar, IntVar, Menu, X, N, BOTH, LEFT, RAISED, HORIZONTAL, _setit, END
from ttk import Frame, Label, Entry, PanedWindow, Button, OptionMenu, Checkbutton
from corpus import Corpus
from processor import TextProcessor
import tkFileDialog

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self)
        self.parent = parent
        self.processor = TextProcessor()

        self.initUI()



    def readCorpus(self, path):
        self.data = Corpus(path)
        self.processor.calculateConditionalFrequency(self.data, self.selCategory.get())
        #self.processor.calculateTotalTermFrequency(self.data)


        self.categoryOption['menu'].delete(0, 'end')
        for attr in self.data.attributes:
            self.categoryOption['menu'].add_command(label=attr, command=lambda v=attr: self.changeCategory(v) )

        self.curdoc=0

        self.txt1.delete('1.0', END)
        self.txt1.insert('1.0', self.data.docs[self.curdoc].text)

    def refreshTextInfo(self):

        if self.selCategory.get() != 'Categories':
            idcat = self.data.attributes.index(self.selCategory.get())
            self.entry1.delete(0, END)
            self.entry1.insert(0, self.data.getAttributeVal(self.curdoc,  self.selCategory.get() ))

        self.txt1.delete('1.0', END)
        self.txt1.insert('1.0', self.data.docs[self.curdoc].text)

        self.applyProcessing()

    def changeCategory(self, value):
        self.selCategory.set(value)
        self.entry1.delete(0, END)
        self.entry1.insert(0, self.data.getAttributeVal(self.curdoc, self.selCategory.get()))
        self.processor.calculateConditionalFrequency(self.data, self.selCategory.get())

    def prevDocument(self):
        if self.curdoc>0:
            self.curdoc-=1
            self.refreshTextInfo()

    def nextDocument(self):
        if self.curdoc<self.data.ndocs-1:
            self.curdoc+=1
            self.refreshTextInfo()

    def popup(self, event):
       print "hello "+str(event.widget)
       self.popupmenu.tk_popup(event.x_root, event.y_root, 0)
       print event.widget.index("@%s,%s" % (event.x, event.y))

    def applyProcessing(self):
        if self.selCategory.get() != 'Categories':
            indxCat = self.data.attributes.index( self.selCategory.get() )
            textResult = self.processor.process(self.data.docs[self.curdoc], indxCat)
        else:
            textResult = ""
        self.txt2.delete('1.0', END)
        self.txt2.insert('1.0', textResult)

    def loadCorpus(self):
	path = tkFileDialog.askdirectory()
        self.readCorpus(path)
	self.refreshTextInfo()

    def hello(self):
        print "Hello"

    def initUI(self):


        self.parent.title("Simple")
        self.pack(fill=BOTH, expand=True)
        self.centerWindow()

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        frame1 = Frame(self, relief=RAISED, borderwidth=1)
        frame1.pack(fill=X)

        button1 = Button(frame1, text=u"<", command=self.prevDocument)
        button1.pack(side=LEFT, padx=5, pady=5)

        button2 = Button(frame1, text=u">", command=self.nextDocument)
        button2.pack(side=LEFT, padx=5, pady=5)


        self.selCategory = StringVar(self)
        self.categoryOption = OptionMenu(frame1, self.selCategory, *["Categories"], command=self.changeCategory)
        self.categoryOption.pack(side=LEFT, padx=5, pady=5)

        self.entry1 = Entry(frame1)
        self.entry1.pack(side=LEFT, padx=5, pady=5)

        self.ignoreActualDocVar = IntVar(self)

        checkButton1 = Checkbutton(frame1, text="Ignored", variable=self.ignoreActualDocVar)
        checkButton1.pack(side=LEFT, padx=5, pady=5)

        button3 = Button(frame1, text=u"Save document", command=self.prevDocument)
        button3.pack(side=LEFT, padx=5, pady=5)

        #entry1 = Entry(frame1)
        #entry1.pack(fill=X, padx=5, expand=True)




        frame2 = PanedWindow(self, orient=HORIZONTAL)
        frame2.pack(fill=BOTH, expand=1)

        self.txt1 = Text(frame2, width=sw/22)
        frame2.add(self.txt1)

        self.txt2 = Text(frame2)
        self.txt2.bind("<Button-3>", self.popup)      
        frame2.add(self.txt2)






        frame3 = Frame(self, relief=RAISED, borderwidth=1)
        frame3.pack(fill=X)

        #lbl3 = Label(frame3, text="Author", width=6)
        #lbl3.pack(side=LEFT, padx=5, pady=5)

        #entry3 = Entry(frame3)
        #entry3.pack(fill=X, padx=5, expand=True)

        self.swVar = IntVar(self)
        checkButton1 = Checkbutton(frame3, text="Remove stop words", variable=self.swVar)
        checkButton1.pack(side=LEFT, padx=5, pady=5)

        self.lowerVar = IntVar(self)
        checkButton1 = Checkbutton(frame3, text="Convert to lower case", variable=self.lowerVar)
        checkButton1.pack(side=LEFT, padx=5, pady=5)

        button3 = Button(frame3, text=u"Apply", command=self.applyProcessing)
        button3.pack(side=LEFT, padx=5, pady=5)

        #self.readCorpus()
        


	# create a toplevel menu
	menubar = Menu(self)


        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=self.parent.quit)
        filemenu.add_command(label="Open corpus", command=self.loadCorpus)
        menubar.add_cascade(label="Project", menu=filemenu)
	#menubar.add_command(label="Quit!")  # , command=root.quit

	# display the menu
	self.parent.config(menu=menubar)

	self.popupmenu = Menu(self.parent, tearoff=0)
	self.popupmenu.add_command(label="Undo", command=self.hello)
	self.popupmenu.add_command(label="Redo", command=self.hello)


    def centerWindow(self):

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        w = sw/1.5
        h = sh/1.5

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

def main():
    root = Tk()
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
