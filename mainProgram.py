#this function finds the first process while sorting the process
from urllib import response



#from gui import total_processes

#total_processes = numOfprocess
def theLeastOne(processes):
    min_index=0
    num = len(processes) #shortened to not pass it through numofprocesses
    #we arrange according to arrival time and priority
    for i in range(1,num):
          if(processes[i]["arrival time"]<processes[min_index]["arrival time"] or
            processes[i]["arrival time"]==processes[min_index]["arrival time"] and
            (processes[i]["priority"] < processes[min_index]["priority"])):
             min_index=i
    #we swap here to get the min process to move to be the first process
    temp=processes[0]
    processes[0]= processes[min_index]
    processes[min_index]= temp
    return processes[0]["burst time"]

#sorts processes
def sortingProcesses(processes, numOfProcess):
    theLeastOne(processes) #gets the first process
   #here after i get the first process from i store it's current time ali bisawy elmoda el wslt fihel burst bta3tha 3shan ashof anhi wa7da mn elprocess el gayn a7to wraha
   #Curr time = arrival + burst
    currentTime = processes[0]["arrival time"] + processes[0]["burst time"]
 #hena ana bbd2 aqarun aho 3shan a5tar bs msh bqarun bs 3la asas
# el arrival time bs fi el war2a el b3t fiha bnrtb 3la asas eh htfhmo el goz2 da
    for i in range(1, numOfProcess):
        if currentTime > processes[i]["arrival time"] :
            for j in range(i + 1, numOfProcess):
                if (processes[j]["priority"] < processes[i]["priority"]):
                    temp=processes[j]
                    processes[j]=processes[i]
                    processes[i]=temp
                elif(processes[j]["priority"] == processes[i]["priority"]):
                    if (processes[j]["arrival time"] < processes[i]["arrival time"]):
                     temp=processes[j]
                     processes[j]=processes[i]
                     processes[i]=temp
            currentTime += processes[i]["burst time"]
        elif(currentTime== processes[i]["arrival time"]):
            for j in range(i + 1, numOfProcess):
                if (processes[j]["arrival time"] < processes[i]["arrival time"]):
                    temp=processes[j]
                    processes[j]=processes[i]
                    processes[i]=temp
                elif(processes[j]["arrival time"] == processes[i]["arrival time"]):
                    if (processes[j]["priority"] < processes[i]["priority"]):
                     temp=processes[j]
                     processes[j]=processes[i]
                     processes[i]=temp
            currentTime += processes[i]["burst time"]
        else:
            minArrivalIndex = i
            for j in range(i + 1, numOfProcess):
                if processes[j]["arrival time"] < processes[minArrivalIndex]["arrival time"]:
                    minArrivalIndex = j
                elif (processes[j]["arrival time"] == processes[minArrivalIndex]["arrival time"] and 
                      processes[j]["priority"] < processes[minArrivalIndex]["priority"]):
                    minArrivalIndex = j
            if minArrivalIndex != i:
             temp=processes[i]
             processes[i]= processes[minArrivalIndex]
             processes[minArrivalIndex]=temp

            currentTime += processes[i]["burst time"]
            #currentTime += processes[i]["arrival time"] Ghalat.
    return processes #added for integration with gui will remove probabily.

#elfunction di bst5dmha 3shan atb3 el process bta3ty b3d el sort 
def printingList(processes):
    print("\nThe processes you entered:")
    for process in processes:
        print(process["process name"],end=" ")
    print()
#elfunction di bst5dmha 3shan ad5l el data bta3ty 
def enteringData(processes,numOfProcess):
   for i in range(numOfProcess):
    nameProcess = input("Enter the name of the process: ")
    burstTime = input("Enter the burst time: ")
    if burstTime.isalpha() or int (burstTime) <0 :
      print("this is not allowed")
    else:
       burstTime = int(burstTime)
    priority = input("Enter the priority: ")
    if priority.isalpha() or int(priority) <0 :
      print("this is not allowed")
    else:
       priority = int(priority)
    arrivalTime=input("Enter the arrivaltime: ")
    if arrivalTime.isalpha() or int(arrivalTime) < 0 :
      print("this is not allowed")
    else:
       arrivalTime = int(arrivalTime)
    #hena da 3bara 3n dictionary gwa el list bta3ty 3shan yqon lkol process 7agtha m3 b3d
    processes.append({"process name": nameProcess, "burst time": burstTime, "priority": priority,"arrival time":arrivalTime})
#di function bt7sb el completion time el bs5dmo fi turnround time 'da qanon shofoh''turn round=completion -arrival'
def calcCompletionTime(processes, numOfProcess):
    #s: move condition in loop, make sure only the first operation starts when it arrives
    completionTime = []
    for i in range(numOfProcess):
        if i == 0:
            start = processes[i]["arrival time"]
        #other operations are calculated based on the completion of the previous one or arrival time
        else:
            if completionTime[i-1] < processes[i]['arrival time']:
                start = processes[i]["arrival time"]
            else:
                start = completionTime[i-1]
                #start = processes[i - 1]["arrival time"]
                #the process starts either when it arrives or when the other finishes
                #so we use previous process completion time otherwise error fe el nateg
        completionTime.append(start + processes[i]["burst time"])
    return completionTime

