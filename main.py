"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS
import sys
import subprocess
import multiprocessing
from multiprocessing import Process
import time

manager = multiprocessing.Manager()
b_m = manager.list()
b_p = manager.list()
b_e = manager.list()
m = manager.list()
p = manager.list()
e = manager.list()

b_m = [sys.maxsize]
b_p = []
b_e = []

m = [sys.maxsize]
p = []
e = []

pcount = True


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

def path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    if(len(route_arr) == 0):
        dist, tp = path_calculate_tsp_distance(end, shelves)
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
            pcount = True
        print(end)
    else:
        for i in range(len(route_arr)):
            # time.sleep(1)
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


def dfs_path_brute_tsp(shelves, route_arr, end = []):
    global m
    global p
    global e
    if(len(route_arr) == 0):
        dist, tp = dfp_path_calculate_tsp_distance(end, shelves)
        if dist < m[0]:
            m[0] = dist
            p = tp
            e = end
        print(end)
    else:
        for i in range(len(route_arr)):
            dfs_path_brute_tsp(shelves, route_arr[:i] + route_arr[i+1:], end + route_arr[i:i+1])

#*******************************************************************************************************************************************

#This function uses the greedy nearest neighbor algorithm to calculate the path and cost between multiple itmes.
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

    #testing bfs or dfs
    route2 = [108335]
    # route2 = [108335, 391825, 340367, 286457, 661741]
    # route2 = [281610, 342706, 111873, 198029, 366109, 287261, 76283]
    # route2 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313]
    l = []    

    shelves = WNS.init_WNS()

    mode = "0"
    print("Input 0 to go into time testing mode, and 1 to go into User menu mode")
    mode = input()

    if mode == "1":
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
                path = WNS.find_item_list_path((0, 0), items, shelves)
                start_pos = (0, 0)
                path = WNS.find_item_list_path(start_pos, items, shelves)
                print("\nThe path to the item is \n")
                WNS.show_path(path)
                WNS.print_path(items[0], shelves, path)
            if val == "4":
                file_path = input("Please input the exact path for the file you want to load as your warehouse\n")
                WNS.change_warehouse_shelves(file_path)
                shelves = WNS.init_WNS()
            if val == "6":
                items = [3000002]
                path,count = WNS.find_item_list_path_dfs((0, 0), 3000002, shelves)
                print(path)
                WNS.print_path(str(items[0]), shelves, path)
            if val == "5":
                break

    elif mode == "0":
        brute = "0"
        print("Enter 1 to test brute force dfs, 2 to test brute force dfs, and 3 to test nearest neighbor")
        brute = input()
        if brute == "1":
            print("dfs")
            print("\nThe Permutations for all possible item pickup combos are printed below: \n")
            dfs_path_brute_tsp(shelves, route2)
            print("\nThe minimum path after Brute force TSP with DFS is:\n ")
            print(m[0])
            print("\nThe full path of the min cost path is: \n")
            print(p)
            print(e)
           
            for i in e:
                l.append(shelves[str(i)])
            print(l)
            WNS.print_path(str(route2[0]), shelves, p)


        elif brute == "2":
            print("bfs")
            print("\nThe Permutations for all possible item pickup combos are printed below: \n")
            path_brute_tsp(shelves, route2)
            print("\nThe minimum path after Brute force TSP with BFS is:\n ")
            print(m[0])
            print("\nThe full path of the min cost path is: \n")
            print(p)
            print(e)
           
            for i in e:
                l.append(shelves[str(i)])
            print(l)
            WNS.print_path(str(route2[0]), shelves, p)


        elif brute == "3":
            print("nn")
            p,c = nearest_neighbor(shelves, route2, 0)
            print(p)
            print("The total cost is: ")
            print(c)

            WNS.print_path(str(route2[0]), shelves, p)
            print(e)

            for i in e:
                l.append(shelves[str(i)])
            print(l)

        else:
            print("invalid input")

    else:
        print("Invalid input exiting program")









    #DEBUG/TODO fix timing

    #timeout test
    # p1 = Process(target=path_brute_tsp(shelves, route2), name='Process_inc_forever')
    # p1.start()
    # p1.join(timeout=3)
    # p1.terminate()
    # if p1.exitcode is None:
    #    print(f'Oops, {p1} timeouts!')
    # if p2.exitcode == 0:
    #     print(f'{p2} is luck and finishes in 10 seconds!')


    #timeout almost working
    # l = []
    # try:
    #     r = subprocess.run(path_brute_tsp(shelves, route2), timeout=3)
    # except:
    #     print("THE FUNCTION HAS TIMED OUT - THE FOLLOWING IS WHAT IT COMPUTED BEFORE THE TIEMOUT")
    #     print("")
    #     print("The minimum path after Brute force TSP is: ")
    #     print("")
    #     if pcount == False:
    #         print(b_m)
    #     else:
    #         print(m)
    #     print("The full path of the min cost path is: ")
    #     if pcount == False:
    #         print(b_p)
    #         print(b_e)
    #         for i in b_e:
    #             l.append(shelves[str(i)])
    #     else:
    #         print(p)
    #         print(e)
    #         for i in e:
    #             l.append(shelves[str(i)])

    #     print(l)
    #     WNS.print_path(str(route2[0]), shelves, p)

    


    #timeout attempt 2
    # l = []
    # action_process = Process(target=path_brute_tsp, args=(shelves, route2))

    # action_process.start()
    # action_process.join(timeout=5)
    # action_process.terminate()
    
    # if action_process != None:
    #     print("THE FUNCTION HAS TIMED OUT - THE FOLLOWING IS WHAT IT COMPUTED BEFORE THE TIEMOUT")
    #     print("")
    #     print("The minimum path after Brute force TSP is: ")
    #     print("")
    #     if pcount == False:
    #         print("pcount is false")
    #         print(b_m)
    #     else:
    #         print("pcount true")
    #         print(m)
    #     print("The full path of the min cost path is: ")
    #     if pcount == False:
    #         print("pcount false 2")
    #         print(b_p)
    #         print(b_e)
    #         for i in b_e:
    #             l.append(shelves[str(i)])
    #     else:
    #         print("pcount true 2")
    #         print(p)
    #         print(e)
    #         for i in e:
    #             l.append(shelves[str(i)])

    #     print(l)
    #     WNS.print_path(str(route2[0]), shelves, p)

    


