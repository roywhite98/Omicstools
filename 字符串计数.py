'''
Author: Roy White
Date: 2021-11-20 10:54:48
LastEditTime: 2021-11-20 16:31:39
'''
from GUI_elements import OtWin
from collections import Counter

# 就是简单地能将字符串长度、词频算出来的小工具
ow = OtWin()
win = ow.creat_root('字符串词频计数器')
seqs = ow.add_Text(win, 'Sequence:','ATCG')
def run():
    results = seqs.get('0.0', 'end').replace(' ','').rstrip()
    for result in results.split('\n'):
        char_rate=Counter(result).most_common(5)
        print(f'字符串长度：{len(result)}')
        print('词频统计：')
        for i in range(5):
            try:
                charNo=char_rate[i]
                print(f'{charNo[0]}:{round(charNo[1]/len(result)*100,2)}%')
            except IndexError:
                pass
ow.add_buttom(win,command=run)

win.mainloop()
