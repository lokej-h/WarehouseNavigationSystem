"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS

if __name__ == "__main__":
    shelves = WNS.init_WNS()

    # WNS.prep_data_for_computation(arr, shelves)
    # val = "0"
    # while val != "5":
    #     val = WNS.display_start()
    #     if val == "1":
    #         WNS.print_warehouse()
    #         print()
    #     if val == "2":
    #         pid = WNS.get_one_item()
    #         WNS.show_item_location(pid, shelves)
    #     if val == "3":
    #         items = WNS.get_item_list()
    #         path = WNS.find_item_list_path((0, 0), items, shelves)
    #         start_pos = (0, 0)
    #         path = WNS.find_item_list_path(start_pos, items, shelves)
    #         print("\nThe path to the item is \n")
    #         WNS.show_path(path)
    #         WNS.print_path(items[0], shelves, path)
    #     if val == "4":
    #         file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
    #         WNS.change_warehouse_shelves(file_path)
    #         shelves = WNS.init_WNS()
    #     if val == "6":
    #         items = [3000002]
    #         path = WNS.find_item_list_path_bfs((0, 0), items, shelves)
    #         print(path)
    #     if val == "5":
    #         break

    # for key in shelves.keys():
    #     items = [key]
    #     p3 = WNS.find_item_list_path_bfs((0, 0), items, shelves)
    #     print(p3)

    # route3 = [-1, str(108335), str(391825), str(340367), str(286457), str(661741)]
    # route = [-1, str(281610), str(342706), str(111873), str(198029), str(366109), str(287261), str(76283), str(254489), str(258540), str(286457)]
    route2 = [-1, str(427230), str(372539), str(396879), str(391680), str(208660), str(105912), str(332555), str(227534), str(68048), str(188856), str(736830), str(736831), str(479020), str(103313), str(1)]
    left = 0
    right = 1
    while right < len(route2):
        items = [route2[right]]
        if route2[left] == -1:
            start = (0,0)
        else:
            start = shelves[route2[left]]

        p4 = WNS.find_item_list_path_bfs(start, items, shelves)
        # print(p4)
        right = right + 1
        left = left + 1



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
