# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 20:33:06 2023

@author: kryst
"""

# DATA PLOTTER by Krystian Mistewicz

from tkinter import Tk, Label, Button, Menu, filedialog, messagebox, Frame, Entry, Canvas, ttk
import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

app_ver = 6.8 #version of the application

czy_import_udany = False
macierz_wynikow = []
macierz_plikow = []
Nmax = 10 # maksymalna możliwa liczba plików do wczytania przez program
# macierz załadowanych plików zawierająca:
# pełną nazwę pliku (wraz ze ścieżką), liczbę kolumn w pliku, inf. czy obrazować plik na wykresie, nr kolumny X, nr kolumny Y

#%% funkcja przypisania separatora danych do przecinka, tabulatora lub spacji
def separator_przypisz(n):
    global separator
    if n == 1:
        separator = ','
    elif n == 2:
        separator = '\t'
    elif n == 3:
        separator = ' '
    okno_sep.destroy()
    odczyt_danych()

#%% funkcja wywołująca okno z pytaniem o separator danych
def okno_wczytaj_separator():
    global okno_sep
    okno_sep = Tk()
    #okno_sep.attributes('-disabled', True)
    okno_sep.title("Choose data separator")
    szerokosc_okna = 600
    wysokosc_okna = 400
    w = okno_sep.winfo_screenwidth()
    h = okno_sep.winfo_screenheight()
    x = int((w - szerokosc_okna)/2)
    y = int((h - wysokosc_okna)/2)
    okno_sep.configure(bg='white')
    okno_sep.geometry("%ix%i+%i+%i" % (szerokosc_okna, wysokosc_okna, x, y))
    ramka1 = Frame(okno_sep)
    ramka1.pack()
    ramka1.configure(bg='white')
    tekst1 = Label(ramka1, bg='white', text="\n\nWhich data separator does the file contain?\n\n", font='Helvetica 16')
    tekst1.pack()
    ramka2 = Frame(okno_sep)
    ramka2.pack()
    ramka2.configure(bg='white')
    przycisk1 = Button(ramka2, text="comma", font='Helvetica 12', width=10, command=lambda:separator_przypisz(1))
    przycisk1.pack()
    tekst2 = Label(ramka2, bg='white', text="\n", font='Helvetica 3', width=10)
    tekst2.pack()
    przycisk2 = Button(ramka2, text="tab", font='Helvetica 12', width=10, command=lambda:separator_przypisz(2))
    przycisk2.pack()
    tekst3 = Label(ramka2, bg='white', text="\n", font='Helvetica 3')
    tekst3.pack()
    przycisk3 = Button(ramka2, text="space", font='Helvetica 12', width=10, command=lambda:separator_przypisz(3))
    przycisk3.pack()
    okno_sep.mainloop()

#%% funkcja odczytu pliku
def odczyt_pliku():
    global plik
    if len(macierz_wynikow) < Nmax:
        p = filedialog.askopenfile()
        if p == None:
            messagebox.showerror("Error", "File was not loaded.")
        else:
            plik = p
            okno_wczytaj_separator()
    else:
        messagebox.showerror("Data limit", "You can load only up to %i files." % Nmax)

#%% funkcja modyfikująca tekst przycisku i jego stan, gdzie n to numer przycisku
def modyfikuj_przycisk(n, przycisk):
    tekst1 = "Yes"
    tekst2 = "No"
    kolor1 = 'blue'
    kolor2 = 'red'
    czcionka = 'Helvetica 12'
    if not macierz_plikow [n-1][2]:
        przycisk.configure(text=tekst1, fg=kolor1, font=czcionka)
    else:
        przycisk.configure(text=tekst2, fg=kolor2, font=czcionka)
    macierz_plikow [n-1][2] = not macierz_plikow [n-1][2]

#%% funkcja rysujacą część tabeli
def rysuj_elementy_tabeli(N, k):
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=0, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=1, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=2, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=3, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=4, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='vertical').grid(column=5, row=N + k, rowspan=3, sticky='nse')
    ttk.Separator(ramka_tabela, orient='horizontal').grid(column=1, row=N + 3, columnspan=7, sticky='wen')

#%% funkcja odczytu danych z pliku
def odczyt_danych():
    global czy_import_udany
    global macierz_wynikow
    global lista_plikow
    global nr_kolumny_x01, nr_kolumny_x02, nr_kolumny_x03, nr_kolumny_x04, nr_kolumny_x05, nr_kolumny_x06, nr_kolumny_x07, nr_kolumny_x08, nr_kolumny_x09, nr_kolumny_x10
    global nr_kolumny_y01, nr_kolumny_y02, nr_kolumny_y03, nr_kolumny_y04, nr_kolumny_y05, nr_kolumny_y06, nr_kolumny_y07, nr_kolumny_y08, nr_kolumny_y09, nr_kolumny_y10
    global przycisk01, przycisk02, przycisk03, przycisk04, przycisk05, przycisk06, przycisk07, przycisk08, przycisk09, przycisk10
    macierz = []
    while True:
        linia = plik.readline()
        if len(linia) == 0:
            break
        lista_wartosci_kolumn = linia.split(separator)
        lista_wynikow = []
        for kolumna in range (len(lista_wartosci_kolumn)):
            try:
                lista_wynikow.append(float(lista_wartosci_kolumn[kolumna]))
                udana_konwersja = True
            except ValueError:
                udana_konwersja = False
        if udana_konwersja:
            macierz.append(lista_wynikow)
    if len(macierz) > 0:
        macierz_wynikow.append(macierz)
        macierz_plikow [len(macierz_wynikow)-1][0] = plik.name
        macierz_plikow [len(macierz_wynikow)-1][1] = len(macierz [0])
    if len(macierz) == 0:
        czy_sa_dane = False
    else:
        czy_sa_dane = True
    czy_import_udany = czy_sa_dane
    if czy_import_udany:
        messagebox.showinfo("Data was loaded", "Data was successfully loaded from file\n%s." % plik.name)
        N = len(macierz_wynikow) # liczba zastawów danych
        sciezka = macierz_plikow[N - 1][0]
        nazwa_pliku = sciezka.split('/')[len(sciezka.split('/')) - 1]
        if N == 1:
            ramka_tabela.configure(bg='white')
            ramka_tabela.pack()
            tekst_pusty = Label(ramka_tabela, bg='white', text="", font='Helvetica 16', width=10)
            tekst_pusty.grid(row=1, column=1)
            tekst1_nagl = Label(ramka_tabela, bg='white', text="File name", font='Helvetica 12 bold', width=30)
            tekst1_nagl.grid(row=N+1, column=1)
            tekst2_nagl = Label(ramka_tabela, bg='white', text="Number\nof columns\nin file", font='Helvetica 12 bold', width=15)
            tekst2_nagl.grid(row=N+1, column=2)
            tekst3_nagl = Label(ramka_tabela, bg='white', text="Plot data\nfrom file?", font='Helvetica 12 bold', width=15)
            tekst3_nagl.grid(row=N+1, column=3)
            tekst4_nagl = Label(ramka_tabela, bg='white', text="Indicate\nnumber of\nX column", font='Helvetica 12 bold', width=15)
            tekst4_nagl.grid(row=N+1, column=4)
            tekst5_nagl = Label(ramka_tabela, bg='white', text="Indicate\nnumber of\nY column", font='Helvetica 12 bold', width=15)
            tekst5_nagl.grid(row=N+1, column=5)
            tekst11 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst11.grid(row=N+2, column=1)
            tekst12 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst12.grid(row=N+2, column=2)
            przycisk01 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk01), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk01.grid(row=N+2, column=3)
            nr_kolumny_x01 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x01.grid(row=N+2, column=4)
            nr_kolumny_y01 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y01.grid(row=N+2, column=5)
            ttk.Separator(ramka_tabela, orient='horizontal').grid(column=1, row=N+1, columnspan=7, sticky='wen')
            ttk.Separator(ramka_tabela, orient='horizontal').grid(column=1, row=N+2, columnspan=7, sticky='wen')
            rysuj_elementy_tabeli(N, 1)
        elif N == 2:
            tekst21 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst21.grid(row=N+2, column=1)
            tekst22 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst22.grid(row=N+2, column=2)
            przycisk02 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk02), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk02.grid(row=N+2, column=3)
            nr_kolumny_x02 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x02.grid(row=N+2, column=4)
            nr_kolumny_y02 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y02.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 3:
            tekst31 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst31.grid(row=N+2, column=1)
            tekst32 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst32.grid(row=N+2, column=2)
            przycisk03 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk03), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk03.grid(row=N+2, column=3)
            nr_kolumny_x03 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x03.grid(row=N+2, column=4)
            nr_kolumny_y03 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y03.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 4:
            tekst41 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst41.grid(row=N+2, column=1)
            tekst42 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst42.grid(row=N+2, column=2)
            przycisk04 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk04), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk04.grid(row=N+2, column=3)
            nr_kolumny_x04 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x04.grid(row=N+2, column=4)
            nr_kolumny_y04 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y04.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 5:
            tekst51 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst51.grid(row=N+2, column=1)
            tekst52 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst52.grid(row=N+2, column=2)
            przycisk05 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk05), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk05.grid(row=N+2, column=3)
            nr_kolumny_x05 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x05.grid(row=N+2, column=4)
            nr_kolumny_y05 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y05.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 6:
            tekst61 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst61.grid(row=N+2, column=1)
            tekst62 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst62.grid(row=N+2, column=2)
            przycisk06 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk06), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk06.grid(row=N+2, column=3)
            nr_kolumny_x06 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x06.grid(row=N+2, column=4)
            nr_kolumny_y06 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y06.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 7:
            tekst71 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst71.grid(row=N+2, column=1)
            tekst72 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst72.grid(row=N+2, column=2)
            przycisk07 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk07), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk07.grid(row=N+2, column=3)
            nr_kolumny_x07 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x07.grid(row=N+2, column=4)
            nr_kolumny_y07 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y07.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 8:
            tekst81 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst81.grid(row=N+2, column=1)
            tekst82 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst82.grid(row=N+2, column=2)
            przycisk08 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk08), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk08.grid(row=N+2, column=3)
            nr_kolumny_x08 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x08.grid(row=N+2, column=4)
            nr_kolumny_y08 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y08.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 9:
            tekst91 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst91.grid(row=N+2, column=1)
            tekst92 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst92.grid(row=N+2, column=2)
            przycisk09 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk09), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk09.grid(row=N+2, column=3)
            nr_kolumny_x09 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x09.grid(row=N+2, column=4)
            nr_kolumny_y09 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y09.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
        elif N == 10:
            tekst101 = Label(ramka_tabela, bg='white', text=nazwa_pliku, font='Helvetica 12', width=30)
            tekst101.grid(row=N+2, column=1)
            tekst102 = Label(ramka_tabela, bg='white', text=str(macierz_plikow [N-1][1]), font='Helvetica 12', width=20)
            tekst102.grid(row=N+2, column=2)
            przycisk10 = Button(ramka_tabela, command=lambda:modyfikuj_przycisk(N, przycisk10), fg='red', text="No", font='Helvetica 12', width=5)
            przycisk10.grid(row=N+2, column=3)
            nr_kolumny_x10 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_x10.grid(row=N+2, column=4)
            nr_kolumny_y10 = Entry(ramka_tabela, width=5, justify='center')
            nr_kolumny_y10.grid(row=N+2, column=5)
            rysuj_elementy_tabeli(N, 2)
    else:
        messagebox.showinfo("Data was not loaded", "Data was not loaded from file\n%s.\nSomething went wrong." % plik.name)
    if len(macierz_wynikow) < Nmax:
        pytanie_kolejny_odczyt = messagebox.askyesno("Load next file?", "Doy you want to load other data file?")
        if pytanie_kolejny_odczyt:
            odczyt_pliku()

#%% funkcja rysowania wykresu
def narysuj_wykres(macierz_wynikow):
    if len(macierz_wynikow) > 0:
        rysuj = True
        licznik = 0
        for i in range(Nmax):
            if macierz_plikow[i][2]:
                if i == 0:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x01.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y01.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 1:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x02.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y02.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 2:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x03.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y03.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 3:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x04.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y04.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 4:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x05.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y05.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 5:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x06.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y06.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 6:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x07.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y07.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 7:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x08.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y08.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 8:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x09.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y09.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
                elif i == 9:
                    try:
                        macierz_plikow [i][3] = int(nr_kolumny_x10.get())
                        macierz_plikow [i][4] = int(nr_kolumny_y10.get())
                        if macierz_plikow [i][3] < 1 or macierz_plikow [i][3] > macierz_plikow [i][1] or macierz_plikow [i][4] < 1 or macierz_plikow [i][4] > macierz_plikow [i][1]:
                            rysuj = False
                    except ValueError:
                        rysuj = False
            else:
                licznik += 1
        if licznik == Nmax:
            messagebox.showerror("No data to show", "Data was not selected! Graph cannot be created.")
        else:
            if rysuj:
                modul_rysowania(macierz_wynikow)
            else:
                messagebox.showerror("Error", "You inserted wrong column numbers. Graph cannot be created.")
    else:
        messagebox.showerror("No data to show", "Data was not loaded! Graph cannot be created.")

def modul_rysowania(macierz_wynikow):
    sposob_rysowania = ['ks-', 'ro-', 'bx-', 'g*-', 'c+-', 'mh-', 'yD-', 'k<-', 'b>-', 'rp-']
    nr_wykresu = 0
    for i in range(Nmax):
        X = []
        Y = []
        if macierz_plikow[i][2]:
            nr_wykresu += 1
            for j in range(len(macierz_wynikow[i])):
                X.append(macierz_wynikow[i][j][macierz_plikow[i][3] - 1])
                Y.append(macierz_wynikow[i][j][macierz_plikow[i][4] - 1])
            sciezka = macierz_plikow[i][0]
            plt.plot(X, Y, sposob_rysowania[(nr_wykresu-1) % 10], label=sciezka.split('/')[len(sciezka.split('/'))-1])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc='lower right')
    plt.grid()
    plt.show()
    # rysunek = plt.figure()
    # obszar = FigureCanvasTkAgg(rysunek, master=okno)
    # obszar.draw()
    # obszar.get_tk_widget().pack()
    # toolbar = NavigationToolbar2Tk(obszar, okno)
    # toolbar.update()
    # obszar.get_tk_widget().pack()

#%% funkcja zamykania programu
def zamknij_program():
    pytanie = messagebox.askyesno("Exit warning", "Doy you want to close the program?")
    if pytanie:
        okno.destroy()

#%% funkcja usuwająca wczytane dane
def usun_dane():
    global czy_import_udany, macierz_wynikow, macierz_plikow, Nmax, ramka_tabela
    if len(macierz_wynikow) == 0:
        messagebox.showerror("Error", "Data was not loaded!")
    else:
        pytanie = messagebox.askyesno("Data removal", "Are you sure to clear loaded data?")
        if pytanie:
            czy_import_udany = False
            macierz_wynikow = []
            macierz_plikow = []
            for i in range(Nmax):
                macierz_plikow.append(['', 0, False, 0, 0])
            ramka_tabela.destroy()
            ramka_tabela = Frame(okno)

#%% funkcja okna powitalnego
def start():
    global okno_powitalne, Nmax
    okno_powitalne = Tk()
    szerokosc_okna = 900
    wysokosc_okna = 600
    w = okno_powitalne.winfo_screenwidth()
    h = okno_powitalne.winfo_screenheight()
    x = int((w - szerokosc_okna)/2)
    y = int((h - wysokosc_okna)/2)
    okno_powitalne.title('Welcome to data plotter')
    okno_powitalne.configure(bg='white')
    okno_powitalne.geometry("%ix%i+%i+%i" % (szerokosc_okna, wysokosc_okna, x, y))
    #sekcja1 = Canvas(okno_powitalne, bg='white', width=szerokosc_okna, height=20)
    #sekcja1.pack()
    #sekcja1.create_line(0, 10, szerokosc_okna, 10, width=2)
    #sekcja1.create_rectangle(10, 10, 50, 50, width=2)
    tekst1 = Label(okno_powitalne, bg='white', text="\n\nDATA PLOTTER ver %s" % str(app_ver), font='Tahoma 22 bold')
    tekst1.pack()
    tekst2 = Label(okno_powitalne, bg='white', text="by K. Mistewicz\n", font='Tahoma 18 bold')
    tekst2.pack()
    tekst3 = Label(okno_powitalne, bg='white', text="\nThis is an application that will allow you to load the data and show it in graph.", font='Helvetica 14')
    tekst3.pack()
    tekst4 = Label(okno_powitalne, bg='white', text="Data must be delimited by comma, tab, or space. You can visualize up to %i data files.\n" % Nmax, font='Helvetica 14')
    tekst4.pack()
    tekst5 = Label(okno_powitalne, bg='white', text="\n", font='Helvetica 16')
    tekst5.pack()
    przycisk1 = Button(okno_powitalne, width=13, height=2, text='Continue', font='Helvetica 12', command=lambda:aplikacja())
    przycisk1.pack()
    tekst6 = Label(okno_powitalne, bg='white', text="\n", font='Helvetica 6')
    tekst6.pack()
    przycisk2 = Button(okno_powitalne, width=13, height=2, text='Exit program', font='Helvetica 12', command=lambda:zamknij_okno_powitalne())
    przycisk2.pack()
    # sekcja2 = Canvas(okno_powitalne, bg='white', width=szerokosc_okna, height=20)
    # sekcja2.pack()
    # sekcja2.create_line(0, 10, szerokosc_okna, 10, width=2)
    okno_powitalne.mainloop()

#%% zamknięcie okna powitalnego
def zamknij_okno_powitalne():
    okno_powitalne.destroy()

#%% funkcja głowna aplikacji - m.in. stworzenie okna i menu
def aplikacja():
    global okno, ramka_tabela
    for i in range(Nmax):
        macierz_plikow.append(['', 0, False, 0, 0])
    zamknij_okno_powitalne()
    okno = Tk()
    ramka_tabela = Frame(okno)
    szerokosc_okna = okno.winfo_screenwidth()
    wysokosc_okna = okno.winfo_screenheight()
    okno.option_add("*Font", 'Helvetica 12')
    okno.title('Data plotter ver %s by Krystian Mistewicz' % str(app_ver))
    okno.geometry("%dx%d" % (szerokosc_okna, wysokosc_okna))
    okno.configure(bg='white')
    menu = Menu(okno)
    podmenu1 = Menu(menu, tearoff=0)
    menu.add_cascade(label="  DATA  ", menu=podmenu1)
    podmenu1.add_command(label="Load data from file", command=lambda:odczyt_pliku())
    podmenu1.add_command(label="Clear data from memory", command=lambda:usun_dane())
    podmenu2 = Menu(menu, tearoff=0)
    menu.add_cascade(label="  PLOT  ", menu=podmenu2)
    podmenu2.add_command(label="Plot loaded data", command=lambda:narysuj_wykres(macierz_wynikow))
    # podmenu2.add_command(label="Clear graph", command=lambda:usun_dane())
    podmenu3 = Menu(menu, tearoff=0)
    menu.add_cascade(label="  EXIT  ", menu=podmenu3)
    podmenu3.add_command(label="Exit program", command=lambda:zamknij_program())
    okno.config(menu=menu)
    okno.mainloop()


start()