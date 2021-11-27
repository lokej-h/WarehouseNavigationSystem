"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS
import sys

import time


b_m = [sys.maxsize]
b_p = []
b_e = []

m = [sys.maxsize]
p = []
e = []

pcount = True

fl = [[]]

start_time = 0
end_time = 0

t_o = 60
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
        path, cost = WNS.find_item_list_path_bfs((0,0), route_arr[x], shelves)
        pre_dict[(-1, route_arr[x])] = cost
        pre_dict[(route_arr[x], -1)] = cost

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
    mod_end.insert(0, -1)
    mod_end.append(-1)
    shelves[str(-1)] = (0,0)

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
    mod_end.insert(0, -1)
    mod_end.append(-1)
    shelves[str(-1)] = (0,0)

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
    global t_o
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
    f_path = [[]]
    nn_c = 0

    same = False

    while(len(unvisited) > 0):
        end_time = time.perf_counter()
        if end_time - start_time > t_o:
            print("nearest neighbor timed out")
            raise Exception("Timeout!")
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
            f_path.append((p[:], str(shortest_item)))

    shelves[str(-1)] = (0,0)
    p,c = WNS.find_item_list_path_bfs(current, -1, shelves)
    p.pop()
    c = c-1
    nn_c = nn_c + c
    nn_path.extend(p[:])
    f_path.append((p[:], str(-1)))


    return nn_path,nn_c, f_path



