"""

Main module to act as an entrypoint for pyinstaller

This code can be moved into __main__.py without changing functionality

"""
import WNS
import sys

import time
import copy



# backup variables for max cost path and order of items
# cost
b_m = [sys.maxsize]
# path (locations) travelled
b_p = []
# item IDs picked up in order
b_e = []


# variables for min cost path and order of items
m = [sys.maxsize]
# path (locations) travelled
p = []
# item IDs picked up in order
e = []

# used to check if full was computed at timeout
pcount = True

# a list of lists which contains the paths, a second way of representing the full path
fl = [[]]

# start and end time used for timeout
start_time = 0
end_time = 0

# timeout variable used to configure custom timeout in seconds (menu option)
t_o = 60

# start and end location to configure custom start and end (menu option)
start_loc = (0, 0)
end_loc = (0, 0)

# this function creates a dictionary that contains the cost between every two items in the input route array using BFS
def preprocess_distances(route_arr, shelves):

    # initialize graph datastructure stored as a python dictionary

    pre_dict = dict()

    # for loop to go through each element in the list of items to pick up

    for i in range(0, len(route_arr)):
        # nested for loop to go through every pair of elements in list of items to pick up

        for j in range(i + 1, len(route_arr)):
            # call bfs function to find distance and path between the two item

            path, cost = WNS.find_item_list_path_bfs(
                shelves[str(route_arr[i])], route_arr[j], shelves
            )
            # distance calculated is the straight line distance from actual shelf location to next actual shelf location

            # in the tsp portion of the code you nagivate from whichever point next to the shelf that you end at to, the top left bottom or right of the next shelf.

            # store cost for the items in the dictionary. key: tuple containing two items, value: cost

            pre_dict[(route_arr[i], route_arr[j])] = cost
            # store same cost for the items in the dictionary in opposite direction. key: tuple containing two items, value: cost

            pre_dict[(route_arr[j], route_arr[i])] = cost

    # for loop to go through each element of items list

    for x in range(0, len(route_arr)):
        # calculate distance from start location to each item using bfs function

        path, cost = WNS.find_item_list_path_bfs(start_loc, route_arr[x], shelves)
        # store the calculated cost into dictionary

        pre_dict[("start", route_arr[x])] = cost
        # store the calculated cost into dictionary

        pre_dict[(route_arr[x], "start")] = cost

    # for loop to go through each element of items list

    for x in range(0, len(route_arr)):
        # calculate distance from end location to each item using bfs function

        path, cost = WNS.find_item_list_path_bfs(end_loc, route_arr[x], shelves)
        # store the calculated cost into dictionary

        pre_dict[("end", route_arr[x])] = cost
        # store the calculated cost into dictionary

        pre_dict[(route_arr[x], "end")] = cost

    # function returns the dictionary which is essentially our graph
    return pre_dict


# this function creates a dictionary that contains the cost,and path between every two items in the input route array using BFS
def preprocess_with_paths_bfs(route_arr, shelves):

    # initialize graph datastructure stored as a python dictionary

    path_pre_dict = dict()

    # for loop to go through each element in the list of items to pick up
    for i in range(0, len(route_arr)):
        # nested for loop to go through every pair of elements in list of items to pick up
        for j in range(i + 1, len(route_arr)):
            # call bfs function to find distance and path between the two item
            path, cost = WNS.find_item_list_path_bfs(
                shelves[str(route_arr[i])], route_arr[j], shelves
            )
            # distance calculated is the straight line distance from actual shelf location to next actual shelf location

            # in the tsp portion of the code you nagivate from whichever point next to the shelf that you end at to, the top left bottom or right of the next shelf.

            # store cost and path for the items in the dictionary. key: tuple containing two items, value: cost, path
            path_pre_dict[(route_arr[i], route_arr[j])] = (cost, path[:])
            # reverse path to store opposite direction path
            path.reverse()
            # store cost for the items in the dictionary. key: tuple containing two items, value: cost, path
            path_pre_dict[(route_arr[j], route_arr[i])] = (cost, path[:])

    # for loop to go through each element of items list
    for x in range(0, len(route_arr)):
        # calculate distance from start location to each item using bfs function
        path, cost = WNS.find_item_list_path_bfs((0, 0), route_arr[x], shelves)
        # store cost and path for the items in the dictionary. key: tuple containing two items, value: cost, path
        path_pre_dict[(-1, route_arr[x])] = (cost, path[:])
        # reverse path to get path for oppsite direction
        path.reverse()
        # store cost and path for the items in the dictionary. key: tuple containing two items, value: cost, path
        path_pre_dict[(route_arr[x], -1)] = (cost, path[:])

    # function returns the dictionary which is essentially our graph
    return path_pre_dict


# this function creates a dictionary that contains the cost between every two items in the input route array using DFS
def dfs_preprocess_distances(route_arr, shelves):

    # initialize graph datastructure stored as a python dictionary

    pre_dict = dict()

    # for loop to go through each element in the list of items to pick up
    for i in range(0, len(route_arr)):
        # nested for loop to go through every pair of elements in list of items to pick up
        for j in range(i + 1, len(route_arr)):
            # call dfs function to find distance and path between the two item
            path, cost = WNS.find_item_list_path_dfs(
                shelves[str(route_arr[i])], route_arr[j], shelves
            )
            # distance calculated is the straight line distance from actual shelf location to next actual shelf location

            # in the tsp portion of the code you nagivate from whichever point next to the shelf that you end at to, the top left bottom or right of the next shelf.

            # store cost for the items in the dictionary. key: tuple containing two items, value: cost
            pre_dict[(route_arr[i], route_arr[j])] = cost
            # store cost for the items in the dictionary. key: tuple containing two items, value: cost
            pre_dict[(route_arr[j], route_arr[i])] = cost

    # for loop to go through each element of items list
    for x in range(0, len(route_arr)):
        # calculate distance from start location to start using dfs function
        path, cost = WNS.find_item_list_path_dfs((0, 0), route_arr[x], shelves)
        # store cost for the item in the dictionary. key: tuple containing two items, value: cost
        pre_dict[(-1, route_arr[x])] = cost
        # store cost for the item in the dictionary. key: tuple containing two items, value: cost
        pre_dict[(route_arr[x], -1)] = cost

    # function returns the dictionary which is essentially our graph
    return pre_dict


