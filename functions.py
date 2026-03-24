from asyncio.windows_events import NULL
import os
import re
from dotenv import load_dotenv
import mysql.connector as cn
from tkinter import *
import PySimpleGUI as pysimplegui
from db.connection import mydb, mycursor
import datetime  

# SEARCH
def search_sql(model, size=[], color=[]):
    # if the user did not input the size and color, we return all data for this model
    if size == [] and color == []:
        mycursor.execute("SELECT * FROM shoes where numModel = %s", (model,))

    # if the user did not input size (but did input color)
    elif not size:
        mycursor.execute("SELECT * FROM shoes WHERE numModel = %s AND color = %s", (model, color[0]))

    # if the user did not input color (but did input size)
    elif color == []:
        mycursor.execute("SELECT * FROM shoes where numModel = %s and size = %s", (model, size[0]))

    else:
        mycursor.execute("SELECT * FROM shoes WHERE numModel = %s AND size = %s AND color = %s",
                         (model, size[0], color[0]))

    # showing the table data
    myresult = mycursor.fetchall()
    field_names = [i[0] for i in mycursor.description]
    layout = [
        [pysimplegui.Text(":פירוט הזוגות שנמצאים במלאי", font=("Arial", 20), justification=CENTER)],
        [pysimplegui.Table(values=myresult, headings=field_names, max_col_width=20, auto_size_columns=True,
                  justification=CENTER, size=(100, 15))],
        [pysimplegui.Button("אישור", font="Arial, 20", button_color='green', size=(5, 1))]]

    window = pysimplegui.Window("פירוט המלאי", layout, element_justification=CENTER, margins=(200, 100))
    while True:
        event, values = window.read()
        if event in (pysimplegui.WIN_CLOSED, "אישור"):
            break
    window.close()

