import WNS

if __name__ == "__main__":
    shelves = WNS.init_WNS()

items = [str(a) for a in [633, 1321, 3401, 5329, 10438, 372539, 396879, 16880, 208660,
                          105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313, 1, 20373]]

start_pos = (0, 0)
paths = WNS.find_item_list_path(start_pos, items, shelves)
