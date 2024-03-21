import tkinter as tk
from time import sleep
from OLIMP import futball, bascet, tennis, fb, ft, bt, fbt
from threading import Thread
from multiprocessing import Process, Queue
from processing import obrbotka
import pandas as pd

window = tk.Tk()
window.title("Бот")
window.geometry("500x400")



def clear_window():
    widgets = window.winfo_children()
    for widget in widgets:
        widget.destroy()

def update_gui(queue):
    if not queue.empty():
        print(queue)
        df = queue.get()  # Получение DataFrame из очереди
        # label_itog.config(text=str(df))  # Обновление метки данными из df
        window.after(1000, update_gui, df) # Повторный вызов функции через 0,5 сек

if __name__ == "__main__":
    
    travel = Queue()
    queue = Queue()

    def counter():
        vibor = str(entry.get())
        prochent = float(entry1.get())
        
        clear_window()

        # Запуск соответствующего потока в зависимости от выбора пользователя
        if vibor == "f":
            t1 = Thread(target=futball, args=(travel,))
            t1.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(queue,))
            t8.start()
 
        elif vibor == "t":
            t2 = Thread(target=tennis, args=(travel,))
            t2.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(travel,))
            t8.start()
 
        elif vibor == "b":
            t3 = Thread(target=bascet, args=(travel,))
            t3.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(travel,))
            t8.start()

        elif vibor == "ft":
            t4 = Thread(target=ft, args=(travel,))
            t4.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(travel,))
            t8.start()

        elif vibor == "fb":
            t5 = Thread(target=fb, args=(travel,))
            t5.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(travel,))
            t8.start()

        elif vibor == "bt":
            t6 = Process(target=bt, args=(travel,))
            t6.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Thread(target=update_gui, args=(travel,))
            t8.start()

        elif vibor == "fbt":
            t6 = Process(target=fbt, args=(travel,))
            t6.start()
            t7 = Process(target=obrbotka, args=(travel, prochent,))
            t7.start()
            t8 = Process(target=update_gui, args=(queue,))
            t8.start()

    label_itog = tk.Label(window, text="Ожидание данных...")
    label_itog.pack()

    label1 = tk.Label(window, text="Выберите тип игры: \n f - футбол \n t - тенис \n b - баскетбол \n ft - футбол и теннис \n fb - футбол и баскетбол \n bt - баскетбол и теннис \n fbt - футбол, баскетбол, тенис ")
    entry = tk.Entry(window)
    label8 = tk.Label(window, text="Введите % максимальной прибыльно ставки")
    entry1 = tk.Entry(window)
    button = tk.Button(window, text="Начать", command=counter)


    # Упаковка виджетов
    label1.pack()
    entry.pack()
    label8.pack()
    entry1.pack()
    button.pack()

    window.mainloop()
