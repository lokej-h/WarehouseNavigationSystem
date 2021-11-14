"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS
import sys
import errno
import os
import signal
import functools


m = sys.maxsize
p = []
e = []


class TimeoutError(Exception):
    pass

def timeout(seconds=60, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator

def preprocess_distances(route_arr, shelves):

    pre_dict = dict()

    for i in range(0, len(route_arr)):
        for j in range(i+1, len(route_arr)):
            path, cost = WNS.find_item_list_path_bfs(shelves[str(route_arr[i])], route_arr[j], shelves)
            pre_dict[(route_arr[i], route_arr[j])] = cost
            pre_dict[(route_arr[j], route_arr[i])] = cost

    for x in range(0, len(route_arr)):
        path, cost = WNS.find_item_list_path_bfs((0,0), route_arr[x], shelves)
        pre_dict[(-1, route_arr[x])] = cost
        pre_dict[(route_arr[x], -1)] = cost

    return pre_dict

def preprocess_with_paths_bfs(route_arr, shelves):

    path_pre_dict = dict()

    for i in range(0, len(route_arr)):
        for j in range(i+1, len(route_arr)):
            path, cost = WNS.find_item_list_path_bfs(shelves[str(route_arr[i])], route_arr[j], shelves)
            path_pre_dict[(route_arr[i], route_arr[j])] = (cost, path[:])
            path.reverse()
            path_pre_dict[(route_arr[j], route_arr[i])] = (cost, path[:])

    for x in range(0, len(route_arr)):
        path, cost = WNS.find_item_list_path_bfs((0,0), route_arr[x], shelves)
        path_pre_dict[(-1, route_arr[x])] = (cost, path[:])
        path.reverse()
        path_pre_dict[(route_arr[x], -1)] = (cost, path[:])

    return path_pre_dict


def dfs_preprocess_distances(route_arr, shelves):

    pre_dict = dict()

    for i in range(0, len(route_arr)):
        for j in range(i+1, len(route_arr)):
            path, cost = WNS.find_item_list_path_dfs(shelves[str(route_arr[i])], route_arr[j], shelves)
            pre_dict[(route_arr[i], route_arr[j])] = cost
            pre_dict[(route_arr[j], route_arr[i])] = cost

    for x in range(0, len(route_arr)):
        path, cost = WNS.find_item_list_path_dfs((0,0), route_arr[x], shelves)
        pre_dict[(-1, route_arr[x])] = cost
        pre_dict[(route_arr[x], -1)] = cost

    return pre_dict

def calculate_tsp_distance(end, pre_dict, shelves):
    mod_end = list(end)
    mod_end.insert(0, -1)
    mod_end.append(-1)

    left = 0
    right = 1

    total_cost = 0
    while(right < len(mod_end)):
        if((mod_end[left], mod_end[right]) in pre_dict):
            total_cost = total_cost + pre_dict[(mod_end[left], mod_end[right])]
        left = left + 1
        right = right + 1

    return total_cost




def brute_force_tsp(pre_dict, shelves, route_arr, end = []):
    global m
    if(len(route_arr) == 0):
        dist = calculate_tsp_distance(end, pre_dict, shelves)
        if dist < m:
            m = dist
        print(end)
    else:
        for i in range(len(route_arr)):
            brute_force_tsp(pre_dict, shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])





#adding path functions ******************************************************************************************************************
def path_calculate_tsp_distance(end, shelves):
    mod_end = list(end)
    mod_end.insert(0, -1)
    mod_end.append(-1)
    shelves[str(-1)] = (0,0)

    left = 0
    right = 1

    total_cost = 0
    total_path = []

    while(right < len(mod_end)):
        if left == 0:
            path, cost = WNS.find_item_list_path_bfs(shelves[str(mod_end[left])], str(mod_end[right]), shelves)
            path.pop()
            cost = cost - 1
            total_path.extend(path[:])
            total_cost = total_cost + cost
        else:
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                path, cost = WNS.find_item_list_path_bfs((total_path[len(total_path)-1][0], total_path[len(total_path)-1][1]), str(mod_end[right]), shelves)
                path.pop()
                cost = cost - 1
                total_path.extend(path[:])
                total_cost = total_cost + cost
        left = left + 1
        right = right + 1

    return total_cost, total_path

@timeout(10, os.strerror(errno.ETIMEDOUT))
def path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    if(len(route_arr) == 0):
        dist, tp = path_calculate_tsp_distance(end, shelves)
        if dist < m:
            m = dist
            p = tp
            e = end
        print(end)
    else:
        for i in range(len(route_arr)):
            path_brute_tsp(shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])

#*******************************************************************************************************************************************

#adding path functions DFS ******************************************************************************************************************
def dsp_path_calculate_tsp_distance(end, shelves):
    mod_end = list(end)
    mod_end.insert(0, -1)
    mod_end.append(-1)
    shelves[str(-1)] = (0,0)

    left = 0
    right = 1

    total_cost = 0
    total_path = []

    while(right < len(mod_end)):
        if left == 0:
            path, cost = WNS.find_item_list_path_dfs(shelves[str(mod_end[left])], str(mod_end[right]), shelves)
            path.pop()
            cost = cost - 1
            total_path.extend(path[:])
            total_cost = total_cost + cost
        else:
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                path, cost = WNS.find_item_list_path_dfs((total_path[len(total_path)-1][0], total_path[len(total_path)-1][1]), str(mod_end[right]), shelves)
                path.pop()
                cost = cost - 1
                total_path.extend(path[:])
                total_cost = total_cost + cost
        left = left + 1
        right = right + 1

    return total_cost, total_path


