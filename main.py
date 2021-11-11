"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS

if __name__ == "__main__":
    shelves = WNS.init_WNS()

    val = "0"
    while val != "5":
        val = WNS.display_start()
        if val == "1":
            WNS.print_warehouse()
            print()
        if val == "2":
            pid = WNS.get_one_item()
            WNS.show_item_location(pid, shelves)
        if val == "3":
            items = WNS.get_item_list()
            start_pos = (0, 0)
            path = WNS.find_item_list_path(start_pos, items, shelves)
            print("\nThe path to the item is \n")
            WNS.show_path(path)
            WNS.print_path(items[0], shelves, path)
        if val == "4":
            file_path = input(
                "Please input the exact path for the file you want to load as your warehouse\n")
            WNS.change_warehouse_shelves(file_path)
            shelves = WNS.init_WNS()
        if val == "5":
            break
