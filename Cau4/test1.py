import numpy
import random
class node:
    weight=[]
    soConnect=1
    function = ""
    temp=0
    result=0
    def __init__(self, soConnect, function):
        self.weight=[]
        self.soConnect = soConnect
        self.function = function
        for i in range(soConnect):
            self.weight.append(random.uniform(-1,1))
    def toi(self, input):
        self.result = []
        self.temp = 0
        for i in range(self.soConnect):
            self.temp += self.weight[i]*input[i]
        if self.function == "tuyenTinh":
            self.result = self.temp
            return self.result
        elif self.function == "sigma":
            self.result = 1/(1+numpy.e**(-self.temp))
            return self.result
        elif self.function == "one":
            self.result = 1
            return 1
        else:
            return "error"


class layer:
    soNode = 0
    soInput = 0
    result = []
    mnode=[]
    def __init__(self, soNode, soInput, function,type):
        self.mnode = []
        self.soNode = soNode
        self.soInput = soInput
        for i in range(soNode):
            if (type == "input" or type == "hidder") and i == 0:
                self.mnode.append(node(0,'one'))
            else:
                self.mnode.append(node(soInput, function))
    def toi(self,input):
        self.result = []
        for i in range(self.soNode):
            self.result.append(self.mnode[i].toi(input))
        return self.result
    def setOut(self, input):
        self.result = input
        return self.result

class neuralNetwork:
    mlayer = []
    soLayer = 0
    result = []
    def __init__(self, soNode, soLayer):
        self.soLayer = soLayer
        self.mlayer = []
        self.result = []
        for i in range(soLayer):
            if i == 0:
                self.mlayer.append(layer(soNode[i],0,'tuyenTinh','input'))
            elif i == 1:
                self.mlayer.append(layer(soNode[i],soNode[i-1],'sigma','hidder'))
            elif i == soLayer-1:
                self.mlayer.append(layer(soNode[i],soNode[i-1],'tuyenTinh','output'))
            else:
                self.mlayer.append(layer(soNode[i],soNode[i-1],'tuyenTinh','hidder'))
    def predict(self, input):
        self.result = []
        mainResult = []
        for layerCurrent in range(self.soLayer):
            if layerCurrent == 0:
                self.result.append(self.mlayer[0].setOut(input))
            else:
                self.result.append(self.mlayer[layerCurrent].toi(self.result[layerCurrent-1]))
        self.mainResult = self.result[self.soLayer-1]
        return self.mainResult
    def updateWeight(self, input):
        for layerCurrent in range(self.soLayer):
            for i in range(self.mlayer[layerCurrent].soNode):
                self.mlayer[layerCurrent].mnode[i].weight = []
                self.mlayer[layerCurrent].mnode[i].weight = input.mlayer[layerCurrent].mnode[i].weight
    def radientDes(self, heso, disscurt, reward, qMaxNext, input):
        diffLoss = 0
        action = numpy.argmax(self.predict(input))
        print(action)
        qCurrent = self.predict(input)[action]
        for layerCurrent in range(self.soLayer):
            if layerCurrent >= 1:
                for i in range(self.mlayer[layerCurrent].soNode):
                    for j in range(self.mlayer[layerCurrent].mnode[i].soConnect):
                        temp = self.mlayer[layerCurrent].mnode[i].weight[j]
                        tempPredict = (reward + disscurt*qMaxNext - self.predict(input)[action])**2
                        self.mlayer[layerCurrent].mnode[i].weight[j] + 0.1
                        diffLoss = ((reward + disscurt*qMaxNext - self.predict(input)[action])**2-tempPredict)/0.1
                        print("diff: ",diffLoss)
                        #x=input()
                        self.mlayer[layerCurrent].mnode[i].weight[j] = temp - heso*1000*diffLoss
        lossFunction = (reward + disscurt*qMaxNext - self.predict(input)[action])**2
        return lossFunction   
taget = neuralNetwork([5,5,5,4], 4)
taget1 = neuralNetwork([5,5,5,4], 4)
while(1):
    loss = taget1.radientDes(1, 0.8, -1, 0.5, [1,1,2,1,-1])
    print(loss)             
'''  
input = [1,2,-3,-1]
input.insert(0, 1)
taget = neuralNetwork([5,5,5,4], 4)    
taget1 = neuralNetwork([5,5,5,4], 4)  

taget.predict(input)
taget1.predict(input)
print(taget.mainResult)
print(taget1.mainResult)

print("===========================")
taget1.updateWeight(taget)
taget.predict(input)
taget1.predict(input)
print(taget.mainResult)
print(taget1.mainResult)

print("===========================")
taget1.updateWeight(taget)
taget.predict(input)
taget1.predict(input)
print(taget.mainResult)
print(taget1.mainResult)
'''
'''
input = [1,2,-2,0]
input.insert(0, 1)
taget = neuralNetwork([5,5,5,4], 4)
current = neuralNetwork([5,5,5,4], 4)
taget.predict(input)
current.predict(input)
print("input", input)
#print(taget.mlayer[1].mnode[1].weight)
#print(current.mlayer[1].mnode[1].weight)
#print("lan 1: ",taget.mlayer[0].result)
#print("lan 1: ",taget.mlayer[1].result)
#print("lan 1: ",taget.mlayer[2].result)
#print("lan 1: ",taget.mlayer[3].result)
#print(taget)
#taget.predict(input)
#print("lan 2: ",taget.mlayer[0].result)
#print("lan 2: ",taget.mlayer[1].result)
#print("lan 2: ",taget.mlayer[2].result)
#print("lan 2: ",taget.mlayer[3].result)
#print("taget: ",taget.result)
#print("current: ",current.result)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("taget: ",taget.mlayer[i].mnode[j].weight)
        print("current: ",current.mlayer[i].mnode[j].weight)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
for i in range(4):
    print("taget: ",taget.mlayer[i].result)
    print("currnet: ",current.mlayer[i].result)
print("===========Sau khi update=========")
print("input", input)
taget.updateWeight(current)
taget.predict(input)
current.predict(input)
#print(taget.mlayer[1].mnode[1].weight)
#print(current.mlayer[1].mnode[1].weight)
#print("taget: ",taget.result)
#print("current: ",current.result)

for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("taget: ",taget.mlayer[i].mnode[j].weight)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("current: ",current.mlayer[i].mnode[j].weight)

for i in range(4):
    print("taget: ",taget.mlayer[i].result)
    print("currnet: ",current.mlayer[i].result)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("taget: ",taget.mlayer[i].mnode[j].weight)
        print("current: ",current.mlayer[i].mnode[j].weight)
print ("==============again===========")
print("input", input)
taget.updateWeight(current)
taget.predict(input)
current.predict(input)
#print(taget.mlayer[1].mnode[1].weight)
#print(current.mlayer[1].mnode[1].weight)
#print("taget: ",taget.result)
#print("current: ",current.result)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("taget: ",taget.mlayer[i].mnode[j].weight)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("current: ",current.mlayer[i].mnode[j].weight)
for i in range(4):
    print("taget: ",taget.mlayer[i].result)
    print("currnet: ",current.mlayer[i].result)
for i in range(4):
    for j in range(taget.mlayer[i].soNode):
        print("taget: ",taget.mlayer[i].mnode[j].weight)
        print("current: ",current.mlayer[i].mnode[j].weight)
'''