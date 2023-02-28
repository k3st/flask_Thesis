class Priority_Queue:
    def __init__(self):
        self.pqueue = []
        self.length = 0
    
    def insert(self, node):
        for i in self.pqueue:
            get_bound(i)
        i = 0
        while i < len(self.pqueue):
            if self.pqueue[i].bound > node.bound:
                break
            i+=1
        self.pqueue.insert(i,node)
        self.length += 1

    def print_pqueue(self):
        for i in list(range(len(self.pqueue))):
            print ("pqueue",i, "=", self.pqueue[i].bound)
                    
    def remove(self):
        try:
            result = self.pqueue.pop()
            self.length -= 1
        except: 
            print("Priority queue is empty, cannot pop from empty list.")
        else:
            return result

class Node:
    def __init__(self, level, profit, weight):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.items = []

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
p_per_weight = [0]   

def computeCargo(Cargo, capacity):  
    global vehicleSize,n
    if len(weight) > 0:
        profit.clear()
        weight.clear()
        p_per_weight.clear()

    weight.append(0)
    profit.append(0)
    p_per_weight.append(0)
    

    volumes = Cargo.query.all()
    for index in volumes:
        print(index.cbm)
        print(index.profit)
        print(index.price_per_weight)
        weight.append(index.cbm)
        profit.append(index.profit)
        p_per_weight.append(index.price_per_weight)
         
    vehicleSize = convertToInt(capacity)
    n = len(weight)

    print("Total Items: ", n)    
    print("weight: ",weight)    
    print("vehicleSize ", vehicleSize)
    print("profit ", profit)
    print("p_per_weight: ",p_per_weight)
    # Start of Algorithm
    nodesGenerated = 0
    prioQueue = Priority_Queue()

    v = Node(-1, 0, 0) # v initialized to be the root with level = 0, profit = $0, weight = 0
    nodesGenerated+=1
    
    maxProfit = 0 # maxProfit initialized to $0
    v.bound = get_bound(v)
    print(":asdas:")
    #print("v.bound = ", v.bound)


    
    prioQueue.insert(v)

    print("\n\nInitializing Algorithm.... ")

    while prioQueue.length != 0:
        v = prioQueue.remove() #remove node with best bound
        # print("\nNode removed from prioQueue.")
        # print("Priority Queue: ") 
        prioQueue.print_pqueue()

        # print("\nmaxprofit = ", maxProfit)
        # print("Parent Node: ")
        ### print("v.level = ", v.level, "v.profit = ", v.profit, "v.weight = ", v.weight, "v.bound = ", v.bound, "v.items = ", v.items)

        if v.bound > maxProfit: #check if node is still promising
            print("running")
            #set u to the child that includes the next item
            u = Node(0, 0, 0)
            nodesGenerated+=1
            u.level = v.level + 1
            u.profit = v.profit + profit[u.level]
            u.weight = v.weight + weight[u.level]
            #take v's list and add u's list
            u.items = v.items.copy()
            u.items.append(u.level) # adds next item
            # print("child that includes the next item: ")
            # print("Child 1:")
            # print("u.level = ", u.level, "u.profit = ", u.profit, "u.weight = ", u.weight)
            # print("u.items = ", u.items)
            if u.weight <= vehicleSize and u.profit > maxProfit: 
                
                #update maxProfit
                maxProfit = u.profit
                # print("\nmaxprofit updated = ", maxProfit)
                bestItems = u.items
                print("bestItems!! = ", bestItems)
            u.bound = get_bound(u)
            ##print("vehicleSize ", vehicleSize)
            ##print("u.bound = ", u.bound)
            if u.bound > maxProfit:
                prioQueue.insert(u)
                # print("Node u1 inserted into prioQueue.")
                # print("Priority Queue : ") 
                prioQueue.print_pqueue()
            #set u to the child that does not include the next item
            u2 = Node(u.level, v.profit, v.weight)
            nodesGenerated+=1
            u2.bound = get_bound(u2)
            u2.items = v.items.copy()
            # print("child that doesn't include the next item: ")
            # print("Child 2:")
            # print("u2.level = ", u2.level, "u2.profit = ", u2.profit, "u2.weight = ", u2.weight, "u2.bound = ", u2.bound)
            # print("u2.items = ", u2.items)
            if u2.bound > maxProfit:
                prioQueue.insert(u2)
                # print("Node u2 inserted into prioQueue.")
                # print("Priority Queue : ") 
                prioQueue.print_pqueue()
            print("\nAlgorithm DONE..... \n\n")
    
   
    print("vehicleSize ", vehicleSize)
    print("\nEND maxProfit = ", maxProfit, "nodes generated = ", nodesGenerated)
    bubble_sort(bestItems)
    print("bestItems = ", bestItems)

    # profit.clear(),weight.clear(),p_per_weight.clear()
    data = {'Profit':maxProfit, 'Items':bestItems}
    return data



def get_bound(node):
    if node.weight >= vehicleSize:
        return 0
    else:
        result = node.profit
        j = node.level + 1
        totweight = node.weight
        while j <= n-1 and totweight + weight[j] <= vehicleSize:
            totweight = totweight + weight[j]
            result = result + profit[j]
            j+=1
        k = j
        if k<=n-1:
            result = result + (vehicleSize - totweight) * p_per_weight[k]
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