def Search_Window():
    layout_search = [
        [pysimplegui.Text("חיפוש נעליים", font=('Arial', 18, 'bold'), justification='center', expand_x=True)],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Text("?איזה זוג נעליים תרצה למצוא", font=('Arial', 13), justification='right', expand_x=True)],
        [pysimplegui.Input(size=(12, 1), font=('Arial', 12)), pysimplegui.Text(':מספר דגם*', font=('Arial', 12))],
        [pysimplegui.Listbox([36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5,
                     42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48],
                    size=(8, 7), font=('Arial', 11)), pysimplegui.Text(':מידה', font=('Arial', 12))],
        [pysimplegui.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4), font=('Arial', 11)), pysimplegui.Text(':צבע', font=('Arial', 12))],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Button(button_text="אישור", size=(8, 2), pad=(10, 15), button_color="green", font=('Arial', 12)),
         pysimplegui.Button(button_text="ביטול", size=(8, 2), pad=(10, 15), button_color="red", font=('Arial', 12))]
    ]

    SearchWindow = pysimplegui.Window("חיפוש", layout_search, element_justification='center', margins=(100, 40))

    while True:
        event_Search, values_Search = SearchWindow.read()
        if event_Search in (pysimplegui.WIN_CLOSED, 'ביטול'):
            break
        # if the user did not input any model
        elif values_Search[0] == "":
            layout_error = [
                [pysimplegui.Text("שגיאה! חובה להזין מספר דגם", size=(20, 2), text_color="black", font=('Arial', 14))],
                [pysimplegui.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = pysimplegui.Window("!שגיאה", layout_error, element_justification='center', margins=(50, 25))
            while True:
                event_error, values_error = ErrorWindow.read()
                if event_error in (pysimplegui.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()
        elif event_Search == "אישור":
            search_sql(values_Search[0], values_Search[1], values_Search[2])
    SearchWindow.close()

def Add_Window():
    layout_Add = [
        [pysimplegui.Text("הוספת נעליים למלאי", font=('Arial', 18, 'bold'), justification='center', expand_x=True)],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Text("?איזה זוג נעליים תרצה להוסיף למלאי", font=('Arial', 13), justification='right', expand_x=True)],
        [pysimplegui.Input(size=(12, 1), key="MODEL", font=('Arial', 12)), pysimplegui.Text(':מספר דגם*', font=('Arial', 12))],
        [pysimplegui.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4), key="COLOR", font=('Arial', 11)), pysimplegui.Text(':צבע*', font=('Arial', 12))],
        [pysimplegui.Listbox([1, 2], size=(10, 2), key="FLOOR", font=('Arial', 11)), pysimplegui.Text(':קומה*', font=('Arial', 12))],
        [pysimplegui.Listbox(["חורף", "קיץ", "סתיו", "אביב"],
                    size=(10, 4), key="SEASON", font=('Arial', 11)), pysimplegui.Text(':עונה', font=('Arial', 12))],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Button(button_text="אישור", size=(8, 2), pad=(10, 15), button_color="green", font=('Arial', 12)),
         pysimplegui.Button(button_text="ביטול", size=(8, 2), pad=(10, 15), button_color="red", font=('Arial', 12))]
    ]

    AddWindow = pysimplegui.Window("הוספה", layout_Add, element_justification='center', margins=(100, 40))

    while True:
        event_Add, values_Add = AddWindow.read()
        if event_Add in (pysimplegui.WIN_CLOSED, 'ביטול'):
            break

        # if the user did not input model/size/floor -- ERROR WINDOW
        elif values_Add['MODEL'] == "" or values_Add['COLOR'] == [] or values_Add['FLOOR'] == []:
            layout_Error = [[pysimplegui.Text("שגיאה! פרטים חסרים", size=(20, 2), text_color="black", font=('Arial', 15))],
                            [pysimplegui.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = pysimplegui.Window("!שגיאה", layout_Error, element_justification='center', margins=(50, 25))
            while True:
                event_Error, values_Error = ErrorWindow.read()
                if event_Error in (pysimplegui.WIN_CLOSED, "אישור"):
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
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36), pysimplegui.Text('36')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37), pysimplegui.Text('37')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38), pysimplegui.Text('38')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39), pysimplegui.Text('39')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40), pysimplegui.Text('40')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41), pysimplegui.Text('41')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42), pysimplegui.Text('42')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43), pysimplegui.Text('43')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44), pysimplegui.Text('44')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45), pysimplegui.Text('45')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46), pysimplegui.Text('46')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47), pysimplegui.Text('47')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=48), pysimplegui.Text('48')],
    ]

    sizeshalfes = [
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=36.5), pysimplegui.Text('36.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=37.5), pysimplegui.Text('37.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=38.5), pysimplegui.Text('38.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=39.5), pysimplegui.Text('39.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=40.5), pysimplegui.Text('40.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=41.5), pysimplegui.Text('41.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=42.5), pysimplegui.Text('42.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=43.5), pysimplegui.Text('43.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=44.5), pysimplegui.Text('44.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=45.5), pysimplegui.Text('45.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=46.5), pysimplegui.Text('46.5')],
        [pysimplegui.Spin([i for i in range(0, 11)], initial_value=0, size=(2, 10), key=47.5), pysimplegui.Text('47.5')],
    ]

    buttons = [
        [pysimplegui.Button(button_text="הוסף", size=(6, 2), button_color="green")],
        [pysimplegui.Button(button_text="חזור", size=(6, 2), button_color="grey")]
    ]
    layout_add_sizes = [[
        pysimplegui.Column(sizesint),
        pysimplegui.VSeparator(),
        pysimplegui.Column(sizeshalfes),
        pysimplegui.Column(buttons)]
    ]

    Add_Sizes_Window = pysimplegui.Window('מידות להוספה', layout_add_sizes, margins=(250, 100))
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
                [pysimplegui.Text("הפריטים הוספו לבקשתך", size=(20, 2), text_color="black", font=('Arial', 15))],
                [pysimplegui.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="blue")]]
            confirmation_window = pysimplegui.Window("הפריטים הוספו", layout_confirmation, element_justification='center',
                                            margins=(50, 25))
            while True:
                confirm_event, confirm_values = confirmation_window.read()
                if confirm_event in (pysimplegui.WIN_CLOSED, "אישור"):
                    break
            confirmation_window.close()

            break

        elif event_add_sizes in (pysimplegui.WIN_CLOSED, layout_add_sizes[0][3] == "חזור"):
            break

        Add_Sizes_Window.close()
    Add_Sizes_Window.close()


