import math 
import numpy

from tkinter import Tk, Toplevel, Canvas, Frame, BOTH, LEFT, messagebox
from tkinter.ttk import Frame, Button, Style, Label, Entry, Radiobutton


dt = 0.5

class myRobot:
    
    def __init__(self, x_center, y_center, width, height, speed, cursAngle):
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.speed = speed
        self.cursAngle = -cursAngle
        self.distance = 0
        self.normalSpeed = speed

    def setVars(self, x_center, y_center, cursAngle):
        self.x_center = x_center
        self.y_center = y_center
        self.cursAngle = cursAngle

class pointObstacle:
    def __init__(self, x_center, y_center, k):
        self.x_center = x_center
        self.y_center = y_center
        self.k = k

        self.power = 0.0

    def getPower(self, r):
        self.power = math.exp(-k*r)
        return self.power

class mountObstacle:
    def __init__(self, x_center, y_center, high, angle):
        self.x_center = x_center
        self.y_center = y_center
        self.high = high
        self.angle = angle

        self.radius = high / math.tan(math.radians(self.angle))
        

class area:
    def __init__(self, x1, y1, x2, y2, p):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.p = p

class finishArea:
    def __init__(self, x_center, y_center, radius, k):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.k = k

# ФУНКЦИИ СОЗДАНИЯ ОБЪЕКТОВ КЛАССОВ

realFinishArea = finishArea (1,1,1,1)

def createfinishArea(x_center, y_center, radius, k):
    realFinishArea.x_center = x_center
    realFinishArea.y_center = y_center
    realFinishArea.radius = radius
    realFinishArea.k = k
  

groupRobots = list()

def createRobot(x_center, y_center, width, height, speed, cursAngle):
    newRobot = myRobot(x_center, y_center, width, height, speed, cursAngle)
    groupRobots.append(newRobot)

pointObstacles = list()

def createPointObstacle(x_center, y_center, k):
    newPointObstacle = pointObstacle(x_center, y_center, k)
    pointObstacles.append(newPointObstacle)

mountObstacles = list()

def createMountObstacle(x_center, y_center, hihg, angle):
    newMountObstacle = mountObstacle(x_center, y_center, hihg, angle)
    mountObstacles.append(newMountObstacle)

areas = list()

def createArea(x1,y1,x2,y2,p):
    newArea = area(x1,y1,x2,y2,p)
    areas.append(newArea)
    for i in areas:
        print(i.p)
        print(i.y1)

# ОПИСАНИЕ КЛАССА ГЛАВНОГО ОКНА ПРОГРАММЫ

