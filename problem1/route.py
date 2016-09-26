'''
Created on Sep 18, 2016

@author: Ishita
'''
from math import sin, radians, cos, sqrt, asin
import sys, time

#ANSWER 1: A star algorithm works best for routing options 'distance' and 'time'
#BFS works the best for routing option 'segments', 
#ANSWER 2: The fastest running algorithm is A star. For hundred iterations, A star takes : 73.68 seconds, BFS takes : 112.32 seconds, DFS takes : 172.83 seconds
# IDS takes: 92.45 seconds  
#ANSWER 3: The least memory is taken by BFS,the length of the fringe is 215, for A star it is 501, and for DFS it is 1150  
#ANSWER 4: Used Haversine distance as a heuristic when the routing option is 'Distance';
#For routing option "Time", calculated the heuristic by dividing the total distance of the path by the maximum speed between any two cities;
#For routing option "Segments", calculated the heuristic
#For routing option "Scenic", calculated the heuristic
#ANSWER 5:
def calculateHaversineDistance(lat1, long1, lat2, long2):
    #convert degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1,lat1,long2,lat2])
    lon = long2-long1
    lat = lat2-lat1
    a = sin(lat/2)**2 + cos(lat1) * cos(lat2) * sin(lon/2)**2
    c = 2* asin(sqrt(a))
    distance = 3961*c
    return distance

def calculateHeuristicForTime(h):
    return h/speed

def calculateHeuristicForScenic(h):
    return h*(0.2)   

#read the file for longitudes and latitudes
long_lat_dict = {}
with open("city-gps.txt","r") as city_gps:
    for line in city_gps:
        data = line.split(" ")
        position = []
        position.extend([data[1],data[2]])
        long_lat_dict[data[0]] = position
#create an empty dictionary
data_dict = {}
speed = 0
with open("road-segments.txt","r") as road_segments: #read the file and store the data in data_dict
    for line in road_segments:
        value = []
        swap_value = []
        data = line.split(" ")
        if data[0] in data_dict:
            val = data_dict[data[0]]
            val.extend([data[1],data[2],data[3],data[4]])
            if(data[3]!='' and int(data[3])>speed):
                speed =int(data[3])
        else:
            value.extend([data[1],data[2],data[3],data[4]])
            data_dict[data[0]] = value
            if(data[3]!='' and int(data[3])>speed):
                speed=int(data[3])
        if data[1] in data_dict:
            val = data_dict[data[1]]
            val.extend([data[0],data[2],data[3],data[4]])
        else:
            swap_value.extend([data[0],data[2],data[3],data[4]])
            data_dict[data[1]] = swap_value 

fringe,visitedCities,path,inputCity = [],[],[],[]
routingOption,endCity,routingAlgorithm = '','',''
results,heuristic= {},{}  
         

#returns the path of the current successor from the start city
#Depending on the routing option, it will decide which path is the shortest path if we have two paths leading to the same city
def returnPath(subList,path):
    old_path = results[subList[0]]
    #compare the two distances
    old_distance,new_dist,old_time,new_time,old_count,new_count = 0,0,0,0,0,0
    for i in range(1,len(old_path)):
        list_path = old_path[i]
        old_distance= old_distance + int(list_path[1])
        if(list_path[2] == "0" or list_path[2] == ''):
            list_path[2] = "1"
        old_time = old_time + (float(list_path[1])/float(list_path[2]))
        if(list_path[3]<55):
            old_count+=1
    for j in range(1,len(path)):
        list_newpath = path[j]
        new_dist = new_dist + int(list_newpath[1])
        if(list_newpath[2] == "0" or list_newpath[2]==''):
            list_newpath[2] = "1"
        new_time = new_time + (float(list_newpath[1])/float(list_newpath[2]))
        if(list_newpath[3]<55):
            new_count+=1
    if (old_distance<new_dist and routingOption == 'distance') or (old_time<new_time and routingOption == 'time') or ((len(old_path)<len(path)) and routingOption == 'segments') or ((old_count>new_count) and routingOption == 'scenic'):
        path = old_path
   
    return path  
