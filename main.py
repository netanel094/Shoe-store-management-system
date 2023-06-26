import functions as f
from asyncio.windows_events import NULL
import PySimpleGUI as sg


layout = [[sg.Button("חיפוש", size=(12, 3)), sg.Button("רכישה", size=(12, 3))],
          [sg.Button("הוספה", size=(12, 3)), sg.Button("עדכון", size=(12, 3))],
          [sg.Button("קופה יומית", size=(26, 2), button_color="green")]]

# Create the window (Home page)
window = sg.Window("San diego Shoes", layout, margins=(250, 150))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or presses the OK button
    if event == sg.WIN_CLOSED:
        break
    elif event == "חיפוש":
        f.Search_Window()
    elif event == "הוספה":
        f.Add_Window()
    elif event  == "קופה יומית":
        f.DailyCheckOutWindow()
    elif event  == "רכישה":
        f.purches_window()


window.close()
