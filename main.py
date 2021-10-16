import WNS

if __name__ == "__main__":
    shelves = WNS.get_warehouse_shelves(WNS.config.WAREHOUSE_DATA_DIR)
    WNS.prep_data_for_computation(shelves)
    decision = WNS.display_start()
    while decision != WNS.MenuDecision.QUIT:
        if decision == WNS.MenuDecision.FIND_ITEM:
            item = WNS.get_one_item()
            shelf = WNS.find_item(item)
            WNS.show_item_location()
        elif decision == WNS.MenuDecision.FIND_ITEM_PATH:
            items = WNS.get_item_list()
            path = WNS.find_item_list_path(items)
            WNS.show_path(path)
        else:
            raise Exception("This isn't possible, have you returned 'decision?'")
