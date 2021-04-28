from copy import deepcopy
from random import choice
from time import time


class Backtracking:
    def __init__(self,size):
        self.d=size #size of the board size x size
        self.solution = list()
        self.domains=self.initialDomains(size)
        self.queens=list()
        self.isGoal=False
        self.stackDomains=list()
        self.stackVisits=list()
        self.runningTime=0
        self.expandedNodes = 0
        self.steps=0
        self.visited=self.initialVisits(size)


    def start(self):
        start = time() 
        col=0 
        count=0 
        self.stackDomains.append(self.domains)#add the initial domains to the domain stack
        self.stackVisits.append(self.visited)#add the initial visteds to the visited stack
        while not self.isGoal:#while we are not at the goal
            if col ==self.d:#if we are up to the last col
                self.isGoal=True#we are finished
                break#end the program
            if not self.isDanger(): #if we are not in danger 
                ypos = choice(self.stackDomains[len(self.stackDomains)-1][col])#gets next col value
                temp = deepcopy(self.domains)#make a deepcopy of the domain
                newD = self.updateDomains(ypos, col,temp)#update the domain using the new value
                self.stackDomains.append(newD)#add the new domain to the stack
                self.expandedNodes+=1 #increment our expanded nodes
                tempvisited = deepcopy(self.visited)#make a deepcopy of the visited 
                newVisited = self.updatevisits(ypos,col,tempvisited)#get new visited 
                self.stackVisits.append(newVisited)#add newvisited to the stack
                col+=1#increment our columns
                count+=1#increment out count
            else:#if we are in danger
                self.stackDomains.pop() #pop the domain stack
                popUp=self.stackVisits.pop()#get the visited off the stack as well
                col-=1#decrement the col
                self.updateVisits(popUp,col) #update our visited
                index=len(self.stackVisits)-1#set index 
                checkVisit=self.allVisited(col,self.stackVisits[index],self.stackDomains[len(self.stackDomains) -1])#check if we have visited all our domain values
                checkLength=len(self.stackDomains[len(self.stackDomains) -1][col])<=1#checks if the length of the domain for this col is <=1
                while checkLength or checkVisit: 
                    col-=1#decrement col #moving backwards
                    self.stackDomains.pop() #pop of the domain stack
                    popDown=self.stackVisits.pop() #pop of the visited
                    self.updateVisits(popDown, col) #update our visits
                    index = len(self.stackVisits) - 1 #update our index
                    checkVisit = self.allVisited(col, self.stackVisits[index],self.stackDomains[len(self.stackDomains) - 1])#check visits again
                    checkLength = len(self.stackDomains[len(self.stackDomains) - 1][col]) <= 1 #and check the length
                self.domains = self.stackDomains[len(self.stackDomains) -1]#add domains to the stack
                self.visited=self.stackVisits[len(self.stackVisits) -1]#add visits to the stack
                yneg = self.choice(col)#choice next value
                dtemp=deepcopy(self.domains) #make deep copy of the current domain
                newD = self.updateDomains(yneg, col,dtemp) #get new domain
                self.stackDomains.append(newD)#add domain to the stack
                visitsTemp=deepcopy(self.visited) #get new visit
                newvisits = self.updatevisits(yneg, col,visitsTemp) #update the visits
                self.stackVisits.append(newvisits) #add visits the stack
                col+=1 #increment col
                count+=1 #increment count
        end = time() #end of while loop
        self.runningTime=end-start #get our running time
        self.steps=count #get our steps
        for k,v in self.domains.items():
            self.solution.append(v[0])

    #gets initial domain values for each
    def initialDomains(self, size):
        temp=dict()
        for i in range(size):
            temp[i]=list(range(size)) #initially every queen has possible values equal to the size of the board
        return temp
        
    #updates our domains after a new assignment
    def updateDomains(self, ival, col, temp1):
        temp1[col]=[ival] #set the domain of our current column to the value we have selected
        for i in range(col+1,self.d): #for the range one column over to the end of the board
            d = deepcopy(temp1[i]) #make a deep copy of temp1 at the current index
            for j in d: #for each value in the deepcopy at the given index
                if j == ival: 
                    temp1[i].remove(j) #remove j from the domain of index i(i is just a column)
                if abs(j-ival) == abs(col-i):
                    temp1[i].remove(j) #removes if there is a match
        self.domains=temp1 #set our domain to temp1
        return temp1
        
    #checks if we have run out of domain values for a given column
    def isDanger(self):
        for i in range(len(self.domains)):
            if len(self.domains[i]) == 0:
                return True
        return False
        
    #prints our report   
    def report(self):
        print("BackTracking Solution")
        print("Running Time : ",self.runningTime,"s")
        print("Number of steps : ",self.steps)
        print("Number of Expanded Nodes : ",self.expandedNodes)
        print("The Solution >> ",self.solution)
        print("The Final State\n")
        self.constructBoard()
        print("= = = = = = = = = = = = = = = = = = = =")
        
    def reportNoBoard(self):
        print("BackTracking Solution")
        print("Running Time : ",self.runningTime,"s")
        print("Number of steps : ",self.steps)
        print("Number of Expanded Nodes : ",self.expandedNodes)
        print("The Solution >> ",self.solution)
        #print("The Final State\n")
        print("= = = = = = = = = = = = = = = = = = = =")
    
    #constructs the board 0->solutions length        
    def constructBoard(self):
        for i in range(0,len(self.solution)):
            temp = ['#'] * self.d
            index = self.solution.index(i)
            temp[index]='Q'
            for j in range(len(temp)):
                if temp[j] == 'Q':
                    print(temp[j], end = " ")
                else:
                    print(temp[j], end=" ")
            print()

    #fills up our initial_vists sets all of them equal to false
    def initialVisits(self, size):
        temp = dict()
        for i in range(size):
            temp[i] = [False] * size
        return temp

    def updatevisits(self, ypos, col, tempvisited):
        tempvisited[col][ypos]=True
        self.visited=tempvisited
        return tempvisited
    
    #checks if we have visited all domain values for a given column                
    def allVisited(self, col, o, o1):
        count=0
        for i in o1[col]:
            if o[col][i]:
                count+=1
        if count == len(o1[col]):
            return True
        return False

    #gets previous visiteds out of the stack 
    def updateVisits(self, popUp, col):
        self.stackVisits[len(self.stackVisits)-1][col]=popUp[col]
        
    #chooses the next domain value to be expanded
    def choice(self, col):
        for i in self.domains[col]:
            if self.visited[col][i]==False:
                return i
                
    #checks if one queen threatens another queen
    #def isThreaten(self, i, param, j, param1):
    #    if i == j:
    #        return True
    #    if param == param1:
    #        return True
    #    if abs(i - j) == abs(param1 - param):
    #        return True
    #    return False
        
       
       
       
     #----------------------------------------  --------------------------------------------  -------------------------------------  ----------------------------------------    
        #for forward checking I want it to choose the next column to work on based off of the one with the fewest remaining domain values
        #so I think I will need to choose my next column based off of len[domain[i]] and the one with the smallest length is next
        #because in my code much is done by just incrementing the col variable I think I will have to do a good amount of work to get this to work the way I want it to  
        
