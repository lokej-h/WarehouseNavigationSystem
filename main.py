import WNS
from WNS.View.warehouse_view import *
from WNS.Model.path_model import *

if __name__ == "__main__":
    shelves = WNS.get_warehouse_shelves(WNS.config.WAREHOUSE_DATA_DIR)
    find_max_x = []
    find_max_y = []
    for key in shelves:
        find_max_x.append(shelves[key][0])
        find_max_y.append(shelves[key][1])

    
    print(max(find_max_x))
    print(max(find_max_y))


    rows, cols = (max(find_max_x) + 3, max(find_max_y) + 3)
    arr = [['.' for i in range(cols)] for j in range(rows)]
    # for i in range(1, rows):
    #     for j in range(1, cols):
    #         if j > 9:
    #             arr[i][j] = '.' + ' '
    #         else:
    #             arr[i][j] = '.' + ' '

    # for i in range(1,len(arr)):
    #     if i < 11:
    #         arr[i][0] = str(i-1) + '  '
    #     else:
    #         arr[i][0] = str(i-1) + ' '

    # for i in range(1,len(arr[0])):
        
    #     if i == 1:
    #        arr[0][i] = '  ' + str(i-1) + ' '
    #     # elif i < 11:
    #     #     arr[0][i] = str(i-1) + ' '
    #     elif i < 10:
    #         arr[0][i] = str(i-1) + ' '
    #     else:
    #         arr[0][i] = str(i-1)


    prep_data_for_computation(arr, shelves)


    val = '0'
    while val != '4':
        val = input("Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n4. Quit navigation and end program\n")
        
        if val == '1':
            print_warehouse(arr)
            print()
        if val == '2':
            pid = input("Enter product ID of the product you are searching for: ")
            print("The product with ID: ", pid, "is at the following location: (", shelves[pid][0] + 1, chr(shelves[pid][1] + 98), ')')
            arr[shelves[pid][0]+1][shelves[pid][1]+1] = 'O'
            print("The following is the map of the warehouse, with the product selected being denoted by an O")
            print_warehouse(arr)
            arr[shelves[pid][0]+1][shelves[pid][1]+1] = 'X'
            print()
        if val == '3':
            print("todo")
            print()
        if val == '4':
            break

    #WNS.prep_data_for_computation(shelves)
    
    # decision = WNS.display_start()
    # print("test")
    # while decision != WNS.MenuDecision.QUIT:
    #     if decision == WNS.MenuDecision.FIND_ITEM:
    #         item = WNS.get_one_item()
    #         shelf = WNS.find_item(item)
    #         WNS.show_item_location()
    #     elif decision == WNS.MenuDecision.FIND_ITEM_PATH:
    #         items = WNS.get_item_list()
    #         path = WNS.find_item_list_path(items)
    #         WNS.show_path(path)
    #     else:
    #         raise Exception("This isn't possible, have you returned 'decision?'")
