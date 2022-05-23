import mysql.connector
from tkinter import *
import PySimpleGUI as sg

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="shoesstore",
)

mycursor = mydb.cursor()


## SEARCH
def search_sql(model, size=None, color=None):
    # if the user did not input the size and color, we return all data for this model
    #if color is []:
     #   color = []
    #if size is []:
     #   size = []
    if size == [] and color == []:
        mycursor.execute("SELECT * FROM inventory where NumModel = %s", (model,))

    # if the user did not input size (but did input color)
    elif size == []:
        color_ = color[0]
        mycursor.execute("SELECT * FROM inventory where NumModel = %s and color = %s", (model, color_))

    # if the user did not input color (but did input size)
    elif color == []:
        size_ = size[0]
        mycursor.execute("SELECT * FROM inventory where NumModel = %s and Size = %s", (model, size_))

    else:
        size_ = size[0]
        color_ = color[0]

        mycursor.execute("SELECT * FROM inventory WHERE NumModel = %s AND size = %s AND color = %s",
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


## ADD
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
                    inserting_to_inventory = "INSERT INTO inventory (NumModel, Size, Color, Amount, Floor, Season)" \
                                             " VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (model, up + 36, color, values_add_sizes[up + 36], floor, season)
                    mycursor.execute(inserting_to_inventory, val)

                    mydb.commit()
                up += 0.5

            layout_confirmation = [  # Confirmation window after inserting
                [sg.Text("הפריטים הוספו לבקשתך", size=(20, 2), text_color="black", font=('Tahoma', 15))],
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


# Adding the costumer to "Buyer" table and deleting the shoes he bought from "inventory" table
def Buyer_sql(model, size, color, firstname=None, lastname=None, phone=None):
    # inserting the costumer
    inserting_to_Buyer = "INSERT INTO buyer (FirstName, LastName, PhoneNumber) VALUES (%s, %s, %s)"
    val = (firstname, lastname, phone)
    mycursor.execute(inserting_to_Buyer, val)

    mydb.commit()

    layout_confirmation = [  # Confirmation window after inserting
        [sg.Text("בוצע", size=(20, 2), text_color="black", font=('Tahoma', 15))],
        [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="blue")]]
    confirmation_window = sg.Window("הפריטים הוספו", layout_confirmation, element_justification='center',
                                    margins=(50, 25))
    while True:
        confirm_event, confirm_values = confirmation_window.read()
        if confirm_event in (sg.WIN_CLOSED, "אישור"):
            break
    confirmation_window.close()

    # updating the shoe from inventory
    purchased_shoe = "SELECT Amount FROM inventory WHERE NumModel = %s and size = %s and color = %s"
    shoe_val = (model, size, color)
    mycursor.execute(purchased_shoe, shoe_val)  # Getting the Amount value
    Amount = mycursor.fetchall()
    update_inventory_sql = "UPDATE inventory SET Amount = %s WHERE Amount in " \
                           "(SELECT * FROM (SELECT Amount FROM inventory WHERE " \
                           "NumModel = %s and Size = %s and Color = %s) as Amount) "
    update_val = (Amount[0][0] - 1, model, size, color)
    mycursor.execute(update_inventory_sql, update_val)

    mydb.commit()
