# Apartado que debe unir las series bases con el nuevo periodo

import tkinter as tk
import pandas  as pd
import shutil  as sh
from   glob               import glob
from   threading          import Thread
from   tkinter.filedialog import askdirectory, askopenfilenames

CENTER = {
    'fill'   : 'both',
    'expand' : True
}
TITLE = {
    'font' : ('Century Gothic',15)
}

class UpdateTab(tk.Frame):
    def __init__(self,window):
        super().__init__()
        self.window = window
        window.notebook.add(self, text = '2. Actualizar las Series')
        self.base_type = tk.IntVar()
        self.selected_items_msg_1 = tk.StringVar()
        self.selected_items_msg_2 = tk.StringVar()
        self.selected_items_msg_1.set('Se han seleccionado 0 archivos')
        self.selected_items_msg_2.set('Se han seleccionado 0 archivos')

        self.header()
        self.body()
        self.footer()
    
    def header(self):
        tk.Label(self,text='Función de Actualizar', **TITLE).pack(**CENTER)
        
    def body(self):
        container = tk.Frame(self)
        container.pack(padx=[20, 0],pady=[0, 10],**CENTER)

        tk.Label(
            container,
            text = '1. Seleccione las variables que contiene la serie base'
        ).grid(row = 0,column=0,sticky = 'w')

        tk.Radiobutton(
            container,
            text='Hidrometeorológicas',
            variable=self.base_type,
            value = 0
        ).grid(row = 0,column = 1, sticky = 'w')

        tk.Radiobutton(
            container,
            text='Meteorológicas',
            variable=self.base_type,
            value=1
        ).grid(row = 0,column = 2, sticky = 'w')

        tk.Label(
            container,
            text = '2. Selecciona la carpeta que contiene los archivos base: '
        ).grid(row = 1,column = 0, sticky = 'w')

        tk.Label(
            container,
            textvariable = self.selected_items_msg_1
        ).grid(row = 1,column = 1, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = self.search1
        ).grid(row = 1,column = 2, sticky = 'nsew')

        tk.Label(
            container,
            text = '3. Selecciona la carpeta que contiene los archivos adicionales: '
        ).grid(row = 2,column = 0, sticky = 'w')

        tk.Label(
            container,
            textvariable = self.selected_items_msg_2
        ).grid(row = 2,column = 1, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = self.search2
        ).grid(row = 2,column = 2, sticky = 'nsew')

        tk.Label(
            container,
            text='4. Selecciona la carpeta donde guardar los resultados: '
        ).grid(row = 3,column = 0, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = self.search3
        ).grid(row = 3,column = 1, columnspan=2, sticky = 'nsew')

        tk.Button(
            container,
            text    = 'Ejecutar',
            command = lambda: self.new_Thread(self.run)
        ).grid(row = 4,column=0,columnspan=3,sticky='nsew')

        tk.Button(
            container,
            text    = 'Completar',
            command = self.complete
        ).grid(row = 4,column=0,columnspan=3,sticky='nsew')

        tk.Button(
            container,
            text    = 'Cerrar',
            command = self.close
        ).grid(row = 6,column=0,columnspan=3,sticky='nsew')

    def search1(self):
        self.paths_1 = askopenfilenames(filetypes=(('Archivos CSV','*.csv'),))
        self.selected_items_msg_1.set('Se ha(n) seleccionado {} archivo(s)'.format(len(self.paths_1)))

    def search2(self):
        self.paths_2 = askopenfilenames(filetypes=(('Archivos CSV','*.csv'),))
        self.selected_items_msg_2.set('Se ha(n) seleccionado {} archivo(s)'.format(len(self.paths_2)))
    
    def search3(self):
        self.out_dir = askdirectory()
    
    def close(self):
        self.window.destroy()

    def new_Thread(self,function):
        thread = Thread(target=function)
        thread.start()
    
    def run(self):
        columns_h = ['Fecha','Hora','Temperatura [°C]','Precipitación Acumulada [mm]',
                     'Precipitación incremental [mm]','Nivel [cm]','Nivel Corregido [cm]']

        columns_m = ['Fecha','Hora','Temperatura [°C]','Vel.Viento [m/s]','Dir.Viento [°]',
                     'Dir.Rosa','Presión.B [mmHg]','Humedad Relativa [%]',
                     'Precipitación Acumulada [mm]','Precipitación incremental [mm]',
                     'Radiación [W/m2]','E.T. Acumulada [mm]','E.T. incrimental [mm]']

        for path in self.paths_1:
            name      = path.rsplit('\\',1)[-1]
            base_file = list(filter(lambda x: name in x, self.paths_2))[0]
            df        = pd.read_csv(base_file,sep=',',encoding='utf-8',low_memory=False)

            columns     = columns_h if df.shape[6] == 6 else \
                          columns_h if self.base_type.get() == 0 else \
                          columns_m
            
            df.columns  = columns

            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df2         = pd.read_csv(path,sep=',',encoding='utf-8',low_memory=False)

            df2 = df2.iloc[:,range(6)] if df.shape[1] == 6 else df2

            df2.columns  = columns
            df2['Fecha'] = pd.to_datetime(df2['Fecha'])
            
            df3          = pd.concat([df,df2])
            df3.to_csv(self.out_dir+'\\'+name,index=False,encoding='utf-8')

    def complete(self):

        paths_updated = glob(self.out_dir + '\\*.csv')

        for path in [path_updated.rsplit('\\',1)[-1].replace('.csv','') for path_updated in paths_updated]:
            self.paths_1.remove(list(filter(lambda x: path in x, self.paths_1))[0])

        for path in self.paths_1:
            sh.copy(path,self.out_dir + path.rsplit('\\',1)[-1])

    def footer(self):
        tk.Label(self,text='Hecho por: Franklin Andrés Lizarazo Muñoz').pack(**CENTER)