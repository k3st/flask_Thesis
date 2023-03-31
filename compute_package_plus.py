import heapq
class Node:
    def __init__(self, level, weight, profit, bound):
        self.level = level
        self.weight = weight
        self.profit = profit
        self.bound = bound
    
    def __lt__(self, other):
        return self.bound > other.bound

def convertToInt(capacity):
    print("convertToInt() ",capacity)
    if capacity == "4 CBM":
        return 4        # 4.6 CBM  / 162.447 CBF (cubic foot)
    elif capacity == "12 CBM":
        return 12       # 12.2 CBM / 430.8389 CBF (cubic foot)
    elif capacity == "21 CBM":
        return 21       # 21.4 CBM / 755.7339 CBF (cubic foot)
    elif capacity == "55 CBM":
        return 55       # 55.1 CBM / 1945.838 CBF (cubic foot)
    else:
        print("ERROR RETURNING ... ")
        return False
    

print("run initial")    

# Initialize Variables
#knapsack capacity, 6 Pallets is default
profit = [0]      # profit
weight = [0]      # weight

def computeCargo(Cargo, size):  
    global capacity,n
    if len(weight) > 0:
        profit.clear()
        weight.clear()

    # weight.append(0)
    # profit.append(0)
    

    volumes = Cargo.query.all()
    print(volumes)
    print("********")
    for index in volumes:
        print(index.cbm)
        print(index.profit)
        weight.append(index.cbm)
        profit.append(index.profit)
         
    capacity = convertToInt(size)
    n = len(weight)

    print("Total Items: ", n)    
    print("weight: ",weight)    
    print("capacity ", capacity)
    print("profit ", profit)


    # Start of Algorithm
    q = []
    root = Node(-1, 0, 0, 0)
    root.bound = bound(root, n, capacity, weight, profit)
    heapq.heappush(q, root)
    max_profit = 0

    print("\n\nInitializing Algorithm.... ")
    while q:
        node = heapq.heappop(q)
        if node.bound < max_profit:
            continue
        if node.level == n - 1:
            bestItems = node.weight
            max_profit = node.profit
            print("current optimal  ", bestItems, "\t",max_profit)
            continue
        # Exclude next item
        exclude = Node(node.level + 1, node.weight, node.profit, node.bound)
        exclude.bound = bound(exclude, n, capacity, weight, profit)
        if exclude.bound > max_profit:
            heapq.heappush(q, exclude)
        # Include next item
        include = Node(node.level + 1, node.weight + weight[node.level+1], node.profit + profit[node.level+1], node.bound)
        include.bound = bound(include, n, capacity, weight, profit)
        if include.bound > max_profit:
            heapq.heappush(q, include)
    
    print("\nAlgorithm DONE..... \n\n")
    print("capacity ", capacity)
    print("\nEND max_profit = ", max_profit,)
    # bubble_sort(bestItems)
    print("bestItems = ", bestItems)
    # for fixing inaccurate cargo #
    # print("bestitems 1st", bestItems[0])
    # for i in bestItems:
    #     data = append bestItems[i]

    # profit.clear(),weight.clear()
    data = {'Profit':max_profit, 'Items':bestItems}
    print("data results : ",data)
    return data



def bound(node, n, capacity, weight, profit):
    if node.weight >= capacity:
        return 0
    result = node.profit
    j = node.level + 1
    tot_weight = node.weight
    while j < n and tot_weight + weight[j] <= capacity:
        tot_weight += weight[j]
        result += profit[j]
        j += 1
    if j < n:
        result += (capacity - tot_weight) * profit[j] / weight[j]
    return result
        
def bubble_sort(nlist):
    for i in range(len(nlist) - 1, 0, -1):
        no_swap = True
        for j in range(0, i):
            if nlist[j + 1] > nlist[j]:
                nlist[j], nlist[j + 1] = nlist[j + 1], nlist[j]
                no_swap = False
        if no_swap:
            return 