def print_steps(shelves, algo):
    try:
        l = []
        p.append((0,0))
        print("\nThe minimum path after Brute force TSP with ", str(algo), " is: ")
        print(m[0])

        print("The items were picked up in this order: ")
        print(e)
        fl.pop(0)
        fl[len(fl)-1][0].append((0,0))

                   
        for i in e:
            l.append(shelves[str(i)])
        print("The location of the items that were picked up in order is: ")
        print(l)

        print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

        item_count = 0
        for r in range(0,len(fl)-1):
            WNS.print_path(str(fl[r][1]), shelves, fl[r][0])
            item_count = item_count + 1
        WNS.print_path(str(-1), shelves, fl[len(fl) - 1][0])

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
    route2 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313]
    l = []
    curr_line = 0

    shelves, row_m, col_m = WNS.init_WNS()
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

        if mode == "1":
            val = "0"
            while val != "6":
                b_m = [sys.maxsize]
                b_p = []
                b_e = []

                m = [sys.maxsize]
                p = []
                e = []
                l = []  

                pcount = True

                fl = [[]]
                val = WNS.display_start()
                if val == "1":
                    WNS.print_warehouse()
                    print()
                if val == "2":
                    try:
                        pid = WNS.get_one_item()
                        WNS.show_item_location(pid, shelves)
                    except:
                        print("Error getting item location, try again")
                if val == "3":
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

                    
                    # try:
                    #     items = WNS.get_item_list()
                    #     start_pos = (0, 0)
                    #     path, cost = WNS.find_item_list_path_bfs(start_loc, int(items[0]), shelves)
                    #     path.pop()
                    #     cost = cost - 1
                    #     print(path)
                    #     print("\nThe path to the item is:")
                    #     english = WNS.show_path(path)
                    #     print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")
                    #     WNS.print_path(items[0], shelves, path)
                    # except:
                    #     print("Error with selected item, try again")
                if val == "4":
                    file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
                    try:
                        WNS.change_warehouse_shelves(file_path)
                        shelves = WNS.init_WNS()
                    except:
                        print("Invalid file. Try Again")
                if val == "5":
                    print("Input a list of values items you want to pick up separated by comma")
                    pickup = input()
                    pickup_items = pickup.split(",")
                    for i in range(0,len(pickup_items)):
                        pickup_items[i] = int(pickup_items[i])
                    print("Input 1 to find the BEST POSSIBLE route to pickup these items, Input 2 to find a route to pickup the items in FASTEST time")
                    best = input()
                    if best == "1":
                        shelves[str(-1)] = (0,0)
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

                    elif best == "2":
                        shelves[str(-1)] = (0,0)
                        try:
                            start_time = time.perf_counter()
                            p,c,f_path = nearest_neighbor(shelves, pickup_items, 0)
                            p.append((0,0))
                            f_path[len(f_path)-1][0].append((0,0))
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
                            WNS.print_path(str(-1), shelves, f_path[len(f_path) - 1][0])


                            print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                            english = WNS.show_path(p)
                            print()
                        except Exception as ex:
                            print(ex)
                            print("NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN")

                    else:
                        print("Invalid selection try again")



                if val == "6":
                    break

        elif mode == "0":
            brute = "0"
            print("Enter 1 to test brute force dfs, 2 to test brute force bfs, and 3 to test nearest neighbor")
            brute = input()
            if brute == "1":
                #dfs
                shelves[str(-1)] = (0,0)
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

            elif brute == "2":
                # print("bfs")
                shelves[str(-1)] = (0,0)
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


            elif brute == "3":
                shelves[str(-1)] = (0,0)
                try:
                    #nearest neighbor
                    start_time = time.perf_counter()
                    p,c,f_path = nearest_neighbor(shelves, route2, 0)
                    p.append((0,0))
                    f_path[len(f_path)-1][0].append((0,0))
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
                    WNS.print_path(str(-1), shelves, f_path[len(f_path) - 1][0])


                    print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                    english = WNS.show_path(p)
                except Exception as ex:
                    print(ex)
                    print("NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN")

            else:
                print("invalid input")

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

            if choice == '1':
                print(contents[curr_line])
                start_time = time.perf_counter()
                p,c,f_path = nearest_neighbor(shelves, contents[curr_line], 0)
                p.append((0,0))
                f_path[len(f_path)-1][0].append((0,0))
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
                WNS.print_path(str(-1), shelves, f_path[len(f_path) - 1][0])


                print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                english = WNS.show_path(p)

                curr_line = curr_line + 1
                if curr_line > len(contents):
                    print("All orders fullfilled starting from the beginning")
                    curr_line = 0


            elif choice == '2':
                print("Select which line to fullfill")
                l_num = input()
                start_time = time.perf_counter()
                p,c,f_path = nearest_neighbor(shelves, contents[int(l_num)-1], 0)
                p.append((0,0))
                f_path[len(f_path)-1][0].append((0,0))
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
                WNS.print_path(str(-1), shelves, f_path[len(f_path) - 1][0])


                print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
                english = WNS.show_path(p)

            else:
                print("invalid choice, try again")

        elif mode == "3":
            print("What should time out be for brute force bfs, dfs, and nearest neighbor?")
            t_o = int(input())

        elif mode == "4":
            correction = 1
            print("Enter start row coordinate")
            start_x = int(input())
            print("Enter start col coordinate")
            start_y = int(input())

            print("Enter end row coordinate")
            end_x = int(input())
            print("Enter end col coordinate")
            end_y = int(input())

            if any([True for ke,va in shelves.items() if va == (start_x - correction, start_y)]) and (start_x - correction != 0 or start_y != 0):
                print("Starting location invalid, try again")

            elif start_x - correction < 0 or start_x - correction > col_m:
                print("starting location out of range, try again")

            elif start_y < 0 or start_y > row_m:
                print("starting location out of range, try again")

            elif end_x - correction < 0 or end_x - correction > col_m:
                print("ending location out of range, try again")

            elif end_y < 0 or end_y > row_m:
                print("ending location out of range, try again")

            elif any([True for ke,va in shelves.items() if va == (end_x - correction, end_y)]):
                print("Ending location invalid, try again")
            else:
                start_x = start_x - correction
                end_x = end_x - correction
                start_loc = (start_x, start_y)
                end_loc = (end_x, end_y)

            # end_loc[0] = end_x
            # end_loc[1] = end_y





        elif mode == "5":
            break

        else:
            print("Invalid input try again")




    


