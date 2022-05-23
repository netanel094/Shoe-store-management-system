import PySimpleGUI as sg
import sql

## test git

def Search_Window():
    layout_Search = [
        [sg.Text("?איזה זוג נעליים תרצה למצוא", size=(25, 2), font=('Tahoma', 17))],
        [sg.Input(size=(13, 4)), sg.Text(':מספר דגם*', size=(11, 1), font=('Tahoma', 12))],
        [sg.Listbox([36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 40.5, 41, 41.5,
                     42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48],
                    size=(10, 4)), sg.Text(':מידה', size=(11, 1), font=('Tahoma', 12))],
        [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4)), sg.Text(':צבע', size=(11, 1), font=('Tahoma', 12))],
        [sg.Button(button_text="אישור", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="green"),
         sg.Button(button_text="ביטול", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="red")]
    ]

    SearchWindow = sg.Window("חיפוש", layout_Search, element_justification='center', margins=(100, 70))

    while True:
        event_Search, values_Search = SearchWindow.read()
        if event_Search in (sg.WIN_CLOSED, 'ביטול'):
            break
        # if the user did not input any model
        elif values_Search[0] == "":
            layout_error = [
                [sg.Text("שגיאה! חובה להזין מספר דגם", size=(20, 2), text_color="black", font=('Tahoma', 14))],
                [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("!שגיאה", layout_error, element_justification='center', margins=(50, 25))
            while True:
                event_error, values_error = ErrorWindow.read()
                if event_error in (sg.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()
        elif event_Search == "אישור":
            sql.search_sql(values_Search[0], values_Search[1], values_Search[2])
    SearchWindow.close()


def Add_Window():
    layout_Add = [
        [sg.Text("?איזה זוג נעליים תרצה להוסיף למלאי", size=(30, 2), font=('Tahoma', 15))],
        [sg.Input(size=(13, 4), key="MODEL"), sg.Text(':מספר דגם*', size=(11, 1), font=('Tahoma', 12))],
        [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(10, 4), key="COLOR"), sg.Text(':צבע*', size=(11, 1), font=('Tahoma', 12))],
        [sg.Listbox([1, 2], size=(10, 4), key="FLOOR"), sg.Text(':קומה*', size=(11, 1), font=('Tahoma', 12))],
        [sg.Listbox(["חורף", "קיץ", "סתיו", "אביב"],
                    size=(10, 4), key="SEASON"), sg.Text(':עונה', size=(11, 1), font=('Tahoma', 12))],
        [sg.Button(button_text="אישור", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="green"),
         sg.Button(button_text="ביטול", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="red")]
    ]

    AddWindow = sg.Window("הוספה", layout_Add, element_justification='center', margins=(100, 50))

    while True:
        event_Add, values_Add = AddWindow.read()
        if event_Add in (sg.WIN_CLOSED, 'ביטול'):
            break

        # if the user did not input model/size/floor -- ERROR WINDOW
        elif values_Add['MODEL'] == "" or values_Add['COLOR'] == [] or values_Add['FLOOR'] == []:
            layout_Error = [[sg.Text("שגיאה! פרטים חסרים", size=(20, 2), text_color="black", font=('Tahoma', 15))],
                            [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("!שגיאה", layout_Error, element_justification='center', margins=(50, 25))
            while True:
                event_Error, values_Error = ErrorWindow.read()
                if event_Error in (sg.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()
        elif event_Add == "אישור":
            if not values_Add['SEASON']:
                values_Add['SEASON'].append(None)
            sql.Add_sql(values_Add['MODEL'], values_Add['COLOR'][0], values_Add['FLOOR'][0], values_Add['SEASON'][0])
    AddWindow.close()


def Purchase_Window():
    layout_Purchase = [
        [sg.Input(size=(13, 4), key="FIRSTNAME"), sg.Text(":שם פרטי לקוח", size=(15, 1), font=('Tahoma', 12))],
        [sg.Input(size=(13, 4), key="LASTNAME"), sg.Text(":שם משפחה לקוח", size=(15, 1), font=('Tahoma', 12))],
        [sg.Input(size=(13, 4), key="PHONE"), sg.Text(":מספר טלפון", size=(15, 1), font=('Tahoma', 12))],
        [sg.Input(size=(13, 4), key="MODEL"), sg.Text(':מספר דגם*', size=(15, 1), font=('Tahoma', 12))],
        [sg.Input(size=(13, 4), key="SIZE"), sg.Text(':מידה*', size=(15, 1), font=('Tahoma', 12))],
        [sg.Listbox(["אדום", "שחור", "לבן", "ירוק", "אפור", "חום", "כחול", "צבעוני"],
                    size=(13, 4), key="COLOR"), sg.Text(':צבע*', size=(15, 1), font=('Tahoma', 12))],
        [sg.Input(size=(13, 4), key="SUM"), sg.Text(':סכום קניה*', size=(15, 1), font=('Tahoma', 12))],
        [sg.Button(button_text="אישור", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="green"),
         sg.Button(button_text="ביטול", size=(8, 2), font=('Tahoma', 11), button_color="red")]
    ]

    PurchaseWindow = sg.Window("רכישה", layout_Purchase, element_justification='center', margins=(100, 50))

    while True:
        event_Purchase, values_Purchase = PurchaseWindow.read()
        if event_Purchase in (sg.WIN_CLOSED, 'ביטול'):
            break
        # if the user did not input model/size/color -- ERROR WINDOW
        elif values_Purchase['MODEL'] == "" or values_Purchase['COLOR'] == [] \
                or values_Purchase['SIZE'] == [] or values_Purchase['SIZE'] == "":
            layout_Error = [[sg.Text("שגיאה! פרטים חסרים", size=(20, 2), text_color="black", font=('Tahoma', 15))],
                            [sg.Button(button_text="אישור", size=(5, 1), pad=(10, 20), button_color="grey")]]
            ErrorWindow = sg.Window("!שגיאה", layout_Error, element_justification='center', margins=(50, 25))
            while True:
                event_Error, values_Error = ErrorWindow.read()
                if event_Error in (sg.WIN_CLOSED, "אישור"):
                    break
            ErrorWindow.close()

        elif event_Purchase == "אישור":
            sql.Buyer_sql(values_Purchase['MODEL'], values_Purchase['SIZE'], values_Purchase['COLOR'][0],
                          values_Purchase['FIRSTNAME'], values_Purchase['LASTNAME'], values_Purchase['PHONE'])
            PurchaseWindow.close()
    PurchaseWindow.close()


def Daily_cash_register():
    layout_Daily_cash = [
        [sg.Text(":כסף יומי שנצבר", size=(20, 2), font=('Tahoma', 15))],
        [sg.Button(button_text="אישור", size=(8, 2), font=('Tahoma', 11), pad=(10, 20), button_color="green")]

    ]
    DailyCashWindow = sg.Window("חיפוש", layout_Daily_cash, element_justification='center', margins=(100, 70))
    while True:
        event_DailyCash, values_DailyCash = DailyCashWindow.read()
        if event_DailyCash in (sg.WIN_CLOSED, 'אישור'):
            break
    DailyCashWindow.close()


def HomePage_Window():
    layout = [[sg.Button("חיפוש", size=(12, 3)), sg.Button("רכישה", size=(12, 3))],
              [sg.Button("הוספה", size=(12, 3)), sg.Button("עדכון", size=(12, 3))],
              [sg.Button("קופה יומית", size=(26, 2), button_color="green")]]

    window = sg.Window("San diego Shoes", layout, margins=(250, 150))

    # Create an event loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:  # End program if user closes window
            break
        elif event == "חיפוש":
            Search_Window()
        elif event == "הוספה":
            Add_Window()
        elif event == "רכישה":
            Purchase_Window()
        elif event == "קופה יומית":
            Daily_cash_register()
    window.close()


HomePage_Window()
## TEST

