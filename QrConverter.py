import qrcode
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


class mainWindow():
    def __init__(self, master):
        self.master = master
        self.master.title("Generador QR")
        self.master.geometry("500x350")
        self.master.resizable(0,0)
        self.master.iconbitmap("QrIcon.ico")
        self.frame = Frame(self.master)
        self.frame.pack()

        self.linkVar = StringVar()
        self.direcVAR = StringVar()
        self.nameVar = StringVar()
        self.sizeVal = StringVar()
        self.sizeVal.set("Pequeño")
        self.sizeVal.trace('w', self.optionSize)
        self.customVal = StringVar()
        self.customVal.trace('w', self.validate)

        self.imageScreen = PhotoImage(file="Images/QrSmall.png")
        self.textScreen = StringVar()
        self.textScreen.set("128x128")


        self.width = 50
        self.extraHeight = 550
        self.sizeQr = 51
        self.custom = False

        self.linkLabel = Label(self.frame, text="URL:")
        self.linkLabel.grid(row=0, column=0,sticky='e')

        self.linkEntry = Entry(self.frame, textvariable=self.linkVar, width=self.width)
        self.linkEntry.grid(row=0, column=1)

        self.direcLabel = Label(self.frame, text="Nombre:")
        self.direcLabel.grid(row=2, column=0,sticky='e')

        self.nameEntry = Entry(self.frame, textvariable=self.nameVar, width=self.width)
        self.nameEntry.grid(row=2, column=1)

        self.saveQr = Button(self.frame, text="Guardar como", command=self.directory)
        self.saveQr.grid(row=2, column=2, columnspan=2, padx=10)

        self.frame_size = Frame(self.frame)
        self.frame_size.grid(row=3, column=0, columnspan=3, sticky='w')

        self.direcLabel = Label(self.frame_size, text="Tamaño:")
        self.direcLabel.grid(row=0, column=0, sticky='e')

        self.sizeOptions = OptionMenu(self.frame_size, self.sizeVal, "Pequeño", "Mediano", "Grande", "Custom")
        self.sizeOptions.grid(row=0, column=1, sticky='w')

        self.createBut = Button(self.frame, text="Generar", state=DISABLED, command=self.crateQR)
        self.createBut.grid(row=4, column=0, columnspan=4)

        self.screenState = Label(self.frame, width=20, height=2, relief="groove")
        self.screenState.grid(row=5, column=0, columnspan=4, pady=10)

        self.screenImage = Label(self.frame, image=self.imageScreen, relief="groove")
        self.screenImage.grid(row=6, column=0, columnspan=4, pady=2)
        self.screenImage.image = self.imageScreen

        self.screenDescrp = Label(self.frame, textvariable=self.textScreen)
        self.screenDescrp.grid(row=7, column=0, columnspan=4, pady=2)

        #Barra de menu ----------------------->

        self.barraMenu = Menu(self.master)
        self.master.config(menu=self.barraMenu)

        self.fileMenu = Menu(self.barraMenu, tearoff=0)
        self.fileMenu.add_command(label="Limpiar", command=self.limpiar)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Cerrar", command=self.salir)

        self.helpMenu = Menu(self.barraMenu, tearoff=0)
        self.helpMenu.add_command(label="Ayuda", command=self.ayuda)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Acerca de..", command=self.info)



        self.barraMenu.add_cascade(label="Archivo", menu=self.fileMenu)
        self.barraMenu.add_cascade(label="Ayuda", menu=self.helpMenu)


    def directory(self):
        direc = filedialog.askdirectory()
        if not direc == "":
            self.createBut.config(state=NORMAL)
            self.direcVAR.set(direc)

    def crateQR(self):
        data = self.linkVar

        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        youtube_regex_match = re.match(youtube_regex, data.get())
        try:
            if self.custom:
                self.sizeQr = int(self.customVal.get())
            else:
                pass

            if youtube_regex_match:

                dirc = self.direcVAR.get() + "/" + '{}.png'.format(self.nameVar.get())

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=10,
                    border=4
                )
                qr.add_data(data.get())
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                img = img.resize((self.sizeQr,self.sizeQr),resample=0)

                img.save(dirc)

                self.screenState.config(text="Código generado")

            else:
                messagebox.showwarning("URL no válida", "Ingresa un link de YouTube válido")
        except ValueError:
            messagebox.showerror("Resolución no válida", "Escribe la resolución de la imagen")

    def optionSize(self, *args):
        size = self.sizeVal.get()
        if size == "Pequeño":
            self.sizeQr = 128
            self.imageScreen.config(file="Images/QrSmall.png")
            self.master.geometry("500x330")
            self.textScreen.set("{}x{}".format(128, 128))
            if self.custom:
                self.customEntry.destroy()
                self.labelPix.destroy()
                self.custom = False
        elif size == "Mediano":
            self.sizeQr = 256
            self.imageScreen.config(file="Images/QrMedium.png")
            self.master.geometry("500x456")
            self.textScreen.set("{}x{}".format(256,256))
            if self.custom:
                self.customEntry.destroy()
                self.labelPix.destroy()
                self.custom = False
        elif size == "Grande":
            self.sizeQr = 512
            self.imageScreen.config(file="Images/QrBig.png")
            self.master.geometry("550x722")
            self.textScreen.set("{}x{}".format(512, 512))
            if self.custom:
                self.customEntry.destroy()
                self.labelPix.destroy()
                self.custom = False
        elif size == "Custom":
            self.sizeQr = 256
            self.imageScreen.config(file="Images/QrMedium.png")
            self.master.geometry("500x456")
            self.custom = True
            self.customEntry = Entry(self.frame_size, textvariable=self.customVal, justify='right', width=5)
            self.customEntry.grid(row=0, column=2)
            self.labelPix = Label(self.frame_size, text="px")
            self.labelPix.grid(row=0, column=3, sticky='w')
            self.textScreen.set("Se muestra 256X256, pero se exportará {}x{}".format(self.customEntry.get(), self.customEntry.get()))


    def validate(self, *args):
        value = self.customVal.get()
        if not value.isdigit():
            self.customVal.set("".join(filter(str.isdigit, value)))
        if len(value) > 4:
            self.customVal.set(value[:4])

        self.textScreen.set("Se muestra 256X256, pero se exportará {}x{}".format(self.customVal.get(), self.customVal.get()))

    def limpiar(self):
        self.master.geometry("500x350")
        self.linkEntry.delete(0, END)
        self.nameEntry.delete(0, END)
        self.createBut.config(state=DISABLED)
        self.screenState.config(text="")
        self.sizeVal.set("Pequeño")
        self.imageScreen.config(file="Images/QrSmall.png")


    def salir(self):
        self.master.destroy()

    def ayuda(self):

        messagebox.showinfo("Ayuda", "Para el generar el código QR debes:\n"
                                             "  > Ingresar el URL de YouTube.\n"
                                             "  > Ingresar un nombre para la imágen.\n"
                                             "  > Seleccionar un directorio para guardar.\n"
                                             "  > Seleccionar el tamaño.\n"
                                             "  > Oprimir el botón 'Generar'.\n\n"
                                             "Nota: las imágenes se guardarán en PNG.")

    def info(self):
        helpWin = Toplevel(self.master)
        helpWindow(helpWin)


