from tkinter import *
import mysql.connector
from ast import Lambda
from tkinter import ttk
from PIL import ImageTk, Image

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_praktikum"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    # Input 4
    options_gender = [("Laki-laki", "Laki-laki"), ("Perempuan", "Perempuan")]
    input_jenis_kelamin = StringVar(root)
    input_jenis_kelamin.set("Laki-laki")
    label5 = Label(dframe, text ="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    
    # Input 5
    options_hobi = ["Main Game", "Nonton Anime", "Nonton Vtuber", "Gambar"]
    label6 = Label(dframe, text="Hobi").grid(row=4, column=0, sticky="w")
    input_hobi = ttk.Combobox(dframe, value=options_hobi)
    input_hobi.current(0)
    input_hobi.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    i=1
    for text, gender, in options_gender:
        Radiobutton(dframe, text=text, variable=input_jenis_kelamin, value=gender).grid(row=3, column=i, sticky="w")
        i+=1

    def clicked(value):
        myLabel = Label(root, text=value)
        myLabel.pack()

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, input_jenis_kelamin, input_hobi), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Gak jadi / Kembali", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)



# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jenis_kelamin, hobi):
    top = Toplevel()
    # Get data

    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jenis_kelamin = jenis_kelamin.get()
    hobi = hobi.get()

    x = len(nama)
    y = len(nim)
    z = len(jurusan)
    p = len(jenis_kelamin)
    q = len(hobi)

    # Input data disini
    if x == 0 or y == 0 or z == 0 or p == 0 or q == 0:
        btn_g_ok = Button(top, text="Ngok, data anda tidak lengkap ngok", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_g_ok.pack(padx=10, pady=10)
    else:
        sql = "INSERT INTO mahasiswa (nama, nim, jurusan, jenis_kelamin, hobi) VALUES (%s, %s, %s, %s, %s)"
        val = (nama, nim, jurusan, jenis_kelamin, hobi)
        dbcursor.execute(sql, val)
        mydb.commit()

        btn_ok = Button(top, text="Syap!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

def facility():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasiitas Kampus")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Fasilitas Kampus")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    imageFrame = LabelFrame(frame)
    imageFrame.grid(row=1, column = 0, columnspan=3)

    my_img1 = ImageTk.PhotoImage(Image.open('images/control_center.png'))
    my_img2 = ImageTk.PhotoImage(Image.open('images/reception.png'))
    my_img3 = ImageTk.PhotoImage(Image.open('images/office.png'))
    my_img4 = ImageTk.PhotoImage(Image.open('images/workshop.png'))
    my_img5 = ImageTk.PhotoImage(Image.open('images/trading_post.png'))

    image_list = [my_img1, my_img2, my_img3, my_img4, my_img5]

    my_label = Label(imageFrame, image=my_img1)
    my_label.grid(row=1, column=0, columnspan=3)

    def forward(image_number):
        nonlocal my_label
        global button_forward
        global button_back

        my_label.grid_forget()
        my_label = Label(imageFrame, image=image_list[image_number - 1])
        button_forward = Button(imageFrame, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(imageFrame, text="<<", command=lambda: back(image_number - 1))

        if image_number == 5:
            button_forward = Button(root, text=">>", state=DISABLED)

        my_label.grid(row=0, column=1)
        button_back.grid(row=2, column=2)
        button_forward.grid(row=2, column=3)


    def back(image_number):
        nonlocal my_label
        global button_forward
        global button_back

        my_label.grid_forget()
        my_label = Label(imageFrame, image=image_list[image_number - 1])
        button_forward = Button(imageFrame, text=">>", command=lambda: forward(image_number + 1))
        button_back = Button(imageFrame, text="<<", command=lambda: back(image_number - 1))

        if image_number == 1:
            button_back = Button(imageFrame, text="<<", state=DISABLED)

        my_label.grid(row=0, column=1)
        button_back.grid(row=2, column=2)
        button_forward.grid(row=2, column=3)

    button_back = Button(imageFrame, text="<<", command=lambda: back(), state=DISABLED)
    button_exit = Button(imageFrame, text="Exit Program", command=root.quit)
    button_forward = Button(imageFrame, text=">>", command=lambda: forward(2))

    button_back.grid(row=2, column=0)
    button_exit.grid(row=2, column=1)
    button_forward.grid(row=2, column=2)

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Yakin mau hapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Tapi boong", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

def delAll():
    top = Toplevel()
    # Delete data disini
    sql = "TRUNCATE TABLE mahasiswa"
    dbcursor.execute(sql)
    mydb.commit()

    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ceritanya ini database mahasiswa ngab")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Semua Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Facility btn
b_clear = Button(buttonGroup, text="Fasilitas Kampus", command=facility, width=30)
b_clear.grid(row=2, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()