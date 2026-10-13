"""Public DEMO application. Independent data and intentionally restricted capabilities.

This module never imports the FULL app, its Database, or its private paths.
"""
from __future__ import annotations

import sqlite3
import sys
from contextlib import contextmanager
import tkinter as tk
from datetime import date, timedelta
from pathlib import Path
from tkinter import messagebox, ttk

from shared_ui.calendar_widget import ProductionCalendar
from shared_ui.palette import COLORS

APP_NAME = 'CineStage Manager — DEMO'
VERSION = '2.1.0-rc1-art-direction'
DATA_DIR = Path.home() / 'Documents' / 'CineStageManager_DEMO'
DB_FILE = DATA_DIR / 'demonstracion.db'
TABLES = {
    'Producciones': ('projects', 5, [('name','Producción'),('kind','Formato'),('status','Estado'),('budget','Presupuesto')]),
    'Clientes': ('clients', 10, [('name','Nombre'),('organization','Organización'),('status','Estado')]),
    'Guiones': ('scripts', 3, [('title','Guion'),('project','Producción'),('status','Estado')]),
    'Elenco y equipo': ('cast', 15, [('name','Integrante'),('role','Función'),('project','Producción')]),
    'Agenda': ('events', 20, [('event_date','Fecha AAAA-MM-DD'),('title','Actividad'),('kind','Tipo'),('project','Producción')]),
    'Finanzas': ('finance', 15, [('txn_date','Fecha AAAA-MM-DD'),('concept','Concepto'),('kind','Tipo'),('amount','Importe ARS')]),
}


