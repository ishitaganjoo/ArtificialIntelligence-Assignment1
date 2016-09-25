'''
Created on Sep 18, 2016

@author: Ishita
'''
from math import sin, radians, cos, sqrt, asin
import sys

def calculateDistance(lat1, long1, lat2, long2):
    #convert degrees to radians
    long1, lat1, long2, lat2 = map(radians, [long1,lat1,long2,lat2])
    lon = long2-long1
    lat = lat2-lat1
    a = sin(lat/2)**2 + cos(lat1) * cos(lat2) * sin(lon/2)**2
    c = 2* asin(sqrt(a))
    distance = 3961*c
    return distance

def calculateDistance1(lat1, long1, lat2, long2):
    diffBtwnLat = (lat2 - lat1)**2
    diffBtwnLong = (long2 - long1)**2
    return (diffBtwnLat+diffBtwnLong)**(1/2)

#read the file for longitudes and latitudes
long_lat_dict = {}
with open("C:/Users/Ishita/Documents/Elements of AI/Assignment1/city-gps.txt","r") as city_gps:
    for line in city_gps:
        data = line.split(" ")
        position = []
        position.extend([data[1],data[2]])
        long_lat_dict[data[0]] = position
#create an empty dictionary
data_dict = {}
with open("C:/Users/Ishita/Documents/Elements of AI/Assignment1/road-segments.txt","r") as road_segments: #read the file and store the data in data_dict
    for line in road_segments:
        value = []
        swap_value = []
        data = line.split(" ")
        if data[0] in data_dict:
            val = data_dict[data[0]]
            val.extend([data[1],data[2],data[3],data[4]])
        else:
            value.extend([data[1],data[2],data[3],data[4]])
            data_dict[data[0]] = value
        if data[1] in data_dict:
            val = data_dict[data[1]]
            val.extend([data[0],data[2],data[3],data[4]])
        else:
            swap_value.extend([data[0],data[2],data[3],data[4]])
            data_dict[data[1]] = swap_value 

routingOption = ''
routingAlgorithm = ''
           
def readInputs(argv):
    inputCity = argv[1]
    endCity = argv[2]
    routingOption = argv[3]
    routingAlgorithm = argv[4]

          
fringe = []
d = ''
results,heuristic = {},{}
path = []
visitedCities,addedCities = [],[]
inputCity = []
inputCity.append("Bloomington,_Indiana")
endCity = "Ann_Arbor,_Michigan"
#handles bfs and dfs
def return_distance(startCity, endCity):
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
                    old_path = results[subList[0]]
                    #compare the two distances
                    old_distance,new_dist,old_time,new_time,old_count,new_count = 0,0,0,0,0,0
                    for i in range(1,len(old_path)):
                        list_path = old_path[i]
                        old_distance= old_distance + int(list_path[1])
                        if(list_path[2] == "0" or list_path[2]==''):
                            list_path[2] = "1"
                        old_time = old_time + (float(list_path[1])/float(list_path[2]))
                        if(list_path[3]<55):
                            old_count+=1
                        #print("old_time",old_time)
                    for j in range(1,len(path)):
                        list_newpath = path[j]
                        new_dist = new_dist + int(list_newpath[1])
                        if(list_newpath[2] == "0" or list_newpath[2]==''):
                            list_newpath[2] = "1"
                        print("ishita",list_newpath[2])
                        new_time = new_time + (float(list_newpath[1])/float(list_newpath[2]))
                        if(list_newpath[3]<55):
                            new_count+=1
                        #print("new_time",new_time)
                    if old_distance<new_dist and routingOption == '':
                        path = old_path
                    if old_time<new_time and routingOption == '':
                        pass
                        #print("old time is less")   
                    if(len(old_path)<len(path)) and routingOption == '':
                        pass
                        #print("length of old and new path is:", len(old_path),len(path))  
                    if(old_count>new_count) and routingOption == '':
                        print("scenic distance")  
                else:
                    fringe.append(subList)                         
                results[subList[0]] =  path
                if subList[0] == endCity:
                    return endCity
                                    
    return None 
return_distance(inputCity,endCity)

while len(fringe)>0:        
    successor = fringe.pop(0) # BFS
    result  = return_distance(successor,endCity)
    if result == endCity:
        break

#IDS SEARCH
def startIDS(inputCity):
    depth = 1
    while depth>0:
        isGoal = IdsSearch(depth,inputCity)
        if isGoal == endCity:
            break
        else:
            depth = isGoal
            
        