# this function uses the BFS Dict to calculate the cost of traversing through the passed in route
def calculate_tsp_distance(end, pre_dict, shelves):
    # this function is the brute force travelling salesmen implementation.

    # the brute_force_tsp function below calculates permutations of every single route then passes it to this function.

    # In this function we first append start and end to the item permutation then use a two pointer approach to find the TSP total cost.

    # This specific implementation uses the preprocessed dictionary to get costs

    # copy item list to new list
    mod_end = list(end)
    # append start to the item list
    mod_end.insert(0, -1)
    # append end to the item list
    mod_end.append(-1)

    # left pointer
    left = 0
    # right pointer
    right = 1

    # tsp cost
    total_cost = 0
    # loop until right pointer is past the list length.
    while right < len(mod_end):
        # if tuple of ptr of left and right are in the preprocessed dictionary add the cost to total cost
        if (mod_end[left], mod_end[right]) in pre_dict:
            # add the cost to total cost
            total_cost = total_cost + pre_dict[(mod_end[left], mod_end[right])]
        # increment left
        left = left + 1
        # increment right
        right = right + 1

    # return total cost
    return total_cost


# this function calculates the permutation of every single route of a given list of items, it then calls the calculate_tsp_distance function
# to compute the cost of each permutation to find the minimum cost permutation
def brute_force_tsp(pre_dict, shelves, route_arr, end=[]):
    # global variable that holds cost
    global m
    if len(route_arr) == 0:
        # when end list is full (equal to the length of items to pick up) call the brute force tsp function
        dist = calculate_tsp_distance(end, pre_dict, shelves)
        # if the calculated path is the smallest path seen assign that path to be the new minimum path
        if dist < m:
            # assign that path to be the new minimum path
            m = dist
        # print the list
        print(end)
    else:
        # loop through the route array
        for i in range(len(route_arr)):
            # recursively call the function inside the loop
            brute_force_tsp(
                pre_dict,
                shelves,
                route_arr[:i] + route_arr[i + 1 :],
                end + route_arr[i : i + 1],
            )


# These functions don't use the preprocess dictionaries, instead they call BFS directly to get the cost and path
# The reason for this is because we want to navigate exactly from current location to next item.
# This information isn't available in the preprocess dictionary since it only contains costs of distances from one item to every
# other item.
# adding path functions ******************************************************************************************************************
def path_calculate_tsp_distance(end, shelves):
    # this function is the brute force travelling salesmen implementation.

    # the brute_force_tsp function below calculates permutations of every single route then passes it to this function.

    # In this function we first append start and end to the item permutation then use a two pointer approach to find the TSP total cost.

    # this function actually calculates the dsitance from current spot to the left, right, top, or bottom of next item. To do this the actual

    # bfs function is called instead of using the preprocess dictionary

    # copy item list to new list
    mod_end = list(end)
    # append start to the item list
    mod_end.insert(0, "start")
    # append end to the item list
    mod_end.append("end")
    # shelves[str(-1)] = (0,0)

    # left pointer
    left = 0
    # right pointer
    right = 1

    # total cost
    total_cost = 0
    # total path stored
    total_path = []
    # another representation of total path
    f_path = [[]]

    # loop till right less than length of index
    while right < len(mod_end):
        # first iteration
        if left == 0:
            # calculate bfs from start to first item
            path, cost = WNS.find_item_list_path_bfs(
                shelves[str(mod_end[left])], str(mod_end[right]), shelves
            )
            # path will go until left, right, bottom, or top of item location

            # this line pops out the actual location from the path to ensure that it goes to left, right, bottom, or top
            path.pop()
            # decrement cost because of last line
            cost = cost - 1
            # add path to total path
            total_path.extend(path[:])
            # if the item wasnt at the same location as the last iteration
            if len(path) > 0:
                # add path to alternative path structure
                f_path.append((path[:], str(mod_end[right])))
            # add to total cost
            total_cost = total_cost + cost
        else:
            # every other iteration
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                # if path is at a different location than
                path, cost = WNS.find_item_list_path_bfs(
                    (
                        total_path[len(total_path) - 1][0],
                        total_path[len(total_path) - 1][1],
                    ),
                    str(mod_end[right]),
                    shelves,
                )
                # what was previously visited, call the bfs function from the last spot that user was at to the location of the next item

                # pop out the last element of path in order to make sure user ends up at top left bottom or right of the item
                path.pop()
                # decrement cost accordingly
                cost = cost - 1
                # add path to total path
                total_path.extend(path[:])
                # add path to total path in alternative format
                f_path.append((path[:], str(mod_end[right])))
                # add cost to total cost
                total_cost = total_cost + cost
        # increment left
        left = left + 1
        # increment right
        right = right + 1

    # return total cost, path, and alternative for path
    return total_cost, total_path, f_path


