from bs4 import BeautifulSoup
import requests
import yfinance
import pandas as pd
import os
from matplotlib import pyplot as plt
import pyautogui
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from tkinter import *
import time


def stop():
    screen.quit()

sns.set_style("darkgrid")
screen = Tk()
screen.title("Stock price checker")
screen.geometry("400x120")
# de invoervelden en buttons

menu = Menu(screen)
screen.config(menu=menu)

Submenu = Menu(menu)
menu.add_cascade(label="Quit", menu=Submenu)
Submenu.add_cascade(label = "Quit", command=stop)


entry1 = Entry(screen)
entry2 = Entry(screen)
Label1 = Label(screen, text="Startdatum:")
Label2 = Label(screen, text="Einddatum:")
Label1.grid(row=5,column=0)
Label2.grid(row=6,column=0 )
entry1.grid(row=5,column=1)
entry2.grid(row=6,column=1)
entry3 = Entry(screen)
entry2.insert(0,"2020.03.20")
entry1.insert(0,"2000.01.10")
entry3.grid(row=4,column=1)
label3 = Label(screen,text="Stock/index:")
label3.grid(row=4,column=0)

def lol():

    class All_Aex_stocks:


        def Get_stock_ticks(page):
            empty_stock_ticks = []

            # scrape the AEX
            page = requests.get(page)
            soup = BeautifulSoup(page.content, "html.parser")
            stock_ticks= soup.findAll("a",{"class":"C($c-fuji-blue-1-b) Cur(p) Td(n) Fw(500)"})

            for x in stock_ticks:
                x = x.get_text()
                empty_stock_ticks.append(x)
            return empty_stock_ticks


        # Create dateframe
        def Stock_data(tickers):
            txt1 = entry1.get()
            txt3=re.sub("\.","-",txt1)
            txt2 = entry2.get()
            txt4 = re.sub("\.", "-", txt2)
            b = yfinance.download(a,start=txt3,end=txt4)
            return b

# set and check values
    g = entry3.get()
    g = g.upper()
    a =All_Aex_stocks.Get_stock_ticks("https://finance.yahoo.com/quote/%5E"+g+"/components?p=%5E"+g)
    df = All_Aex_stocks.Stock_data(a)
    txt5= entry1.get()
    txt6 = entry2.get()
    df=df[txt5:txt6]
    df= df["Adj Close"]
    df= df.resample("M").mean()


    for val in df:
        df1= round(df[val].iloc[0],2)
        df2=round(df[val].iloc[-1],2)
        df3 = round((df2-df1)/df1*100,2)
        df[val] = round((df2-df1)/df1*100,2)


    df = df.iloc[0]
    df = df.sort_values(ascending=False)
    df.plot(kind="bar")
    df.columns = ['diff',"diff"]
    df.to_excel("rtrtrtrt.xlsx")
    os.startfile("rtrtrtrt.xlsx")
    plt.show()

button1 = Button(screen, text="Index", command=lol,width=15,height=1)
button1.grid(row=0,column=0)

def loli():
    stocky = entry3.get()
    print(stocky)
    class enhance_data:
        def __init__(self):
            self.df = []

        def Push(self,tick):
            self.df.append(tick)

        def Clear(self):
            self.df.pop()

        def Check(self):
            return self.df

        def Check_empty(self):
            return self.df == []

        def Download(self):
            v= yfinance.download(self.df,start="2000-1-1",end="2020-3-16")
            return v

    def Trends(x):
        if x > 0:
            x = 1

        if x < 0:
            x = 0
        return x

    def enhance_stock():
        s = enhance_data()
        s.Push(stocky)# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        #s.Clear()
        b_df = s.Download()
        txt7 = entry1.get()
        txt8 = entry2.get()


        b_df = b_df.reset_index()
        b_df["Date"] = pd.to_datetime(b_df["Date"])
        b_df["day"] = b_df["Date"].dt.day
        b_df["month"] = b_df["Date"].dt.month
        b_df["year"] = b_df["Date"].dt.year
        b_df["Adj Close1"]= b_df["Adj Close"].shift(-1)
        b_df["rendement"] = b_df["Adj Close1"] - b_df["Adj Close"]
        b_df["Trend"] = b_df["rendement"].apply(Trends)
        el = round(b_df.groupby(["month"])["rendement","Adj Close"].agg(["mean","min","max"]),2)
        print(b_df["Trend"].value_counts())
        mini = b_df["Adj Close"].min()
        maxi = b_df["Adj Close"].max()

        print("the min is: {} and the max is {}".format(mini,maxi))

        return round(b_df,2)

    choice1= pyautogui.prompt("volume graph:1, Slotkoers:2,Trends:3")
    if int(choice1) == 1:
        vi = enhance_stock()
        vi = vi.set_index(vi["Date"])
        vi = vi["Volume"].plot()
        plt.title("Volume van " + stocky)
        plt.xlabel("volume van "+ stocky)
        plt.ylabel("Datum")
        plt.show()

        try:
            enhance_stock().to_excel("stock.xlsx")
        except Exception as e:
            pyautogui.alert("Sluit het excel bestand voor een update")

        z = pyautogui.prompt("wil je het bestand openen typ: y")
        if z == "y":
            try:
                os.startfile("stock.xlsx")
            except Exception as e:
                print(e)

    if int(choice1) == 2:
        slot = enhance_stock()
        slot=slot.set_index(slot["Date"])
        slot = slot["Adj Close"].plot()
        plt.title("Slot van " + stocky)
        plt.xlabel("Slot van " + stocky)
        plt.ylabel("Datum")
        plt.show()

        try:
            enhance_stock().to_excel("stock.xlsx")
        except Exception as e:
            pyautogui.alert("Sluit het excel bestand voor een update")

        z = pyautogui.prompt("wil je het bestand openen typ: y")
        if z == "y":
            try:
                os.startfile("stock.xlsx")
            except Exception as e:
                print(e)

    if int(choice1) == 3:
        count = enhance_stock()
        count=count["Trend"].value_counts()
        sns.countplot(x =count, data = count,label=count)
        plt.legend(loc="best")
        plt.show()

    try:
        enhance_stock().to_excel("stock.xlsx")
    except Exception as e:
        pyautogui.alert("Sluit het excel bestand voor een update")

    z= pyautogui.prompt("wil je het bestand openen typ: y")
    if z == "y":
        try:
            os.startfile("stock.xlsx")
        except Exception as e:
            print(e)

button2 = Button(screen, text="stock",command=loli,width=19,height=1)
button2.grid(row=0,column=1)

def lolii():
    stocky = entry3.get()
    stocky=stocky.upper()
    print(stocky)
    e = yfinance.Ticker(stocky)
    print(e.dividends)
    plt.figure(figsize=(10,10))
    plt.xticks(rotation="45")
    plt.title("dividend van "+ stocky )
    e.dividends.plot(kind="barh")
    plt.xlabel("Datum")
    plt.ylabel("dividend van "+ stocky)
    plt.show()
    time.sleep(0.1)

button3 = Button(screen, text="dividend", command=lolii,width=10,height=1)
button3.grid(row=0,column=3)

screen.mainloop()























