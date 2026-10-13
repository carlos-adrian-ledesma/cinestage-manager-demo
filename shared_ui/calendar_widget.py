"""Interactive production calendar, with no external calendar dependency."""
from __future__ import annotations

import calendar
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk
from collections.abc import Callable

from .palette import COLORS

MONTHS = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
DAYS = ("Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do")


def shift_month(year: int, month: int, offset: int) -> tuple[int, int]:
    serial = year * 12 + month - 1 + offset
    year, m0 = divmod(serial, 12)
    if not 1 <= year <= 9999:
        raise ValueError("Año fuera de rango")
    return year, m0 + 1


class ProductionCalendar(tk.Frame):
    def __init__(self, parent: tk.Misc, on_select: Callable[[date], None], selected: date | None = None):
        super().__init__(parent, bg=COLORS['panel'])
        self.selected = selected or date.today()
        self.year, self.month = self.selected.year, self.selected.month
        self.on_select = on_select
        self.marked: set[date] = set()
        self.month_var = tk.StringVar(value=MONTHS[self.month-1])
        self.year_var = tk.StringVar(value=str(self.year))
        navigation = tk.Frame(self, bg=COLORS['panel'])
        navigation.pack(fill='x', padx=7, pady=(5, 8))
        ttk.Button(navigation, text='◀', width=3, command=lambda: self.shift(-1)).pack(side='left')
        self.month_select = ttk.Combobox(navigation, values=MONTHS, textvariable=self.month_var, width=11, state='readonly')
        self.month_select.pack(side='left', fill='x', expand=True, padx=4)
        self.month_select.bind('<<ComboboxSelected>>', self._on_month_change)
        self.year_select = ttk.Combobox(navigation, values=tuple(str(i) for i in range(1900, 2101)), textvariable=self.year_var, width=6, state='readonly')
        self.year_select.pack(side='left', padx=3)
        self.year_select.bind('<<ComboboxSelected>>', self._on_year_change)
        ttk.Button(navigation, text='▶', width=3, command=lambda: self.shift(1)).pack(side='left')
        self.grid_holder = tk.Frame(self, bg=COLORS['panel'])
        self.grid_holder.pack(fill='both', expand=True, padx=7)
        actions = tk.Frame(self, bg=COLORS['panel'])
        actions.pack(fill='x', padx=9, pady=7)
        ttk.Button(actions, text='Hoy', command=self.today).pack(side='left')
        self.selected_label = tk.Label(actions, text='', bg=COLORS['panel'], fg=COLORS['red_bright'], font=('Segoe UI Semibold', 9))
        self.selected_label.pack(side='right')
        self.redraw()

    def _on_month_change(self, _event=None):
        self.month = MONTHS.index(self.month_var.get())+1
        self._sync_date()

    def _on_year_change(self, _event=None):
        try:
            year = int(self.year_var.get())
            if not 1900 <= year <= 2100:
                raise ValueError('El año debe estar entre 1900 y 2100')
            self.year = year
        except ValueError:
            self.year_var.set(str(self.year))
            return
        self._sync_date()

    def _sync_date(self):
        day = min(self.selected.day, calendar.monthrange(self.year, self.month)[1])
        self.select(date(self.year, self.month, day))

    def shift(self, delta: int):
        try:
            self.year, self.month = shift_month(self.year, self.month, delta)
        except ValueError:
            return
        self._sync_date()

    def today(self):
        self.select(date.today())

    def select(self, selected: date, *, notify: bool = True):
        self.selected = selected
        self.year, self.month = selected.year, selected.month
        self.month_var.set(MONTHS[self.month - 1])
        self.year_var.set(str(self.year))
        self.redraw()
        if notify:
            self.on_select(self.selected)

    def set_marked(self, dates: set[date]):
        self.marked = dates
        self.redraw()

    def redraw(self):
        for widget in self.grid_holder.winfo_children():
            widget.destroy()
        for col, name in enumerate(DAYS):
            tk.Label(self.grid_holder, text=name, bg=COLORS['panel'], fg=COLORS['muted'], font=('Segoe UI Semibold', 9)).grid(row=0, column=col, sticky='nsew')
            self.grid_holder.grid_columnconfigure(col, weight=1)
        for r, week in enumerate(calendar.monthcalendar(self.year, self.month), start=1):
            self.grid_holder.grid_rowconfigure(r, weight=1)
            for col, day in enumerate(week):
                if not day:
                    tk.Label(self.grid_holder, text='', bg=COLORS['panel']).grid(row=r, column=col, sticky='nsew')
                    continue
                d = date(self.year, self.month, day)
                active = d == self.selected
                now = d == date.today()
                marked = d in self.marked
                tk.Button(self.grid_holder, text=f'{day}{"•" if marked else ""}',
                          command=lambda value=d: self.select(value),
                          font=('Segoe UI Semibold' if active else 'Segoe UI', 9),
                          fg=COLORS['bg'] if active else (COLORS['red_bright'] if now or marked else COLORS['text']),
                          bg=COLORS['red_bright'] if active else COLORS['panel2'],
                          activebackground=COLORS['red_dark'], activeforeground=COLORS['text'],
                          relief='flat', bd=0, highlightthickness=0, padx=1, pady=3).grid(row=r, column=col, padx=2, pady=2, sticky='nsew')
        self.selected_label.configure(text=self.selected.strftime('%d/%m/%Y'))
