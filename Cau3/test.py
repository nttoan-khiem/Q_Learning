#import libary
import GameQL
import numpy
import matplotlib
import matplotlib.pyplot as libPlot
matplotlib.use('AGG')
#init evironment
e = GameQL.UFO([200,200],[0,0],[0,0])
#init const Q_learning
c_anpha = 0.1
c_gramma = 0.9
#init mylibary
#init anlysis agent
showCycle = 100
listReward = []
lanHocShow = {'lanHoc': [], 'trungBinh': [], 'max': [], 'min': []}
#Init variable enviroment

def anhXa(input):           #ánh xạ state póition and speed into integer
    result = [0,0,0,0]
    xAxis = e.show_xAxis()
    yAxis = e.show_yAxis()
    speedX = e.show_speedX()
    speedY = e.show_speedY()
    offsetPosition = [(xAxis[1]-xAxis[0])/10,(yAxis[1]-yAxis[0])/10]
    offsetSpeed = [(speedX[1]-speedX[0])/10,(speedY[1]-speedY[0])/20]
    result[0] = int((input[0]-xAxis[0])/offsetPosition[0])
    result[1] = int((input[1]-yAxis[0])/offsetPosition[1])
    result[2] = int((input[2]-speedX[0])/offsetSpeed[0])
    result[3] = int((input[3]-speedY[0])/offsetSpeed[1])
    return result
#end mtlibary
#init Q_learning table
qTable = numpy.random.uniform(low=0, high=0.5, size=([11,11,11,21]+[5])) #400 trang thai theo truc x, 514 trang thai vi tri truc y,
#qTable = numpy.load('testt.npy')
#29 trang thai toc do theo truc x, 35 trang thai toc do theo truc y, 5 hanh dong cho moi trang thai
#end init Q_learning table
for lanHoc in range(5000000):
    realCurrentState = e.reset()
    currentStateAnhXa = anhXa(realCurrentState)
    end = 0
    render = 0
    success = 0
    totol = 0
    listAction = []
    if lanHoc % 10000 == 0:
        render = 1
    while not end:
        action = numpy.argmax(qTable[currentStateAnhXa[0],currentStateAnhXa[1],currentStateAnhXa[2],currentStateAnhXa[3]])
        listAction.append(action)
        realNextState, end, rewar, fuel, success = e.doAction(action=action)
        totol += rewar
        if render:
            e.render(action)
        nextStateAnhXa = anhXa(realNextState)
        #print("realState: ",realNextState)
        #print("nextState: ",nextStateAnhXa)
        qStateOld = qTable[currentStateAnhXa[0],currentStateAnhXa[1],currentStateAnhXa[2],currentStateAnhXa[3],action]
        #print(nextStateAnhXa)
        maxQnextState = numpy.max(qTable[nextStateAnhXa[0],nextStateAnhXa[1],nextStateAnhXa[2],nextStateAnhXa[3]])
        qTable[currentStateAnhXa[0],currentStateAnhXa[1],currentStateAnhXa[2],currentStateAnhXa[3],action] = qStateOld + c_anpha*(rewar+c_gramma*maxQnextState-qStateOld)
        #print(qTable[currentStateAnhXa[0],currentStateAnhXa[1],currentStateAnhXa[2],currentStateAnhXa[3],action])
        #print("Qtable: ",qTable[currentStateAnhXa[0],currentStateAnhXa[1],currentStateAnhXa[2],currentStateAnhXa[3]])
        currentStateAnhXa = nextStateAnhXa
        #print("state: ",currentStateAnhXa)
        #print("action: ",action)
        #print("end: ",end)
        #sprint("rewar: ",rewar)
        #print("success: ",success)
        #print("-------------------------------------------")
    e.close()
    listReward.append(totol)
    #print("Lan hoc: ",lanHoc)
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
    if success and lanHoc >= 55000:
        state = [0,0,0,0]
        print("success o lan thu: ",lanHoc)
        e.reset()
        for action in listAction:
            state, end, rewar, fuel, success = e.doAction(action)
            e.render(action)
            #print("state: ",state)
    if lanHoc % 200000 == 0:
        numpy.save('testt.npy',qTable)