#handles bfs and dfs
#Start State : Input City
#Goal state : End City
#The function accepts the input city, finds its successors, saves the path of the successor from the input city in a dictionary
#As soon as it encounters the goal city, it breaks out of the loop 
def return_distance(startCity, endCity):
    if not data_dict.get(startCity[0]) or startCity[0]==endCity:
        return None
    visitedCities.append(startCity[0])
    childNodes  = data_dict[startCity[0]]
    if childNodes is not None:  
        for i in range(0,len(childNodes),4):
            subList = childNodes[i:i+4]
            if subList[0] not in visitedCities: # add check if subLIst[0] not in fringe 
                path=[]
                if results.has_key(startCity[0]):
                    value = results[startCity[0]]
                    for list in value:
                        path.append(list)
                    path.append(subList)
                else:
                    path.extend([startCity,subList])
                if results.has_key(subList[0]):
                    path = returnPath(subList,path)
                else:
                    fringe.append(subList)                         
                results[subList[0]] =  path
                if subList[0] == endCity:
                    return endCity
    return None

#IDS SEARCH
def startIDS(inputCity):
    start= time.time()
    depth = 1
    while depth>0:
        isGoal = IdsSearch(depth,inputCity)
        if isGoal == endCity:
            stop=time.time()
            print("time taken for ids is", stop-start)
            break
        else:
            depth = isGoal
            
#The function starts from the input city, finds its successors, checks if a goal state is encountered, if so, breaks out of the loop
#If the successor is not the goal state, it increments the count and after iterating on all the successors it returns the count
#Now the function is called with the new count and loops on the successors till the goal is found        
def IdsSearch(depth, inputCity):
    fringe_ids = []
    visitedCities = []
    fringe_ids.append(inputCity[0])
    visitedCities.append(inputCity[0])
    results_ids = {}
    count = depth
    for i in range(0,depth):
        startCity = fringe_ids.pop(0)
        successors = data_dict[startCity]
        for j in range(0,len(successors),4):
            succ = successors[j:j+4]
            if succ[0] not in visitedCities:
                path=[]
                if results_ids.has_key(startCity):
                    value = results_ids[startCity]
                    for list in value:
                        path.append(list)
                    path.append(succ)
                else:
                    path.extend([startCity,succ])
                if results_ids.has_key(succ[0]):
                    path = returnPath(succ,path)
                elif succ[0] not in visitedCities and succ[0] != endCity:
                    fringe_ids.append(succ[0])
                    visitedCities.append(succ[0])
                    count+=1                   
                results_ids[succ[0]] =  path    
                if succ[0] == endCity:
                    print(path)
                    results[succ[0]] = path
                    return endCity
    return count    

def return_distance_Astar(startCity, endCity):
    if not data_dict.get(startCity[0]) or startCity[0]==endCity:
        return None
    visitedCities.append(startCity[0])
    childNodes  = data_dict[startCity[0]]
    locationEndCity = long_lat_dict[endCity]
    if childNodes is not None:  
        for i in range(0,len(childNodes),4):
            subList = childNodes[i:i+4]
            if subList[0] not in visitedCities: # add check if subLIst[0] not in fringe 
                path=[]
                if results.has_key(startCity[0]):
                    value = results[startCity[0]]
                    for list in value:
                        path.append(list)
                    path.append(subList)
                else:
                    path.extend([startCity,subList])
                if results.has_key(subList[0]):
                    path = returnPath(subList,path)
                else:
                    fringe.append(subList)                         
                results[subList[0]] =  path 
                if subList[0] == endCity:
                    return path
                if (long_lat_dict.get(subList[0]) is not None):
                    buildHeuristicDict(subList,locationEndCity,path)
                else:
                    visitedCities.append(subList[0])
                    successors = data_dict[subList[0]]
                    for j in range(0,len(successors),4):
                            succ = successors[j:j+4]
                            if succ[0] not in visitedCities: # add check if subLIst[0] not in fringe 
                                path=[]
                                if results.has_key(subList[0]):
                                    value = results[subList[0]]
                                    for list in value:
                                        path.append(list)
                                    path.append(succ)
                                else:
                                    path.extend([subList,succ])
                                if results.has_key(succ[0]):
                                    path = returnPath(succ,path)  
                                else :
                                    fringe.append(succ)                         
                                results[succ[0]] =  path
                                if succ[0] == endCity:
                                    return path 
                                if long_lat_dict.get(succ[0]) is not None:
                                    buildHeuristicDict(succ, locationEndCity, path)
                                else:
                                    heuristic[succ[0]] = float(2000)                   
                                
    return None   

