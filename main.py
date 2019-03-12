'''
Car light annotation tool

Author: chenjinsheng
Date: 2019.03.11
'''

"""
注意事项：保存图的名字中不能有空格
标注步骤：
1.选择存图文件夹
2.选择txt文件夹
3.点击开始
"""
import os
import tkinter
import tkinter.messagebox
from tkinter.filedialog import askdirectory

from PIL import Image, ImageTk
from functools import partial

current = -1
image_path = ''

root = tkinter.Tk()
root.title("车灯标注工具")

# 初始化value
v_l = tkinter.IntVar()
v_r = tkinter.IntVar()
v_u = tkinter.IntVar()
v_d = tkinter.IntVar()
v_s = tkinter.IntVar()
pic = ''
save_txt_path = tkinter.StringVar()
line_number = -1

def show_img():
    def save_res_to_txt():
        global save_txt_path, v_l, v_r, v_u, v_d, v_s, pic, line_number
        txt_name = 'label.txt'
        print(line_number)
        if line_number != -1:
            f = open(os.path.join(save_txt_path.get(), txt_name), 'r+')
            flist = f.readlines()
            old = flist[line_number].split()
            flist[line_number] = old[0] + ' ' + str(v_l.get()) + ' ' \
                       + str(v_r.get()) + ' ' + str(v_u.get()) + ' ' \
                       + str(v_d.get()) + ' ' + str(v_s.get()) + '\n'
            f = open(os.path.join(save_txt_path.get(), txt_name), 'w+')
            f.writelines(flist)

        else:
            with open(os.path.join(save_txt_path.get(), txt_name), 'a+') as f:
                f.write(pic)
                f.write(' ')
                f.write(str(v_l.get()))
                f.write(' ')
                f.write(str(v_r.get()))
                f.write(' ')
                f.write(str(v_u.get()))
                f.write(' ')
                f.write(str(v_d.get()))
                f.write(' ')
                f.write(str(v_s.get()))
                f.write('\n')

    def load_txt_res(name):
        global save_txt_path, v_l, v_s, v_r, v_u, v_d, pic
        txt_name = 'label.txt'

        with open(os.path.join(save_txt_path.get(), txt_name), 'r') as f:
            res = f.readlines()
            for i, each_line in enumerate(res):
                if each_line.split()[0] == name:
                    v_l.set(each_line.split()[1])
                    v_r.set(each_line.split()[2])
                    v_u.set(each_line.split()[3])
                    v_d.set(each_line.split()[4])
                    v_s.set(each_line.split()[5])
                    return i
                else:
                    v_l.set(0)
                    v_r.set(0)
                    v_u.set(0)
                    v_d.set(0)
                    v_s.set(0)
            return -1

    def start_show():
        # 获取当前文件夹中所有图片文件列表
        global image_path
        if image_path != '':
            suffix = ('.jpg', '.bmp', '.png')

            pics = [os.path.join(image_path,p) for p in os.listdir(image_path) if p.endswith(suffix)]

            def changePic(new):
                '''flag=-1表示上一个，flag=1表示下一个'''
                #global current
                #new = current + flag
                if new < 0:
                    tkinter.messagebox.showerror('', '这已经是第一张图片了')
                elif new >= len(pics):
                    tkinter.messagebox.showerror('', '这已经是最后一张图片了')
                else:
                    # 获取要切换的图片文件名
                    global pic
                    pic = pics[new]
                    # 创建Image对象并进行缩放
                    im = Image.open(pic)
                    w, h = im.size

                    # 这里假设用来显示图片的Label组件尺寸为400*600
                    if w < 400:
                        h = int(h * 400 / w)
                        w = 400
                        im = im.resize((w, h))
                    if h < 600:
                        w = int(w * 600 / h)
                        h = 600
                        im = im.resize((w, h))
                    if w > 800:
                        h = int(h * 800 / w)
                        w = 800
                        im = im.resize((w, h))
                    if h > 1200:
                        w = int(w * 1200 / h)
                        h = 1200
                        im = im.resize((w, h))

                    # im = im.resize((w,h))
                    # 创建PhotoImage对象，并设置Label组件图片
                    im1 = ImageTk.PhotoImage(im)
                    lbPic['image'] = im1
                    lbPic.image = im1

                global line_number
                line_number = load_txt_res(pic)

            # “上一张”按钮
            def btnPreClick():
                global v_l, v_r, v_u, v_d, v_s
                if v_l.get() == 0 or v_r.get() == 0 or v_u.get() == 0 or v_d.get() == 0 or v_s == 0:
                    tkinter.messagebox.showerror('', '有状态未选择')
                else:
                    save_res_to_txt()
                    global current
                    current -= 1
                    changePic(current)

            btnPre = tkinter.Button(root, text='上一张', command=btnPreClick)
            btnPre.place(x=1000, y=440, width=80, height=30)

            # “下一张”按钮
            def btnNextClick():
                global v_l, v_r, v_u, v_d, v_s
                if v_l.get() == 0 or v_r.get() == 0 or v_u.get() == 0 or v_d.get() == 0 or v_s == 0:
                    tkinter.messagebox.showerror('', '有状态未选择')
                else:
                    save_res_to_txt()
                    global current
                    current += 1
                    changePic(current)

            btnNext = tkinter.Button(root, text='下一张', command=btnNextClick)
            btnNext.place(x=1000, y=470, width=80, height=30)
            # 用来显示图片的Label组件
            lbPic = tkinter.Label(root, text='')
            global current
            current = 0
            changePic(current)
            lbPic.place(x=10, y=70)
            # 左灯
            l = tkinter.Label(root, bg='yellow', width=20, text='左车灯')
            l.place(x=1000, y=20, width=80, height=30)
            l.place(x=1000, y=20, width=80, height=30)
            # l.pack()
            bt1 = tkinter.Radiobutton(root, text="暗", variable=v_l, value=1)  # .pack(anchor=tkinter.W)
            bt1.place(x=1000, y=50, width=80, height=30)
            bt2 = tkinter.Radiobutton(root, text="亮", variable=v_l, value=2)  # .pack(anchor=tkinter.W)
            bt2.place(x=1000, y=80, width=80, height=30)

            # 右灯
            l = tkinter.Label(root, bg='yellow', width=20, text='右车灯')
            l.place(x=1000, y=110, width=80, height=30)
            # l.pack()
            bt1 = tkinter.Radiobutton(root, text="暗", variable=v_r, value=1)  # .pack(anchor=tkinter.W)
            bt1.place(x=1000, y=140, width=80, height=30)
            bt2 = tkinter.Radiobutton(root, text="亮", variable=v_r, value=2)  # .pack(anchor=tkinter.W)
            bt2.place(x=1000, y=170, width=80, height=30)

            # 上灯
            l = tkinter.Label(root, bg='yellow', width=20, text='上车灯')
            l.place(x=1000, y=200, width=80, height=30)
            # l.pack()
            bt3 = tkinter.Radiobutton(root, text="暗", variable=v_u, value=1)  # .pack(anchor=tkinter.W)
            bt3.place(x=1000, y=230, width=80, height=30)
            bt4 = tkinter.Radiobutton(root, text="亮", variable=v_u, value=2)  # .pack(anchor=tkinter.W)
            bt4.place(x=1000, y=260, width=80, height=30)
            bt5 = tkinter.Radiobutton(root, text="无", variable=v_u, value=3)  # .pack(anchor=tkinter.W)
            bt5.place(x=1000, y=290, width=80, height=30)

            # 方向
            l = tkinter.Label(root, bg='yellow', width=20, text='车体方向')
            l.place(x=1000, y=320, width=80, height=30)
            # l.pack()
            bt6 = tkinter.Radiobutton(root, text="前", variable=v_d, value=1)  # .pack(anchor=tkinter.W)
            bt6.place(x=1000, y=350, width=80, height=30)
            bt7 = tkinter.Radiobutton(root, text="侧", variable=v_d, value=2)  # .pack(anchor=tkinter.W)
            bt7.place(x=1000, y=380, width=80, height=30)
            bt8 = tkinter.Radiobutton(root, text="后", variable=v_d, value=3)  # .pack(anchor=tkinter.W)
            bt8.place(x=1000, y=410, width=80, height=30)

            # 车辆类型
            l = tkinter.Label(root, bg='yellow', width=20, text='车辆类型')
            l.place(x=1100, y=20, width=80, height=30)
            l.place(x=1100, y=20, width=80, height=30)
            # l.pack()

            bt9 = tkinter.Radiobutton(root, text="小汽车", variable=v_s, value=1)  # .pack(anchor=tkinter.W)
            bt9.place(x=1100, y=50, width=80, height=30)
            bt10 = tkinter.Radiobutton(root, text="卡车", variable=v_s, value=2)  # .pack(anchor=tkinter.W)
            bt10.place(x=1100, y=80, width=80, height=30)
            bt11 = tkinter.Radiobutton(root, text="大巴车", variable=v_s, value=3)  # .pack(anchor=tkinter.W)
            bt11.place(x=1100, y=120, width=80, height=30)
            bt12 = tkinter.Radiobutton(root, text="出租车", variable=v_s, value=4)  # .pack(anchor=tkinter.W)
            bt12.place(x=1100, y=150, width=80, height=30)
            bt13 = tkinter.Radiobutton(root, text="救护车", variable=v_s, value=5)  # .pack(anchor=tkinter.W)
            bt13.place(x=1100, y=180, width=80, height=30)

        mylist = tkinter.Listbox(root, width=100)  # 列表框
        mylist.place(x=1000, y=500, width=200, height=200)

        def callback(event):
            try:
                if v_l.get() == 0 or v_r.get() == 0 or v_u.get() == 0 or v_d.get() == 0 or v_s.get() == 0:
                    pass
                else:
                    save_res_to_txt()
                global current
                current = mylist.curselection()[0]
                changePic(current)
            except IndexError as e:
                pass
        # 创建一个列表
        for item in pics:  # 插入内容
            mylist.insert(tkinter.END, item)  # 从尾部插入
        mylist.bind("<Button-1>", callback)

    def selectPath(path):
        path_ = askdirectory()
        path.set(path_)
        global image_path
        image_path = path_

    # 创建tkinter应用程序窗口
    path = tkinter.StringVar()
    bt_choose_path = tkinter.Button(root, text="读图文件夹", command=partial(selectPath, path))
    bt_choose_path.place(x=100, y=10, width=100, height=30)
    lb_choose_path = tkinter.Label(root, textvariable=path,
                                   bg='white', font=('Arial', 12))
    lb_choose_path.place(x=300, y=10, height=30)

    # 存txt路径
    bt_choose_path = tkinter.Button(root, text="存txt文件夹", command=partial(selectPath, save_txt_path))
    bt_choose_path.place(x=100, y=40, width=100, height=30)
    lb_choose_path = tkinter.Label(root, textvariable=save_txt_path,
                                   bg='white', font=('Arial', 12))
    lb_choose_path.place(x=300, y=40, height=30)
    bt_start_show = tkinter.Button(root, text="开始", command=partial(start_show))
    bt_start_show.place(x=200, y=10, width=80, height=30)
    # 设置窗口大小和位置
    root.geometry('1200x1200+40+30')
    # 不允许改变窗口大小
    root.resizable(True, True)
    # 启动消息主循环
    root.mainloop()


if __name__ == '__main__':
    show_img()