'''def sumOfData(processes, numOfProcess):
    s = 0
    for i in range(numOfProcess):
        s += processes[i]["burst time"]
    return s'''
#di bst5dmha 3shan a3rd bs el turn round w el respons w waiting bta3 kol process
'''def displaying(time):
    lens=len(time)
    for t in range(lens):
        print(time[t])'''
#b7sb el turn round time ktbt el qanon fo2
def calcTurnroundTime(processes,completionTime,turnRound,numOfProcess):
  s=0
  for i in range(numOfProcess):
      s+= (completionTime[i]-processes[i]["arrival time"])#processes[process]["arrival"] di m3naha ano hiwsl llarival time bs
      turnRound.append(s)
      s=0
  return turnRound
#hena b3ml calc llwaiting time fna mbasia turn round time fi el function 3shan qanon ='turn roun -burst
def calcwaitingTime(processes,waiting,turnroundTime, numOfProcess):
  for i in range(numOfProcess):
    wt = turnroundTime[i] - processes[i]["burst time"]
    waiting.append(wt)
  return waiting

#di func bt7sb el start time 3shan a7sb el response time
def calcStartTime(startTime,processes, numOfProcess):
    s = processes[0]["arrival time"]
    startTime.append(s)

    for i in range(1, numOfProcess):
        #process starts by the end of prev, given that it has arrived
        if s+processes[i-1]["burst time"] < processes[i]["arrival time"]:
            s = processes[i]["arrival time"]
        else:
            s = s+ processes[i-1]["burst time"]
        startTime.append(s)
    return startTime
#di bt7sb el response b2a 
def calcResponseTime(startTime, processes, response, numOfProcess):
  s=0
  n = min(len(startTime), len(processes)) #kept crashing
  for i in range(n):
      s+= (startTime[i]-processes[i]["arrival time"])
      response.append(s)
      s=0
  return response
#di l7sab ay avg time 3mtn 3shan msh hn3od n3ml lkol wa7da msh fadyeen a7na hehe sorry...h7trm nfsy 5lass
def avgTime(Time):
    if Time == 0: #division by zero exception handling
        raise Exception("Division by zero is not allowed")
    s=0
    lens=len(Time)
    for i in range(lens):
        s+=Time[i]
    return s/lens

def run_PScheduler(processes, numOfProcess):
    #returns process calculation in the form of a dictionary
    #dictionaries in py are key:value pairs where u can retrieve the val easily via key

    turnaround = []
    waiting = []
    startTime = []
    response = []
    completionTime = []

    processes = sortingProcesses(processes,numOfProcess)
    compTime = calcCompletionTime(processes, numOfProcess)
    tat = calcTurnroundTime(processes,compTime,[], numOfProcess)
    wt = calcwaitingTime(processes,[],tat,numOfProcess)
    startTime = calcStartTime([],processes, numOfProcess)
    respT = calcResponseTime(startTime,processes,[], numOfProcess)
    return{
        #"processes": f'P{i + 1}',
        "compTime": compTime,
        "tat": tat,
        "wt": wt,
        "startTime": startTime,
        "respT": respT,
        "avg turnaround": avgTime(tat),
        "avg waiting": avgTime(wt),
        "avg response": avgTime(respT)
    }

#Noor's logic code for standalone testing seperate from GUI
'''Priority_Scheduling = []
completionTime=[]
turnroundTime=[]
waitingTime=[]
startTime=[]
responseTime=[]

numOfProcess= int(input("Enter the number of processes:"))
enteringData(Priority_Scheduling,numOfProcess)
printingList(Priority_Scheduling)
theLeastOne(Priority_Scheduling)
sortingProcesses(Priority_Scheduling, numOfProcess)
print("THE LIST AFTER SORTING IS:\n")
printingList(Priority_Scheduling)
calcCompletionTime(Priority_Scheduling, numOfProcess)
print("Processes:", len(Priority_Scheduling))
print("Completion Time:", len(completionTime))
print("THE TURNROUND TIME OF EACH PROCESS:")
calcTurnroundTime(Priority_Scheduling,completionTime, turnroundTime, numOfProcess)
displaying(turnroundTime)
print("THE WAITING TIME OF EACH PROCESS:")
calcwaitingTime(Priority_Scheduling,waitingTime,turnroundTime, numOfProcess)
displaying(waitingTime)
calcStartTime(startTime,Priority_Scheduling, numOfProcess)
calcResponseTime(startTime,Priority_Scheduling,responseTime, numOfProcess)
print("THE RESPONSE TIME OF EACH PROCESS\n")
displaying(responseTime)
print("THE AVERAGE OF RESPONSE TIME IS:",avgTime(responseTime))
print("THE AVERAGE OF WAITING TIME IS:",avgTime(waitingTime))
print("THE AVERAGE OF TURNROUND TIME IS:",avgTime(turnroundTime))'''



