# import PySimpleGUI as sg
# def PopupWindow():

#     #sg.theme('DarkAmber')   # Add a touch of color
    
#     options = ['Tướng','Sĩ','Tượng', 'Xe', 'Pháo', 'Mã', 'Tốt', 'Xe đỏ', 'Button']
    
#     # All the stuff inside your window.
#     layout = [ 
#                 [sg.Listbox(options,select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,size=(10,len(options)))],
#                 [sg.Button('Ok'), sg.Button('Cancel')]
#             ]
    
#     # Create the Window
#     window = sg.Window('Make your choice', layout)
    
#     # Event Loop to process "events" and get the "values" of the input
#     while True:
#         event, values = window.read()
#         print( f"event={event}" )
#         if event is None or event == 'Ok' or event == 'Cancel': # if user closes window or clicks cancel
#             print(values)
#             break
        
            
#     # close  the window        
#     window.close()
    
#     if event == "Cancel":
#         print( "You cancelled" )
#     else:
        
#         value = values[0]
#         value1 = value[0]
#         print('You entered ', value1)
#         return value1
# new_chess = PopupWindow()

name = "Tướng"
name2 = "Tướng2"
if name in name2:
    print(True)