def buildHeuristicDict(subList,locationEndCity,path):
    locationStartCity = long_lat_dict[subList[0]]
    locationInputCity = long_lat_dict[inputCity[0]]
    sum = 0
    h = calculateHaversineDistance(float(locationStartCity[0]),float(locationStartCity[1]),float(locationEndCity[0]),float(locationEndCity[1]))
    if(routingOption == 'distance'):
        g= calculateSumOfPath(path,sum)
    if(routingOption == 'time'):
        g = calculateTotalTime(path, sum)    
        h = calculateHeuristicForTime(h)
    if(routingOption == 'scenic'):
        g = calculateScenic(path, sum)
        h = calculateHeuristicForScenic(h)
    if(routingOption == 'segments'):
        g = calculateNoOfSegments(path, sum)
        s=0 
    heuristic[subList[0]] = g+h 
         
def calculateSumOfPath(path,sum):
    for i in range(1,len(path)):
        city = path[i]
        sum = sum + int(city[1])
    return float(sum)

def calculateTotalTime(path,sum):
    for i in range(1,len(path)):
        city = path[i]
        if(city[2]== "0" or city[2]==''):
            city[2] = "1"
        sum = sum + (float(city[1])/float(city[2]))
    return float(sum)

def calculateNoOfSegments(path,sum):
    return len(path)-1

def calculateScenic(path,sum):
    for i in range(1,len(path)):
        city=path[i]
        if(city[3]>55):
            sum+=1
    return sum
        
if(routingAlgorithm == 'astar'):
    start = time.time()
    return_distance_Astar(inputCity,endCity)
    #A star:
    while len(fringe)>0:
        prev_val = 0
        for succ in fringe:
            if prev_val == 0 and heuristic.get(succ[0]) != None:
                prev_val = heuristic[succ[0]]
                successor = succ
            elif (heuristic.get(succ[0]) != None and heuristic[succ[0]]< prev_val):
                prev_val = heuristic[succ[0]]
                successor = succ
        #successor = heuristic[min(heuristic)]
        if successor[0] == endCity:
            break                   
        fringe.remove(successor)
        heuristic.pop(successor[0])            
        value = return_distance_Astar(successor,endCity)
        if value is not None :
            stop = time.time()
            print("time for astar is",stop-start)
            break   
        
if(routingAlgorithm == 'ids'):
    startIDS(inputCity)
    
if(routingAlgorithm == 'bfs'):
    start = time.time() 
    return_distance(inputCity,endCity)
    while len(fringe)>0:
        successor = fringe.pop(0) # BFS
        result  = return_distance(successor,endCity)
        if result == endCity:
            stop = time.time()
            print("time for bfs is",stop-start)
            time.sleep(1)
            break 
       
if(routingAlgorithm == 'dfs'):
    start = time.time()  
    return_distance(inputCity,endCity)
    while len(fringe)>0:
        successor = fringe.pop() # DFS
        result  = return_distance(successor,endCity)
        if result == endCity:
            stop = time.time()
            print("time for dfs is",stop-start)
            break    
def readInputs(args):
    inputCity = args[1]
    endCity = args[2]
    routingOption = args[3]
    routingAlgorithm = args[4]
    if data_dict.get(inputCity) == None :
        print("Enter a valid start city!!")
    if data_dict.get(endCity) == None:
        print("Enter a valid end city!!")    
    if not(routingAlgorithm == 'bfs' or  routingAlgorithm == 'dfs' or routingAlgorithm == 'astar' or routingAlgorithm == 'ids'):
        print("Please enter a valid routing algorithm")
    if not(routingOption == 'distance' or routingOption == 'time' or routingOption == 'segments' or routingOption == 'scenic'):
        print("Please enter a valid routing option") 
        
readInputs(sys.argv)               
output = []
finalPath=''
output = results.get(endCity)
distance, time =0,0
distance = calculateSumOfPath(output, distance)
time = calculateTotalTime(output, time)
#print("SUM IS", distance, time) 

for i in range (0,len(output)):
    startCity = output[i]
    nextCity = output[i+1]
    finalPath+=startCity[0] + " "
    print("Travel from",startCity[0],"to",nextCity[0],"for",nextCity[1],"miles","in",round(float(nextCity[1])/float(nextCity[2]),4),"hours")
    if(i==len(output)-2):
        finalPath+= nextCity[0]
        break
print(str(distance) + " " + str(round(time,4))+" "+ finalPath)    