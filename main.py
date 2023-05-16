# Importación de módulos
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

# Funciones

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir) 

def tick():
    tiempo = time.strftime('%H:%M:%S')
    clock.config(text=tiempo)
    clock.after(200, tick)

def contact():
    mess._show(title='Contáctenos', message="Por favor contáctenos en : '1362503@gmail.com' ")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Falta un archivo', message='Póngase en contacto con nosotros')
        window.destroy()

# Guardar contraseña
def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pass = tsd.askstring('Contraseña antigua no encontrada', 'Por favor, introduzca una nueva contraseña a continuación', show='*')
        if new_pass == None:
            mess._show(title='No se ha introducido la contraseña', message='¡No se ha establecido la contraseña! Por favor, inténtelo de nuevo')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pass)
            mess._show(title='Contraseña registrada', message='¡¡La nueva contraseña se ha registrado correctamente!!')
            return
    op = (old.get())
    newp =(new.get())
    nnewp = (nnew.get())
    if (op == key):
        if(newp == nnewp):
            txf = open("TrainingImageLabel\psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirme de nuevo la nueva contraseña')
            return
    else:
        mess._show(title='Contraseña incorrecta', message='Por favor, introduzca la contraseña antigua correcta.')
        return
    mess._show(title='Contraseña cambiada', message='Contraseña modificada correctamente')
    master.destroy()

# Cambiar contraseña
def change_pass():
    global master
    master = tk.Tk()
    master.geometry("400x160")
    master.resizable(False,False)
    master.title("Cambiar contraseña")
    master.configure(background="white")
    lbl4 = tk.Label(master,text='    Introducir contraseña antigua',bg='white',font=('times', 12, ' bold '))
    lbl4.place(x=10,y=10)
    global old
    old=tk.Entry(master,width=25 ,fg="black",relief='solid',font=('times', 12, ' bold '),show='*')
    old.place(x=180,y=10)
    lbl5 = tk.Label(master, text='   Introducir nueva contraseña', bg='white', font=('times', 12, ' bold '))
    lbl5.place(x=10, y=45)
    global new
    new = tk.Entry(master, width=25, fg="black",relief='solid', font=('times', 12, ' bold '),show='*')
    new.place(x=180, y=45)
    lbl6 = tk.Label(master, text='Confirmar nueva contraseña', bg='white', font=('times', 12, ' bold '))
    lbl6.place(x=10, y=80)
    global nnew
    nnew = tk.Entry(master, width=25, fg="black", relief='solid',font=('times', 12, ' bold '),show='*')
    nnew.place(x=180, y=80)
    cancel=tk.Button(master,text="Cancel", command=master.destroy ,fg="black"  ,bg="red" ,height=1,width=25 , activebackground = "white" ,font=('times', 10, ' bold '))
    cancel.place(x=200, y=120)
    save1 = tk.Button(master, text="Save", command=save_pass, fg="black", bg="#3ece48", height = 1,width=25, activebackground="white", font=('times', 10, ' bold '))
    save1.place(x=10, y=120)
    master.mainloop()

def psw(): 
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Contraseña antigua no encontrada', 'Introduzca una nueva contraseña', show='*')
        if new_pas == None:
            mess._show(title='No se ha introducido la contraseña', message='¡No se ha establecido la contraseña! Por favor, inténtelo de nuevo')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Contraseña registrada', message='La nueva contraseña se ha registrado correctamente!!')
            return
    password = tsd.askstring('Contraseña', 'Introducir contraseña', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Contraseña incorrecta', message='Ha introducido una contraseña incorrecta')

def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # incremento del número de muestra
                sampleNum = sampleNum + 1
                # guardar la cara capturada en la carpeta del conjunto de datos TrainingImage.
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # visualizar el marco
                cv2.imshow('Taking Images', img)
            # esperar 100 milisegundos
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # romper si el número de muestras es superior a 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Imágenes tomadas para identificación : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Introduzca el nombre correcto"
            message.configure(text=res)


def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No hay inscripciones', message='Por favor, registre a alguien primero')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Perfil guardado correctamente"
    message1.configure(text=res)
    message.configure(text='Total de inscripciones hasta ahora  : ' + str(ID[0]))



def getImagesAndLabels(path):
    # obtener la ruta de todos los archivos de la carpeta
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # crear lista de caras de empleados
    faces = []
    # crear una lista ID vacía
    Ids = []
    # ahora recorriendo todas las rutas de imágenes y cargando los Ids y las imágenes
    for imagePath in imagePaths:
        # cargar la imagen y convertirla a escala de grises
        pilImage = Image.open(imagePath).convert('L')
        # Ahora convertimos la imagen PIL en un array numpy
        imageNp = np.array(pilImage, 'uint8')
        # obtener el Id de la imagen
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extraer el rostro de la muestra de imágenes de entrenamiento
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Faltan datos', message='Haga clic en Guardar perfil para restablecer los datos')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Faltan detalles', message='Faltan datos de los estudiantes, ¡compruébelo!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Por favor, registre a alguien primero')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Perfil guardado correctamente"
    message1.configure(text=res)
    message.configure(text='Total de inscripciones hasta ahora  : ' + str(ID[0]))

#

def getImagesAndLabels(path):
    # obtener la ruta de todos los archivos de la carpeta
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # crear lista de caras de empleados
    faces = []
    # crear una lista ID vacía
    Ids = []
    # ahora recorriendo todas las rutas de imágenes y cargando los Ids y las imágenes
    for imagePath in imagePaths:
        # cargar la imagen y convertirla a escala de grises
        pilImage = Image.open(imagePath).convert('L')
        # Ahora convertimos la imagen PIL en un array numpy
        imageNp = np.array(pilImage, 'uint8')
        # obtener el Id de la imagen
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extraer el rostro de la muestra de imágenes de entrenamiento
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()   # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Faltan datos', message='Haga clic en Guardar perfil para restablecer los datos')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Faltan detalles', message='Faltan datos de los estudiantes, por favor, compruébelos')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }

# Interfaz Gráfica
window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Sistema de asistencia")
window.configure(background='#0a0a0a')

# Espacio 1
frame1 = tk.Frame(window, bg="#151c99")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

# Espacio 2
frame2 = tk.Frame(window, bg="#151c99")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

# Titulo
message3 = tk.Label(window, text="Sistema de control de asistencia basado en el reconocimiento facial" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

# Mostrar Hora
frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)

# Mostrar Fecha
frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.36, rely=0.09, relwidth=0.16, relheight=0.07)