def dsp_path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    if(len(route_arr) == 0):
        dist, tp = dsp_path_calculate_tsp_distance(end, shelves)
        if dist < m:
            m = dist
            p = tp
            e = end
        print(end)
    else:
        for i in range(len(route_arr)):
            dsp_path_brute_tsp(shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])

#*******************************************************************************************************************************************


def nearest_neighbor(shelves, route_arr, index):
    pre_dict = preprocess_distances(route_arr, shelves)
    visited = set()
    unvisited = set()
    for i in route_arr:
        unvisited.add(i)

    current = (0,0)
    curr_item = -1

    mindistance = sys.maxsize
    shortest_item = 0

    nn_path = []
    nn_c = 0

    same = False

    while(len(unvisited) > 0):
        same = False
        mindistance = sys.maxsize
        for x in unvisited:
            if curr_item != -1:
                if shelves[str(x)] == shelves[str(curr_item)]:
                    same = True
                    unvisited.remove(x)
                    visited.add(x)
                    curr_item = x
                    e.append(curr_item)
                    break
            if pre_dict[curr_item, x] < mindistance:
                mindistance = pre_dict[curr_item, x]
                shortest_item = x

        if same == False:
            unvisited.remove(shortest_item)
            visited.add(shortest_item)
            curr_item = shortest_item
            e.append(shortest_item)

            p,c = WNS.find_item_list_path_bfs(current, shortest_item, shelves)
            p.pop()
            c = c-1
            current = (p[len(p) -1][0], p[len(p) -1][1])
            nn_c = nn_c + c
            nn_path.extend(p[:])

    shelves[str(-1)] = (0,0)
    p,c = WNS.find_item_list_path_bfs(current, -1, shelves)
    p.pop()
    c = c-1
    nn_c = nn_c + c
    nn_path.extend(p[:])


    return nn_path,nn_c






if __name__ == "__main__":
    shelves = WNS.init_WNS()

#     val = "0"
#     while val != "5":
#         val = WNS.display_start()
#         if val == "1":
#             WNS.print_warehouse()
#             print()
#         if val == "2":
#             pid = WNS.get_one_item()
#             WNS.show_item_location(pid, shelves)
#         if val == "3":
#             items = WNS.get_item_list()
#             path = WNS.find_item_list_path((0, 0), items, shelves)
#             start_pos = (0, 0)
#             path = WNS.find_item_list_path(start_pos, items, shelves)
#             print("\nThe path to the item is \n")
#             WNS.show_path(path)
#             WNS.print_path(items[0], shelves, path)
#         if val == "4":
#             file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
#             WNS.change_warehouse_shelves(file_path)
#             shelves = WNS.init_WNS()
#         if val == "6":
#             items = [3000002]
#             path,count = WNS.find_item_list_path_dfs((0, 0), 3000002, shelves)
#             print(path)
#             WNS.print_path(str(items[0]), shelves, path)
#         if val == "5":
#             break




    #testing bfs or dfs
    # route2 = [108335]
    # route2 = [108335, 391825, 340367, 286457, 661741]
    # route2 = [281610, 342706, 111873, 198029, 366109, 287261, 76283]
    route2 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313]
  

    # route2.insert(0, -1)
    # left = 0
    # right = 1
    # full_path = []
    # mc = -1
    # while right < len(route2):
    #     items = route2[right]
    #     if route2[left] == -1:
    #         start = (0,0)
    #     else:
    #         start = shelves[str(route2[left])]

    #     print("START IS: ", start)

    #     p4,mc  = WNS.find_item_list_path_bfs(start, items, shelves)
    #     # print("MOVE COUNT IS: ")
    #     # print(mc)
    #     # print(len(p4))

    #     # WNS.print_path(str(route2[right]), shelves, p4)
    #     full_path.extend(p4)
    #     full_path.append("NEXT")
    #     # print(p4)
    #     right = right + 1
    #     left = left + 1

    # # WNS.print_path(str(route2[left]), shelves, full_path)
    # print("FULL PATH")
    # print(full_path)




  



    # testing brute force tsp

    # print("Starting Preprocessing - Debug Prints Below")

    # pre_dict = preprocess_distances(route2, shelves)

    # # bfs_dict = preprocess_distances(route2, shelves)

    # print("")
    # print("The Preprocess Dictionary is: ")
    # print("")
    # print(pre_dict)

    # # print("")
    # # print("The BFS Dictionary is: ")
    # # print("")
    # # print(bfs_dict)


    # print("")
    # print("The Permutations for all possible item pickup combos are printed below: ")
    # print("")
    # brute_force_tsp(pre_dict, shelves, route2)

    # print("")
    # print("The minimum path after Brute force TSP is: ")
    # print("")
    # print(m)



    #thorough path testing without preprocessing
    print("The Permutations for all possible item pickup combos are printed below: ")
    print("")
    path_brute_tsp(shelves, route2)
    print("")
    print("The minimum path after Brute force TSP is: ")
    print("")
    print(m)
    print("The full path of the min cost path is: ")
    print(p)
    print(e)
    l = []
    for i in e:
        l.append(shelves[str(i)])
    print(l)
    WNS.print_path(str(route2[0]), shelves, p)



    #nearest neighbor testing
    # p,c = nearest_neighbor(shelves, route2, 0)
    # print(p)
    # print("The total cost is: ")
    # print(c)

    # WNS.print_path(str(route2[0]), shelves, p)
    # print(e)
    # l = []
    # for i in e:
    #     l.append(shelves[str(i)])
    # print(l)