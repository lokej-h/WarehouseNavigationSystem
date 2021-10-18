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

    rows, cols = (max(find_max_x) + 5, max(find_max_y) + 5)
    arr = [['.' for i in range(cols)] for j in range(rows)]


    prep_data_for_computation(arr, shelves)

    val = input("Enter what you would like to do on the warehouse application.\nThe following are your options\n1. Print the Warehouse view to see the products in the warehouse.\n2. Enter a product ID to see where in the warehouse you can find the product.\n3. Enter a product ID to find navigation steps to that product.\n")
    
    if val == '1':
        print_warehouse(arr)
    if val == '2':
        pid = input("Enter product ID of the product you are searching for: ")
        print(pid, " is at the following location")
        print(shelves[pid][0], " ", shelves[pid][1])
    if val == '3':
        print("todo")

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
