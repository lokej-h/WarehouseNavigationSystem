"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS
import sys

import time
from collections import deque, defaultdict
from functools import cache


#backup variables for max cost path and order of items
b_m = [sys.maxsize] #cost
b_p = [] #path
b_e = [] #items


#variables for max cost path and order of items
m = [sys.maxsize]
p = []
e = []

#used to check if full was computed at timeout
pcount = True

#a list of lists which contains the paths, a second way of representing the full path
fl = [[]]

#start and end time used for timeout
start_time = 0
end_time = 0

t_o = 60 #timeout variable used to configure custom timeout in seconds (menu option)

#start and end location to configure custom start and end (menu option)
start_loc = (0,0)
end_loc = (0,0)

#this function creates a dictionary that contains the cost between every two items in the input route array using BFS
def preprocess_distances(route_arr, shelves):

    pre_dict = dict()

    for i in range(0, len(route_arr)):
        for j in range(i+1, len(route_arr)):
            path, cost = WNS.find_item_list_path_bfs(shelves[str(route_arr[i])], route_arr[j], shelves)
            pre_dict[(route_arr[i], route_arr[j])] = cost
            pre_dict[(route_arr[j], route_arr[i])] = cost

    for x in range(0, len(route_arr)):
        path, cost = WNS.find_item_list_path_bfs(start_loc, route_arr[x], shelves)
        pre_dict[("start", route_arr[x])] = cost
        pre_dict[(route_arr[x], "start")] = cost

    for x in range(0, len(route_arr)):
        path, cost = WNS.find_item_list_path_bfs(end_loc, route_arr[x], shelves)
        pre_dict[("end", route_arr[x])] = cost
        pre_dict[(route_arr[x], "end")] = cost

    return pre_dict

#this function creates a dictionary that contains the cost,and path between every two items in the input route array using BFS
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

#this function creates a dictionary that contains the cost between every two items in the input route array using DFS
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

#this function uses the BFS Dict to calculate the cost of traversing through the passed in route
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



#this function calculates the permutation of every single route of a given list of items, it then calls the calculate_tsp_distance function
#to compute the cost of each permutation to find the minimum cost permutation
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




#These functions don't use the preprocess dictionaries, instead they call BFS directly to get the cost and path
#The reason for this is because we want to navigate exactly from current location to next item.
#This information isn't available in the preprocess dictionary since it only contains costs of distances from one item to every
#other item.
#adding path functions ******************************************************************************************************************
def path_calculate_tsp_distance(end, shelves):
    mod_end = list(end)
    mod_end.insert(0, "start")
    mod_end.append("end")
    # shelves[str(-1)] = (0,0)

    left = 0
    right = 1

    total_cost = 0
    total_path = []
    f_path = [[]]

    while(right < len(mod_end)):
        if left == 0:
            path, cost = WNS.find_item_list_path_bfs(shelves[str(mod_end[left])], str(mod_end[right]), shelves)
            path.pop()
            cost = cost - 1
            total_path.extend(path[:])
            if len(path) > 0:
                f_path.append((path[:], str(mod_end[right])))
            total_cost = total_cost + cost
        else:
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                path, cost = WNS.find_item_list_path_bfs((total_path[len(total_path)-1][0], total_path[len(total_path)-1][1]), str(mod_end[right]), shelves)
                path.pop()
                cost = cost - 1
                total_path.extend(path[:])
                f_path.append((path[:], str(mod_end[right])))
                total_cost = total_cost + cost
        left = left + 1
        right = right + 1

    return total_cost, total_path, f_path

def path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    global fl
    global start_time
    global end_time
    global t_o
    if(len(route_arr) == 0):
        dist, tp, f_path = path_calculate_tsp_distance(end, shelves)
        if dist < m[0]:
            if m != sys.maxsize:
                b_m = m[:]
                b_p = p[:]
                b_e = e[:]

            #backup
            pcount = False
            m[0] = dist
            p = tp
            e = end
            fl = f_path
            pcount = True
        end_time = time.perf_counter()
        if end_time - start_time > t_o:
            raise Exception("Timeout!")
    else:
        for i in range(len(route_arr)):
            path_brute_tsp(shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])

