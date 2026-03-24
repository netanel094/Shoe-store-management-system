import functions as f
import PySimpleGUI as sg

sg.theme('DarkTeal4')

layout = [
    [sg.Text('San Diego Shoes', font=('Arial', 26, 'bold'), justification='center', expand_x=True, pad=(0, 20))],
    [sg.HorizontalSeparator()],
    [sg.Button("חיפוש", size=(15, 4), font=('Arial', 13)),
     sg.Button("רכישה", size=(15, 4), font=('Arial', 13))],
    [sg.Button("הוספה", size=(15, 4), font=('Arial', 13)),
     sg.Button("עדכון", size=(15, 4), font=('Arial', 13))],
    [sg.HorizontalSeparator()],
    [sg.Button("קופה יומית", size=(32, 2), font=('Arial', 13), button_color=('white', '#2e7d32'))],
]

window = sg.Window("San Diego Shoes", layout, margins=(180, 80), element_justification='center')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "חיפוש":
        f.Search_Window()
    elif event == "הוספה":
        f.Add_Window()
    elif event == "קופה יומית":
        f.DailyCheckOutWindow()
    elif event == "רכישה":
        f.purchase_window()

window.close()
