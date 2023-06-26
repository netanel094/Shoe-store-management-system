from asyncio.windows_events import NULL
import os
import re
from dotenv import load_dotenv
import mysql.connector as cn
from tkinter import *
import PySimpleGUI as sg
from connectToMySQL import mydb,mycursor
import datetime  

## SEARCH
def search_sql(model, size=[], color=[]):
    # if the user did not input the size and color, we return all data for this model
    if size == [] and color == []:
        mycursor.execute("SELECT * FROM shoes where numModel = %s", (model,))

    # if the user did not input size (but did input color)
    elif size == []:
        color_ = color[0]
        mycursor.execute("SELECT * FROM shoes where numModel = %s and color = %s", (model, color_))

    # if the user did not input color (but did input size)
    elif color == []:
        size_ = size[0]
        mycursor.execute("SELECT * FROM shoes where numModel = %s and size = %s", (model, size_))

    else:
        size_ = size[0]
        color_ = color[0]

        mycursor.execute("SELECT * FROM shoes WHERE numModel = %s AND size = %s AND color = %s",
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
            Add_sql(values_Add['MODEL'], values_Add['COLOR'][0], values_Add['FLOOR'][0], values_Add['SEASON'][0])
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

            try:
                for i in range(all_sizes):
                    size = up + 36
                    # quantity of shoes 
                    if values_add_sizes[up + 36] != 0:

                        size = up + 36
                        quantityInStockQUERY =  "SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s" 
                        mycursor.execute(quantityInStockQUERY, (model, color,size,season,floor))
                        result = mycursor.fetchone()

                        # if the model and color is not in stock
                        if result is None or result[0] == 0:
                            inserting_to_stock = "INSERT INTO shoes (numModel, color, size, quantity ,floor, season)" \
                                            " VALUES (%s, %s, %s, %s, %s, %s)"
                            val = (model, color , up + 36, values_add_sizes[up + 36], floor, season)
                            mycursor.execute(inserting_to_stock, val)
                            # save the changes to the database permanently
                            mydb.commit()

                        else:
                            updateQuery = "UPDATE shoes SET quantity = %s WHERE numModel = %s AND color = %s AND size = %s season = %s"
                            newQuantity = result[0] + values_add_sizes[up + 36]
                            update_values = (newQuantity, model, color, size,season)
                            mycursor.execute(updateQuery, update_values)
                            mydb.commit()
                            mydb.close()

                    up += 0.5

            except cn.Error as e:
                print(f'Error creating tables: {e}')
                
                
            # Confirmation window after inserting   
            layout_confirmation = [  
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

def DailyCheckOutWindow():
    layout_Search = [
        [sg.Text(":סכום כסף בקופה", size=(20, 2), font=('Arial', 20), justification='center')],
        [sg.Text("", size=(20, 2), font=('Arial', 20), justification='center')],
        [sg.Button(button_text="יציאה", size=(6, 2), pad=(10, 20), button_color="red")]]
      

    current_date = datetime.date.today()

    # Format the date as a string in the format 'YYYY-MM-DD'
    formatted_date = current_date.strftime('%Y-%m-%d')

    # SQL query to calculate the sum of orders for the current day
    query = "SELECT SUM(order_total) FROM orders WHERE order_date = %s"
    mycursor.execute(query, formatted_date)

    # Fetch the result
    result = mycursor.fetchone()
    # Access the sum of orders
    sum_of_orders = result[0]

    print("Sum of orders for the current day:", sum_of_orders)

    window = sg.Window("חיפוש", layout_Search, element_justification='center', margins=(100, 50))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'יציאה'):
            window.close()
            break


def purches_window():

    layout = [
    [sg.Input(size=(10, 4), key="PRICE"), sg.Text(':מחיר*', font=('Arial', 12))],
    [sg.Input(size=(10, 4), key="MODEL"), sg.Text(':מספר דגם*', font=('Arial', 12))],
    [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                size=(10, 4), key="COLOR"), sg.Text(':צבע*', font=('Arial', 12))],
    [sg.Input(size=(10, 4), key="PHONE"), sg.Text(':פלאפון*', font=('Arial', 12))],
    [sg.Button(button_text="אישור", size=(6, 2), pad=(10, 20), button_color="green", key="אישור")],
    [sg.Button(button_text="ביטול", size=(6, 2), pad=(10, 20), button_color="red", key="ביטול")]
]

    window = sg.Window("רכישה", layout, element_justification='center', margins=(100, 80))


    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'ביטול'):
            window.close()
            break
        
        if event == "אישור":
            if not all(values.values()):
                sg.popup("יש למלא את כל השדות", title="שדות חסרים")
                break
            
            else:
                price_input = values['PRICE']
                model = values['MODEL']

                if not re.match(r'^\d+(\.\d{1,2})?$', price_input) or not re.match(r'^\d+(\.\d{1,2})?$',model):
                    sg.popup('פרטים לא תקינים', title='Error')
                    continue
                
                phone_input = values['PHONE']
                pattern = r'^\d{10}$'  # Regex pattern for phone number in the format: xxx-xxx-xxxx
                if not re.match(pattern, phone_input):
                    sg.Popup("הכנס מספר פלאפון תקין", keep_on_top=True)
                    continue
    
                print("before addPurchaseSQL")
                addPurchaseSQL(phone_input, model, values['COLOR'][0], values['PRICE'])


def addPurchaseSQL(phone, model, color,price):
    
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        query = "INSERT INTO Orders (phone, numModel, color, order_date, price) VALUES (%s, %s, %s, %s, %s)"
        values = (phone, model,color, currentDate, price)
        mycursor.execute(query, values)
        mydb.commit()



    except cn.Error as e:
                print(f'Error update order table: {e}')
