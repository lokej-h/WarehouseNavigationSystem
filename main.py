"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS

if __name__ == "__main__":
    shelves = WNS.get_warehouse_shelves()
    WNS.init_array(shelves)

    # WNS.prep_data_for_computation(arr, shelves)
    val = "0"
    while val != "4":
        val = WNS.display_start()
        if val == "1":
            WNS.print_warehouse()
            print()
        if val == "2":
            pid = WNS.get_one_item()
            WNS.show_item_location(pid, shelves)
        if val == "3":
            items = WNS.get_item_list()
            path = WNS.find_item_list_path((0, 0), items, shelves)
            start_pos = (0, 0)
            path = WNS.find_item_list_path(start_pos, items, shelves)
            print("\nThe path to the item is \n")
            WNS.show_path(path)
            WNS.print_path(items[0], shelves, path)
        if val == "4":
            break

    # WNS.prep_data_for_computation(shelves)

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
