#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ISJ project 2013/2014: Finding and downloading reports of research projects
# Author: Martin Veselovsky, xvesel60
# -----------------------------------

import tkinter as tk, threading
from tkinter import ttk
import spider

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Web spider for scientific documents')
        self.window.geometry('800x600')
        self.window.minsize(width=500, height=500)
        self.frame = tk.Frame(self.window)
        self.createWidgets()
        self.Entry.insert(0, 'http://www.kiwi-project.eu/')

        self.spiders = []
        self.t = None

    def createWidgets(self):
        # adapt for window's resizing
        tk.Grid.rowconfigure(self.window,0,weight=1)
        tk.Grid.columnconfigure(self.window,0,weight=1)

        background = 'lightblue'

        # create frame above whole window for widgets
        self.frame.grid(sticky=tk.W+tk.E+tk.N+tk.S)
        self.frame['bg'] = background

        # menu
        #self.Menu = tk.Menu(self.frame)
        #self.Menu.option_add('aa', 15)

        # widgets
        self.Label_url = tk.Label(self.frame, text='Site url:', bg=background)
        self.Entry = tk.Entry(self.frame)
        self.Button_search = tk.Button(self.frame, text='Search', command=lambda: self.search())
        self.Label_visited = tk.Label(self.frame, text='Visited links:', bg=background)
        self.Button_cancel = tk.Button(self.frame, text='Cancel', comman=lambda: self.cancel())
        self.Visited = tk.Listbox(self.frame, height=5)
        self.Label_reports = tk.Label(self.frame, text='Reports found:', bg=background)
        self.Results = ttk.Treeview(self.frame, columns=('url'))
        self.Results.heading('url', text='url')
        self.Button_download_all = tk.Button(self.frame, text='Download all', command=lambda: self.download_all())
        self.Button_download_selected = tk.Button(self.frame, text='Download selected', command=lambda: self.download_selected())
        self.Label_status = tk.Label(self.frame, bg=background, fg='red')

        # grid settings
        self.frame.columnconfigure(0, pad=5)
        self.frame.columnconfigure(1, pad=10, weight=1)
        self.frame.columnconfigure(2, pad=20)
        self.frame.columnconfigure(3)
        self.frame.rowconfigure(0, pad=10)
        self.frame.rowconfigure(1, pad=5)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(3)
        self.frame.rowconfigure(4, pad=10)
        self.frame.rowconfigure(5, weight=4)
        self.frame.rowconfigure(6)
        self.frame.rowconfigure(7, pad=15)

        # layout of widgets
        self.Label_url.grid(row=0, column=0)
        self.Entry.grid(row=0, column=1, sticky=tk.W+tk.E)
        self.Button_search.grid(row=0, column=2)
        self.Label_visited.grid(row=1, sticky=tk.W)
        self.Button_cancel.grid(row=1, column=2)
        self.Visited.grid(row=2, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S)
        self.Label_reports.grid(row=4, sticky=tk.W)
        self.Results.grid(row=5, columnspan=3, sticky=tk.W+tk.E+tk.N+tk.S)
        self.Button_download_all.grid(row=7)
        self.Button_download_selected.grid(row=7, column=1, sticky=tk.W)
        self.Label_status.grid(row=7, column=2)

        scroll_visited = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.Visited.yview)
        scroll_visited.grid(column=3, row=2, sticky=tk.N+tk.S)
        self.Visited['yscrollcommand'] = scroll_visited.set

        scroll_visited2 = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.Visited.xview)
        scroll_visited2.grid(columnspan=3, row=3, sticky=tk.W+tk.E)
        self.Visited['xscrollcommand'] = scroll_visited2.set

        scroll_results = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.Results.yview)
        scroll_results.grid(column=3, row=5, sticky=tk.N+tk.S)
        self.Results['yscrollcommand'] = scroll_results.set

        scroll_results2 = ttk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.Results.xview)
        scroll_results2.grid(columnspan=3, row=6, sticky=tk.W+tk.E)
        self.Results['xscrollcommand'] = scroll_results2.set


    def search(self):
        self.url = self.Entry.get()
        self.spiders.append( spider.Spider(self.url, self.insert_to_visited, self.insert_to_results) )
        self.t = threading.Thread(target=self.spiders[-1].get)
        self.t.daemon = True
        self.t.start()
        self.Results.insert('', 'end', self.url, text=self.url, tags='nodownload')

    def cancel(self):
        if self.t != None:
            self.spiders[-1].cancel = True

    def insert_to_visited(self, url):
        self.Visited.insert(0, url)
        self.window.update_idletasks()

    def insert_to_results(self, key, value):
        self.Results.insert(self.url, 0, value, text=key, value=value)
        self.window.update_idletasks()

    def download_selected(self):
        selected = self.Results.selection()
        item = self.Results.item(selected[0])
        if len(item['tags']) == 0:
            spider.download_file(item['text'], item['values'][0])
            self.Label_status['text'] = 'Download complete'
        else:
            self.Label_status['text'] = 'Please select report'

    def download_all(self):
        for sp in self.spiders:
            for url, name in sp.results.items():
                spider.download_file(name, url)
        self.Label_status['text'] = 'Download complete'

def main():
    app = App()
    app.window.mainloop()

if __name__ == "__main__":
      main()

# def search():
#     global results
#     s = spider.Spider(e1.get())
#     s.get()
# l1.grid(row=0, column=0)
# e1.grid(row=0, column=1)
# b1.grid(row=0, column=2)
# box.grid(row=1, column=0, columnspan=3)
#
# win.mainloop()