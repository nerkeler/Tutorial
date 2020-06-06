import requests,json
from tkinter import *
from tkinter import Scrollbar
import tkinter.font as tf


class AnswerGUI(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.master.bind("<Button-3>",self.buttonTest)
        self.ft = tf.Font(family='微软雅黑', size=12)       #设置输出文本框字体
        self.grid()
        self.createWiget()
        #self.information()

    def createWiget(self):#创建布局

        """输入框"""
        v1 = StringVar()
        self.eny1 = Entry(self.master, textvariable=v1,width=30,font=self.ft )
        self.eny1.grid(row=1,column=0,columnspan=3,sticky=NSEW,pady=5,padx=5)
        self.eny1.bind("<Return>",self.enter)           #绑定回车按键


        """确定按键"""
        btn = Button(self.master,text='确定',command=self.get_answer,)
        btn.grid(row=1,column=3,sticky=NSEW,pady=5,padx=5)


        """text 输出框"""
        self.tet = Text(self.master, width=40, height=13,font=self.ft)
        self.tet.grid(row=2,column=0,columnspan=4,pady=5,padx=5)

        """初始使用说明"""
        self.tet.insert(INSERT,"1、本应用为超星尔雅查题工具，支持超星尔雅平台和智慧树知道平台。\n")
        self.tet.insert(INSERT,"2、第一行为题目输入框，支持右键粘贴和 ctrl+v \n")
        self.tet.insert(INSERT,"3、支持回车确定，添加了纵向滚动条\n")
        self.tet.insert(INSERT,"4、输出文本框禁用编辑\n")
        self.tet.insert(INSERT,"5、联系反馈邮箱：2739038007@qq.com\n")
        self.tet.insert(INSERT,"6、基于python tkinter 编写，技术不足之处还望谅解。\n\n")
        self.tet.insert(INSERT,"友情提示：\n    由于查题api是调用外部接口，所以应用需要不定期更改查题接口。")
        self.tet.insert(INSERT,"如发现查题失败，请尽快联系本人，并附上你的联系方式,我会尽快修复！\n感谢支持！")
        self.tet.config(state=DISABLED)         #禁用编辑

        """添加纵向滚动条"""
        scroll = Scrollbar(root)
        scroll.grid(row=2,column=4,sticky='ns')
        self.tet.configure(yscrollcommand = scroll.set)
        scroll.configure(command=self.tet.yview)

    """调用api搜索题目"""
    def get_answer(self):
        self.tet.config(state=NORMAL)               #设置可写
        self.tet.delete(1.0,END)                    #清空文本框
        self.question = self.eny1.get()
        self.answer = f"http://api.xmlm8.com/tk.php?t={self.question}"      #合成搜索链接
        #print(self.answer)
        res = requests.get(self.answer)
        res.encoding =  res.apparent_encoding

        if res.status_code == 200:
            #print(res.text)
            a = json.loads(res.text)
            #print(a['da'])
            if a['da'] != "":

                self.tet.insert(1.0,f"题目：\n   {a['tm']}\n\n")
                self.tet.insert(INSERT,f"答案：\n   {a['da']}")
                self.tet.config(state=DISABLED)     #禁止编辑
            else:
                self.answer = f"http://47.112.247.80/wkapi.php?q={self.question}" #合成搜索链接
                res = requests.get(self.answer)
                res.encoding = res.apparent_encoding

                if res.status_code == 200:
                    a = json.loads(res.text)
                    #print(a)
                    #print(a['answer'])
                    if a['answer'] != "":
                        self.tet.insert(1.0, f"题目：\n  {a['tm']}\n\n")
                        self.tet.insert(INSERT, f"答案：\n  {a['answer']}")
                        self.tet.config(state=DISABLED)     #禁止编辑
                    else:
                        print("抱歉，暂时没有查询出答案")
                else:
                    return None
        else:
            return None

    def enter(self,event):
        self.get_answer()

    def buttonTest(self,event):
        s = root.clipboard_get()
        self.eny1.insert(1,s)


if __name__ == '__main__':
    root = Tk()
    root.iconbitmap("xuexitong.ico")
    root.geometry("400x340+500+300")
    root.title('超星尔雅查题工具')
    app = AnswerGUI(master=root)
    root.mainloop()