def IdsSearch(depth, inputCity):
    fringe_ids = []
    visitedCities = []
    fringe_ids.append(inputCity[0])
    visitedCities.append(inputCity[0])
    results = {}
    count = depth
    for i in range(0,depth):
        startCity = fringe_ids.pop(0)
        successors = data_dict[startCity]
        for j in range(0,len(successors),4):
            succ = successors[j:j+4]
            if succ[0] not in visitedCities:
                path=[]
                if results.has_key(startCity):
                    value = results[startCity]
                    for list in value:
                        path.append(list)
                    path.append(succ)
                else:
                    path.extend([startCity,succ])
                        
                if results.has_key(succ[0]):
                    old_path = results[succ[0]]
                    #compare the two distances
                    old_distance,new_dist,old_time,new_time,old_count,new_count = 0,0,0,0,0,0
                    for i in range(1,len(old_path)):
                        list_path = old_path[i]
                        old_distance= old_distance + int(list_path[1])
                        old_time = old_time + (float(list_path[1])/float(list_path[2]))
                        if(list_path[3]<55):
                            old_count+=1
                        #print("old_time",old_time)
                    for j in range(1,len(path)):
                        list_newpath = path[j]
                        new_dist = new_dist + int(list_newpath[1])
                        new_time = new_time + (float(list_newpath[1])/float(list_newpath[2]))
                        if(list_newpath[3]<55):
                            new_count+=1
                        #print("new_time",new_time)
                    if old_distance<new_dist and routingOption == '':
                        path = old_path
                    if old_time<new_time and routingOption == '':
                        pass
                        #print("old time is less")   
                    if(len(old_path)<len(path)) and routingOption == '':
                        pass
                        #print("length of old and new path is:", len(old_path),len(path))  
                    if(old_count>new_count) and routingOption == '':
                        pass
                        #print("scenic distance")        
                elif (succ[0] not in visitedCities and succ[0] != endCity):
                    fringe_ids.append(succ[0])
                    visitedCities.append(succ[0])
                    count+=1                   
                results[succ[0]] =  path    
                if succ[0] == endCity:
                    print(path)
                    return endCity
                                       
    return count    


heuristic = {}
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
                        #print("old_time",old_time)
                    for j in range(1,len(path)):
                        list_newpath = path[j]
                        new_dist = new_dist + int(list_newpath[1])
                        if(list_newpath[2] == "0" or list_newpath[2]==''):
                            list_newpath[2] = "1"
                        print("ishita",list_newpath[2])
                        new_time = new_time + (float(list_newpath[1])/float(list_newpath[2]))
                        if(list_newpath[3]<55):
                            new_count+=1
                        #print("new_time",new_time)
                    if old_distance<new_dist and routingOption == '':
                        path = old_path
                    if old_time<new_time and routingOption == '':
                        pass
                        #print("old time is less")   
                    if(len(old_path)<len(path)) and routingOption == '':
                        pass
                        #print("length of old and new path is:", len(old_path),len(path))  
                    if(old_count>new_count) and routingOption == '':
                        print("scenic distance")  
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
                                    old_path = results[succ[0]]
                                    #compare the two distances
                                    old_distance,new_dist,old_time,new_time,old_count,new_count = 0,0,0,0,0,0
                                    for i in range(1,len(old_path)):
                                        list_path = old_path[i]
                                        old_distance= old_distance + int(list_path[1])
                                        if(list_path[2] == "0" or list_path[2]==''):
                                            list_path[2] = "1"
                                        old_time = old_time + (float(list_path[1])/float(list_path[2]))
                                        if(list_path[3]<55):
                                            old_count+=1
                                        #print("old_time",old_time)
                                    for j in range(1,len(path)):
                                        list_newpath = path[j]
                                        new_dist = new_dist + int(list_newpath[1])
                                        if(list_newpath[2] == "0" or list_newpath[2]==''):
                                            list_newpath[2] = "1"
                                        new_time = new_time + (float(list_newpath[1])/float(list_newpath[2]))
                                        if(list_newpath[3]<55):
                                            new_count+=1
                                    if old_distance<new_dist and routingOption == '':
                                        path = old_path
                                    if old_time<new_time and routingOption == '':
                                        pass 
                                    if(len(old_path)<len(path)) and routingOption == '':
                                        pass  
                                    if(old_count>new_count) and routingOption == '':
                                        print("scenic distance")  
                                else :
                                    fringe.append(succ)                         
                                results[succ[0]] =  path
                                if succ[0] == endCity:
                                    return path 
                                if long_lat_dict.get(succ[0]) is not None:
                                    buildHeuristicDict(succ, locationEndCity, path)
                                else:
                                    heuristic[succ[0]] = float(1000)                    
                                
    return None 

def buildHeuristicDict(subList,locationEndCity,path):
    locationStartCity = long_lat_dict[subList[0]]
    sum = 0
    g= calculateSumOfPath(path,sum)
    h = calculateDistance(float(locationStartCity[0]),float(locationStartCity[1]),float(locationEndCity[0]),float(locationEndCity[1]))
    heuristic[subList[0]] = g+h   
         
def calculateSumOfPath(path,sum):
    for i in range(1,len(path)):
        city = path[i]
        sum = sum + int(city[1])
    return float(sum)

#return_distance_Astar(inputCity,endCity)

#A star:
"""while len(fringe)>0:
    prev_val = 0
    for succ in fringe:
        if prev_val == 0 and heuristic.get(succ[0]) != None:
            prev_val = heuristic[succ[0]]
            successor = succ
        elif (heuristic.get(succ[0]) != None and heuristic[succ[0]]< prev_val):
            prev_val = heuristic[succ[0]]
            successor = succ
    if successor[0] == endCity:
        break                   
    fringe.remove(successor)            
    value = return_distance_Astar(successor,endCity)
    if value is not None :
        break"""
 
startIDS(inputCity)    
output = [] 
output = results.get(endCity)
print("output is" ,output) 
sum=0
sum = calculateSumOfPath(output, sum)
print("SUM IS", sum)
 