class Forwardchecking (Backtracking):
    def __init__(self,size):
        self.stackColumn = list() #add in a stack for the col so if we have to track back we can keep track of which col we were at last
        self.colsHasNoVal = self.initialValues(size) #keep track of which columns have a val
        Backtracking.__init__(self,size) #get the properties from Backtracking class


    #will have to update it to choose the next col to work on based off of the least remaing domain values
    #as well as make sure that every column up until my problem size has a value in it to be sure we do not skip one
    #will have to choose next col using getNextColumn
    #will have to keep a stack of the columns I am working on
    #will have to keep track of the cols that have a value
    #use is goal to keep track of if all cols have a value
    def start(self):
            start = time()
            col = 0
            count = 0
            self.stackDomains.append(self.domains)
            self.stackVisits.append(self.visited)
            while not self.isGoal:
                    if not self.colsHasNoVal:
                            self.isGoal = True
                            break
                    if not self.isDanger():
                            ival = choice(self.stackDomains[len(self.stackDomains)-1][col])
                            temp = deepcopy(self.domains)
                            newD = self.updateDomains(ival, col, temp)
                            self.stackDomains.append(newD)
                            self.expandedNodes += 1
                            tempVisited = deepcopy(self.visited)
                            newVisited = self.updatevisits(ival, col, tempVisited)
                            self.stackVisits.append(newVisited)
                            self.stackColumn.append(col)
                            #might need if for below
                            col = self.getNextColumn()
                            count += 1
                    else:
                            self.stackDomains.pop()
                            popUp = self.stackVisits.pop()
                            col = self.stackColumn.pop()
                            #if col not in self.colsHasNoVal: 
                            self.colsHasNoVal.append(col)
                            self.updateVisits(popUp, col)
                            index = len(self.stackVisits) - 1
                            checkVisits = self.allVisited(col, self.stackVisits[index], self.stackDomains[len(self.stackDomains)-1])
                            checkLength = len(self.stackDomains[len(self.stackDomains)-1][col])<= 1
                            while checkLength or checkVisits:
                                    #nexst two lines had if statments
                                    #if col != 0: 
                                    col = self.stackColumn.pop()
                                    #if col not in self.colsHasNoVal: 
                                    self.colsHasNoVal.append(col)
                                    self.stackDomains.pop()
                                    popDown = self.stackVisits.pop()
                                    self.updateVisits(popDown, col)
                                    index = len(self.stackVisits) - 1
                                    checkVisits = self.allVisited(col, self.stackVisits[index], self.stackDomains[len(self.stackDomains)-1])
                                    checkLength = len(self.stackDomains[len(self.stackDomains)-1][col]) <= 1
                            self.domains = self.stackDomains[len(self.stackDomains)-1]
                            self.visited = self.stackVisits[len(self.stackVisits) - 1]
                            yneg = self.choice(col)
                            self.stackColumn.append(col)
                            dtemp = deepcopy(self.domains)
                            newD = self.updateDomains(yneg, col, dtemp)
                            self.stackDomains.append(newD)
                            visitsTemp = deepcopy(self.visited)
                            newvisits = self.updatevisits(yneg, col, visitsTemp)
                            self.stackVisits.append(newvisits)
                            col = self.getNextColumn()
                            count += 1
            end = time()
            self.runningTime = end-start
            self.steps = count
            for k,v in self.domains.items():
                    self.solution.append(v[0])
                    
    def updateDomains(self, ival, col, temp1):
            temp1[col] = [ival]
            #might need if statment
            self.colsHasNoVal.remove(col)
            for i in self.colsHasNoVal:
                    d = deepcopy(temp1[i])
                    for j in d:
                            if j == ival:
                                    temp1[i].remove(j)
                            else: 
                                    if abs(j-ival) == abs(col-i):
                                            temp1[i].remove(j)
            self.domains = temp1
            return temp1          
                    
                    