def purchase_window():

    layout = [
    [pysimplegui.Text("רכישה", font=('Arial', 18, 'bold'), justification='center', expand_x=True)],
    [pysimplegui.HorizontalSeparator()],
    [pysimplegui.Input(size=(12, 1), key="NAME", font=('Arial', 12)), pysimplegui.Text(':שם לקוח*', font=('Arial', 12))],
    [pysimplegui.Input(size=(12, 1), key="PHONE", font=('Arial', 12)), pysimplegui.Text(':פלאפון*', font=('Arial', 12))],
    [pysimplegui.HorizontalSeparator()],
    [pysimplegui.Input(size=(12, 1), key="MODEL", font=('Arial', 12)), pysimplegui.Text(':מספר דגם*', font=('Arial', 12))],
    [pysimplegui.Input(size=(12, 1), key="SIZE", font=('Arial', 12)), pysimplegui.Text(':מידה*', font=('Arial', 12))],
    [pysimplegui.Input(size=(12, 1), key="PRICE", font=('Arial', 12)), pysimplegui.Text(':מחיר*', font=('Arial', 12))],
    [pysimplegui.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                size=(10, 4), key="COLOR", font=('Arial', 11)), pysimplegui.Text(':צבע*', font=('Arial', 12))],
    [pysimplegui.Listbox(["1", "2"], size=(5, 2), key="FLOOR", font=('Arial', 11)), pysimplegui.Text(':קומה*', font=('Arial', 12))],
    [pysimplegui.Listbox(["חורף", "קיץ", "סתיו", "אביב"],
                size=(10, 4), key="SEASON", font=('Arial', 11)), pysimplegui.Text(':עונה', font=('Arial', 12))],
    [pysimplegui.HorizontalSeparator()],
    [pysimplegui.Button(button_text="אישור", size=(8, 2), pad=(20, 15), button_color="green", font=('Arial', 12)),
    pysimplegui.Button(button_text="ביטול", size=(8, 2), pad=(20, 15), button_color="red", font=('Arial', 12))]
]

    purchaseW = pysimplegui.Window("רכישה", layout, element_justification='center', margins=(80, 40))
 
    while True:
        event, values = purchaseW.read()

        if event in (pysimplegui.WIN_CLOSED, 'ביטול'):
            purchaseW.close()
            break

        price = values['PRICE']
        model = values['MODEL']
        name = values['NAME']
        size = values['SIZE']
        color = values['COLOR'][0]
        phone = values['PHONE']
        floor =values['FLOOR'][0]
        season = values['SEASON'][0]

        if check_if_model_exist(model,size,color) == False:
                pysimplegui.popup("הדגם לא נמצא במלאי", title="דגם חסר במלאי")
                continue

        
        # Check if the size is correct
        if not size.isdigit() or not 36 <= int(size) <= 47:
            pysimplegui.Popup("יש להזין ערך מידה תקין (36-47)", keep_on_top=True)
            continue
        
        if event == "אישור":
            if not all(values.values()):
                pysimplegui.popup("יש למלא את כל השדות", title="שדות חסרים")
                continue

            else:
               
                if not re.match(r'^\d+(\.\d{1,2})?$', price) or not re.match(r'^\d+(\.\d{1,2})?$',model):
                    pysimplegui.popup('פרטים לא תקינים', title='Error')
                    continue
                
           
                pattern = r'^\d{10}$'  # Regex pattern for phone number in the format: xxx-xxx-xxxx
                if not re.match(pattern, phone):
                    pysimplegui.Popup("הכנס מספר פלאפון תקין", keep_on_top=True)
                    continue
    
                
                add_purchase_sql(model, price, size,floor, name, phone, color)
                updateShoesTableAfterPurchase(model, color, size, floor, season)
                pysimplegui.popup("רכישה בוצעה בהצלחה", title="Success")
                purchaseW.close()
                break