class MainWindow(Frame):
    # функция инициализации и открытия основного окна
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Group Navigation")
        self.pack(fill=BOTH, expand=1)
        # БАЗОВАЯ ВЕРСТКА:
        # получаем значение ширины и высоты экрана текущего компьютера
        self.W  = self.parent.winfo_screenwidth()
        self.H  = self.parent.winfo_screenheight()
        self.kX=0
        self.kY=0
        # выччисляем центр экрана текущего компьютера и создаем окно
        x_center_w = self.W / 2
        y_center_w = self.H / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.W, self.H, x_center_w, y_center_w))
        self.parent.configure(bg='#FDF5E6')

        self.canvas = Canvas(self, width=self.W*0.8, height=self.H*0.9, bg='white')
        self.canvas.pack(side=LEFT)
        
        # СОЗДАНИЕ ЦЕЛИ:
        # меню создания цели
        createFinishAreaButton = Button(self, text="Задать целевой район", command=self.getFinishAreaParametersAndCreate)
        createFinishAreaButton.place(x=self.W*0.81, y=self.H*0.02)

        finishAreaLabel1 = Label(self,text="Х центр цели:\n\nY центр цели:")
        finishAreaLabel1.place(x=self.W*0.81, y =self.H*0.06)

        finishAreaLabel2 = Label(self,text="радиус зоны:\n\nкоэффициент:")
        finishAreaLabel2.place(x=self.W*0.905, y =self.H*0.06)

        self.x_center_finishArea_text = Entry(self, width = 4) 
        self.x_center_finishArea_text.place(x=self.W*0.88, y=self.H*0.06)

        self.y_center_finishArea_text = Entry(self, width = 4) 
        self.y_center_finishArea_text.place(x=self.W*0.88, y=self.H*0.10)

        self.radius_finishArea_text = Entry(self, width = 4) 
        self.radius_finishArea_text.place(x=self.W*0.97, y=self.H*0.06)

        self.k_finishArea_text = Entry(self, width = 4) 
        self.k_finishArea_text.place(x=self.W*0.97, y=self.H*0.10)

        # СОЗДАНИЕ РОБОТОВ:
        # меню создания робота
        createRobotButton = Button(self, text="Создать робота", command=self.getRobotParametersAndCreate)
        createRobotButton.place(x=self.W*0.81, y=self.H*0.14)

        robot_label1 = Label(self, text="Х центр робота: \n\nY центр робота: \n\nширина (м):") 
        robot_label1.place(x=self.W*0.81, y=self.H*0.18)

        robot_label2 = Label(self, text="длина (м): \n\nскорость:\n(м\с)\nугол (град):") 
        robot_label2.place(x=self.W*0.905, y=self.H*0.18)

        # ввод параметров робота
        self.x_center_robot_text = Entry(self, width = 4) 
        self.x_center_robot_text.place(x=self.W*0.88, y=self.H*0.18)
        
        self.y_center_robot_text = Entry(self, width = 4) 
        self.y_center_robot_text.place(x=self.W*0.88, y=self.H*0.22)

        self.width_robot_text = Entry(self, width = 4) 
        self.width_robot_text.place(x=self.W*0.88, y=self.H*0.26)

        self.height_robot_text = Entry(self, width = 4) 
        self.height_robot_text.place(x=self.W*0.97, y=self.H*0.18)

        self.speed_robot_text = Entry(self, width = 4) 
        self.speed_robot_text.place(x=self.W*0.97, y=self.H*0.22)

        self.cursAngle_robot_text = Entry(self, width = 4) 
        self.cursAngle_robot_text.place(x=self.W*0.97, y=self.H*0.26)

        # СОЗДАНИЕ ТОЧЕЧНОГО ПРЕПЯТСТВИЯ
        # меню создания точечного препятсвия
        createPointObstacleButton = Button(self, text="Создать точечное препятсвие", command=self.getPointObstacleParametersAndCreate)
        createPointObstacleButton.place(x=self.W*0.81, y=self.H*0.3)

        pointObstacle_label = Label(self, text="Х центр препятсвия: \n\nY центр препятсвия: \n\nкоэффициент:") 
        pointObstacle_label.place(x=self.W*0.81, y=self.H*0.34)

        # ввод параметров препятсвия 
        self.x_center_pointObstacle_text = Entry(self, width = 4) 
        self.x_center_pointObstacle_text.place(x=self.W*0.9, y=self.H*0.34)

        self.y_center_pointObstacle_text = Entry(self, width = 4) 
        self.y_center_pointObstacle_text.place(x=self.W*0.9, y=self.H*0.38)

        self.k_pointObstacle_text = Entry(self, width = 4) 
        self.k_pointObstacle_text.place(x=self.W*0.9, y=self.H*0.42)

        # СОЗДАНИЕ ПРЕПЯСТВИЯ ТИПА "ХОЛМ"
        # меню создания препятсвия типа "холм"
        createPointObstacleButton = Button(self, text="Создать холм", command=self.getMountObstacleParametersAndCreate)
        createPointObstacleButton.place(x=self.W*0.81, y=self.H*0.46)

        pointObstacle_label = Label(self, text="Х центр препятсвия: \n\nY центр препятсвия: \n\nвысота (м): \n\nугол (град):") 
        pointObstacle_label.place(x=self.W*0.81, y=self.H*0.5)

        # ввод параметров препятсвия 
        self.x_center_mountObstacle_text = Entry(self, width = 4) 
        self.x_center_mountObstacle_text.place(x=self.W*0.9, y=self.H*0.5)

        self.y_center_mountObstacle_text = Entry(self, width = 4) 
        self.y_center_mountObstacle_text.place(x=self.W*0.9, y=self.H*0.54)

        self.high_mountObstacle_text = Entry(self, width = 4) 
        self.high_mountObstacle_text.place(x=self.W*0.9, y=self.H*0.58)

        self.angle_mountObstacle_text = Entry(self, width = 4) 
        self.angle_mountObstacle_text.place(x=self.W*0.9, y=self.H*0.62)

        # СОЗДАНИЕ СВОЙСТВ ГРУНТА
        
        self.grunt = 0.0
        RadioMaker = 0
        createAreaButton = Button(self, text="Задать свойства грунта", command=self.getAreaParametersAndCreate)
        createAreaButton.place(x=self.W*0.81, y=self.H*0.66)
        
        grunt_Bitum_rad = Radiobutton(self, text='Асфальт', command=self.getPBitum, variable=RadioMaker, value = 1)
        grunt_Bitum_rad.place(x=self.W*0.81, y=self.H*0.7)

        grunt_Dirty_rad = Radiobutton(self, text='Грязь',command=self.getPDirty, variable=RadioMaker, value = 2)
        grunt_Dirty_rad.place(x=self.W*0.865, y=self.H*0.7)

        grunt_Herb_rad = Radiobutton(self, text='Трава',command=self.getPHerd, variable=RadioMaker, value = 3 )
        grunt_Herb_rad.place(x=self.W*0.91, y=self.H*0.7)


        grunt_label_1 = Label(self, text="Х 1: \n\nY 1:") 
        grunt_label_1.place(x=self.W*0.81, y=self.H*0.74)

        grunt_label_2 = Label(self, text="Х 2: \n\nY 2:") 
        grunt_label_2.place(x=self.W*0.85, y=self.H*0.74)

        self.x1_grunt_text = Entry(self, width = 3) 
        self.x1_grunt_text.place(x=self.W*0.83, y=self.H*0.74)

        self.y1_grunt_text = Entry(self, width = 3) 
        self.y1_grunt_text.place(x=self.W*0.83, y=self.H*0.78)

        self.x2_grunt_text = Entry(self, width = 3) 
        self.x2_grunt_text.place(x=self.W*0.87, y=self.H*0.74)

        self.y2_grunt_text = Entry(self, width = 3) 
        self.y2_grunt_text.place(x=self.W*0.87, y=self.H*0.78)

        # задание дальности обзора для всех роботов
        viev_robots_label = Label(self, text="Дальность\nвидимости\nроботов:") 
        viev_robots_label.place(x=self.W*0.91, y=self.H*0.74)

        self.viev_robots_text = Entry(self, width = 3) 
        self.viev_robots_text.place(x=self.W*0.97, y=self.H*0.76)

        # кнопка старта моделирования
        startModelButton = Button(self, text="Моделирование", command=self.startModel)
        startModelButton.place(x=self.W*0.915, y=self.H*0.02)

        # кнопка заполнения поля
        drowButton = Button(self, text="Заполнить поле", command=self.drowMap1)
        drowButton.place(x=self.W*0.81, y=self.H*0.87)

        # кнопка отчистки поля
        clearButton = Button(self, text="Отчистить поле", command=self.clearMap)
        clearButton.place(x=self.W*0.9, y=self.H*0.87)

        # кнопка и настройки определения масштаба
        makeMacshButton = Button(self, text="Задать поле", command=self.makeMacsh)
        makeMacshButton.place(x=self.W*0.81, y=self.H*0.82)

        macsh_label_x = Label(self, text="Ширина:") 
        macsh_label_x.place(x=self.W*0.87, y=self.H*0.825)

        macsh_label_y = Label(self, text="Длина:") 
        macsh_label_y.place(x=self.W*0.94, y=self.H*0.825)

        self.x_macsh_text = Entry(self, width = 5) 
        self.x_macsh_text.place(x=self.W*0.91, y=self.H*0.825)

        self.y_macsh_text = Entry(self, width = 5) 
        self.y_macsh_text.place(x=self.W*0.97, y=self.H*0.825)

    def makeGrid(self,x,y,kx,ky):
        self.canvas.create_line(10,10,self.W*0.8,10)
        self.canvas.create_line(10,10,10,self.H*0.9)

        self.canvas.create_text(self.W*0.78,25, text=x, fill='black', font=18)
        self.canvas.create_text(25,self.H*0.88, text=y, fill='black', font=18)
        self.canvas.create_text(25,25, text='0,0', fill='black', font=18)

        for i in range(x):
            self.canvas.create_line(10+kx*i,10,10+kx*i,10+self.H*0.9, dash=(4,2))
        for i in range(y):
            self.canvas.create_line(10,10+ky*i,10+self.W*0.8,10+ky*i, dash=(4,2))
            
    def makeMacsh(self):
        x_macsh_int = int(self.x_macsh_text.get())
        y_macsh_int = int(self.y_macsh_text.get())

        self.kX = self.W * 0.8 / x_macsh_int
        self.kY = self.H * 0.9 / y_macsh_int
        
        self.makeGrid(x_macsh_int,y_macsh_int,self.kX,self.kY)

    def getFinishAreaParametersAndCreate(self):
        x_center_finishArea_int = int(self.x_center_finishArea_text.get())
        y_center_finishArea_int = int(self.y_center_finishArea_text.get())
        radius_finishArea_int = int(self.radius_finishArea_text.get())
        k_finishArea_int = int(self.k_finishArea_text.get())

        createfinishArea(x_center_finishArea_int, y_center_finishArea_int, radius_finishArea_int, k_finishArea_int)
        

    def drowFinishAreas(self):
        
            self.canvas.create_oval(10+self.kX*(realFinishArea.x_center-realFinishArea.radius),10+self.kY*(realFinishArea.y_center+realFinishArea.radius),10+self.kX*(realFinishArea.x_center+realFinishArea.radius),10+self.kY*(realFinishArea.y_center-realFinishArea.radius), width=3)
            self.canvas.create_text(10+self.kX*realFinishArea.x_center,10+self.kY*realFinishArea.y_center, text='Финиш', fill='black', font=18)

    def getRobotParametersAndCreate(self):
        x_center_robot_int = int(self.x_center_robot_text.get())
        y_center_robot_int = int(self.y_center_robot_text.get())
        width_robot_int = int(self.width_robot_text.get())
        height_robot_int = int(self.height_robot_text.get())
        speed_robot_int = int(self.speed_robot_text.get())
        cursAngle_robot_int = int(self.cursAngle_robot_text.get())
             
        createRobot(x_center_robot_int,y_center_robot_int,width_robot_int,height_robot_int,speed_robot_int,cursAngle_robot_int)
        
    def drowRobots(self): 
        counter = 1
        for i in groupRobots:
            x1_local = x4_local = i.width / 2
            x2_local = x3_local = -i.width / 2

            y1_local = y2_local = i.height / 2
            y3_local = y4_local = -i.height / 2
 

            new_x1_local =  x1_local * math.cos(math.radians(i.cursAngle)) - y1_local * math.sin(math.radians(i.cursAngle))
            new_y1_local =  x1_local * math.sin(math.radians(i.cursAngle)) + y1_local * math.cos(math.radians(i.cursAngle))

            new_x2_local =  x2_local * math.cos(math.radians(i.cursAngle)) - y2_local * math.sin(math.radians(i.cursAngle))
            new_y2_local =  x2_local * math.sin(math.radians(i.cursAngle)) + y2_local * math.cos(math.radians(i.cursAngle))

            new_x3_local =  x3_local * math.cos(math.radians(i.cursAngle)) - y3_local * math.sin(math.radians(i.cursAngle))
            new_y3_local =  x3_local * math.sin(math.radians(i.cursAngle)) + y3_local * math.cos(math.radians(i.cursAngle))

            new_x4_local =  x4_local * math.cos(math.radians(i.cursAngle)) - y3_local * math.sin(math.radians(i.cursAngle))
            new_y4_local =  x4_local * math.sin(math.radians(i.cursAngle)) + y3_local * math.cos(math.radians(i.cursAngle))

            new_x1 = 10 + self.kX*(new_x1_local + i.x_center)
            new_x2 = 10 + self.kX*(new_x2_local + i.x_center)
            new_x3 = 10 + self.kX*(new_x3_local + i.x_center)
            new_x4 = 10 + self.kX*(new_x4_local + i.x_center)

            new_y1 = 10 + self.kY*(new_y1_local + i.y_center)
            new_y2 = 10 + self.kY*(new_y2_local + i.y_center)
            new_y3 = 10 + self.kY*(new_y3_local + i.y_center)
            new_y4 = 10 + self.kY*(new_y4_local + i.y_center)
            
            self.canvas.create_line(new_x1,new_y1,new_x2,new_y2, fill = 'red', width = 3)
            self.canvas.create_line(new_x2,new_y2,new_x3,new_y3, fill = 'red', width = 3)
            self.canvas.create_line(new_x3,new_y3,new_x4,new_y4, fill = 'red', width = 3)
            self.canvas.create_line(new_x4,new_y4,new_x1,new_y1, fill = 'red', width = 3)

            x1_arrow = 10 + self.kX*(i.width * math.cos(math.radians(i.cursAngle))+i.x_center)
            y1_arrow = 10 + self.kY*(i.width * math.sin(math.radians(i.cursAngle))+i.y_center)

            self.canvas.create_line(10+self.kX*i.x_center,10+self.kY*i.y_center,x1_arrow,y1_arrow,fill = 'red', width = 3)
            self.canvas.create_text(10+self.kX*i.x_center,10+self.kY*i.y_center, text=counter, fill='black', font=18)
            counter+=1

    def getPointObstacleParametersAndCreate(self):
        x_center_pointObstacle_int = int(self.x_center_pointObstacle_text.get())
        y_center_pointObstacle_int = int(self.y_center_pointObstacle_text.get())
        k_pointObstacle_int = int(self.k_pointObstacle_text.get())

        createPointObstacle(x_center_pointObstacle_int,y_center_pointObstacle_int,k_pointObstacle_int)
        
    def drowPointObstacles(self):
        counter = 1
        for i in pointObstacles:
            self.canvas.create_oval(10+self.kX*(i.x_center-i.k/2),10+self.kY*(i.y_center+i.k/2),10+self.kX*(i.x_center+i.k/2),10+self.kY*(i.y_center-i.k/2), fill='black', width=3)
            self.canvas.create_text(10+self.kX*i.x_center,10+self.kY*i.y_center, text=counter, fill='white', font=18)
            
            counter+=1

    def getMountObstacleParametersAndCreate(self):
        x_center_mountObstacle_int = int(self.x_center_mountObstacle_text.get())
        y_center_mountObstacle_int = int(self.y_center_mountObstacle_text.get())
        high_mountObstacle_int = int(self.high_mountObstacle_text.get())
        angle_mountObstacle_int = int(self.angle_mountObstacle_text.get())

        createMountObstacle(x_center_mountObstacle_int,y_center_mountObstacle_int,high_mountObstacle_int,angle_mountObstacle_int)  

    def drowMountObstacles(self):
        counter = 1
        for i in mountObstacles:
            self.canvas.create_oval(10+self.kX*(i.x_center-i.radius),10+self.kY*(i.y_center+i.radius),10+self.kX*(i.x_center+i.radius),10+self.kY*(i.y_center-i.radius), width=3)
            self.canvas.create_text(10+self.kX*i.x_center,10+self.kY*i.y_center, text=str(counter)+", высота: "+str(i.high)+" м", fill='black', font=18)
            
            counter+=1

    

    def getAreaParametersAndCreate(self):
        x1_int = int(self.x1_grunt_text.get())
        y1_int = int(self.y1_grunt_text.get())

        x2_int = int(self.x2_grunt_text.get())
        y2_int = int(self.y2_grunt_text.get())
        p = self.grunt
        createArea(x1_int,y1_int,x2_int,y2_int,p)

    def drowAreas(self):
        for i in areas:
            print(i.p)
            if i.p == 1:
                color = '#A9A9A9'
            if i.p == 0.5:
                color = '#9ACD32'
            if i.p == 0.1:
                color = '#7F6C5B'

            self.canvas.create_rectangle(10+self.kX*(i.x1),10+self.kY*(i.y1),10+self.kX*(i.x2),10+self.kY*(i.y2), fill = color)

    def getPBitum(self):
        self.grunt = 1
        

    def getPDirty(self):
        self.grunt = 0.1
        

    def getPHerd(self):
        self.grunt = 0.5
        

    def clearMap(self): 
        self.canvas.delete("all")

    def drowMap1(self):
        self.drowAreas()
        self.makeMacsh()
        self.drowRobots()
        self.drowPointObstacles()
        self.drowMountObstacles()
        self.drowFinishAreas()
       

    def drowMap(self):
        self.makeMacsh()
        self.drowRobots()
        self.drowPointObstacles()
        self.drowMountObstacles()
        self.drowFinishAreas()
        
    # ФУНКЦИЯ МОДЕЛИРОВАНИЯ

    def startModel(self):
        # считываем значение дальности обзора роботов
        viev_robot_int = int(self.viev_robots_text.get())
        self.drowAreas()
        # определение средней дистанции роботов до центра целевого района
        R = 0.0
        counter = 0
        for i in groupRobots:
            R += math.sqrt((realFinishArea.x_center - i.x_center) ** 2 + (realFinishArea.y_center - i.y_center) ** 2)
            counter+=1
        R = R / counter
        num = counter
        # время выполнения перемещения всей группы роботов до целевого района
        T = 0.0
        while(num > 0):
            
            for i in groupRobots:
            # определим координаты "углов" каждого робота в масштабной СК
                # координаты без учета поворота
                x1_local = x4_local = i.width / 2
                x2_local = x3_local = -i.width / 2

                y1_local = y2_local = i.height / 2
                y3_local = y4_local = -i.height / 2
                # координаты с учетом поворота
                rot_x1_local =  i.x_center + x1_local * math.cos(math.radians(i.cursAngle)) - y1_local * math.sin(math.radians(i.cursAngle))
                rot_y1_local =  i.y_center + x1_local * math.sin(math.radians(i.cursAngle)) + y1_local * math.cos(math.radians(i.cursAngle))

                rot_x2_local =  i.x_center + x2_local * math.cos(math.radians(i.cursAngle)) - y2_local * math.sin(math.radians(i.cursAngle))
                rot_y2_local =  i.y_center + x2_local * math.sin(math.radians(i.cursAngle)) + y2_local * math.cos(math.radians(i.cursAngle))

                rot_x3_local =  i.x_center + x3_local * math.cos(math.radians(i.cursAngle)) - y3_local * math.sin(math.radians(i.cursAngle))
                rot_y3_local =  i.y_center + x3_local * math.sin(math.radians(i.cursAngle)) + y3_local * math.cos(math.radians(i.cursAngle))

                rot_x4_local =  i.x_center + x4_local * math.cos(math.radians(i.cursAngle)) - y3_local * math.sin(math.radians(i.cursAngle))
                rot_y4_local =  i.x_center + x4_local * math.sin(math.radians(i.cursAngle)) + y3_local * math.cos(math.radians(i.cursAngle))
                vector = [0.0,0.0]

                F1v = numpy.array(vector)
                F2v = numpy.array(vector)
                F3v = numpy.array(vector)
                F4v = numpy.array(vector)
                F_v = numpy.array(vector)
               
                # влияние цели
                dist_finish = math.sqrt((realFinishArea.x_center - i.x_center) ** 2 + (realFinishArea.y_center - i.y_center) ** 2)
                angle_finish =  abs(math.acos((abs(realFinishArea.x_center - i.x_center))/dist_finish ))
                
                mod_finish = realFinishArea.k

                x = mod_finish*math.cos(angle_finish)
                y = mod_finish*math.sin(angle_finish)

                if realFinishArea.y_center - i.y_center >= 0 and realFinishArea.x_center - i.x_center >= 0:
                    x = x
                    y = -y
                if realFinishArea.y_center - i.y_center < 0 and realFinishArea.x_center - i.x_center > 0:
                    x = x
                    y = y
                if realFinishArea.y_center - i.y_center < 0 and realFinishArea.x_center - i.x_center < 0:
                    x = -x
                    y = y
                if realFinishArea.y_center - i.y_center > 0 and realFinishArea.x_center - i.x_center < 0:
                    x = -x
                    y = -y

             
                
                toVector = [x,y]
                nowVector = numpy.array(toVector)
                F_v+=nowVector
            
                m = 0
                # влияние точечных препятсвий
                for j in pointObstacles:
                    mod_1 = mod_2 = mod_3 = mod_4 = 0.0
                    R_now = math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)
                    if R_now < viev_robot_int:
                        
                        dist = math.sqrt((rot_x1_local - j.x_center) ** 2 + (rot_y1_local - j.y_center) ** 2)
                        
                        mod_1 =   math.exp(-(dist-j.k*0.5)*j.k)
                        print(dist)
                        print(mod_1)
                        angle_1 = abs(math.acos((rot_x1_local - j.x_center)/math.sqrt((rot_x1_local - j.x_center) ** 2 + (rot_y1_local - j.y_center) ** 2)))

                        x =  abs(mod_1*math.cos(angle_1))
                        y =  abs(mod_1*math.sin(angle_1))

                        if j.y_center - rot_y1_local  >= 0 and j.x_center - rot_x1_local >= 0:
                            x = -x
                            y = y
                        if j.y_center - rot_y1_local  < 0 and j.x_center - rot_x1_local > 0:
                            x = -x
                            y = -y
                        if  j.y_center - rot_y1_local  < 0 and j.x_center - rot_x1_local  < 0:
                            x = x
                            y = -y
                        if j.y_center - rot_y1_local   > 0 and j.x_center - rot_x1_local < 0:
                            x = x
                            y = y


                        

                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F1v+=nowVector

                        dist = math.sqrt((rot_x2_local - j.x_center) ** 2 + (rot_y2_local - j.y_center) ** 2)
                        
                        mod_2 =  math.exp(-(dist-j.k*0.5)*j.k)

                        angle_2 = abs(math.acos((rot_x2_local - j.x_center)/math.sqrt((rot_x2_local - j.x_center) ** 2 + (rot_y2_local - j.y_center) ** 2)))
                        
                        x = abs( mod_2*math.cos(angle_2))
                        y = abs( mod_2*math.sin(angle_2))

                        if j.y_center - rot_y2_local  >= 0 and j.x_center - rot_x2_local >= 0:
                            x = -x
                            y = y
                        if j.y_center - rot_y2_local  < 0 and j.x_center - rot_x2_local > 0:
                            x = -x
                            y = -y
                        if  j.y_center - rot_y2_local  < 0 and j.x_center - rot_x2_local  < 0:
                            x = x
                            y = -y
                        if j.y_center - rot_y2_local   > 0 and j.x_center - rot_x2_local < 0:
                            x = x
                            y = y

                        
                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F2v+=nowVector

                        dist = math.sqrt((rot_x3_local - j.x_center) ** 2 + (rot_y3_local - j.y_center) **2)
                        
                        mod_3 =  math.exp(-(dist-j.k*0.5)*j.k)

                        angle_3 = abs(math.acos((rot_x3_local - j.x_center)/math.sqrt((rot_x3_local - j.x_center) ** 2 + (rot_y3_local - j.y_center) ** 2)))

                        x =  abs(mod_3*math.cos(angle_3))
                        y =  abs(mod_3*math.sin(angle_3))

                        if j.y_center - rot_y3_local  >= 0 and j.x_center - rot_x3_local >= 0:
                            x = -x
                            y = y
                        if j.y_center - rot_y3_local  < 0 and j.x_center - rot_x3_local > 0:
                            x = -x
                            y = -y
                        if  j.y_center - rot_y3_local  < 0 and j.x_center - rot_x3_local  < 0:
                            x = x
                            y = -y 
                        if j.y_center - rot_y3_local   > 0 and j.x_center - rot_x3_local < 0:
                            x = x
                            y = y 

                        
                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F3v+=nowVector

                       
                        dist = math.sqrt((rot_x4_local - j.x_center)**2 + (rot_y4_local - j.y_center)**2)
                        
                        mod_4 =  math.exp(-(dist-j.k*0.7)*j.k)

                        angle_4 = abs(math.acos((rot_x4_local - j.x_center)/math.sqrt((rot_x4_local - j.x_center) ** 2 + (rot_y4_local - j.y_center) ** 2)))

                        x =  abs(mod_4*math.cos(angle_4))
                        y =  abs(mod_4*math.sin(angle_4))

                        if j.y_center - rot_y4_local  >= 0 and j.x_center - rot_x4_local >= 0:
                            x = -x
                            y = y
                        if j.y_center - rot_y4_local  < 0 and j.x_center - rot_x4_local > 0:
                            x = -x
                            y = -y
                        if  j.y_center - rot_y4_local  < 0 and j.x_center - rot_x4_local  < 0:
                            x = x
                            y = -y 
                        if j.y_center - rot_y4_local   > 0 and j.x_center - rot_x4_local < 0:
                            x = x
                            y = y 

                        
                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F4v+=nowVector
                       
                # ВЛИЯНИЕ ПРЕПЯТСВИЙ ТИПА "ХОЛМ"
                for j in mountObstacles:
                    mod_mount = 0.0
                    R_now = math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)
                    if R_now < viev_robot_int*10:
                        
                        dist = math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)
                        if dist < j.radius:
                            mod_mount = abs(math.tan(math.radians(j.angle)))*0.3
                        else:
                            mod_mount = 0
                        
                        angle_mount = abs(math.acos((i.x_center - j.x_center)/math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)))

                        x =  abs(mod_mount*math.cos(angle_mount))
                        y =  abs(mod_mount*math.sin(angle_mount))

                        if j.y_center - i.y_center  >= 0 and j.x_center - i.x_center >= 0:
                            x = -x
                            y = y
                        if j.y_center - i.y_center  < 0 and j.x_center - i.x_center > 0:
                            x = -x
                            y = -y
                        if  j.y_center - i.y_center  < 0 and j.x_center - i.x_center  < 0:
                            x = x
                            y = -y
                        if j.y_center - i.y_center   > 0 and j.x_center - i.x_center < 0:
                            x = x
                            y = y
                        

                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F_v+=nowVector

                        

                # Влияние других роботов
                for j in groupRobots:
              
                    R_now = math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)
                    if R_now < viev_robot_int and R_now != 0:
                        
                        dist = math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)
                        
                        mod_other_robot =   math.exp(-(dist-1*0.5)*1)*4
                           
                        angle_1 = abs(math.acos((i.x_center - j.x_center)/math.sqrt((i.x_center - j.x_center) ** 2 + (i.y_center - j.y_center) ** 2)))

                        x =  abs(mod_other_robot*math.cos(angle_1))
                        y =  abs(mod_other_robot*math.sin(angle_1))

                        if j.y_center - i.y_center  >= 0 and j.x_center - i.x_center >= 0:
                            x = -x
                            y = y
                        if j.y_center - i.y_center  < 0 and j.x_center - i.x_center > 0:
                            x = -x
                            y = -y
                        if  j.y_center - i.y_center  < 0 and j.x_center - i.x_center  < 0:
                            x = x
                            y = -y
                        if j.y_center - i.y_center   > 0 and j.x_center - i.x_center < 0:
                            x = x
                            y = y

                        toVector = [x,y]
                        nowVector = numpy.array(toVector)
                        F_v+=nowVector

                F_v = F_v + F1v + F2v + F3v + F4v
               

                newAngle = abs(math.atan(abs(F_v[1])/abs(F_v[0])))
                if F_v[0] > 0 and F_v[1] > 0:
                    newAngle = -newAngle
                if F_v[0] < 0 and F_v[1] > 0:
                    newAngle =  math.pi + newAngle 
                if F_v[0] < 0 and F_v[1] < 0:
                    newAngle = math.pi - newAngle
                if F_v[0] > 0 and F_v[1] < 0:
                    newAngle = newAngle
               
                i.speed = i.normalSpeed

                if dist_finish < 0.5*realFinishArea.radius:
                    i.speed = 0.3*i.normalSpeed

                if dist_finish < 0.3*realFinishArea.radius:
                    i.speed = 0
                else:
                    # ОПРЕДЕЛЕНИЕ СКОРОСТИ ТЕКУЩЕГО РОБОТА ОТНОСИТЕЛЬНО ХАРАКТЕРА ПОВЕРХНОСТИ ПОД НИМ
                    for j in areas:
                        if i.x_center >= j.x1 and i.x_center <= j.x2 and i.y_center >= j.y1 and i.y_center <= j.y2:
                            i.speed = i.speed * j.p
                    i.cursAngle =   math.degrees(newAngle)
                    i.x_center = i.x_center + math.cos(newAngle)*i.speed*dt
                    i.y_center = i.y_center + math.sin(newAngle)*i.speed*dt
                    
            self.drowMap()
            
            T+=dt

            # условие перехода к следующей иттерации цикла
   
            counter = 0
            for i in groupRobots:
                dist_finish = math.sqrt((realFinishArea.x_center - i.x_center) ** 2 + (realFinishArea.y_center - i.y_center) ** 2)
                if dist_finish > realFinishArea.radius:
                    counter+=1
         
            num = counter

        msg = "Время проезда всей группы " + str(T) + " сек"
        messagebox.showinfo("Моделирование завершено!", msg)

def main():
    root = Tk()
    GroupNavigation = MainWindow(root)
    # начало обработки событий
    root.mainloop()
 
if __name__ == '__main__':
    main()