def path_brute_tsp(shelves, route_arr, end=[]):
    # recursive function to find all permutations of route array and put them in end. When end list fills up the calculate tsp distance function is called to get the actual tsp cost.

    # global variable for cost
    global m
    # global variable for path
    global p
    # global variable for items
    global e
    # global variable for path in alternate format
    global fl
    # global variable for start time
    global start_time
    # global variable for end time
    global end_time
    # global variable for timeout
    global t_o

    # when end array is filled up
    if len(route_arr) == 0:
        # call the distance function to get the actual distance
        dist, tp, f_path = path_calculate_tsp_distance(end, shelves)
        # if distance calculated is minimum
        if dist < m[0]:
            # if distance doesn't equal
            if m != sys.maxsize:
                # copy cost to backup cost
                b_m = m[:]
                # copy path to backup path
                b_p = p[:]
                # copy item order to backup order
                b_e = e[:]

            # backup

            # backup configuration variable
            pcount = False
            # store the lowest cost
            m[0] = dist
            # store the path for that cost
            p = tp
            # store the item list for that
            e = end
            # store the path for that in alternative format
            fl = f_path
            # set boolean equal to true to show paths have been stored
            pcount = True
        # end time for timeout calculation
        end_time = time.perf_counter()
        # time out if time elapsed greater than timeout time

        # raise an exception

        if end_time - start_time > t_o:
            raise Exception("Timeout!")
    else:
        # for loop through array of items
        for i in range(len(route_arr)):
            # recursion inside for loop in order to get all permutations of the items
            path_brute_tsp(
                shelves, route_arr[:i] + route_arr[i + 1 :], end + route_arr[i : i + 1]
            )


# *******************************************************************************************************************************************


# These functions are exaclty like the above two functions, but they use DFS instead of BFS
# adding path functions DFS ******************************************************************************************************************
def dfp_path_calculate_tsp_distance(end, shelves):
    # this function is the dfs version of brute force travelling salesmen implementation.

    # the dfs_path_brute_tsp function below calculates permutations of every single route then passes it to this function.

    # In this function we first append start and end to the item permutation then use a two pointer approach to find the TSP total cost.

    # this function actually calculates the dsitance from current spot to the left, right, top, or bottom of next item. To do this the actual

    # dfs function is called instead of using the preprocess dictionary

    # make a copy of the list which has items to pick up
    mod_end = list(end)
    # insert start
    mod_end.insert(0, "start")
    # insert end
    mod_end.append("end")
    # shelves[str(-1)] = (0,0)

    # left ptr
    left = 0
    # right ptr
    right = 1

    # variable to keep track of cost
    total_cost = 0
    # variable to store path
    total_path = []
    # variable to store path in alternative format
    f_path = [[]]

    # loop till right goes past item array size
    while right < len(mod_end):
        # first iteration
        if left == 0:
            # calculate dfs from start to first item
            path, cost = WNS.find_item_list_path_dfs(
                shelves[str(mod_end[left])], str(mod_end[right]), shelves
            )
            # path will go until left, right, bottom, or top of item location

            # remove last element of path to make above statement hold true
            path.pop()
            # decrement by 1 accordingly
            cost = cost - 1
            # copy path to total path
            total_path.extend(path[:])
            # if item is in a different spot
            if len(path) > 0:
                # copy to alternative path in order to display it later
                f_path.append((path[:], str(mod_end[right])))
            # add to total path
            total_cost = total_cost + cost
        # every other iteration
        else:
            # item is at same shelf can pick up without moving
            if shelves[str(mod_end[right])] != shelves[str(mod_end[left])]:
                # calculate dfs from start to first item
                path, cost = WNS.find_item_list_path_dfs(
                    (
                        total_path[len(total_path) - 1][0],
                        total_path[len(total_path) - 1][1],
                    ),
                    str(mod_end[right]),
                    shelves,
                )
                # path will go until left, right, bottom, or top of item location

                # pop last element to make above hold true
                path.pop()
                # decrement cost accordingly
                cost = cost - 1
                # add calculated path to total path
                total_path.extend(path[:])
                # addd calculated path to total path in alternative format
                f_path.append((path[:], str(mod_end[right])))
                # add to cost
                total_cost = total_cost + cost
        # increment left
        left = left + 1
        # increment right
        right = right + 1

    # return cost, path, and alternative path

    return total_cost, total_path, f_path


# this function calculates the permutation of every single route of a given list of items, it then calls the dfp_calculate_tsp_distance function
# to compute the cost of each permutation to find the minimum cost permutation
def dfs_path_brute_tsp(shelves, route_arr, end=[]):
    # global variable for cost
    global m
    # global variable for path
    global p
    # global variable for item order
    global e
    # global variable for alternative path
    global fl
    # global variable for timeout
    global t_o
    # if the end array has filled up to all the items needed to pick up
    if len(route_arr) == 0:
        # call the dfs tsp function above to get the total cost and path
        dist, tp, f_path = dfp_path_calculate_tsp_distance(end, shelves)
        # if cost is less than total store it
        if dist < m[0]:
            if m != sys.maxsize:
                # backup store of cost
                b_m = m[:]
                # backup store of path
                b_p = p[:]
                # backup store of item order
                b_e = e[:]

            # backup

            # backup store boolean variable
            pcount = False
            # store cost
            m[0] = dist
            # store path
            p = tp
            # store item order
            e = end
            # store alternative path
            fl = f_path
            # bolean variable for backup done
            pcount = True
        # end_time = time.time()

        # end_time = timer()

        # end time to keep track of time out
        end_time = time.perf_counter()
        # print(end_time - start_time)

        # raise an exception if too much time elapsed

        if end_time - start_time > t_o:
            raise Exception("Timeout!")
    # print(end)

    else:
        # loop going throuhg route array
        for i in range(len(route_arr)):
            # recursion inside the loop in order to get every permutation of route_array
            dfs_path_brute_tsp(
                shelves, route_arr[:i] + route_arr[i + 1 :], end + route_arr[i : i + 1]
            )



