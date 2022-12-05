#program Q_learning
import gym
import numpy 
import matplotlib
import matplotlib.pyplot as libPlot
matplotlib.use('AGG')
import pandas 
import time
#init anlysis agent
showCycle = 100 
listReward = []
lanHocShow = {'lanHoc': [], 'trungBinh': [], 'max': [], 'min': []}
#Init variable enviroment
e = gym.make("MountainCar-v0")
realStateMax = e.observation_space.high         #[0.6  0.07]        max state
realStateMin = e.observation_space.low          #[-1.2  -0.07]      min state
c_anpha = 0.4
c_gramma = 0.9
#Init Q table
Q_table = numpy.random.uniform(low=0.4,high=0.6,size=([20,20]+[3]))        #matrix 20x20x3 
#Q_table = numpy.load('qTable.csv.npy')
listMax = []
maxS = -201
#my lib---------
def anhXa(realState):
    rel = [0,0]
    ofset0 = (realStateMax[0] - realStateMin[0])/20
    ofset1 = (realStateMax[1] - realStateMin[1])/20
    rel[0] = int((realState[0]-realStateMin[0])//ofset0)
    rel[1] = int((realState[1]-realStateMin[1])//ofset1)
    return rel
#end lib--------
#Q_learning------------------
for lanHoc in range(50000):
    listAction = []
    realCurrentState = e.reset()
    currentState = anhXa(realCurrentState)
    reward = 0.0
    stop = False
    totle = 0
    while not stop:
        action = numpy.argmax(Q_table[currentState[0],currentState[1]])
        listAction.append(action)
        realNextState,reward,stop,_ = e.step(action=action)
        totle += reward
        nextState = anhXa(realNextState)
        qStateOld = Q_table[currentState[0],currentState[1],action]
        maxQnextState = numpy.max(Q_table[nextState[0],nextState[1]])
        Q_table[currentState[0],currentState[1],action] = qStateOld + c_anpha*(reward+c_gramma*maxQnextState-qStateOld)
        currentState = nextState 
        #e.render(mode="human")
        #print("Trang thai: {}, test: {}, test1: {}".format(currentState,reward,stop))
    e.close()
    listReward.append(totle)
    if realNextState[0] >= 0.53:
        #print("Len dinh thanh cong tai lan hoc: ",lanHoc)
        #print("So diem la: ",totle)
        #print("-----")
        if totle >= maxS:
            maxS = totle
            listMax = listAction
        '''
        if  totle >= -180:
            e.reset()
            for ac in listAction:
                nextState,_,_,test = e.step(ac)
                e.render(mode="human")
            for i in range(5):
                e.step(0)
                e.render(mode="human")
            e.close()
        '''
    if not lanHoc % showCycle:
        trungBinh = sum(listReward)/len(listReward)
        rewardMiN = min(listReward)
        rewardMax = max(listReward)
        lanHocShow["lanHoc"].append(lanHoc)
        lanHocShow["trungBinh"].append(trungBinh)
        lanHocShow["max"].append(rewardMax)
        lanHocShow["min"].append(rewardMiN)
        listReward = []
        print("lanhoc", lanHoc)
    if not lanHoc % (showCycle*10):
        libPlot.plot(lanHocShow["lanHoc"],lanHocShow["trungBinh"],label="trungBinh")
        libPlot.plot(lanHocShow["lanHoc"],lanHocShow["max"],label="max reward")
        libPlot.plot(lanHocShow["lanHoc"],lanHocShow["min"],label="min reward")
        libPlot.legend(loc=4)  
        libPlot.savefig('plot.png')
        libPlot.close()
    if lanHoc % 2000 == 0:
        numpy.save('qTable.csv',Q_table)
        #QTB = pandas.DataFrame(Q_table)
        #QTB.to_csv("Qtb.csv")
        input('continue.')
e.reset()
for i in listMax:
    e.step(i)
    e.render(mode="human")
for t in range(10):
    e.step(0)
    e.render(mode="human")
e.close()
    