#*******************************************************************************************************************************************


#These functions are exaclty like the above two functions, but they use DFS instead of BFS
#adding path functions DFS ******************************************************************************************************************
def dfp_path_calculate_tsp_distance(end, shelves):
    mod_end = list(end)
    mod_end.insert(0, "start")
    mod_end.append("end")
    # shelves[str(-1)] = (0,0)

    left = 0
    right = 1

    total_cost = 0
    total_path = []
    f_path = [[]]

    while(right < len(mod_end)):
        if left == 0:
            path, cost = WNS.find_item_list_path_dfs(shelves[str(mod_end[left])], str(mod_end[right]), shelves)
            path.pop()
            cost = cost - 1
            total_path.extend(path[:])
            if len(path) > 0:
                f_path.append((path[:], str(mod_end[right])))
            total_cost = total_cost + cost
        else:
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                path, cost = WNS.find_item_list_path_dfs((total_path[len(total_path)-1][0], total_path[len(total_path)-1][1]), str(mod_end[right]), shelves)
                path.pop()
                cost = cost - 1
                total_path.extend(path[:])
                f_path.append((path[:], str(mod_end[right])))
                total_cost = total_cost + cost
        left = left + 1
        right = right + 1

    return total_cost, total_path, f_path


def dfs_path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    global fl
    global t_o
    if(len(route_arr) == 0):
        dist, tp, f_path = dfp_path_calculate_tsp_distance(end, shelves)
        if dist < m[0]:
            if m != sys.maxsize:
                b_m = m[:]
                b_p = p[:]
                b_e = e[:]

            #backup
            pcount = False
            m[0] = dist
            p = tp
            e = end
            fl = f_path
            pcount = True
        # end_time = time.time()
        # end_time = timer()
        end_time = time.perf_counter()
        # print(end_time - start_time)
        if end_time - start_time > t_o:
            raise Exception("Timeout!")
        # print(end)
    else:
        for i in range(len(route_arr)):
            dfs_path_brute_tsp(shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])

#*******************************************************************************************************************************************

#This function uses the greedy nearest neighbor algorithm to calculate the path and cost between multiple itmes.
def nearest_neighbor(shelves, route_arr, index):
    # timeout
    global t_o
    # get distance between two points ( (A, B) -> cost ) where A is start and B is end
    # str "start" and "end" are keys for the start and end locations
    pre_dict = preprocess_distances(route_arr, shelves)
    # visited and unvisited sets
    # initialize unvisited to all PIDs
    visited = set()
    unvisited = set()
    for i in route_arr:
        unvisited.add(i)

    # get start location from global
    # set current item
    current = start_loc
    curr_item = "start"

    # all nodes are al the PIDs plus the special nodes
    # we need this to be const for iterating
    all_nodes = unvisited.union([curr_item])
    # unvisited will pop a node each iter
    unvisited = all_nodes.copy()
# =============================================================================
#     # make a reverse lookup table to get PID ( (coordinate) -> PID )
#     # https://stackoverflow.com/questions/2568673/inverse-dictionary-lookup-in-python
#     inverse_shelves = {v:k for k,v in shelves.items()}
#
# =============================================================================
    # same minimum startegy
    min_distance_found = sys.maxsize
    for node in all_nodes:
        # remove from unvisited and store as current
        unvisited -= {node}
        curr_item = node
        # special case if the next one is the start location
        if curr_item == "start":
            current = start_loc
        else:
            current = shelves[str(node)]

        # do NN from the current node
        nn_path, nn_c, f_path = nearest_neighbor_calculate(pre_dict, t_o, visited, unvisited, current, curr_item)
        # if it is a shorter path, return
        if nn_c < min_distance_found:
            final_nn_path, final_nn_c, final_f_path = nn_path, nn_c, f_path
            min_distance_found = final_nn_c

        unvisited.add(node)

        raise_if_timeout(start_time, t_o)

    return final_nn_path, final_nn_c, final_f_path

def raise_if_timeout(start_time, t_o):
    end_time = time.perf_counter()
    if end_time - start_time > t_o:
        print("nearest neighbor timed out")
        raise Exception("Timeout!")