# *******************************************************************************************************************************************

# This function uses the greedy nearest neighbor algorithm to calculate the path and cost between multiple times.
def unoptimized_nearest_neighbor(shelves, route_arr, index):
    # this is the unoptimized nearest neihgbor function. This code is not as optimal as our actual nearest neighbor because it always starts at start

    # it also always ends at end

    # thus if some route ended very far away from end location this code would not be as optimal

    # global variable for timeout
    global t_o
    # create graph using preprocess dictionary function. Look above for explanation
    pre_dict = preprocess_distances(route_arr, shelves)
    # visited set
    visited = set()
    # unvisited set
    unvisited = set()
    # add every element to unvisited set
    for i in route_arr:
        unvisited.add(i)

    # current = (0,0)

    # curr_item = -1

    # set current to start
    current = start_loc
    # set current item to start
    curr_item = "start"

    # min distance
    mindistance = sys.maxsize
    # shortest path at each iteration
    shortest_item = 0

    # variable for storing nn path
    nn_path = []
    # alternative variable for storing f_path
    f_path = [[]]
    # cost of nn
    nn_c = 0

    # if two items in succession are on the same shelf don't do any additional calculation, both items can be picked up from one spot.
    same = False

    # loop until no more unvisited nodes
    while len(unvisited) > 0:
        # timer for timeout
        end_time = time.perf_counter()
        # time out if too much time has elapsed and raise an exception
        if end_time - start_time > t_o:
            print("nearest neighbor timed out")
            raise Exception("Timeout!")
        # boolean to keep track of if two items are in same location
        same = False
        # min distance
        mindistance = sys.maxsize
        # go through all univisited nodes
        for x in unvisited:
            # if curr_item != -1:

            # Not the first iteration
            if curr_item != "start":
                # check if two items in same spot
                if shelves[str(x)] == shelves[str(curr_item)]:
                    # if so bool is true
                    same = True
                    # remove node and add to visited
                    unvisited.remove(x)
                    visited.add(x)
                    # set node to current item
                    curr_item = x
                    # append the node to the item order list
                    e.append(curr_item)
                    break
            # this part of code checks which item in univisted list is the shortest next path distance
            if pre_dict[curr_item, x] < mindistance:
                # keep track of this distance
                mindistance = pre_dict[curr_item, x]
                # keep track of this item as well
                shortest_item = x

        # two items cannot be picked up from same spot
        if same == False:
            # remove from univisted
            unvisited.remove(shortest_item)
            # add node to visited
            visited.add(shortest_item)
            # make node current node
            curr_item = shortest_item
            # add item to item order list
            e.append(shortest_item)

            # call the BFS function to get the actual path from current location to left, right, bottom, or top of next item
            p, c = WNS.find_item_list_path_bfs(current, shortest_item, shelves)
            # pop last element from path to make the above statement true
            p.pop()
            # decrement accordingly
            c = c - 1
            # set new current location to the location user is currently at
            current = (p[len(p) - 1][0], p[len(p) - 1][1])
            # add to path
            nn_c = nn_c + c
            # copy path
            nn_path.extend(p[:])
            # copy path again
            f_path.append((p[:], str(shortest_item)))

    # shelves[str(-1)] = (0,0)

    # add end node
    p, c = WNS.find_item_list_path_bfs(current, "end", shelves)
    # pop last node for same reason as above
    p.pop()
    # decremement cost
    c = c - 1
    # update cost
    nn_c = nn_c + c
    # update path
    nn_path.extend(p[:])
    # update alternative path
    f_path.append((p[:], str(-1)))

    # print(f_path)

    # return path
    return nn_path, nn_c, f_path


