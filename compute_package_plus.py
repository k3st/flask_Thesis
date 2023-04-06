import heapq
class Node:
    def __init__(self, level, weight, profit, bound, items):
        self.level = level
        self.weight = weight
        self.profit = profit
        self.bound = bound
        self.items = items
    
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
         
    capacity = convertToInt(size) + 1
    n = len(weight)

    print("Total Items: ", n)    
    print("weight: ",weight)    
    print("capacity ", capacity)
    print("profit ", profit)


    # Start of Algorithm
    q = []
    root = Node(-1, 0, 0, 0, [])
    root.bound = bound(root, n, capacity, weight, profit)
    heapq.heappush(q, root)
    max_profit = 0
    bestItems = []
    while q:
        node = heapq.heappop(q)
        if node.bound < max_profit:
            continue
        if node.level == n - 1:
            bestItems = node.items
            max_profit = node.profit
            print("current optimal  ", bestItems, "\t",max_profit)
            continue
        # Exclude next item
        exclude = Node(node.level + 1, node.weight, node.profit, node.bound, node.items.copy())
        exclude.bound = bound(exclude, n, capacity, weight, profit)
        if exclude.bound > max_profit:
            heapq.heappush(q, exclude)
        # Include next item
        include = Node(node.level + 1, node.weight + weight[node.level+1], node.profit + profit[node.level+1], node.bound, node.items.copy())
        include.items.append(node.level+1)
        include.bound = bound(include, n, capacity, weight, profit)
        if include.bound > max_profit:
            heapq.heappush(q, include)
    
    print("\nAlgorithm DONE..... \n\n")
    print("capacity ", capacity)
    print("\nEND max_profit = ", max_profit,)
    # bubble_sort(bestItems)
    print("bestItems(index) = ", bestItems)
    # for fixing inaccurate cargo no.
    # print("bestitems 1st", bestItems[0])
    # for i in bestItems:
    #     data = append bestItems[i]

    _bestItems = []
    _bestProfit = []
    for i in bestItems:
        _bestItems.append(volumes[i].id)
        _bestProfit.append(volumes[i].profit)
    print(_bestItems)
    print(_bestProfit)
    # profit.clear(),weight.clear()
    data = {'Profit':_bestProfit, 'total_profit':max_profit, 'Items':_bestItems}
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
        
def fifo(cargo, size):
    print("\n\nFIFO() running")
    global _capacity
    fifoWeight= []
    fifoProfit = []
    
    if len(fifoWeight) > 0:
        fifoWeight.clear()
        fifoProfit.clear()
        print(" init List cleared...\n\n")

    dataCargo = cargo.query.all()        
    for index in dataCargo:
        fifoWeight.append(index.cbm)
        fifoProfit.append(index.profit)    
    _capacity = convertToInt(size)
    n = len(fifoWeight)
    print("\nControl Data OUTPUT\nTotal Items: ", n)       
    print("_capacity ", _capacity) 
    print("weight: ",fifoWeight)    
    print("profit ", fifoProfit)
    
    i,totalLoad = 0,0
    _addedItem, _rProfit = [],[]
   
    while (i != n):   
        totalLoad += fifoWeight[i]        
        if (totalLoad > _capacity):
            print(f"'{i}' Exceeded {totalLoad}", end=", ")            
            totalLoad -= fifoWeight[i]
            print(f"New Total Load: {totalLoad}")
            i+=1
            continue            
        print(f"data index [ {i} ] Added")
        _addedItem.append(dataCargo[i].id)
        _rProfit.append(fifoProfit[i])
        i+=1
        
    _rtotal_profit = sum(_rProfit)
    print(f"Total Profit is  {_rtotal_profit}")
    _ctrlData = {'_Items':_addedItem, '_Profit':_rProfit, '_total_profit': _rtotal_profit}
    print("data results : ",_ctrlData)
    print("\n","="*25,"FIFO cargo done","="*25)
    return _ctrlData