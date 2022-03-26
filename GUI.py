from db.mysql_db import pool
import mysql.connector.pooling
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
import datetime
import tkinter.messagebox as messagebox  # 弹窗
from service.user_service import UserService
from service.news_service import NewsService
from service.role_service import RoleService


__user_service=UserService()
__news_service=NewsService()
__role_service=RoleService()
class StartPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('图书馆借阅系统')
        self.window.geometry('300x470')  # 这里的乘是小x
        label = Label(self.window, text="图书馆借阅系统", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度
        Button(self.window, text="管理员登陆", font=tkFont.Font(size=16), command=lambda: AdminPage(self.window), width=30,
               height=2, fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="学生登陆", font=tkFont.Font(size=16), command=lambda: StudentPage(self.window), width=30,
               height=2, fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text='退出系统', height=2, font=tkFont.Font(size=16), width=30, command=self.window.destroy,
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        self.window.mainloop()  # 主消息循环
# 管理员登陆页面
class AdminPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员登陆页面')
        self.window.geometry('300x450')  # 这里的乘是小x

        label = tk.Label(self.window, text='管理员登陆', bg='green', font=('Verdana', 20), width=30, height=2)
        label.pack()
        Label(self.window, text='管理员账号：', font=tkFont.Font(size=14)).pack(pady=25)
        self.admin_username = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory')
        self.admin_username.pack()

        Label(self.window, text='管理员密码：', font=tkFont.Font(size=14)).pack(pady=25)
        self.admin_pass = tk.Entry(self.window, width=30, font=tkFont.Font(size=14), bg='Ivory', show='*')
        self.admin_pass.pack()
        Button(self.window, text="登陆", width=8, font=tkFont.Font(size=12), command=self.login).pack(pady=40)
        Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=12), command=self.back).pack()
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        try:
            con = pool.get_connection()
            cursor = con.cursor()
            sql = "SELECT COUNT(*) FROM t_user WHERE  username= '%s' AND AES_DECRYPT(UNHEX(password),'HelloWorld')=%d AND role_id=%d" % (
                self.admin_username.get(), int(self.admin_pass.get()),1)  # SQL 查询语句
            cursor.execute(sql)
            # 获取所有记录列表
            result = cursor.fetchone()[0]
        except Exception as e:
            print("Error: unable to fecth data")
            messagebox.showinfo('警告！', '用户名或密码不正确！')
            print(e)
        finally:
            if "con" in dir():
                con.close()
        if result == 1:
            AdminView(self.window)  # 进入管理员操作界面
        else:
             messagebox.showinfo('警告！', '用户名或密码不正确！')
        #db.close()  # 关闭数据库连接

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口
class AdminView:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员操作界面')
        self.window.geometry('300x470')  # 这里的乘是小x
        label = Label(self.window, text="管理员操作系统", font=("Verdana", 20))
        label.pack(pady=100)  # pady=100 界面的长度
        Button(self.window, text="新闻管理", font=tkFont.Font(size=16), command=lambda: NewsManage(self.window), width=30,
               height=2, fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text="用户管理", font=tkFont.Font(size=16), command=lambda: UserManage(self.window), width=30,
               height=2, fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        Button(self.window, text='退出系统', height=2, font=tkFont.Font(size=16), width=30, command=self.back,
               fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
        self.window.mainloop()  # 主消息循环
    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口
class NewsManage:

    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = Tk()  # 初始框的声明
        self.window.title('新闻管理界面')

        self.frame_left_top = tk.Frame(width=300, height=200)
        self.frame_right_top = tk.Frame(width=200, height=200)
        self.frame_center = tk.Frame(width=500, height=400)
        self.frame_bottom = tk.Frame(width=650, height=50)

        # 定义下方中心列表区域
        self.columns = ("新闻标题", "类型id", "内容id", "是否top", "状态")
        self.tree = ttk.Treeview(self.frame_center, show="headings", height=15, columns=self.columns)
        self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("新闻标题", width=100, anchor='center')  # 表示列,不显示
        self.tree.column("类型id", width=100, anchor='center')
        self.tree.column("内容id", width=100, anchor='center')
        self.tree.column("是否top", width=100, anchor='center')
        self.tree.column("状态", width=100, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.bno = []
        self.bname = []
        self.bress = []
        self.place = []
        self.num = []
        # 打开数据库连接
        db = pool.get_connection()
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "SELECT * FROM t_news"  # SQL 查询语句
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                self.bno.append(row[1])
                self.bname.append(row[3])
                self.bress.append(row[4])
                self.place.append(row[5])
                self.num.append(row[8])
            # print(self.id)
            # print(self.name)
            # print(self.gender)
            # print(self.age)
        except:
            print("Error: unable to fetch data")
            messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接

        print("test***********************")
        for i in range(min(len(self.bno), len(self.bname), len(self.bress), len(self.place), len(self.num))):  # 写入数据
            self.tree.insert('', i, values=(self.bno[i], self.bname[i], self.bress[i], self.place[i], self.num[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top, text="书籍信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_bno = StringVar()  # 声明学号
        self.var_bname = StringVar()  # 声明姓名
        self.var_bress = StringVar()  # 声明性别
        self.var_place = StringVar()  # 声明年龄
        self.var_num = StringVar()
        # 学号
        self.right_top_bno_label = Label(self.frame_left_top, text="新闻标题：", font=('Verdana', 10))
        self.right_top_bno_entry = Entry(self.frame_left_top, textvariable=self.var_bno, font=('Verdana', 10))
        self.right_top_bno_label.grid(row=1, column=0)  # 位置设置
        self.right_top_bno_entry.grid(row=1, column=1)
        # 姓名
        self.right_top_bname_label = Label(self.frame_left_top, text="id：", font=('Verdana', 10))
        self.right_top_bname_entry = Entry(self.frame_left_top, textvariable=self.var_bname, font=('Verdana', 10))
        self.right_top_bname_label.grid(row=2, column=0)  # 位置设置
        self.right_top_bname_entry.grid(row=2, column=1)
        # 性别
        self.right_top_bress_label = Label(self.frame_left_top, text="内容id：", font=('Verdana', 10))
        self.right_top_bress_entry = Entry(self.frame_left_top, textvariable=self.var_bress,
                                           font=('Verdana', 10))
        self.right_top_bress_label.grid(row=3, column=0)  # 位置设置
        self.right_top_bress_entry.grid(row=3, column=1)
        # 年龄
        self.right_top_place_label = Label(self.frame_left_top, text="类型id：", font=('Verdana', 10))
        self.right_top_place_entry = Entry(self.frame_left_top, textvariable=self.var_place,
                                           font=('Verdana', 10))
        self.right_top_place_label.grid(row=4, column=0)  # 位置设置
        self.right_top_place_entry.grid(row=4, column=1)

        self.right_top_num_label = Label(self.frame_left_top, text="状态：", font=('Verdana', 10))
        self.right_top_num_entry = Entry(self.frame_left_top, textvariable=self.var_num,
                                         font=('Verdana', 10))
        self.right_top_num_label.grid(row=5, column=0)  # 位置设置
        self.right_top_num_entry.grid(row=5, column=1)

        # 定义右上方区域
        self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(self.frame_right_top, text='审批新闻', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新新闻信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除新闻', width=20,
                                            command=self.del_row)
        # 位置设置
        self.right_top_title.grid(row=1, column=0, pady=10)
        self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=3, column=0, padx=20, pady=10)

        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_bno.set(self.row_info[0])
        self.var_bname.set(self.row_info[1])
        self.var_bress.set(self.row_info[2])
        self.var_place.set(self.row_info[3])
        self.var_num.set(self.row_info[4])
        self.right_top_bno_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_bno,
                                         font=('Verdana', 15))

        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


    def new_row(self):
        print('123')
        print(self.var_bname.get())
        print(self.bname)
        #if str(self.var_bname.get()) in self.bname:
        i=1;
        if  i==1:
            __user_service = UserService()
            __news_service = NewsService()
            __role_service = RoleService()
            page=1
            result = __news_service.search_unreview_list(page)
            news_id = result[int(self.var_bname.get()) - 1][0]
            __news_service.update_unreview_news(news_id)
            bno_index = self.bname.index(self.row_info[1])
            self.num[bno_index] = "已审批"
            self.tree.update()
            messagebox.showinfo('提示！', '审批成功！')
        else:
            messagebox.showinfo('警告！', '该学生不存在！')

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            if self.var_bno.get() == self.row_info[0]:  # 如果所填学号 与 所选学号一致
                # 打开数据库连接
                db = pool.get_connection()
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "UPDATE book SET bname = '%s', bress = '%s', place = '%s',num='%d' \
    				 WHERE bno = '%d'" % (
                    self.var_bname.get(), self.var_bress.get(), self.var_place.get(), int(self.var_num.get()),
                    int(self.var_bno.get()))  # SQL 插入语句
                try:
                    cursor.execute(sql)  # 执行sql语句
                    db.commit()  # 提交到数据库执行
                    messagebox.showinfo('提示！', '更新成功！')
                except:
                    db.rollback()  # 发生错误时回滚
                    messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
                db.close()  # 关闭数据库连接

                bno_index = self.bno.index(self.row_info[0])
                self.bname[bno_index] = self.var_bname.get()
                self.bress[bno_index] = self.var_bress.get()
                self.place[bno_index] = self.var_place.get()
                self.num[bno_index] = self.var_num.get()
                self.tree.item(self.tree.selection()[0], values=(
                    self.var_bno.get(), self.var_bname.get(), self.var_bress.get(),
                    self.var_place.get(), self.var_num.get()))  # 修改对于行信息
            else:
                messagebox.showinfo('警告！', '不能修改学生学号！')

    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行
            __user_service = UserService()
            __news_service = NewsService()
            __role_service = RoleService()
            page = 1
            result = __news_service.search_list(page)
            news_id = result[int(self.row_info[1]) - 1][0]
            __news_service.delete_by_id(news_id)
            bno_index = self.bno.index(self.row_info[0])
            print(bno_index)
            del self.bno[bno_index]
            del self.bname[bno_index]
            del self.bress[bno_index]
            del self.place[bno_index]
            del self.num[bno_index]
            print(self.bno)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())


class UserManage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('用户管理系统')
        self.window.geometry('300x470')  # 这里的乘是小x

if __name__ == '__main__':
    __config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "nyy0120",
        "database": "vega",
        "auth_plugin": "mysql_native_password"
    }

    try:
        pool = mysql.connector.pooling.MySQLConnectionPool(
            **__config,
            pool_size=10
        )
        db = pool.get_connection()
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 如果数据表不存在则创建表 若存在则跳过
        # 设置主键唯一

        # 关闭数据库连接
        db.close()

        # 实例化Application
        window = tk.Tk()
        StartPage(window)
    except:
        messagebox.showinfo('错误！', '连接数据库失败！')