# This function uses the greedy nearest neighbor algorithm to calculate the path and cost between multiple times.
def nearest_neighbor(shelves, route_arr, index):
    # this is the optimized nearest neihgbor function.

    # in this function we loop through each element and start from that element and do a nearest neighbor.

    # for each iteration we add start and end to the code

    # Thus we perform nearest neighbor AND include the start and end in the optimized path

    # global timeout variable
    global t_o
    # global item order list
    global e
    # preprocess dictionary to create the graph
    pre_dict = preprocess_distances(route_arr, shelves)

    # path to return
    r_nn_path = []
    # path to return alternative
    r_f_path = [[]]
    # cost to return
    r_nn_c = 0

    # min cost of each nn iteration
    min_nn_c = sys.maxsize

    # iterate through each element of array and start from there. This is what makes this NN implementation optimal
    for el in range(0, len(route_arr)):

        # visited set
        visited = set()
        # unvisited set
        unvisited = set()
        # add first item to visited
        visited.add(route_arr[el])
        # loop through and add every other item to unvisited

        for i in range(0, len(route_arr)):
            if i != el:
                unvisited.add(route_arr[i])

        # reset nn path
        nn_path = []
        # reset alternative path for nn
        f_path = [[]]
        # reset cost
        nn_c = 0

        # reset temp item list
        temp_e = []

        # variable to hold min distance
        mindistance = sys.maxsize
        # variable to hold shortest next item
        shortest_item = 0

        # add start to path

        # call bfs function to add item to path. Go from left, right, bottom, or top, of one shelf to the left, right, bottom, or top of another
        p, c = WNS.find_item_list_path_bfs(start_loc, route_arr[el], shelves)
        # pop to make sure you dont stay on a shelf
        p.pop()
        # decrement cost
        c = c - 1
        # add cost to total cost
        nn_c = nn_c + c
        # add to path
        nn_path.extend(p[:])
        # add to alternative path
        f_path.append((p[:], str(route_arr[el])))
        # reset first_loc
        first_loc = (p[len(p) - 1][0], p[len(p) - 1][1])

        # current should now be set to the first node travelled too
        current = first_loc
        # current item should also be accordingly updated
        curr_item = route_arr[el]
        # put the item pickup order in a temporary list
        temp_e.append(curr_item)

        # if two items in succession are on the same shelf don't do any additional calculation, both items can be picked up from one spot.
        same = False

        # loop until no more unvisited nodes
        while len(unvisited) > 0:
            # timeout code

            end_time = time.perf_counter()
            if end_time - start_time > t_o:
                print("nearest neighbor timed out")
                raise Exception("Timeout!")
            # boolean to check if two items on same list
            same = False

            # minimum distance reset

            mindistance = sys.maxsize
            # loop through each univisited node

            for x in unvisited:
                # if curr_item != -1:

                if curr_item != "start":
                    # checks if no movement necessary to pickup item
                    if shelves[str(x)] == shelves[str(curr_item)]:
                        # sets this flag to indicate that
                        same = True
                        # remove from univisited
                        unvisited.remove(x)
                        # add to visited
                        visited.add(x)
                        # set that item to current item
                        curr_item = x
                        # e.append(curr_item)

                        # add item picked up to item order list
                        temp_e.append(curr_item)
                        break
                # code that checks the straight line distance from current node to every other node in curr_item
                if pre_dict[curr_item, x] < mindistance:
                    # update min distance if distance is smaler
                    mindistance = pre_dict[curr_item, x]
                    # set the min distance item to be the shortest next hop item
                    shortest_item = x

            # if you had to move to get the item come into this code
            if same == False:
                # remove item from unvisited
                unvisited.remove(shortest_item)
                # add item to visited
                visited.add(shortest_item)
                # set current item to that shortests item calculated before
                curr_item = shortest_item
                # e.append(shortest_item)

                # add the item to the item order temporary list
                temp_e.append(shortest_item)

                # call bfs to actually go from left, right, bottom, or top of item to left, right, bottom, or top of next item.
                p, c = WNS.find_item_list_path_bfs(current, shortest_item, shelves)
                # this pop makes the above happen
                p.pop()
                # decrement accordingly
                c = c - 1
                # set current spot to wherever user is from previous travel
                current = (p[len(p) - 1][0], p[len(p) - 1][1])
                # update the cost
                nn_c = nn_c + c
                # update the path
                nn_path.extend(p[:])
                # update the alternative path used for printing the path
                f_path.append((p[:], str(shortest_item)))

        # add end to path

        # for each iteration add the end to the item list do the same calculation from above for this last node
        p, c = WNS.find_item_list_path_bfs(current, "end", shelves)
        # pop for same reason as above
        p.pop()
        # decrement accordingly
        c = c - 1
        # add to cost
        nn_c = nn_c + c
        # add to path
        nn_path.extend(p[:])
        # add to alternative path
        f_path.append((p[:], str(-1)))

        # if this iterations NN with start and end is the optimal path and cost
        if nn_c < min_nn_c:
            # set the min equal to that cost
            min_nn_c = nn_c
            # r_nn_path = nn_path[:]

            # put the path into the return list
            r_nn_path = copy.deepcopy(nn_path)
            # put the cost into the return variable
            r_nn_c = nn_c
            # put the alternative path into the return list
            r_f_path = copy.deepcopy(f_path)
            # put the item order into the return list
            e = copy.deepcopy(temp_e)

    # return all the necessary variables

    return r_nn_path, r_nn_c, r_f_path


# helper function to print the path in englsh and the map, takes in algorithm to use
def print_steps(shelves, algo):
    try:
        l = []
        # p.append((0,0))

        # add end location for printing
        p.append(end_loc)
        # print minimum cost

        print("\nThe minimum path after Brute force TSP with ", str(algo), " is: ")
        print(m[0])

        # print item order

        print("The items were picked up in this order: ")
        print(e)
        fl.pop(0)
        # fl[len(fl)-1][0].append((0,0))

        fl[len(fl) - 1][0].append(end_loc)

        # loop through and add locations of item order to a new list then print that

        for i in e:
            l.append(shelves[str(i)])
        print("The location of the items that were picked up in order is: ")
        print(l)

        # print directions on map

        print("\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n")

        # loop through and print each individual direction

        item_count = 0
        for r in range(0, len(fl) - 1):
            WNS.print_path(str(fl[r][1]), shelves, fl[r][0])
            item_count = item_count + 1
        WNS.print_path("end", shelves, fl[len(fl) - 1][0])

        # print directions in english

        print("\n********************DIRECTIONS SHOWN IN ENGLISH********************\n")
        english = WNS.show_path(p)
        print("")
    except:
        print("Error in processing items, try again")


