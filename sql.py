from asyncio.windows_events import NULL
import mysql.connector as cn
from tkinter import *
import PySimpleGUI as sg

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

mydb = cn.connect(
    host= os.getenv("HOST"),
    user=os.getenv("USER"),
    password =os.getenv("PASSWORD"),
    database =os.getenv("DATABASE"),
)



if mydb.is_connected():
    print("Connected to MySQL!")
    # Perform further operations on the database
    mycursor = mydb.cursor()


else:
    print("Failed to connect to MySQL.")
    

## SEARCH
def search_sql(model, size=[], color=[]):
    # if the user did not input the size and color, we return all data for this model
    if size == [] and color == []:
        mycursor.execute("SELECT * FROM instock where NumModel = %s", (model,))

    # if the user did not input size (but did input color)
    elif size == []:
        color_ = color[0]
        mycursor.execute("SELECT * FROM instock where NumModel = %s and color = %s", (model, color_))

    # if the user did not input color (but did input size)
    elif color == []:
        size_ = size[0]
        mycursor.execute("SELECT * FROM instock where NumModel = %s and Size = %s", (model, size_))

    else:
        size_ = size[0]
        color_ = color[0]

        mycursor.execute("SELECT * FROM instock WHERE NumModel = %s AND size = %s AND color = %s",
                         (model, size_, color_))

    # showing the table data
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    layout = [
        [sg.Text(":פירוט הזוגות שנמצאים במלאי", font=("Arial", 20), justification=CENTER)],
        [sg.Table(values=myresult, headings=field_names, max_col_width=20, auto_size_columns=True,
                  justification=CENTER, size=(100, 15))],
        [sg.Button("אישור", font="Arial, 20", button_color='green', size=(5, 1))]]

    window = sg.Window("פירוט המלאי", layout, element_justification=CENTER, margins=(200, 100))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "אישור"):
            break
    window.close()

