'''
Author: Roy White
Date: 2021-09-12 16:45:29
LastEditTime: 2021-11-20 16:28:01
'''
import tkinter as tk
from tkinter.constants import E, END, N, W

import windnd
# if you would like to test this code, you sould run line 13
class OtWin:
    def __init__(self) -> None:
        # self.root = self.creat_root()
        self.counter = self.createCounter()
        
    
    def creat_root(self, root_title): # create root window
        root = tk.Tk()
        root.title('Omicstools')
        root.geometry('600x400')
        root.iconbitmap("Omics.ico")
        
        l_title = tk.Label(
            root, text=root_title, font=('Black', 20))
        l_title.grid(row=0, column=0, padx=25, pady=5, columnspan=5)

        return root
        # root.mainloop()

        
    def add_menu(self): # edit menu, add new items
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        anly_fa = tk.Menu(menu_bar, tearoff=0)
        easy_blast = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_cascade(label='Analysis fasta file', menu=anly_fa)
        menu_bar.add_cascade(label='Easy blast', menu=easy_blast)

        file_menu.add_cascade(label='New',command=self.main)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        self.root.config(menu=menu_bar)
    

    def new_window(self, win_title): # create new window on root window
        win = tk.Toplevel()
        win.title('Omicstools')
        win.geometry('655x380')
        win.iconbitmap("Omics.ico")

        l_title = tk.Label(
            win, text=win_title, font=('Arial', 20))
        l_title.grid(row=0, column=0, padx=25, pady=5, columnspan=5)

        return win


    def add_Entry(self, win, label, hint): # add input field
        i = self.counter()
        # query label
        l_query = tk.Label(win, text=label)
        l_query.grid(row=i, column=0, padx=5, pady=5)

        # query entry
        query = tk.StringVar()
        query.set(hint)
        e_query = tk.Entry(win, textvariable=query, width=70)
        e_query.grid(row=i, column=1, columnspan=3, padx=5, pady=5)

        OtWin.dragged_files_Entry(e_query, query)
        return query

    def add_Text(self, win, label, hint):
        i = self.counter()
        # label
        t_label = tk.Label(win, text=label)
        t_label.grid(row=i, column=0, padx=5, pady=5, sticky=N)

        # text
        t_list = tk.Text(win, width=70, height=16)
        t_list.insert('end', hint)
        t_list.grid(row=i, column=1,padx=5, pady=5)
        
        OtWin.dragged_files_Text(t_list)
        return t_list


    def add_buttom(self, win, command):
        i = self.counter()
        run = tk.Button(win, text='Run', width=55, command=command)
        run.grid(row=i, column=0, columnspan=5, padx=5,pady=5)
        # win.grid_columnconfigure(0,weight=1)
        # win.grid_rowconfigure(0,weight=1)
        # win.grid_columnconfigure(1,weight=1)
        # win.grid_rowconfigure(1,weight=1)


    def createCounter(self):
        li = [0]
        def counter():
            li[0] += 1
            return li[0]
        return counter


    def dragged_files_Entry(entry, tk_strvar): # dragged file function for Entry
        def dragged_files(files):
            msg = '\n'.join(item.decode('gbk')for item in files)
            entry.delete(0, END)
            tk_strvar.set(msg)
        windnd.hook_dropfiles(entry, func=dragged_files)
    
    
    def dragged_files_Text(t_list): # dragged file function for Text
        def dragged_files(files):
            msg = '\n'.join(item.decode('gbk')for item in files)
            t_list.delete('1.0', 'end')
            t_list.insert('end', msg)
        windnd.hook_dropfiles(t_list, func=dragged_files)

    @staticmethod
    def test(e1, e2, e3):
        e1 = e1.get()
        e2 = e2.get()
        e3 = e3.get('0.0', 'end').rstrip().split('\n')
        print(e1, e2, e3)


    def main(self): # file-new-function
        win = self.new_window('This is a title')
        e1 = self.add_Entry(win, 'This is a Label:', 'This is a guide word.')
        e2 = self.add_Entry(win, 'another Label:', 'Another guide word.')
        e3 = self.add_Text(win, 'This is a Label:', 'This is a text.')
        self.add_buttom(win, lambda:self.test(e1, e2, e3))
        

if __name__=='__main__':
    App = OtWin()
    App.add_menu()
    App.root.mainloop()

    