@contextmanager
def demo_connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_FILE, timeout=10)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_demo(reset=False):
    """Reinitialization intentionally never opens private storage."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if reset and DB_FILE.exists():
        DB_FILE.unlink()
    with demo_connect() as con:
        con.execute('CREATE TABLE IF NOT EXISTS demo_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        for table, (_, _, columns) in [(spec[0], spec) for spec in TABLES.values()]:
            ddl = ', '.join(f'{col} {"REAL" if col in ("budget","amount") else "TEXT"}' for col, _ in columns)
            con.execute(f'CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {ddl})')
        if con.execute("SELECT value FROM demo_meta WHERE key='seeded'").fetchone():
            return
        day = date.today()
        d = lambda offset: (day + timedelta(days=offset)).isoformat()
        con.executemany('INSERT INTO projects(name,kind,status,budget) VALUES(?,?,?,?)', [
            ('Horizonte de Cristal', 'Largometraje', 'Producción', 15000000),
            ('La Última Función', 'Teatro', 'Ensayos', 2500000),
            ('Ecos de la Ciudad', 'Cortometraje', 'Preproducción', 950000),
        ])
        con.executemany('INSERT INTO clients(name,organization,status) VALUES(?,?,?)', [
            ('Valeria Torres [FICTICIO]', 'Estudio Boreal [DEMO]', 'Activo'),
            ('Nicolás Varela [FICTICIO]', 'Compañía Escena Sur [DEMO]', 'Activo'),
            ('Camila Ferrer [FICTICIO]', 'Producciones Horizonte [DEMO]', 'Activo'),
        ])
        con.executemany('INSERT INTO scripts(title,project,status) VALUES(?,?,?)', [
            ('Horizonte de Cristal — Guion principal','Horizonte de Cristal','Versión 2'),
            ('La Última Función — Acto I','La Última Función','Revisión'),
        ])
        con.executemany('INSERT INTO cast(name,role,project) VALUES(?,?,?)', [
            ('Marina Duarte [FICTICIO]', 'Actriz protagonista','Horizonte de Cristal'),
            ('Tomás Beltrán [FICTICIO]', 'Dirección de fotografía','Horizonte de Cristal'),
            ('Lucía Castro [FICTICIO]', 'Actriz','La Última Función'),
            ('Facundo Ríos [FICTICIO]', 'Iluminación','La Última Función'),
        ])
        con.executemany('INSERT INTO events(event_date,title,kind,project) VALUES(?,?,?,?)', [
            (d(0),'Reunión de producción','Reunión','Horizonte de Cristal'),
            (d(1),'Ensayo general','Ensayo','La Última Función'),
            (d(3),'Pruebas de cámara','Rodaje','Horizonte de Cristal'),
            (d(7),'Función de estreno','Función','La Última Función'),
            (d(12),'Casting','Casting','Ecos de la Ciudad'),
        ])
        con.executemany('INSERT INTO finance(txn_date,concept,kind,amount) VALUES(?,?,?,?)', [
            (d(-3),'Anticipo de producción','Ingreso',1250000),
            (d(-1),'Alquiler de iluminación','Gasto',180000),
            (d(0),'Vestuario y utilería','Gasto',76000),
        ])
        con.execute("INSERT INTO demo_meta(key,value) VALUES('seeded','1')")
        con.commit()


class DemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.configure(bg=COLORS['bg'])
        width = min(1340, max(940, self.winfo_screenwidth()-80))
        height = min(850, max(650, self.winfo_screenheight()-70))
        self.geometry(f'{width}x{height}+20+20')
        self.minsize(920, 630)
        self.current = 'Dashboard'
        self.calendar = None
        self._style()
        self._create_ui()
        self.select('Dashboard')

    def _style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=(11,8), background=COLORS['panel3'], foreground=COLORS['text'])
        style.map('TButton', background=[('active', COLORS['border'])])
        style.configure('TEntry', padding=6, fieldbackground=COLORS['panel2'], foreground=COLORS['text'])
        style.configure('TCombobox', padding=5, fieldbackground=COLORS['panel3'], background=COLORS['panel3'], foreground=COLORS['text'], arrowcolor=COLORS['text'])
        style.map('TCombobox', fieldbackground=[('readonly', COLORS['panel3'])], foreground=[('readonly', COLORS['text'])], selectbackground=[('readonly', COLORS['panel3'])], selectforeground=[('readonly', COLORS['text'])])
        style.configure('Treeview', background=COLORS['panel2'], fieldbackground=COLORS['panel2'], foreground=COLORS['text'], rowheight=30)
        style.map('Treeview', background=[('selected', COLORS['red_dark'])])
        style.configure('Treeview.Heading', background=COLORS['panel3'], foreground=COLORS['text'])
        style.configure('Accent.TButton', padding=9, background=COLORS['red'], foreground=COLORS['bg'])

    def _create_ui(self):
        sidebar=tk.Frame(self,bg=COLORS['panel'],width=244)
        sidebar.pack(side='left',fill='y');sidebar.pack_propagate(False)
        tk.Frame(self,bg=COLORS['red'],width=3).pack(side='left',fill='y')
        brand=tk.Frame(sidebar,bg=COLORS['panel'],padx=13,pady=12);brand.pack(fill='x')
        icon_path=Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent.parent))/'assets'/'cinestage_mark.png'
        try:
            self.logo_image=tk.PhotoImage(file=str(icon_path)).subsample(7,7)
            tk.Label(brand,image=self.logo_image,bg=COLORS['panel']).pack(side='left',padx=(0,9))
        except tk.TclError:
            tk.Label(brand,text='CS',bg=COLORS['panel'],fg=COLORS['yellow']).pack(side='left')
        header=tk.Frame(brand,bg=COLORS['panel']);header.pack(side='left',fill='x')
        tk.Label(header,text='CineStage',bg=COLORS['panel'],fg=COLORS['text'],font=('Segoe UI Semibold',15)).pack(anchor='w')
        tk.Label(header,text='MANAGER / DEMO',bg=COLORS['panel'],fg=COLORS['rose_soft'],font=('Segoe UI',8)).pack(anchor='w')
        tk.Frame(sidebar,bg=COLORS['border'],height=1).pack(fill='x',padx=13,pady=(0,9))
        self.nav_buttons={}
        groups=[('ESTUDIO',['Dashboard','Producciones','Agenda']),('CREACIÓN',['Guiones','Elenco y equipo']),('GESTIÓN',['Clientes','Finanzas']),('SISTEMA',['Acerca de'])]
        for section,items in groups:
            tk.Label(sidebar,text=section,bg=COLORS['panel'],fg=COLORS['rose_soft'],font=('Segoe UI Semibold',8),anchor='w').pack(fill='x',padx=16,pady=(10,4))
            for name in items:
                asset={'Dashboard':'dashboard','Producciones':'projects','Agenda':'agenda','Guiones':'scripts','Elenco y equipo':'cast','Clientes':'clients','Finanzas':'finance','Acerca de':'settings'}.get(name)
                try:self.nav_buttons[name]=tk.PhotoImage(file=str(Path(getattr(sys,'_MEIPASS',Path(__file__).resolve().parent.parent))/'assets'/'icons'/f'{asset}.png'))
                except tk.TclError:self.nav_buttons[name]=None
                tk.Button(sidebar,text='  '+name,image=self.nav_buttons[name],compound='left',anchor='w',
                    command=lambda n=name:self.select(n),bg=COLORS['panel'],fg=COLORS['text'],
                    activebackground=COLORS['panel3'],activeforeground=COLORS['yellow'],
                    relief='flat',borderwidth=0,highlightthickness=0,padx=12,pady=5,font=('Segoe UI',9)).pack(fill='x',padx=10)
        tk.Label(sidebar,text='V'+VERSION+'  ·  DATOS FICTICIOS',bg=COLORS['panel'],fg=COLORS['muted'],font=('Segoe UI',8),anchor='w').pack(side='bottom',fill='x',padx=15,pady=12)
        main=tk.Frame(self,bg=COLORS['bg']);main.pack(side='left',fill='both',expand=True)
        top=tk.Frame(main,bg=COLORS['panel'],height=56);top.pack(fill='x');top.pack_propagate(False)
        self.heading=tk.Label(top,text='',bg=COLORS['panel'],fg=COLORS['text'],font=('Segoe UI Semibold',12))
        self.heading.pack(side='left',padx=20,pady=16)
        tk.Label(top,text='DEMO / EVALUACIÓN',bg=COLORS['panel'],fg=COLORS['yellow'],font=('Segoe UI Semibold',9)).pack(side='right',padx=18)
        self.content=tk.Frame(main,bg=COLORS['bg'])
        self.content.pack(fill='both',expand=True,padx=20,pady=16)

    def _clear(self):
        for child in self.content.winfo_children():child.destroy()
        self.calendar = None

    def select(self, name):
        self.current = name
        self._clear()
        self.heading.configure(text=('ESTUDIO' if name=='Dashboard' else 'CREATIVE SUITE')+'   /   '+name)
        if name == 'Dashboard':
            self._dashboard()
        elif name == 'Acerca de':
            self._about()
        else:
            self._table_view(name)

    def _card(self, parent, title, value):
        card = tk.Frame(parent,bg=COLORS['panel2'],padx=15,pady=13,highlightbackground=COLORS['border'],highlightthickness=1)
        card.pack(side='left',fill='both',expand=True,padx=5)
        tk.Label(card,text=title,bg=COLORS['panel2'],fg=COLORS['muted']).pack(anchor='w')
        tk.Label(card,text=str(value),bg=COLORS['panel2'],fg=COLORS['yellow'],font=('Segoe UI Semibold',22)).pack(anchor='w')

    def _dashboard(self):
        head=tk.Frame(self.content,bg=COLORS['bg']);head.pack(fill='x',pady=(0,16))
        with demo_connect() as c:
            self._card(head,'Producciones',c.execute('SELECT count(*) FROM projects').fetchone()[0])
            self._card(head,'Personas del elenco',c.execute('SELECT count(*) FROM cast').fetchone()[0])
            self._card(head,'Actividades agendadas',c.execute('SELECT count(*) FROM events').fetchone()[0])
        lower=tk.Frame(self.content,bg=COLORS['bg']);lower.pack(fill='both',expand=True)
        events_frame=tk.Frame(lower,bg=COLORS['panel'],padx=12,pady=10)
        events_frame.pack(side='left',fill='both',expand=True,padx=(0,10))
        tk.Label(events_frame,text='Actividades del día seleccionado',bg=COLORS['panel'],fg=COLORS['text'],font=('Segoe UI Semibold',12)).pack(anchor='w',pady=(0,9))
        self.events_list=tk.Listbox(events_frame,bg=COLORS['panel2'],fg=COLORS['text'],font=('Segoe UI',11),relief='flat',highlightthickness=0)
        self.events_list.pack(fill='both',expand=True)
        ttk.Button(events_frame,text='Abrir agenda',command=lambda:self.select('Agenda')).pack(fill='x',pady=10)
        cal_frame=tk.Frame(lower,bg=COLORS['panel'],padx=10,pady=10)
        cal_frame.pack(side='left',fill='both',expand=True)
        tk.Label(cal_frame,text='Calendario de producción',bg=COLORS['panel'],fg=COLORS['text'],font=('Segoe UI Semibold',12)).pack(anchor='w')
        self.calendar=ProductionCalendar(cal_frame,self._calendar_changed)
        self.calendar.pack(fill='both',expand=True)
        self._calendar_changed(self.calendar.selected)

    def _calendar_changed(self, selected):
        if self.calendar is None:return
        self.events_list.delete(0,'end')
        with demo_connect() as c:
            for r in c.execute('SELECT title,kind FROM events WHERE event_date=? ORDER BY title',(selected.isoformat(),)):
                self.events_list.insert('end',f"{r['kind']} · {r['title']}")
            marked=set()
            for r in c.execute('SELECT DISTINCT event_date FROM events WHERE substr(event_date,1,7)=?', (selected.strftime('%Y-%m'),)):
                try:marked.add(date.fromisoformat(r['event_date']))
                except ValueError:pass
        self.calendar.set_marked(marked)
        if not self.events_list.size():self.events_list.insert('end','Sin eventos para esta fecha.')

    def _table_view(self, name):
        table, limit, columns = TABLES[name]
        top=tk.Frame(self.content,bg=COLORS['bg']);top.pack(fill='x',pady=(0,12))
        tk.Label(top,text=f'Base de evaluación creativa · Máximo {limit} registros',bg=COLORS['bg'],fg=COLORS['muted']).pack(side='left')
        ttk.Button(top,text='Nuevo',style='Accent.TButton',command=lambda:self._new(name)).pack(side='right')
        ttk.Button(top,text='Editar',command=lambda:self._edit(name)).pack(side='right',padx=5)
        ttk.Button(top,text='Eliminar',command=lambda:self._delete(name)).pack(side='right')
        frame=tk.Frame(self.content,bg=COLORS['panel']);frame.pack(fill='both',expand=True)
        self.tree=ttk.Treeview(frame,columns=[field for field,_ in columns],show='headings',selectmode='browse')
        for field,title in columns:
            self.tree.heading(field,text=title)
            self.tree.column(field,width=155,stretch=True)
        self.tree.pack(side='left',fill='both',expand=True)
        bar=ttk.Scrollbar(frame,orient='vertical',command=self.tree.yview);bar.pack(side='right',fill='y');self.tree.configure(yscrollcommand=bar.set)
        self.tree.bind('<Double-1>',lambda _:self._edit(name))
        with demo_connect() as c:
            for r in c.execute(f'SELECT * FROM {table} ORDER BY id DESC'):
                self.tree.insert('','end',iid=str(r['id']),values=[r[field] for field,_ in columns])
        foot=tk.Frame(self.content,bg=COLORS['bg']);foot.pack(fill='x',pady=10)
        ttk.Button(foot,text='Exportar versión completa',command=self._restricted).pack(side='left')
        ttk.Button(foot,text='Restablecer demostración',command=self._reset).pack(side='right')

    def _selected(self):
        selected=self.tree.selection()
        if not selected:messagebox.showinfo('Seleccionar','Elegí un registro primero.',parent=self);return None
        return int(selected[0])

    def _form(self, name, initial=None):
        table,_,columns=TABLES[name]
        win=tk.Toplevel(self);win.title('CineStage DEMO — Registro');win.configure(bg=COLORS['panel']);win.transient(self);win.grab_set();win.resizable(False,False)
        win.geometry('550x'+str(130+57*len(columns)))
        fields={}; result={}
        tk.Label(win,text=f'{"Editar" if initial else "Nuevo"} · {name}',bg=COLORS['panel'],fg=COLORS['text'],font=('Segoe UI Semibold',14)).pack(pady=14)
        body=tk.Frame(win,bg=COLORS['panel']);body.pack(fill='both',expand=True,padx=20)
        for col,title in columns:
            line=tk.Frame(body,bg=COLORS['panel']);line.pack(fill='x',pady=4)
            tk.Label(line,text=title,bg=COLORS['panel'],fg=COLORS['muted'],width=22,anchor='w').pack(side='left')
            var=tk.StringVar(value='' if initial is None else str(initial[col] or ''))
            ttk.Entry(line,textvariable=var).pack(side='left',fill='x',expand=True)
            fields[col]=var
        def save():
            payload={name:var.get().strip() for name,var in fields.items()}
            if not all(payload.values()):messagebox.showwarning('Datos incompletos','Completá todos los campos.',parent=win);return
            for field in ('event_date','txn_date'):
                if field in payload:
                    try:date.fromisoformat(payload[field])
                    except ValueError:messagebox.showwarning('Fecha inválida','Usá AAAA-MM-DD.',parent=win);return
            for field in ('amount','budget'):
                if field in payload:
                    try:payload[field]=float(payload[field])
                    except ValueError:messagebox.showwarning('Valor inválido','Ingresá un importe numérico.',parent=win);return
            result.update(payload);win.destroy()
        ttk.Button(win,text='Guardar',style='Accent.TButton',command=save).pack(pady=12)
        win.wait_window()
        return result or None

    def _new(self,name):
        table,limit,columns=TABLES[name]
        with demo_connect() as c:
            if c.execute(f'SELECT count(*) FROM {table}').fetchone()[0] >= limit:
                self._restricted();return
        data=self._form(name)
        if data:
            with demo_connect() as c:
                cols=list(data)
                c.execute(f'INSERT INTO {table} ({",".join(cols)}) VALUES ({",".join("?" for _ in cols)})',tuple(data.values()))
            self.select(name)

    def _edit(self,name):
        ident=self._selected()
        if ident is None:return
        table,_,columns=TABLES[name]
        with demo_connect() as c:r=c.execute(f'SELECT * FROM {table} WHERE id=?',(ident,)).fetchone()
        if r is None:return
        data=self._form(name,r)
        if data:
            with demo_connect() as c:
                c.execute(f'UPDATE {table} SET '+','.join(f'{key}=?' for key in data)+' WHERE id=?',(*data.values(),ident))
            self.select(name)

    def _delete(self,name):
        ident=self._selected()
        if ident is None:return
        if not messagebox.askyesno('Borrar registro DEMO','¿Eliminar este registro ficticio?',parent=self):return
        table,_,_=TABLES[name]
        with demo_connect() as c:c.execute(f'DELETE FROM {table} WHERE id=?',(ident,))
        self.select(name)

    def _reset(self):
        if messagebox.askyesno('Restablecer DEMO','Se eliminarán únicamente los cambios hechos a los datos ficticios. ¿Continuar?',parent=self):
            init_demo(reset=True)
            self.select(self.current)

    def _restricted(self):
        messagebox.showinfo('Función privada','Esta función está disponible en CineStage Manager FULL. La demostración conserva exclusivamente datos ficticios.',parent=self)

    def _about(self):
        block=tk.Frame(self.content,bg=COLORS['panel'],padx=24,pady=24);block.pack(fill='x')
        for text,size,color in [
            ('CineStage Manager',22,COLORS['text']),
            ('Film & Theatre Production Management',12,COLORS['red_bright']),
            (f'Edición DEMO · {VERSION}',11,COLORS['muted']),
            ('Sistema local de gestión de producciones audiovisuales y teatrales.',11,COLORS['text']),
            ('Esta distribución solo utiliza proyectos y contactos ficticios.',11,COLORS['muted']),
            ('La versión completa incorpora guiones extensos, multimedia, respaldos, PDF y Excel.',11,COLORS['muted']),
        ]:tk.Label(block,text=text,bg=COLORS['panel'],fg=color,font=('Segoe UI',size),wraplength=700,justify='left').pack(anchor='w',pady=7)
        ttk.Button(block,text='Restablecer datos de muestra',command=self._reset).pack(anchor='w',pady=12)


def main():
    init_demo()
    app=DemoApp()
    app.mainloop()
    return 0

if __name__=='__main__':
    raise SystemExit(main())
