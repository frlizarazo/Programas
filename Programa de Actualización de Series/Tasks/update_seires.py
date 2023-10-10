# Apartado que debe unir las series bases con el nuevo periodo

import tkinter as tk
from tkinter.filedialog import askdirectory

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
        window.notebook.add(self, text = '2. Actualizar las Series')

        self.header()
        self.body()
        self.footer()
    
    def header(self):
        tk.Label(self,text='Función de Actualizar', **TITLE).pack(**CENTER)
        
    def body(self):
        container = tk.Frame(self)
        container.pack(padx=20,pady=[0, 10],**CENTER)

        tk.Label(
            container,
            text = 'Selecciona la carpeta que contiene los archivos base: '
        ).grid(row = 0,column = 0, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = ...
        ).grid(row = 0,column = 1, sticky = 'nsew')

        tk.Label(
            container,
            text = 'Selecciona la carpeta que contiene los archivos adicionales: '
        ).grid(row = 1,column = 0, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = ...
        ).grid(row = 1,column = 1, sticky = 'nsew')

        tk.Label(
            container,
            text='Selecciona la carpeta donde guardar los resultados: '
        ).grid(row = 2,column = 0, sticky = 'w')

        tk.Button(
            container,
            text    = 'Buscar',
            command = ...
        ).grid(row = 2,column = 1, sticky = 'nsew')

        tk.Button(
            container,
            text    = 'Ejecutar',
            command = ...
        ).grid(row=4,column=0,columnspan=2,sticky='nsew')

    def search1(self):
        self.dir1 = askdirectory()

    def search2(self):
        self.dir2 = askdirectory()
    
    def search3(self):
        self.dir3 = askdirectory()
    
    def run(self):
        columns_h = ['Fecha','Hora','Temperatura [°C]','Precipitación Acumulada [mm]',
                     'Precipitación incremental [mm]','Nivel [cm]','Nivel Corregido [cm]']

        columns_m = ['Fecha','Hora','Temperatura [°C]','Vel.Viento [m/s]','Dir.Viento [°]',
                     'Dir.Rosa','Presión.B [mmHg]','Humedad Relativa [%]',
                     'Precipitación Acumulada [mm]','Precipitación incremental [mm]',
                     'Radiación [W/m2]','E.T. Acumulada [mm]','E.T. incrimental [mm]']

        # ================================= Para estaciones de Albatroz ===================================

        # -------------------------Hidrometeorológicas
        ruta1 = j(base,'New Month\Encabezados',New_Month,'Albatros\Hidrometeorológicas')
        ruta2 = j(base,Base_Months,'Hidrometeorológicas')
        ruta3 = j(base,Output_folder,'Hidrometeorológicas')

        paths1 = g(ruta1+'\\*.csv')
        paths2 = g(ruta2+'\\*.csv')

        for path in paths1:
            columns = columnas_h   
            name      = path.rsplit('\\',1)[-1]
            base_file = list(filter(lambda x: name in x, paths2))[0]
            df        = pd.read_csv(base_file,sep=',',encoding='utf-8',low_memory=False)

            if df.shape[1] == 6:
                columns = columnas_h[0:-1]
            df.columns  = columns

            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df2         = pd.read_csv(path,sep=',',encoding='utf-8',low_memory=False)

            if df.shape[1] == 6:
                df2 = df2.iloc[:,range(6)]

            df2.columns  = columns
            df2['Fecha'] = pd.to_datetime(df2['Fecha'])
            df3          = pd.concat([df,df2])
            df3.columns  = columns
            df3.to_csv(ruta3+'\\'+name,index=False,encoding='utf-8')

        # -------------------------Meteorológicas
        ruta1 = j(base,'New Month\Encabezados',New_Month,'Albatros\Meteorológicas')
        ruta2 = j(base,Base_Months,'Meteorológicas')
        ruta3 = j(base,Output_folder,'Meteorológicas')

        paths1=g(ruta1+'\\*.csv')
        paths2=g(ruta2+'\\*.csv')

        for path in paths1:
            name         = path.rsplit('\\',1)[-1]
            base_file    = list(filter(lambda x: name in x, paths2))[0]
            df           = pd.read_csv(base_file,sep=',',encoding='utf-8',low_memory=False)
            df.columns   = columnas_m
            df['Fecha']  = pd.to_datetime(df['Fecha'])
            df2          = pd.read_csv(path,sep=',',encoding='utf-8',low_memory=False)
            df2.columns  = columnas_m
            df2['Fecha'] = pd.to_datetime(df2['Fecha'])
            df3          = pd.concat([df,df2])
            df3.columns  = columnas_m
            df3.to_csv(ruta3+'\\'+name,index=False,encoding='utf-8')

        #  ============================== Para estaciones del CDIAC ======================================

        # -------------------------Hidrometeorológicas

        ruta1 = j(base,'New Month\Encabezados',New_Month,'CDIAC\Hidrometeorológicas')
        ruta2 = j(base,Base_Months,'Hidrometeorológicas')
        ruta3 = j(base,Output_folder,'Hidrometeorológicas')

        paths1 = g(ruta1+'\\*.csv')
        paths2 = g(ruta2+'\\*.csv')

        for path in paths1:
            columns   = columnas_h
            name      = path.rsplit('\\',1)[-1]
            base_file = list(filter(lambda x: name in x, paths2))[0]
            df        = pd.read_csv(base_file,sep=',',encoding='utf-8',low_memory=False)
            if df.shape[1] == 6:
                columns = columnas_h[0:-1]
            df.columns  = columns
            df['Fecha'] = pd.to_datetime(df['Fecha'])
            df2         = pd.read_csv(path,sep=',',encoding='utf-8',low_memory=False)
            if df.shape[1] == 6:
                df2 = df2.iloc[:,range(6)]
            df2.columns = columns
            df2['Fecha'] = pd.to_datetime(df2['Fecha'])
            df3          = pd.concat([df,df2])
            df3.columns  = columns
            df3.to_csv(ruta3+'\\'+name,index=False,encoding='utf-8')

        # ------------------------- Meteorológicas
        ruta1 = j(base,'New Month\Encabezados',New_Month,'CDIAC\Meteorológicas')
        ruta2 = j(base,Base_Months,'Meteorológicas')
        ruta3 = j(base,Output_folder,'Meteorológicas')

        paths1 = g(ruta1+'\\*.csv')
        paths2 = g(ruta2+'\\*.csv')

        for path in paths1:
            name         = path.rsplit('\\',1)[-1]
            base_file    = list(filter(lambda x: name in x, paths2))[0]
            df           = pd.read_csv(base_file,sep=',',encoding='utf-8',low_memory=False)
            df.columns   = columnas_m
            df['Fecha']  = pd.to_datetime(df['Fecha'])
            df2          = pd.read_csv(path,sep=',',encoding='utf-8',low_memory=False)
            df2.columns  = columnas_m
            df2['Fecha'] = pd.to_datetime(df2['Fecha'])
            df3          = pd.concat([df,df2])
            df3.columns  = columnas_m
            df3.to_csv(ruta3+'\\'+name,index=False,encoding='utf-8')

        # ============================ Verificar las que faltan por actualizar ============================

        dir0 = j(base,Base_Months)
        dir1 = j(base,Output_folder)

        paths         = g(j(dir0,'*','*.csv'))
        paths_updated = g(j(dir1,'*','*.csv'))

        for path in [path_updated.rsplit('\\',1)[-1].replace('.csv','') for path_updated in paths_updated]:
            paths.remove(list(filter(lambda x: path in x, paths))[0])

        for path in paths:
            sh.copy(path,path.replace(Base_Months,Output_folder))

    def footer(self):
        tk.Label(self,text='Hecho por: Franklin Andrés Lizarazo Muñoz').pack(**CENTER)