def check_if_model_exist(model, size, color):
    query = "SELECT * FROM SHOES WHERE numModel = %s AND size = %s AND color = %s"
    values = (model, size, color)
    mycursor.execute(query, values)
    result = mycursor.fetchone()
    if result is not None:
        return True
    else:
        return False
    

def add_purchase_sql(model, price, size,floor, name, phone, color):
    
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        query = "INSERT INTO Orders (numModel, price, size, floor, name, phone, color,order_date) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
        values = (model, price ,size, floor, name, phone, color, current_date)
        mycursor.execute(query, values)

        
        order_id = mycursor.lastrowid # Retrieve the last inserted order_id
        query = "INSERT INTO Customers (phone, name, order_id) VALUES (%s, %s, %s)"
        values = (phone, name, order_id)
        mycursor.execute(query, values)
        
        
        mydb.commit() # Commit the transaction

    except cn.Error as e:
        print(f'Error update order table: {e}')


def updateShoesTableAfterPurchase(model, color , size, floor, season):
    
    try:
        quantityInStockQUERY = "SELECT quantity FROM shoes WHERE numModel = %s AND color = %s AND size = %s AND season = %s AND floor = %s" 
        mycursor.execute(quantityInStockQUERY, (model, color,size, season, floor))
        currentQuantity = mycursor.fetchone()
        newQuantity = currentQuantity[0] - 1

        query = "UPDATE shoes SET quantity = %s Where numModel = %s AND size = %s AND color = %s AND season = %s AND floor = %s"
        values = (newQuantity, model, size, color, season, floor)
        mycursor.execute(query, values)     
        mydb.commit()

    except cn.Error as e:
        print(f'Error update order table: {e}')


def DailyCheckOutWindow():
    layout = [
        [pysimplegui.Text("קופה", font=('Arial', 18, 'bold'), justification='center', expand_x=True)],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Button(button_text="קופה יומית", size=(14, 3), pad=(15, 15), button_color="blue", font=('Arial', 12)),
         pysimplegui.Button(button_text="קופה חודשית", size=(14, 3), pad=(15, 15), button_color=('white', '#e65100'), font=('Arial', 12))],
        [pysimplegui.HorizontalSeparator()],
        [pysimplegui.Button(button_text="יציאה", size=(10, 2), pad=(10, 10), button_color="red", font=('Arial', 12))],
    ]

    window = pysimplegui.Window("קופה", layout, element_justification='center', margins=(120, 60))
        
    # SQL query to calculate the sum of orders for the current day
    dailyProfit  = "SELECT SUM(order_total) FROM orders WHERE order_date = %s"
    monthlyProfit = "SELECT SUM(price) AS profit FROM Orders WHERE MONTH(order_date) =  AND YEAR(order_date) = YEAR(CURRENT_DATE())"
    
    currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # SQL query to calculate the sum of orders for the current day
    dailyProfitQuery = "SELECT SUM(price) FROM Orders WHERE order_date = %s"
    
    # SQL query to calculate the sum of orders for the current month
    monthly_profit_query = "SELECT SUM(price) AS profit FROM Orders WHERE MONTH(order_date) = MONTH(CURRENT_DATE()) AND YEAR(order_date) = YEAR(CURRENT_DATE())"
    
    while True:
        event, values = window.read()

        if event == pysimplegui.WINDOW_CLOSED or event == 'יציאה':
            window.close()
            break
        
        if event == 'קופה יומית':
            # Execute the daily profit query
            mycursor.execute(dailyProfitQuery, (currentDate,))
            result = mycursor.fetchone()
            daily_profit = result[0]
            pysimplegui.Popup(f"הסכום שהצטבר במהלך היום הנוכחי הוא {daily_profit}", font = ('Arial', 16), keep_on_top=True,)
            print("Daily profit:", daily_profit)

        if event == 'קופה חודשית':
            # Execute the monthly profit query
            mycursor.execute(monthly_profit_query)
            result = mycursor.fetchone()
            monthly_profit = result[0]
            pysimplegui.Popup(f"הסכום שהצטבר במהלך החודש הנוכחי הוא {monthly_profit}", font=('Arial', 16), keep_on_top=True)

            
            print("Monthly profit:", monthly_profit)