if __name__ == "__main__":

    # testing bfs or dfs

    # route2 = [1]

    # route2 = [108335]

    # route2 = [108335, 391825, 340367, 286457, 661741]

    # route2 = [281610, 342706, 111873, 198029, 366109, 287261, 76283]

    # boolean to exit the code
    full_exit = False

    # menu code

    while True:
        try:
            # call the change warehouse shelves function to load a new warehouse

            file_path = input(
                "Please input the exact path for the file you want to load as your warehouse\n"
            )
            WNS.change_warehouse_shelves(file_path)
            shelves, row_m, col_m = WNS.init_WNS()
            break
        except:
            pass

    # once warehouse is loaded rest of the menu appears

    while True:
        try:
            # Developer Testing mode, technician could use this hardcoded value as a base testing case and get timing results, or debug program.

            # route2 = [427230, 372539, 396879, 391680, 208660, 105912, 332555, 227534, 68048, 188856, 736830, 736831, 479020, 103313]

            route2 = [108335, 391825, 340367]
            # holds the items helper variable
            l = []
            # current line for file mode
            curr_line = 0
            # set to store file lines that are fulfilled
            lines_done = set()

            # initially set mode to 0
            mode = "0"
            # quit if mode is 5
            while mode != "5":
                # backup cost
                b_m = [sys.maxsize]
                # backup path
                b_p = []
                # backup item list
                b_e = []

                # cost
                m = [sys.maxsize]
                # path
                p = []
                # item list
                e = []
                # list
                l = []

                # variable for backup
                pcount = True

                # alternative path
                fl = [[]]
                print(
                    "Input 0 to go into time testing mode, and 1 to go into User menu mode, 2 to go into file input mode, 3 to specify timeout amount, 4 to change start and end location, 5 to quit"
                )
                mode = input()

                # User Menu Mode

                if mode == "1":
                    val = "0"
                    while val != "6":
                        # backup cost resetting
                        b_m = [sys.maxsize]
                        # backup path resetting
                        b_p = []
                        # backup item list resetting
                        b_e = []

                        # reset cost
                        m = [sys.maxsize]
                        # reset path
                        p = []
                        # reset item order
                        e = []
                        # list showing location of items in e (l is a list of tuples) - debug variable

                        l = []

                        # reset boolean for backup
                        pcount = True

                        # reset alternative path
                        fl = [[]]
                        # function to display the original menu
                        val = WNS.display_start()
                        # print warehouse

                        if val == "1":
                            # function to print warehouse
                            WNS.print_warehouse()
                            # print an extra space
                            print()

                        # show one item location

                        if val == "2":
                            try:
                                # get pid of item
                                pid = WNS.get_one_item()
                                # show item on map
                                WNS.show_item_location(pid, shelves)
                            except:
                                # if error print error
                                print("Error getting item location, try again")

                        # show path to one item

                        if val == "3":
                            try:
                                # menu option to show one item
                                items = WNS.get_item_list()
                                # print the item
                                print(int(items[0]))
                                # start position
                                start_pos = (0, 0)
                                # uses bfs function to get the path to that item
                                path, cost = WNS.find_item_list_path_bfs(
                                    start_loc, int(items[0]), shelves
                                )
                                # print path
                                print(path)
                                # print cost
                                print(cost)
                                # pop off path to normalize
                                path.pop()
                                # decrement cost
                                cost = cost - 1
                                # print path
                                print(path)
                                # print directions on map

                                print("\nThe path to the item is:")
                                english = WNS.show_path(path)
                                print(
                                    "\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n"
                                )
                                WNS.print_path(items[0], shelves, path)

                                shelves, row_m, col_m = WNS.init_WNS()
                            except:
                                print("Error with selected item, try again")

                        # input new file: format - input/qvBox-warehouse-data-test.txt (see warehouse controller for more details)

                        if val == "4":
                            file_path = input(
                                "Please input the exact path for the file you want to load as your warehouse\n"
                            )
                            try:
                                # function to reset warehouse to a different file

                                WNS.change_warehouse_shelves(file_path)
                                shelves, row_m, col_m = WNS.init_WNS()
                                print(
                                    "Resetting start and end location back to default"
                                )
                                start_loc = (0, 0)
                                end_loc = (0, 0)
                            except:
                                print("Invalid file. Try Again")

                        # retrieve a list of items

                        if val == "5":
                            print(
                                "Input a list of values items you want to pick up separated by comma"
                            )
                            pickup = input()
                            # split the pickup items to process
                            pickup_items = pickup.split(",")
                            for i in range(0, len(pickup_items)):
                                # go through each item and make them integers
                                pickup_items[i] = int(pickup_items[i])
                            print(
                                "Input 1 to find the BEST POSSIBLE route to pickup these items, Input 2 to find a route to pickup the items in FASTEST time"
                            )
                            best = input()

                            # retrieve list of items using BFS

                            if best == "1":
                                # shelves[str(-1)] = (0,0)

                                shelves["start"] = start_loc
                                shelves["end"] = end_loc
                                done = False
                                try:
                                    start_time = time.perf_counter()
                                    # function code explained above
                                    path_brute_tsp(shelves, pickup_items)
                                    # print the steps explained above
                                    print_steps(shelves, "BFS")
                                    done = True
                                except:
                                    # timeout
                                    print(
                                        "\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS"
                                    )
                                    if done == False:
                                        # print best found path
                                        print_steps(shelves, "BFS")
                                    else:
                                        print("Error in processing items, try again")
                                    done = False

                                shelves, row_m, col_m = WNS.init_WNS()

                            # retrieve list of items using nearest neighbor

                            elif best == "2":
                                # shelves[str(-1)] = (0,0)

                                shelves["start"] = start_loc
                                shelves["end"] = end_loc
                                try:
                                    start_time = time.perf_counter()
                                    # call nearest neighbor function to get path and cost
                                    p, f_path, e, c = WNS.nearest_neighbor(
                                        shelves, pickup_items, t_o, start_loc, end_loc
                                    )
                                    # p.append((0,0))

                                    # f_path[len(f_path)-1][0].append((0,0))

                                    p.append(end_loc)
                                    # normalize path
                                    f_path[len(f_path) - 1][0].append(end_loc)
                                    # pop off from path
                                    f_path.pop(0)

                                    # print total cost

                                    print("The total cost is: ")
                                    print(c)
                                    print("The items were picked up in this order: ")
                                    print(e)
                                    # print("l is: ")

                                    # print(l)

                                    # print path on map

                                    for i in e:
                                        l.append(shelves[str(i)])
                                    print(
                                        "The location of the items that were picked up in order is: "
                                    )
                                    print(l)

                                    print(
                                        "\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n"
                                    )

                                    for r in range(0, len(f_path) - 1):
                                        WNS.print_path(
                                            str(f_path[r][1]), shelves, f_path[r][0]
                                        )
                                    # changed
                                    WNS.print_path(
                                        "end", shelves, f_path[len(f_path) - 1][0]
                                    )

                                    # print directons in english

                                    print(
                                        "\n********************DIRECTIONS SHOWN IN ENGLISH********************\n"
                                    )
                                    english = WNS.show_path(p)
                                    print()
                                except Exception as ex:
                                    print(ex)
                                    print(
                                        "NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN"
                                    )

                                shelves, row_m, col_m = WNS.init_WNS()

                            else:
                                print("Invalid selection try again")

                        # quit this menu

                        if val == "6":
                            break

                # Developer Testing Mode

                elif mode == "0":
                    brute = "0"
                    print(
                        "Enter 1 to test brute force dfs, 2 to test brute force bfs, and 3 to test nearest neighbor"
                    )
                    brute = input()

                    # dfs

                    if brute == "1":
                        # dfs

                        # shelves[str(-1)] = (0,0)

                        shelves["start"] = start_loc
                        shelves["end"] = end_loc
                        done = False
                        try:
                            start_time = time.perf_counter()
                            # print(time.perf_counter())

                            # dfs function for brute force travelling salesman explained above
                            dfs_path_brute_tsp(shelves, route2)
                            # print time for performance
                            print(time.perf_counter())
                            # print the steps explained above
                            print_steps(shelves, "DFS")
                            done = True
                        except:
                            # timeout
                            print(
                                "\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS"
                            )
                            if done == False:
                                # print best available path
                                print_steps(shelves, "DFS")
                            else:
                                # error
                                print("Error in processing items, try again")
                            done = False

                        shelves, row_m, col_m = WNS.init_WNS()

                    # bfs

                    elif brute == "2":
                        # print("bfs")

                        # shelves[str(-1)] = (0,0)

                        # add start loc to dictionary
                        shelves["start"] = start_loc
                        # add end loc to dictionary
                        shelves["end"] = end_loc

                        done = False
                        try:
                            start_time = time.perf_counter()
                            # bfs to get brute force travelling salesmen
                            path_brute_tsp(shelves, route2)
                            # print steps
                            print_steps(shelves, "BFS")
                            done = True
                        except:
                            # timeout give best available path
                            print(
                                "\nCODE HAS TIMED OUT - SHOWING BEST OF THE COMPUTED PATHS"
                            )
                            if done == False:
                                # print that path
                                print_steps(shelves, "BFS")
                            else:
                                print("Error in processing items, try again")
                            done = False

                        shelves, row_m, col_m = WNS.init_WNS()

                    # nn

                    elif brute == "3":
                        # shelves[str(-1)] = (0,0)

                        # start loc
                        shelves["start"] = start_loc
                        # end loc
                        shelves["end"] = end_loc

                        try:
                            # nearest neighbor

                            start_time = time.perf_counter()
                            # call the nearest neighbor function
                            p, f_path, e, c = WNS.nearest_neighbor(
                                shelves, route2, t_o, start_loc, end_loc
                            )
                            # p.append((0,0))

                            p.append(end_loc)
                            # f_path[len(f_path)-1][0].append((0,0))

                            f_path[len(f_path) - 1][0].append(end_loc)
                            f_path.pop(0)

                            # print the total cost

                            print("The total cost is: ")
                            print(c)
                            # print item order

                            print("The items were picked up in this order: ")
                            print(e)
                            for i in e:
                                l.append(shelves[str(i)])
                            print(
                                "The location of the items that were picked up in order is: "
                            )
                            print(l)

                            # print directions on map

                            print(
                                "\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n"
                            )

                            for r in range(0, len(f_path) - 1):
                                WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                            WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])

                            # print directions in english

                            print(
                                "\n********************DIRECTIONS SHOWN IN ENGLISH********************\n"
                            )
                            english = WNS.show_path(p)
                        except Exception as ex:
                            print(ex)
                            print(
                                "NEAREST NEIGHBOR TIMED OUT - NO PATH FOUND TRY AGAIN"
                            )

                        shelves, row_m, col_m = WNS.init_WNS()

                    else:
                        print("invalid input")

                # file input mode

                elif mode == "2":
                    contents = []
                    print("file reading mode")
                    try:
                        # open file to read from

                        with open(
                            "./input/qvBox-warehouse-orders-list-part01.txt"
                        ) as fil:
                            lines = fil.readlines()
                    except:
                        # throw exception for poor reading from file

                        print(
                            "error reading from file, place file in input folder and try again:"
                        )
                        break

                    # read the line in file, split to process, then add to a dictionary

                    for a_line in lines:
                        # split
                        l_str = a_line.split(",")
                        # process
                        l_ints = [int(x) for x in l_str]

                        # add
                        contents.append(l_ints)

                    print(
                        "Select 1 to fullfill the next order, Select 2 to fullfill any order line of your choice"
                    )
                    choice = input()

                    # fulfill the next unfulfilled order

                    if choice == "1":
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc

                        # loop till next unfilfulled order found

                        # print(curr_line)

                        while True:
                            # print(lines_done)

                            if int(curr_line) in lines_done:
                                # print("line already done")

                                curr_line = curr_line + 1
                            else:
                                break

                        # reset if all orders fulfilled

                        if curr_line > len(contents):
                            curr_line = 0
                            lines_done.clear()
                            print("All orders fullfilled starting from the beginning")

                        # print line to fulfill

                        print(contents[curr_line])
                        start_time = time.perf_counter()
                        # nearest neighbor to fulfill it
                        p, f_path, e, c = WNS.nearest_neighbor(
                            shelves, contents[curr_line], t_o, start_loc, end_loc
                        )
                        # p.append((0,0))

                        # f_path[len(f_path)-1][0].append((0,0))

                        p.append(end_loc)
                        f_path[len(f_path) - 1][0].append(end_loc)
                        f_path.pop(0)
                        # normalize path above

                        # print cost and item order

                        print("The total cost is: ")
                        print(c)
                        print("The items were picked up in this order: ")
                        print(e)
                        for i in e:
                            l.append(shelves[str(i)])
                        print(
                            "The location of the items that were picked up in order is: "
                        )
                        print(l)

                        # print directions on map

                        print(
                            "\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n"
                        )

                        for r in range(0, len(f_path) - 1):
                            WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                        WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])

                        # print directions in english

                        print(
                            "\n********************DIRECTIONS SHOWN IN ENGLISH********************\n"
                        )
                        english = WNS.show_path(p)

                        # reset if all orders fullfilled

                        curr_line = curr_line + 1
                        if curr_line > len(contents):
                            print("All orders fullfilled starting from the beginning")
                            curr_line = 0
                            lines_done.clear()

                    # select a line to fulfill

                    elif choice == "2":
                        print("Select which line to fullfill")
                        # get line to fullfill
                        l_num = input()
                        # try:

                        # process it
                        lines_done.add(int(l_num) - 1)
                        # print("added ", int(l_num) - 1)

                        # except Exception as u:

                        # print(u)

                        # print("line error")

                        start_time = time.perf_counter()
                        shelves["start"] = start_loc
                        shelves["end"] = end_loc
                        
                        # nearest neighbor to fullfill
                        p, f_path, e, c = WNS.nearest_neighbor(
                            shelves, contents[int(l_num)-1], t_o, start_loc, end_loc
                        )
                        # p.append((0,0))

                        # f_path[len(f_path)-1][0].append((0,0))

                        p.append(end_loc)
                        f_path[len(f_path) - 1][0].append(end_loc)
                        f_path.pop(0)
                        # process paths above

                        # print total cost and item order

                        print("The total cost is: ")
                        print(c)
                        print("The items were picked up in this order: ")
                        print(e)
                        for i in e:
                            l.append(shelves[str(i)])
                        print(
                            "The location of the items that were picked up in order is: "
                        )
                        print(l)

                        # print directions on map

                        print(
                            "\n\n********************DIRECTIONS SHOWN ON MAP********************\n\n"
                        )

                        for r in range(0, len(f_path) - 1):
                            WNS.print_path(str(f_path[r][1]), shelves, f_path[r][0])
                        WNS.print_path("end", shelves, f_path[len(f_path) - 1][0])

                        # print directions in english

                        print(
                            "\n********************DIRECTIONS SHOWN IN ENGLISH********************\n"
                        )
                        english = WNS.show_path(p)

                    else:
                        print("invalid choice, try again")

                # user can set the timeout

                elif mode == "3":
                    print(
                        "What should time out be for brute force bfs, dfs, and nearest neighbor?"
                    )
                    # set timeout to user value
                    t_o = int(input())

                # user can set start and end location

                elif mode == "4":
                    # have user input start and end, row and col coordinates

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

                    # Error checking to see if coordinates are in bounds and also if coordinates are at a spot where a shelf is

                    if any(
                        [
                            True
                            for ke, va in shelves.items()
                            if va == (start_x - correction, start_y)
                            and ke != "start"
                            and ke != "end"
                        ]
                    ):
                        print("Starting location invalid, try again")

                    elif start_x - correction < 0 or start_x - correction > col_m:
                        print("starting location out of range, try again")

                    elif start_y < 0 or start_y > row_m:
                        print("starting location out of range, try again")

                    elif end_x - correction < 0 or end_x - correction > col_m:
                        print("ending location out of range, try again")

                    elif end_y < 0 or end_y > row_m:
                        print("ending location out of range, try again")

                    elif any(
                        [
                            True
                            for ke, va in shelves.items()
                            if (
                                va == (end_x - correction, end_y)
                                and ke != "start"
                                and ke != "end"
                            )
                        ]
                    ):
                        print("Ending location invalid, try again")
                    else:
                        start_x = start_x - correction
                        end_x = end_x - correction
                        start_loc = (start_x, start_y)
                        end_loc = (end_x, end_y)

                # end_loc[0] = end_x

                # end_loc[1] = end_y

                # if error checks pass, set the start and end above

                # quit if user wanats to quit

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