#I might have to update my domains here or like go back I think its go back
#    def checkifNeedsVal(self):
#            for k in self.domains:
#                    if (len(self.domains[k]) > 1 or len(self.domains[k])==None) and k not in self.colsHasNoVal:
#                            self.colsHasNoVal.append(k) 
    
    #gets us our next column based off the one with the fewest domain values remaing
    #I guess I will create another array for columns with no values only
    #Gonna rework this one so that it uses the min function
    #This function is sometimes not returning the min of 
    def getNextColumn(self):
        if self.colsHasNoVal:
                nextCol = self.colsHasNoVal[0]
                comparar = len(self.domains[nextCol])
                for i in range (1,len(self.colsHasNoVal)-1): #goes over the correct range
                        if len(self.domains[self.colsHasNoVal[i]]) < comparar:
                                nextCol = self.colsHasNoVal[i]
                                comparar = len(self.domains[nextCol])
                return nextCol
        
    def initialValues(self, size):
        temp = list()
        for i in range(size):
            temp.append(i)
        return temp
        
    def report(self):
        print("With Forward Checking")
        print("Running Time : ",self.runningTime,"s")
        print("Number of steps : ",self.steps)
        print("Number of Expanded Nodes : ",self.expandedNodes)
        print("The Solution >> ",self.solution)
        print("The Final State\n")
        self.constructBoard()
        print("= = = = = = = = = = = = = = = = = = = =")
                    
    def reportNoBoard(self):
        print("With Forward Checking")
        print("Running Time : ",self.runningTime,"s")
        print("Number of steps : ",self.steps)
        print("Number of Expanded Nodes : ",self.expandedNodes)
        print("The Solution >> ",self.solution)
        #print("The Final State\n")
        print("= = = = = = = = = = = = = = = = = = = =")



def main():
    print('.: N-Queens Problem :.')
    size = int(input('Please enter the size of board: '))
    n_queens = Backtracking(size)
    n_queens.start()
    n_queens.report()
    forward_queens = Forwardchecking(size)
    forward_queens.start()
    forward_queens.report()


if __name__ == '__main__':
    main()