class helpWindow():
    def __init__(self, master):
        self.master = master
        self.master.geometry("350x450")
        self.master.title("Acerca de Generador QR")
        self.master.resizable(0, 0)
        self.master.iconbitmap("QrIcon.ico")
        self.frame = Frame(self.master)
        self.frame.pack()


        self.logoImage = PhotoImage(file="Images/QrIcon_About.png")

        self.labelimage = Label(self.frame, image=self.logoImage)
        self.labelimage.grid(row=0, column=0, columnspan=2)
        self.labelimage.image = self.logoImage

        self.labeltitle = Label(self.frame, text="GENERADOR DE CODIGO QR")
        self.labeltitle.grid(row=1, column=0, columnspan=2)

        self.labelDescrip = Label(self.frame, text="Generador de códigos QR para links de YouTube")
        self.labelDescrip.grid(row=2, column=0, columnspan=2)

        self.labelversion = Label(self.frame, text="Version:")
        self.labelversion.grid(row=3, column=0, sticky='e')
        self.labelnumVer = Label(self.frame, text="1.0")
        self.labelnumVer.grid(row=3, column=1, sticky='w')

        self.frameLabel = LabelFrame(self.frame, text="Licencia")
        self.frameLabel.grid(row=4, column=0, columnspan=2, sticky="nsew")

        self.textLicence = Text(self.frameLabel)
        self.textLicence.grid(row=0, column=0)
        self.licence = open("LICENSE")
        self.textLicence.insert(1.0, self.licence.read())

        self.scroll = Scrollbar(self.frameLabel, command=self.textLicence.yview)
        self.scroll.grid(row=0, column=1, sticky='nsew')

        self.textLicence.config(font=("Arial", 5),state=DISABLED, yscrollcommand=self.scroll.set)


        self.acepButton = Button(self.frame, text="Aceptar", width=20, command=self.acpetar)
        self.acepButton.grid(row=5, column=0, columnspan=2, pady=10)

    def acpetar(self):
        self.master.destroy()


if __name__ == '__main__':

    root = Tk()
    mainWindow(root)
    root.mainloop()
