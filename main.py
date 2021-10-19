import WNS
from WNS.View.warehouse_view import *
from WNS.Model.path_model import *

if __name__ == "__main__":
    shelves = WNS.get_warehouse_shelves(WNS.config.WAREHOUSE_DATA_DIR)
    arr = init_array(shelves)
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
        val = display_start()
        if val == '1':
            print_warehouse(arr)
            print()
        if val == '2':
            show_item_location(arr, shelves)
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