def Search_Window():
    layout_Search = [
        [sg.Text("?איזה זוג נעליים תרצה למצוא", size=(25, 2), font=('Arial', 15))],
        [sg.Input(size=(10, 4)), sg.Text(':מספר דגם*', font=('Arial', 12))],
        [sg.Listbox([36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5,
                     42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48],
                    size=(7, 7)), sg.Text(':מידה', font=('Arial', 12))],
        [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4)), sg.Text(':צבע', font=('Arial', 12))],
        [sg.Button(button_text="אישור", size=(6, 2), pad=(10, 20), button_color="green"),
         sg.Button(button_text="ביטול", size=(6, 2), pad=(10, 20), button_color="red")]
    ]

    SearchWindow = sg.Window("חיפוש", layout_Search, element_justification='center', margins=(100, 50))

    while True:
        event_Search, values_Search = SearchWindow.read()
        if event_Search in (sg.WIN_CLOSED, 'ביטול'):
            break
        # if the user did not input any model
        elif values_Search[0] == "":
            layout_error = [
                [sg.Text("שגיאה! חובה להזין מספר דגם", size=(20, 2), text_color="black", font=('Arial', 14))],
                [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("!שגיאה", layout_error, element_justification='center', margins=(50, 25))
            while True:
                event_error, values_error = ErrorWindow.read()
                if event_error in (sg.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()
        elif event_Search == "אישור":
            search_sql(values_Search[0], values_Search[1], values_Search[2])
    SearchWindow.close()

def Add_Window():
    layout_Add = [
        [sg.Text("?איזה זוג נעליים תרצה להוסיף למלאי", size=(30, 2), font=('Arial', 15))],
        [sg.Input(size=(10, 4), key="MODEL"), sg.Text(':מספר דגם*', font=('Arial', 12))],
        [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4), key="COLOR"), sg.Text(':צבע*', font=('Arial', 12))],
        [sg.Listbox([1, 2], size=(10, 4), key="FLOOR"), sg.Text(':קומה*', font=('Arial', 12))],
        [sg.Listbox(["חורף", "קיץ", "סתיו", "אביב"],
                    size=(10, 4), key="SEASON"), sg.Text(':עונה', font=('Arial', 12))],
        [sg.Button(button_text="אישור", size=(6, 2), pad=(10, 20), button_color="green"),
         sg.Button(button_text="ביטול", size=(6, 2), pad=(10, 20), button_color="red")]
    ]

    AddWindow = sg.Window("הוספה", layout_Add, element_justification='center', margins=(100, 40))

    while True:
        event_Add, values_Add = AddWindow.read()
        if event_Add in (sg.WIN_CLOSED, 'ביטול'):
            break

        # if the user did not input model/size/floor -- ERROR WINDOW
        elif values_Add['MODEL'] == "" or values_Add['COLOR'] == [] or values_Add['FLOOR'] == []:
            layout_Error = [[sg.Text("שגיאה! פרטים חסרים", size=(20, 2), text_color="black", font=('Arial', 15))],
                            [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("!שגיאה", layout_Error, element_justification='center', margins=(50, 25))
            while True:
                event_Error, values_Error = ErrorWindow.read()
                if event_Error in (sg.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()
        elif event_Add == "אישור":
            if values_Add['SEASON'] == []:
                values_Add['SEASON'].append(NULL)
            cn.Add_sql(values_Add['MODEL'], values_Add['COLOR'][0], values_Add['FLOOR'][0], values_Add['SEASON'][0])
    AddWindow.close()

# add to mysql
def Add_sql(model, color, floor, season):
    sizesint = [
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36), sg.Text('36')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37), sg.Text('37')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38), sg.Text('38')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39), sg.Text('39')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40), sg.Text('40')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41), sg.Text('41')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42), sg.Text('42')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43), sg.Text('43')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44), sg.Text('44')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45), sg.Text('45')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46), sg.Text('46')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47), sg.Text('47')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=48), sg.Text('48')],
    ]

    sizeshalfes = [
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36.5), sg.Text('36.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37.5), sg.Text('37.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38.5), sg.Text('38.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39.5), sg.Text('39.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40.5), sg.Text('40.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41.5), sg.Text('41.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42.5), sg.Text('42.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43.5), sg.Text('43.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44.5), sg.Text('44.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45.5), sg.Text('45.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46.5), sg.Text('46.5')],
        [sg.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47.5), sg.Text('47.5')],
    ]

    buttons = [
        [sg.Button(button_text="הוסף", size=(6, 2), button_color="green")],
        [sg.Button(button_text="חזור", size=(6, 2), button_color="grey")]
    ]
    layout_add_sizes = [[
        sg.Column(sizesint),
        sg.VSeparator(),
        sg.Column(sizeshalfes),
        sg.Column(buttons)]
    ]

    Add_Sizes_Window = sg.Window('מידות להוספה', layout_add_sizes, margins=(250, 100))
    while True:
        event_add_sizes, values_add_sizes = Add_Sizes_Window.read()

        if event_add_sizes == "הוסף":  # Inserting values
            all_sizes = len(values_add_sizes)
            up = 0
            for i in range(all_sizes):
                if values_add_sizes[up + 36] != 0:
                    inserting_to_stock = "INSERT INTO instock (NumModel, Size, color, amount, Floor, Season)" \
                                         " VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (model, up + 36, color, values_add_sizes[up + 36], floor, season)
                    mycursor.execute(inserting_to_stock, val)

                    mydb.commit()
                up += 0.5

            layout_confirmation = [  # Confirmation window after inserting
                [sg.Text("הפריטים הוספו לבקשתך", size=(20, 2), text_color="black", font=('Arial', 15))],
                [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="blue")]]
            confirmation_window = sg.Window("הפריטים הוספו", layout_confirmation, element_justification='center',
                                            margins=(50, 25))
            while True:
                confirm_event, confirm_values = confirmation_window.read()
                if confirm_event in (sg.WIN_CLOSED, "אישור"):
                    break
            confirmation_window.close()

            break

        elif event_add_sizes in (sg.WIN_CLOSED, layout_add_sizes[0][3] == "חזור"):
            break

        Add_Sizes_Window.close()
    Add_Sizes_Window.close()
