import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
internet_connection = False

"=========================Obsługa strony NBP i poszukiwania pliku xml=============================="
try:
    nbp_page = requests.get("https://www.nbp.pl/home.aspx?f=/kursy/kursya.html")

    soup = BeautifulSoup(nbp_page.content, "html.parser")
    all_links = soup.find_all("a")

    for link in all_links:
        if 'href' in link.attrs:
            if str(link.attrs['href'])[-4:] == ".xml":
                xml_link = "https://www.nbp.pl" + str(link.attrs['href'])
        
    internet_connection = True
except:
    pass

"==============================Obsługa formatu xml tabeli kursów==================================="

try:
    r = requests.get(xml_link)
    data = r.text
    cleaner_data = ET.fromstring(data)
    kursy = ["1","1"]

    for element in cleaner_data.findall("pozycja"): #pętla wyszukuje wszystkie kursy średnie
        kurs = element.find("kurs_sredni").text
        middle_list = []  #pakowanie w listę list pomaga przy zapisywaniu do csv
        middle_list.append(kurs)
        kursy.append(middle_list)

except:
    pass

"=============================Zapis aktualnych kursów do pliku csv================================="

if internet_connection: # brak połączenia z internetem = brak możliwości zapisu aktualnych kursów
    try:
        with open('kursy.csv', 'w') as csvfile_1:
            writer = csv.writer(csvfile_1)
            writer.writerows(kursy)
    except:
        pass

"====================================Odczyt kursów z pliku csv====================================="

with open("kursy.csv") as csvfile_2:
    reader = csv.reader(csvfile_2)
    kursy = list(reader)

"==================================Obsługa listy kursów i państw==================================="

ex_rate = []              # po raz kolejny proszę wybaczyć mieszanie angielskiego z polskim
for element in kursy:
    if len(element) != 0:
        kurs = element[0]
        kurs = kurs.replace(",",".")
        kurs = float(kurs)
        ex_rate.append(kurs)

countries = ["-----",    #zrobienie takiej listy nie jest długim zajęciem, seria kopiuj-wklej
"Złoty (PLN)",
"bat (Tajlandia)",
"dolar amerykański",
"dolar australijski",
"dolar Hongkongu ",
"dolar kanadyjski",
"dolar nowozelandzki",
"dolar singapurski",
"euro",
"forint (Węgry)",
"frank szwajcarski",
"funt szterling", 	
"hrywna (Ukraina)", 	
"jen (Japonia)", 	
"korona czeska", 	
"korona duńska", 	
"korona islandzka", 	
"korona norweska", 	
"korona szwedzka", 	
"kuna (Chorwacja)", 	
"lej rumuński", 	
"lew (Bułgaria)", 	
"lira turecka", 	
"nowy izraelski szekel", 
"peso chilijskie", 	
"peso filipińskie", 	
"peso meksykańskie", 
"rand (Republika Południowej Afryki)", 
"real (Brazylia)", 	
"ringgit (Malezja)", 
"rubel rosyjski", 
"rupia indonezyjska", 
"rupia indyjska", 
"won południowokoreański", 
"yuan renminbi (Chiny)", 
"SDR (MFW)"]

values_dict = dict(zip(countries, ex_rate)) # słownik kluczy: państw i wartości: kursów

"=====================================Aplikacja właściwa=========================================="

root = tk.Tk()
root.title("Prosty przelicznik walut")
root.geometry("800x400")

img = tk.PhotoImage(file='money.png') # tło
img_label = tk.Label(root, image = img)
img_label.place(x=0, y=0)

text = tk.Label(root, text="Wybierz walutę źródłową", font=("Helvetica", 18), relief="ridge", bd = 6)
text.place(x=266,y=17)

text = tk.Label(root, text="Wybierz walutę docelową", font=("Helvetica", 18), relief="ridge", bd = 6)
text.place(x=266,y=93)

text = tk.Label(root, text="Wprowadź żądaną kwotę", font=("Helvetica", 16), relief="ridge", bd = 6)
text.place(x=90,y=225)

country_list = ttk.Combobox(root, values = countries)  # rozwijana lista 1
country_list.current(0)
country_list.pack(fill ="x", padx = 70, pady = 55)

country_list_2 = ttk.Combobox(root, values = countries) # rozwijana lista 2
country_list_2.current(0)
country_list_2.pack(fill ="x", padx = 70, pady = 0)

kwota = tk.Entry(root, cursor = "circle", font=("Helvetica", 15), bd = 5, bg = "#00994C")
kwota.place(height = 40, width = 180, x = 120, y = 260)    # miejsce do wpisania kwoty

def przelicz():

    kraj_1 = country_list.get()
    waluta_źródłowa = values_dict[kraj_1]
    if kraj_1 in ["forint (Węgry)","jen (Japonia)", "korona islandzka", "peso chilijskie",
                  "rupia indyjska", "won południowokoreański"]: # te kraje mają inne przeliczniki
        waluta_źródłowa /= 100
    elif kraj_1 == "rupia indonezyjska":
        waluta_źródłowa /= 10000

    kraj_2 = country_list_2.get()
    waluta_docelowa = values_dict[kraj_2]
    if kraj_2 in ["forint (Węgry)","jen (Japonia)", "korona islandzka", "peso chilijskie",
                  "rupia indyjska", "won południowokoreański"]:
        waluta_docelowa /= 100
    elif kraj_2 == "rupia indonezyjska":
        waluta_docelowa /= 10000

    entry = float(kwota.get())
    wynik = entry*waluta_źródłowa/waluta_docelowa
    wynik = '{:.{}f}'.format(wynik, 3) # wyświetl max 3 miejsca po przecinku

    if eval(wynik) - int(eval(wynik)) == 0:
        wynik = int(eval(wynik))   # bez tego aplikacja wyświetli np. 12 jako 12.000

    try:
        text_1.pack_forget()
        wynik_text.pack_forget()  # czyszczenie poprzedniego wyniku, o ile jest to możliwe
    except:
        pass

    text_1 = tk.Label(root, text="Wynik", font=("Helvetica", 16), relief="ridge", bd = 6)
    text_1.place(x=566,y=225)  
    wynik_text = tk.Label(root, text= wynik, font=("Helvetica", 15), relief="sunken", bd = 5, bg = "#00994C")
    wynik_text.place(height = 40, width = 180, x = 510, y = 260) # wyświetl wynik

Button = tk.Button(root,
    text = "Przelicz",
    command = przelicz,
    bg = "#00994C",
    activebackground = "#006633",
    font=("Helvetica", 15))
Button.place(height = 50, width = 100, x=350, y=340)

root.mainloop()