# Fecha
datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"  |  ", fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
datef.pack(fill='both',expand=1)

# Hora
clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)
tick()

# Titulo para Nuevos Registros
head2 = tk.Label(frame2, text="                       Para nuevas inscripciones                       ", fg="white",bg="#262523" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

# Titulo para ya Registrados
head1 = tk.Label(frame1, text="                       Para los ya inscritos                       ", fg="white",bg="#262523" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0) 

# Titulo para 1er input
lbl = tk.Label(frame2, text="Ingresar ID",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

# 1er input
txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

# Titulo para 2do input
lbl2 = tk.Label(frame2, text="Ingresar nombre",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

# 2do input
txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Tomar imágenes  >>>  2)Guardar perfil" ,bg="#00aeff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

# Titulo
lbl3 = tk.Label(frame1, text="Asistencia",width=20  ,fg="black"  ,bg="#00aeff"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("DetallesDelEstudiante\DetallesDelEstudiante.csv")
if exists:
    with open("DetallesDelEstudiante\DetallesDelEstudiante.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total de inscripciones hasta ahora  : '+str(res))

# Menubar

menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Cambiar contraseña', command = change_pass)
filemenu.add_command(label='Contáctame', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

# TABLA DE ASISTENCIA

tv= ttk.Treeview(frame1,height =13,columns = ('nombre','fecha','tiempo'))
tv.column('#0',width=82)
tv.column('nombre',width=130)
tv.column('fecha',width=133)
tv.column('tiempo',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('nombre',text ='NAME')
tv.heading('fecha',text ='DATE')
tv.heading('tiempo',text ='TIME')

# Scrollbar

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

# Botones
clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)    
takeImg = tk.Button(frame2, text="Tomar imágenes", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Guardar perfil", command=psw ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Tomar asistencia", command=TrackImages  ,fg="black"  ,bg="yellow"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="Exit", command=window.destroy  ,fg="black"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

# Fin
window.configure(menu=menubar)
window.mainloop()