def nearest_neighbor_calculate(pre_dict, t_o, visited, unvisited, current, curr_item):
    # constant for finding minimum distance
    # keep track of the shortest item's PID
    mindistance = sys.maxsize
    shortest_item = 0

    # List of coordinates of where to go
    nn_path = [] # List[tuple[int, int]]
    # List of tuples (directions to, PID)
    f_path = [[]] # List[tuple[List[tuple[int,int], str]]]
    # total computed cost of path
    nn_c = 0

    same = False #if two or more items in succession are on the same shelf don't do any additional calculation, all items can be picked up from one spot.

    # handles 1 item at a time i.e. if there are duplicates, that's one iter
    while (len(unvisited) > 0):
        end_time = time.perf_counter()
        if end_time - start_time > t_o:
            print("nearest neighbor timed out")
            raise Exception("Timeout!")
        same = False
        mindistance = sys.maxsize

        # for all the unvisited nodes
        for x in unvisited:
            # if not the start
            if curr_item != "start":
                # and we have an item at the same spot
                # mark them both as visited and add to visited/remove from unvisited
                if shelves[str(x)] == shelves[str(curr_item)]:
                    # set same flag (we have a duplicate)
                    same = True
                    unvisited.remove(x)
                    visited.add(x)
                    curr_item = x
                    e.append(curr_item)
                    break
            # if we found a new closest item
            # make it the closest found item
            if pre_dict[curr_item, x] < mindistance:
                mindistance = pre_dict[curr_item, x]
                shortest_item = x

        # if we know the next item isn't a duplicate
        if same == False:
            # update bookeeping
            unvisited.remove(shortest_item)
            visited.add(shortest_item)
            curr_item = shortest_item
            e.append(shortest_item)

            # find path and cost to the closest item
            p,c = go_to_next_without_shelf(current, shortest_item, shelves)
            # current is now the last coordinate (pickup location)
            current = (p[len(p) -1][0], p[len(p) -1][1])
            # update total cost
            nn_c = nn_c + c
            # add this path to our final paths
            nn_path.extend(p[:])
            f_path.append((p[:], str(shortest_item)))

    # find path and cost to the end
    p,c = go_to_next_without_shelf(current, "end", shelves)
    # more bookeeping
    nn_c = nn_c + c
    nn_path.extend(p[:])
    # since we are at end, PID is -1
    f_path.append((p[:], str(-1)))


    return nn_path,nn_c, f_path

# this is only computed once thanks to @cache
@cache
def get_inverted_dict(d):
    '''get the inverted dictionary of d, if values of d have duplicates,
    appended to list'''
    inverted = defaultdict(list)
    for k,v in d.items():
        inverted[v].append(k)
    return inverted


def get_all_items_where_we_are(location, shelves):
    inverted_shelves = get_inverted_dict(shelves)
    return inverted_shelves[location]


def get_nearest_neighbor(node, available_neighbors, cost_table):
    return min(available_neighbors, key=lambda v: cost_table[node, v])


def go_to_next_without_shelf(start, end, shelves):
    # find path and cost to item
    p,c = WNS.find_item_list_path_bfs(start, end, shelves)
    # we don't want to go into the shelf
    p.pop()
    # we don't walk into the shelf
    c = c-1
    return p, c

def print_steps(shelves, algo):
    try:
        l = []
        # p.append((0,0))
        p.append(end_loc)
        print("\nThe minimum path after Brute force TSP with ", str(algo), " is: ")
        print(m[0])

        print("The items were picked up in this order: ")
        print(e)
        fl.pop(0)
        # fl[len(fl)-1][0].append((0,0))
        fl[len(fl)-1][0].append(end_loc)


        for i in e:
            l.append(shelves[str(i)])
        print("The location of the items that were picked up in order is: ")
        print(l)

        print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

        item_count = 0
        for r in range(0,len(fl)-1):
            WNS.print_path(str(fl[r][1]), shelves, fl[r][0])
            item_count = item_count + 1
        WNS.print_path("end", shelves, fl[len(fl) - 1][0])

        print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
        english = WNS.show_path(p)
        print("")
    except:
        print("Error in processing items, try again")





