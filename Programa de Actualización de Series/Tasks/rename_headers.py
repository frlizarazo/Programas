# ================================================================================================
# Apartado que renombrar los encabezados de todas las series antes de realizar la union
# 
# STATE : Working 
# UPDATES : [] Optimizar la ejecución
#           [] Extraer common settings y widgets
#           [] Implementar barra de carga
#           [] Añadir estilo
#
# ================================================================================================

import tkinter as tk
import pandas as pd
from threading import Thread
from tkinter.filedialog import askopenfilenames

CENTER = {
    'fill'   : 'both',
    'expand' : True
}

TITLE = {
    'font' : ('Century Gothic',15)
}

class RenameTab(tk.Frame):
    def __init__(self,window):
        super().__init__()
        window.notebook.add(self, text = '1. Renombrar Encabezados')
        self.serie_type = tk.IntVar()
        self.base_type  = tk.IntVar()
        self.selected_items_msg = tk.StringVar()
        self.selected_items_msg.set('Se han seleccionado 0 archivos')

        self.header()
        self.body()
        self.footer()

    def header(self):
        tk.Label(self,text='Función de Renombrar', **TITLE).pack(**CENTER)

    def body(self):
         
        container = tk.Frame(self)
        container.pack(padx=20,pady=[0, 10],**CENTER)

        tk.Label(
            container, 
            text = '1. Seleccione con que tipo de serie de datos esta trabajando'
        ).grid(row=1,column=0,sticky='w')

        tk.Radiobutton(
            container,
            text='Albatros',
            variable=self.serie_type,
            value=0
        ).grid(row = 1,column = 1, sticky = 'w')
        
        tk.Radiobutton(
            container,
            text='Cdiac',
            variable=self.serie_type,
            value=1
        ).grid(row = 1,column = 2, sticky = 'w')


        tk.Label(
            container,
            text = '2. Seleccione las variables que contiene la serie base'
        ).grid(row=2,column=0,sticky = 'w')

        tk.Radiobutton(
            container,
            text='Hidrometeorológicas',
            variable=self.base_type,
            value=0
        ).grid(row = 2,column = 1, sticky = 'w')

        tk.Radiobutton(
            container,
            text='Meteorológicas',
            variable=self.base_type,
            value=1
        ).grid(row = 2,column = 2, sticky = 'w')


        tk.Label(
            container,
            text = '3. Seleccione las series de datos a renombrar'
        ).grid(row=3,column=0,sticky='w')

        tk.Label(
            container,
            textvariable = self.selected_items_msg
        ).grid(row = 3,column = 1, sticky = 'w')

        tk.Button(
            container,
            text='Buscar',
            command=self.search
        ).grid(row = 3,column = 2, sticky = 'nsew')

        tk.Button(
            container,
            text = 'Ejecutar',
            command=lambda: self.new_Thread(self.run)
        ).grid(row=4,column=0,columnspan=3,sticky='nsew')
    
    def footer(self):
        tk.Label(self,text='Hecho por: Franklin Andrés Lizarazo Muñoz').pack(**CENTER)
    
    def search(self):
        self.paths = askopenfilenames(filetypes=(('Archivo CSV','*.csv'),))
        self.selected_items_msg.set('Se ha(n) seleccionado {} archivo(s)'.format(len(self.paths)))

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

        for path in self.paths:

            if self.serie_type.get() == 0:
                df = pd.read_csv(path,skiprows=3,sep=';')
                df = df.iloc[:,[0,1,2,3,4,5,5]] if self.base_type.get() == 0 else \
                     df.iloc[:,range(13)]

            else:
                df = pd.read_csv(path,skiprows=0,sep=',')
                num_vars = df.shape[1]

                if self.base_type.get() == 0:
                    columns = [0,1,3,2,2,10,10] if num_vars==12 else [0,1,3,2,2,2,2]
                    nans    = [3] if num_vars==12 else [2,3,4,5,6]

                else:
                    columns = [0,1,3,5,6,6,8,7,7,2,11,11,9] if num_vars == 12 else \
                              [0,1,3,4,5,5,7,6,6,2,10,10,8] if num_vars == 11 else \
                              [0,1,3,4,5,5,7,6,6,2,8,8,8]
                    
                    nans    = [5,8,11]   if num_vars == 12 else \
                              [3,5,8,11] if num_vars == 11 else [5,8,11,12]

                df              = df.iloc[:,columns]
                df.iloc[:,nans] = pd.nan
            
            df.columns = columns_h if self.base_type.get() == 0 else columns_m
            df.to_csv(path,index=False,encoding='utf-8')