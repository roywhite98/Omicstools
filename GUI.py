'''
Descripttion: 
version: 
Author: Roy White
Date: 2021-08-09 16:35:29
'''

from os import fspath, remove
from re import M
import tkinter as tk
import threading
from tkinter.constants import E, END, W, S, N
from typing import Collection, ForwardRef, Sequence
import functions as func
import OTFasta as ot
import tkinter.messagebox
import windnd
import re
import tkinter
from PIL import Image, ImageTk
from GUI_elements import OtWin


def main():
    threading.Thread(target=gui_thread).start()


def gui_thread():
    root = tk.Tk()
    root.title('Omicstools')
    # root.geometry('600x400')
    center_window(root, 420, 420)
    root.iconbitmap("Omics.ico")
    app = App(root)
    root.mainloop()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height,
                            (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)


class App:
    def __init__(self, root):
        self.frame = tk.Frame(root, padx=5, pady=5, bd=5,
                              relief='groove')  # bd:borderwidth
        self.frame.grid()

        img_open = Image.open("shark.jpg")
        global img_png
        img_png = ImageTk.PhotoImage(img_open)
        label_img = tkinter.Label(self.frame, image=img_png)
        label_img.pack()

        # self.welcome = tk.Label(self.frame, text='Life flies', font=('Times new roman',40))
        # self.welcome.grid()
        self.load_menu(root)

    # Load menu

    def load_menu(self, root):
        # load menu bar
        menu_bar = tk.Menu(root)
        # add menu items
        file_menu = tk.Menu(menu_bar, tearoff=0)
        anly_fa = tk.Menu(menu_bar, tearoff=0)
        easy_blast = tk.Menu(menu_bar, tearoff=0)

        # load menu items
        menu_bar.add_cascade(label='File', menu=file_menu)
        menu_bar.add_cascade(label='Analysis fasta file', menu=anly_fa)
        menu_bar.add_cascade(label='Easy blast', menu=easy_blast)

        # File
        file_menu.add_cascade(label='New')
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        # Fasta analysis
        anly_fa.add_cascade(label='Merge fasta files', 
                            command=self.merge)
        anly_fa.add_cascade(label='Fasta analysis',
                            command=self.fasta_analysis)
        anly_fa.add_cascade(label='Fasta compare',
                            command=self.compare_fasta_files)
        anly_fa.add_cascade(label='Duplicate delete',
                            command=self.duplicate_delete)
        anly_fa.add_cascade(label='Reverse complement',
                            command=self.reverse_complement)
        anly_fa.add_cascade(label='CRISPR', 
                            command=self.CRISPR_primer_designer)
        anly_fa.add_cascade(label='Gerenal primer designer', 
                            command=self.gerenal_primer_designer)
                            

        # Easy_blast
        easy_blast.add_cascade(label='BLAST', command=self.easy_blast)

        # load menu bar
        root.config(menu=menu_bar)

    # 下面这个函数解释器和括号加self差不多，但是将其转化为静态方法，可以避免类类型缺参数的报错
    # 具体原因未知，反正这样就跑通了
    @staticmethod
    # function: merge fasta file
    def merge():
        win = App.new_window('MERGE FASTA FILES')

        t_dirlist = tk.Text(win, width=90, height=18)
        # windnd.hook_dropfiles(t_dirlist, func=dragged_files)
        t_dirlist.insert(
            'end', 'Input file directories like: \n C:/document1/document2/filenames...')
        t_dirlist.grid(row=1, column=1, padx=25, pady=5)
        App.dragged_files_Text(t_dirlist)

        l_outfile = tk.Label(win, text='Out File:')
        l_outfile.grid(row=2, column=1, sticky=W, padx=25, pady=5)
        ##

        out_file = tk.StringVar()
        out_file.set('Out file directory...')
        e_outfile = tk.Entry(win, textvariable=out_file, width=70)
        App.dragged_files_Entry(e_outfile, out_file)

        e_outfile.grid(row=2, column=1)
        
        ##
        # Merge fasta file
        def merge_list():
            dirs = t_dirlist.get('0.0', 'end').rstrip().split('\n')
            file_name = out_file.get()
            func.merge_fasta(dirs, file_name)

        b = tk.Button(win, text='merge', command=merge_list)
        b.grid(row=2, column=1, sticky=E, padx=25, pady=5)

    @staticmethod
    # Analysis fasta file
    def fasta_analysis():
        #
        win_fa = App.new_window('FASTA FILES ANALYSIS')
        
        # initial button, sucessed or failed
        def initial():
            global Fa
            try:
                Fa = ot.Fasta(e_in_file.get())
                tkinter.messagebox.showinfo(
                    'Information', 'Initialize finished')
            except:
                tkinter.messagebox.showerror(
                    'Error', 'Initialize failed, check the directory!')

        def count_seq():
            file_size = str(func.get_FileSize(e_in_file.get()))
            seq_num = Fa.count
            seq_len = Fa.seq_len
            tkinter.messagebox.showinfo(
                'Count seq', f'Sequences number: {seq_num}\n'
                + f'File size: {file_size} MB\n '
                + f'Seq len: {seq_len} bp')

        
        ##
        l_input = tk.Label(win_fa, text='Fasta directory: ')
        l_input.grid(row=1, column=0, padx=5, pady=5)
        ##

        def dragged_files(files):
            msg = '\n'.join(item.decode('gbk')for item in files)
            e_in_file.delete(0, END)
            in_file.set(msg)

        in_file = tk.StringVar()
        in_file.set('Input a fasta file...')
        e_in_file = tk.Entry(win_fa, textvariable=in_file, width=70)
        windnd.hook_dropfiles(e_in_file, func=dragged_files)
        e_in_file.grid(row=1, column=1)
        ##
        b_init = tk.Button(win_fa, text='Initialize...', command=initial)
        b_init.grid(row=1, column=2, padx=5)
        ##
        b_count_seq = tk.Button(win_fa, text='count seq', command=count_seq)
        b_count_seq.grid(row=3)


    @staticmethod
    def easy_blast():
        win = App.new_window('EASY BLAST',row=0, column=2, padx=25, pady=5, sticky=W)

        # query
        # query label
        l_in_file = tk.Label(win, text='Query: ')
        l_in_file.grid(row=1, column=0, padx=5, pady=5)

        # query entry
        query = tk.StringVar()
        query.set('Input a fasta file...')
        e_query = tk.Entry(win, textvariable=query, width=70)
        e_query.grid(row=1, column=1, columnspan=3)

        # query entry dragged func
        App.dragged_files_Entry(e_query, query)

        # Select seq type
        q_v = tk.StringVar()
        q_v.set(3)
        radio1 = tk.Radiobutton(win, text="nucl",
                                variable=q_v, value='nucl')
        radio1.grid(row=2, column=1, sticky=W)
        radio2 = tk.Radiobutton(win, text="prot",
                                variable=q_v, value='prot')
        radio2.grid(row=2, column=2, sticky=W)

        # database
        # db label
        l_in_file = tk.Label(win, text='Database: ')
        l_in_file.grid(row=3, column=0, padx=5, pady=5)

        # db entry
        db = tk.StringVar()
        db.set('Input a fasta file...')
        e_db = tk.Entry(win, textvariable=db, width=70)
        e_db.grid(row=3, column=1, columnspan=3)

        # db entry dragged func
        App.dragged_files_Entry(e_db, db)

        # Select seq type
        db_v = tk.StringVar()
        db_v.set(3)
        radio1 = tk.Radiobutton(win, text="nucl",
                                variable=db_v, value='nucl')
        radio1.grid(row=4, column=1, sticky=W)
        radio2 = tk.Radiobutton(win, text="prot",
                                variable=db_v, value='prot')
        radio2.grid(row=4, column=2, sticky=W)

        # evalue
        # Label evalue
        l_out_file = tk.Label(win, text='Evalue: ')
        l_out_file.grid(row=5, column=0, padx=5, pady=5)
        # Spinbox evalue
        eva = tk.StringVar()
        # eva.set(1e-3)  # 不知为何会被下面的values覆盖掉
        values = []
        for i in range(100, 0, -1):
            values.append('1e-'+str(i))
        for i in range(0, 100):
            values.append(str(i))
        sb = tk.Spinbox(win, values=values, textvariable=eva, width=7)
        eva.set(1e-5)
        sb.grid(row=5, column=1, sticky=W)

        # outfmt
        # Label evalue
        l_out_file = tk.Label(win, text='Outfmt: ')
        l_out_file.grid(row=5, column=2, padx=5, pady=5, sticky=E)
        # Spinbox evalue
        oft = tk.StringVar()
        oft.set(6)
        sb = tk.Spinbox(win, from_=1, to=9, textvariable=oft, width=7)
        sb.grid(row=5, column=3, sticky=W)

        # out file directory
        # Label out file
        l_out_file = tk.Label(win, text='Result: ')
        l_out_file.grid(row=6, column=0, padx=5, pady=5)
        # Entry out file
        result = tk.StringVar()
        result.set('Input a directory...')
        e_result = tk.Entry(win, textvariable=result, width=70)
        e_result.grid(row=6, column=1, columnspan=3)

        # db entry dragged func
        App.dragged_files_Entry(e_result, result)

        # blast button
        def command():
            try:
                func.easy_blast(db.get(), db_v.get(), query.get(
                ), q_v.get(), result.get(), eva.get(), oft.get())
                tkinter.messagebox.showinfo('Information', 'Blast finished!')
            except:
                tkinter.messagebox.showerror('Error', 'Check the directory!')

        b_blast = tk.Button(win, text='Run', width=10, command=command)
        b_blast.grid(row=10, column=1, sticky=W)

    @staticmethod
    def compare_fasta_files():
        win = App.new_window('FASTA COMPARE',row=0, column=2, padx=25, pady=5, sticky=W)
        
        # query
        # query label
        l_in_file = tk.Label(win, text='File1: ')
        l_in_file.grid(row=1, column=0, padx=5, pady=5)

        # query entry
        query = tk.StringVar()
        query.set('Input a fasta file...')
        e_query = tk.Entry(win, textvariable=query, width=70)
        e_query.grid(row=1, column=1, columnspan=3)

        # query entry dragged func
        App.dragged_files_Entry(e_query, query)

        # database
        # db label
        l_in_file = tk.Label(win, text='File2: ')
        l_in_file.grid(row=3, column=0, padx=5, pady=5)

        # db entry
        db = tk.StringVar()
        db.set('Input a fasta file...')
        e_db = tk.Entry(win, textvariable=db, width=70)
        e_db.grid(row=3, column=1, columnspan=3)

        # db entry dragged func
        App.dragged_files_Entry(e_db, db)

        '''
        # out file directory
        ## Label out file 
        l_out_file = tk.Label(window, text='Result: ')
        l_out_file.grid(row=6,column=0,padx=5,pady=5)
        ## Entry out file
        result = tk.StringVar()
        result.set('Input a directory...')
        e_result = tk.Entry(window, textvariable=result, width=70)
        e_result.grid(row=6,column=1,columnspan=3)

        ### db entry dragged func
        App.dragged_files_Entry(e_result, result)
        '''

        # Run button
        def command():
            try:
                result = func.get_directory(query.get())
                out = func.compare_fasta(query.get(), db.get())

                add_file = result + '\\add.txt'
                remove_file = result + '\\remove.txt'
                change_file = result + '\\change.txt'
                same_file = result + '\\same.txt'

                change = out[0]
                add = out[1]
                remove = out[2]
                same = out[3]

                file1 = ot.Fasta(query.get())
                file2 = ot.Fasta(db.get())

                file1.extract_gene(remove, filename=remove_file)
                file1.extract_gene(same, filename=same_file)
                file2.extract_gene(add, filename=add_file)
                file1.extract_gene(change, filename=change_file)
                file2.extract_gene(change, filename=change_file, option='a')

                tkinter.messagebox.showinfo('Information', 'Program finished!')
            except:
                tkinter.messagebox.showerror('Error', 'Check the directory!')

        b_blast = tk.Button(win, text='Run', width=10, command=command)
        b_blast.grid(row=10, column=1, sticky=W)

    @staticmethod
    def duplicate_delete():
        win = App.new_window('DELETE DUPLICATE',row=0, column=2, padx=25, pady=5, sticky=W)
        
        # query
        # query label
        l_in_file = tk.Label(win, text='File: ')
        l_in_file.grid(row=1, column=0, padx=5, pady=5)

        # query entry
        query = tk.StringVar()
        query.set('Input a fasta file...')
        e_query = tk.Entry(win, textvariable=query, width=70)
        e_query.grid(row=1, column=1, columnspan=3)

        # query entry dragged func
        App.dragged_files_Entry(e_query, query)

        # out file directory
        # Label out file
        l_out_file = tk.Label(win, text='Result: ')
        l_out_file.grid(row=6, column=0, padx=5, pady=5)
        # Entry out file
        result = tk.StringVar()
        result.set('Input a directory...')
        e_result = tk.Entry(win, textvariable=result, width=70)
        e_result.grid(row=6, column=1, columnspan=3)

        # db entry dragged func
        App.dragged_files_Entry(e_result, result)

        # Run button
        def command():
            try:
                dic = ot.Fasta(query.get()).dict
                ot.dic2fa(dic, result.get())
                tkinter.messagebox.showinfo('Information', 'Program Finished!')
            except:
                tkinter.messagebox.showerror('Error', 'Check the directory!')

        b_run = tk.Button(win, text='Run', width=10, command=command)
        b_run.grid(row=10, column=1, sticky=W)

    @staticmethod
    # function: merge fasta file
    def reverse_complement():
        win = App.new_window('Reverse Complement Sequence')

        ##
        t_list = tk.Text(win, width=90, height=18)
        t_list.insert('end', 'ATCGatcgggggTTTTTTTTTTT') # example
        t_list.grid(row=1, column=1, padx=25, pady=5)

        ##
        # Reverse_complement
        def reverse_complement():
            seqs = t_list.get('0.0', 'end').rstrip().split('\n')
            result = ''
            for sequence in seqs:
                result += func.reverse_complement(sequence) + '\n'

            win_sub = tk.Toplevel(win)
            win_sub.title('Reverse complement sequence')
            win_sub.geometry('685x265')

            t_result = tk.Text(win_sub, width=90, height=18)
            t_result.pack()
            t_result.insert('end', result)

        b = tk.Button(win, text='run', command=reverse_complement)
        b.grid(row=2, column=1, sticky=E, padx=25, pady=5)

    @staticmethod
    def CRISPR_primer_designer():
        win = App.new_window('CRISPR primer designer')

        ##
        t_list = tk.Text(win, width=90, height=18)
        t_list.insert('end', 'CATGCCAATGTATTGCTGAG')
        t_list.grid(row=1, column=1, padx=25, pady=5)

        ##
        def crispr_primer():
            seqs = t_list.get('0.0', 'end').rstrip().split('\n')
            result = ''
            for sequence in seqs:
                result += str(func.crispr_primer_designer(sequence)) + '\n'

            win_sub = tk.Toplevel(win)
            win_sub.title('DESIGN CRISPR PRIMER')
            win_sub.geometry('685x265')

            t_result = tk.Text(win_sub, width=90, height=18)
            t_result.pack()
            t_result.insert('end', result)

        b = tk.Button(win, text='run', command=crispr_primer)
        b.grid(row=2, column=1, sticky=E, padx=25, pady=5)

    @staticmethod
    def gerenal_primer_designer():
        ow = OtWin()
        win = ow.new_window('Genernal primer designer')
        forward = ow.add_Entry(win, 'Adapters (F):', 'input your seqence...')
        reward = ow.add_Entry(win, 'Adapters (R):', 'input your seqence...')
        target = ow.add_Text(win, 'Feature target seq:', 'input your seqence...')

        def command():
            t_seq = target.get('0.0', 'end').replace(' ','')
            f_seq = forward.get()
            r_seq = reward.get()
            result = ''
            
            result+=(func.infusion_primer_designer(t_seq, f_seq, r_seq))+'\n'

            win_sub = tk.Toplevel(win)
            win_sub.title('DESIGN CRISPR PRIMER')
            win_sub.geometry('685x265')

            t_result = tk.Text(win_sub, width=90, height=18)
            t_result.pack()
            t_result.insert('end', result)

        ow.add_buttom(win, command=command)


    # toplevel window
    def new_window(win_title, paras={'row':0, 'column':1, 'padx':25, 'pady':5}, **promt_paras):
        win = tk.Toplevel()
        win.title('Omicstools')
        win.geometry('685x365')
        win.iconbitmap("Omics.ico")

        l_title = tk.Label(
            win, text=win_title, font=('Arial', 20))
        if not promt_paras:
            l_title.grid(paras)
        else:
            l_title.grid(promt_paras)

        return win


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


    def donothing(self):
        pass


if __name__ == '__main__':
    main()