if __name__ == "__main__":

    #testing bfs or dfs
    # route2 = [1]
    # route2 = [108335]
    # route2 = [108335, 391825, 340367, 286457, 661741]
    # route2 = [281610, 342706, 111873, 198029, 366109, 287261, 76283]
    full_exit = False

    while True:
        try:
            file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
            WNS.change_warehouse_shelves(file_path)
            shelves, row_m, col_m = WNS.init_WNS()
            break
        except:
            pass

    while True:
        try:
            #Developer Testing mode, technician could use this hardcoded value as a base testing case and get timing results, or debug program.
            route2 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313]
            l = []
            curr_line = 0
            lines_done = set() # set to store file lines that are fulfilled

            mode = "0"
            while mode != "5":
                b_m = [sys.maxsize]
                b_p = []
                b_e = []

                m = [sys.maxsize]
                p = []
                e = []
                l = []

                pcount = True

                fl = [[]]
                print("Input 0 to go into time testing mode, and 1 to go into User menu mode, 2 to go into file input mode, 3 to specify timeout amount, 4 to change start and end location, 5 to quit")
                mode = input()

                #User Menu Mode
                if mode == "1":
                    val = "0"
                    while val != "6":
                        b_m = [sys.maxsize]
                        b_p = []
                        b_e = []

                        m = [sys.maxsize]
                        p = []
                        e = []
                        #list showing location of items in e (l is a list of tuples) - debug variable
                        l = []

                        pcount = True

                        fl = [[]]
                        val = WNS.display_start()
                        #print warehouse
                        if val == "1":
                            WNS.print_warehouse()
                            print()

                        #show one item location
                        if val == "2":
                            try:
                                pid = WNS.get_one_item()
                                WNS.show_item_location(pid, shelves)
                            except:
                                print("Error getting item location, try again")

                        #show path to one item
                        if val == "3":
                            try:
                                items = WNS.get_item_list()
                                print(int(items[0]))
                                start_pos = (0, 0)
                                path, cost = WNS.find_item_list_path_bfs(start_loc, int(items[0]), shelves)
                                print(path)
                                print(cost)
                                path.pop()
                                cost = cost - 1
                                print(path)
                                print("\nThe path to the item is:")
                                english = WNS.show_path(path)
                                print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")
                                WNS.print_path(items[0], shelves, path)

                                #DEBUG add this
                                shelves, row_m, col_m = WNS.init_WNS()
                            except:
                                print("Error with selected item, try again")

                        #input new file: format - input/qvBox-warehouse-data-test.txt (see warehouse controller for more details)
                        if val == "4":
                            file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
                            try:
                                WNS.change_warehouse_shelves(file_path)
                                shelves, row_m, col_m = WNS.init_WNS()
                                print("Resetting start and end location back to default")
                                start_loc = (0, 0)
                                end_loc = (0, 0)
                            except:
                                print("Invalid file. Try Again")

                        #retrieve a list of items
                        if val == "5":
                            print("Input a list of values items you want to pick up separated by comma")
                            pickup = input()
                            pickup_items = pickup.split(",")
                            for i in range(0,len(pickup_items)):
                                pickup_items[i] = int(pickup_items[i])
                            print("Input 1 to find the BEST POSSIBLE route to pickup these items, Input 2 to find a route to pickup the items in FASTEST time")
                            best = input()

                            #retrieve list of items using BFS
                            if best == "1":
                                # shelves[str(-1)] = (0,0)
                                shelves["start"] = start_loc
                                shelves["end"] = end_loc
                                done = False
                                try:
                                    start_time = time.perf_counter()
                                    path_brute_tsp(shelves, pickup_items)
                                    print_steps(shelves, "BFS")
                                    done = True
                                except:
                                    print("\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS")
                                    if done == False:
                                        print_steps(shelves, "BFS")
                                    else:
                                        print("Error in processing items, try again")
                                    done = False

                                #DEBUG add this
                                shelves, row_m, col_m = WNS.init_WNS()

                            #retrieve list of items using nearest neighbor
                            elif best == "2":
                                # shelves[str(-1)] = (0,0)
                                shelves["start"] = start_loc
                                shelves["end"] = end_loc
                                try:
                                    start_time = time.perf_counter()
                                    p,c,f_path = nearest_neighbor(shelves, pickup_items, 0)
                                    # p.append((0,0))
                                    # f_path[len(f_path)-1][0].append((0,0))
                                    p.append(end_loc)
                                    f_path[len(f_path)-1][0].append(end_loc)
                                    f_path.pop(0)
                                    print("The total cost is: ")
                                    print(c)
                                    print("The items were picked up in this order: ")
                                    print(e)
                                    # print("l is: ")
                                    # print(l)
                                    for i in e:
                                        l.append(shelves[str(i)])
                                    print("The location of the items that were picked up in order is: ")
                                    print(l)

                                    print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

                                    for r in range(0,len(f_path)-1):
                                        WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                                    WNS.print_path("end", shelves, f_path[len(f_path) - 1][0]) #changed


                                    print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                                    english = WNS.show_path(p)
                                    print()
                                except Exception as ex:
                                    print(ex)
                                    print("NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN")

                                #DEBUG add this
                                shelves, row_m, col_m = WNS.init_WNS()

                            else:
                                print("Invalid selection try again")


                        #quit this menu
                        if val == "6":
                            break

                #Developer Testing Mode
                elif mode == "0":
                    brute = "0"
                    print("Enter 1 to test brute force dfs, 2 to test brute force bfs, and 3 to test nearest neighbor")
                    brute = input()

                    #dfs
                    if brute == "1":
                        #dfs
                        # shelves[str(-1)] = (0,0)
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc
                        done = False
                        try:
                            start_time = time.perf_counter()
                            # print(time.perf_counter())
                            dfs_path_brute_tsp(shelves, route2)
                            print(time.perf_counter())
                            print_steps(shelves, "DFS")
                            done = True
                        except:
                            print("\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS")
                            if done == False:
                                print_steps(shelves, "DFS")
                            else:
                                print("Error in processing items, try again")
                            done = False
                        #DEBUG add this
                        shelves, row_m, col_m = WNS.init_WNS()

                    #bfs
                    elif brute == "2":
                        # print("bfs")
                        # shelves[str(-1)] = (0,0)
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc

                        done = False
                        try:
                            start_time = time.perf_counter()
                            path_brute_tsp(shelves, route2)
                            print_steps(shelves, "BFS")
                            done = True
                        except:
                            print("\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS")
                            if done == False:
                                print_steps(shelves, "BFS")
                            else:
                                print("Error in processing items, try again")
                            done = False
                        #DEBUG add this
                        shelves, row_m, col_m = WNS.init_WNS()


                    #nn
                    elif brute == "3":
                        # shelves[str(-1)] = (0,0)
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc

                        try:
                            #nearest neighbor
                            start_time = time.perf_counter()
                            p,c,f_path = nearest_neighbor(shelves, route2, 0)
                            # p.append((0,0))
                            p.append(end_loc)
                            # f_path[len(f_path)-1][0].append((0,0))
                            f_path[len(f_path)-1][0].append(end_loc)
                            f_path.pop(0)

                            print("The total cost is: ")
                            print(c)
                            print("The items were picked up in this order: ")
                            print(e)
                            for i in e:
                                l.append(shelves[str(i)])
                            print("The location of the items that were picked up in order is: ")
                            print(l)

                            print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

                            for r in range(0,len(f_path)-1):
                                WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                            WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])


                            print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                            english = WNS.show_path(p)
                        except Exception as ex:
                            print(ex)
                            print("NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN")

                        #DEBUG add this
                        shelves, row_m, col_m = WNS.init_WNS()

                    else:
                        print("invalid input")

                #file input mode
                elif mode == "2":
                    contents = []
                    print("file reading mode")
                    try:
                        with open('./input/qvBox-warehouse-orders-list-part01.txt') as fil:
                            lines = fil.readlines()
                    except:
                        print("error reading from file, place file in input folder and try again:")
                        break

                    for a_line in lines:
                        l_str = a_line.split(",")
                        l_ints = [int(x) for x in l_str]

                        contents.append(l_ints)

                    print("Select 1 to fullfill the next order, Select 2 to fullfill any order line of your choice")
                    choice = input()

                    #fulfill the next unfulfilled order
                    if choice == '1':
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc

                        # print(curr_line)
                        while True:
                            # print(lines_done)
                            if int(curr_line) in lines_done:
                                # print("line already done")
                                curr_line = curr_line + 1
                            else:
                                break

                        if curr_line > len(contents):
                            curr_line = 0
                            lines_done.clear()
                            print("All orders fullfilled starting from the beginning")

                        print(contents[curr_line])
                        start_time = time.perf_counter()
                        p,c,f_path = nearest_neighbor(shelves, contents[curr_line], 0)
                        # p.append((0,0))
                        # f_path[len(f_path)-1][0].append((0,0))
                        p.append(end_loc)
                        f_path[len(f_path)-1][0].append(end_loc)
                        f_path.pop(0)

                        print("The total cost is: ")
                        print(c)
                        print("The items were picked up in this order: ")
                        print(e)
                        for i in e:
                            l.append(shelves[str(i)])
                        print("The location of the items that were picked up in order is: ")
                        print(l)

                        print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

                        for r in range(0,len(f_path)-1):
                            WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                        WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])


                        print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                        english = WNS.show_path(p)

                        curr_line = curr_line + 1
                        if curr_line > len(contents):
                            print("All orders fullfilled starting from the beginning")
                            curr_line = 0
                            lines_done.clear()

                    #select a line to fulfill
                    elif choice == '2':
                        print("Select which line to fullfill")
                        l_num = input()
                        # try:
                        lines_done.add(int(l_num)-1)
                        # print("added ", int(l_num) - 1)
                        # except Exception as u:
                        # print(u)
                        # print("line error")
                        start_time = time.perf_counter()
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc
                        p,c,f_path = nearest_neighbor(shelves, contents[int(l_num)-1], 0)
                        # p.append((0,0))
                        # f_path[len(f_path)-1][0].append((0,0))
                        p.append(end_loc)
                        f_path[len(f_path)-1][0].append(end_loc)
                        f_path.pop(0)

                        print("The total cost is: ")
                        print(c)
                        print("The items were picked up in this order: ")
                        print(e)
                        for i in e:
                            l.append(shelves[str(i)])
                        print("The location of the items that were picked up in order is: ")
                        print(l)

                        print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

                        for r in range(0,len(f_path)-1):
                            WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                        WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])


                        print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                        english = WNS.show_path(p)

                    else:
                        print("invalid choice, try again")

                #user can set the timeout
                elif mode == "3":
                    print("What should time out be for brute force bfs, dfs, and nearest neighbor?")
                    t_o = int(input())

                #user can set start and end location
                elif mode == "4":
                    correction = 1
                    print("Enter start row coordinate")
                    start_x = int(input())
                    print("Enter start col coordinate")
                    # start_y = int(input())
                    start_y = ord(input().lower()) - 97

                    print("Enter end row coordinate")
                    end_x = int(input())
                    print("Enter end col coordinate")
                    # end_y = int(input())
                    # temp_y = input()
                    # temp_y = temp_y.lower()
                    end_y = ord(input().lower()) - 97

                    if any([True for ke,va in shelves.items() if va == (start_x - correction, start_y) and ke != "start" and ke != "end"]):
                        print("Starting location invalid, try again")

                    elif start_x - correction < 0 or start_x - correction > col_m:
                        print("starting location out of range, try again")

                    elif start_y < 0 or start_y > row_m:
                        print("starting location out of range, try again")

                    elif end_x - correction < 0 or end_x - correction > col_m:
                        print("ending location out of range, try again")

                    elif end_y < 0 or end_y > row_m:
                        print("ending location out of range, try again")

                    elif any([True for ke,va in shelves.items() if (va == (end_x - correction, end_y) and ke != "start" and ke != "end")]):
                        print("Ending location invalid, try again")
                    else:
                        start_x = start_x - correction
                        end_x = end_x - correction
                        start_loc = (start_x, start_y)
                        end_loc = (end_x, end_y)

                    # end_loc[0] = end_x
                    # end_loc[1] = end_y





                elif mode == "5":
                    full_exit = True
                    break

                else:
                    print("Invalid input try again")

        except:
            print("error in menu run try again")


        if full_exit == True:
            full_exit = False
            break





