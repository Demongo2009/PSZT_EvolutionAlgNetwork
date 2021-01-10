# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np
import random
import math

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def func(y):
    return sum([ x**2 for x in y ])

class Link:

    def __init__(self, name, flowLoad):
        self.name = name
        self.flowLoad = flowLoad





class DE:

    def __init__(self, demands, populationSize = 100, crossoverProbability = 0.9,
                 differentialWeight = 0.8, penaltyFactor = 100, maxfes = 200,
                 penaltyForBadFlow = 100, modularity = 1):
        self.populationSize = populationSize
        self.crossoverProbability = crossoverProbability
        self.differentialWeight = differentialWeight
        self.penaltyFactor = penaltyFactor
        self.maxfes = maxfes
        self.evaluationFunction = self.evaluationFunction
        self.demands = demands
        self.penaltyForBadFlow = penaltyForBadFlow
        self.modularity = modularity

    @staticmethod
    def evaluationFunction(specimen, modularity):
        numberOfSystems = 0

        listOfLinks = []

        # add all loads on links to list
        for i, flowsForDemand in enumerate(specimen):
            for j, flow in enumerate(flowsForDemand):


                if flow <= 0:
                    continue


                correspondingPath = demands[i].admissiblePaths[j]
                for link in correspondingPath:
                    linkExists = False
                    linkIndex = 0
                    for index, l in enumerate(listOfLinks):
                        if l.name == link:
                            linkExists = True
                            linkIndex = index

                    if linkExists:
                        listOfLinks[linkIndex].flowLoad += flow

                    listOfLinks.append(Link(link, flow))

        # for every loaded link add system depending on modularity
        for link in listOfLinks:
            numberOfSystems += math.ceil(link.flowLoad / modularity)

        return numberOfSystems




    def initialization(self):
        return np.random.randint(minValue, maxValue, (self.populationSize, numberOfDemands, maxPathNumber))


    def generate(self, population, index):
        indexSet = {index}
        individuals = [population[i] for i in random.sample(set(range(self.populationSize)) - indexSet, 3)]
        return individuals


    def mutation(self, individuals):
        donorVector = np.add(individuals[0],
                             self.differentialWeight * np.array(np.subtract(individuals[1], individuals[2])))
        return donorVector


    def crossover(self, specimen, donorVector):
        randomI = random.sample(range(numberOfDemands), 1)
        trialVector = [
            donorVector[i] if random.uniform(0, 1) <= self.crossoverProbability or i == randomI else specimen[i] for i
            in range(numberOfDemands)]
        return trialVector


    def constraintViolation(self, indexOfDemand, flows):
        sumOfFlows = flows.sum()
        value = int(sumOfFlows) - self.demands[indexOfDemand].demandValue

        if -sumOfFlows > value:
            value = -sumOfFlows

        # if sumOfFlows != self.demands[indexOfDemand].demandValue:
        #     value = self.penaltyForBadFlow

        # numberOfPaths = len(self.demands[indexOfDemand].admissiblePaths)
        # numberOfBadFlows = 0
        # for i,flow in enumerate(flows):
        #     if flow > 0 and i > numberOfPaths:
        #         numberOfBadFlows += 1
        #
        # value += self.penaltyForBadFlow * numberOfBadFlows
        # print(value)
        return value


    def penalty(self, specimen):
        arr = np.array([self.penaltyFactor * max(0, self.constraintViolation(i,x)) for i,x in enumerate(specimen)])
        penaltyValue = arr.sum()
        # print(penaltyValue)
        return penaltyValue


    def evaluate(self, trialVector, specimen, population):
        x_val = self.evaluationFunction(specimen, self.modularity)
        y_val = self.evaluationFunction(trialVector, self.modularity)
        print(x_val)
        print(y_val)

        x_val += self.penalty(specimen)
        y_val += self.penalty(trialVector)

        print(x_val)
        print(y_val)
        if y_val <= x_val:
            population[np.where( population == specimen )[0][0]] = trialVector


    def run(self):
        global generationNum
        population = self.initialization()
        fes = 0
        while fes < self.maxfes:
            for specimen in population:
                individuals = self.generate(population, np.where( population == specimen )[0][0])
                donorVector = self.mutation(individuals)
                trialVector = self.crossover(specimen, donorVector)
                self.evaluate(trialVector, specimen, population)
                fes+=1
                print_hi(fes)


            generationNum+=1
        generationNum = 0
        return population



class Demand:

    def __init__(self, source, target, demandValue, admissiblePaths):
        self.source = source
        self.target = target
        self.demandValue = demandValue
        self.admissiblePaths = admissiblePaths

    def print(self):
        print("Source: " + self.source)
        print("Target: " + self.target)
        print("DemandValue: " + str(self.demandValue))
        print("AdmissiblePaths: ")
        for i,path in enumerate(self.admissiblePaths):
            print(" Path"+str(i)+": ")
            for link in path:
                print("  "+link)



def getDemandsFromDoc(doc):
    demands = []
    for d in doc.getElementsByTagName("demand"):
        pathList = []
        for path in d.getElementsByTagName('admissiblePath'):
            linksOnPath = []
            for link in path.getElementsByTagName('linkId'):
                linksOnPath.append(link.firstChild.data)
            pathList.append(linksOnPath)

        demands.append(Demand(d.getElementsByTagName('source')[0].firstChild.data,
                              d.getElementsByTagName('target')[0].firstChild.data,
                              int(float(d.getElementsByTagName('demandValue')[0].firstChild.data)),
                              pathList
                              ))
    return demands

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    doc = xml.dom.minidom.parse('data.xml')

    demands = getDemandsFromDoc(doc)

    # for d in demands:
    #     d.print()

    global minValue
    minValue = 0
    global maxValue
    maxValue = max([ x.demandValue for x in demands ])
    global numberOfDemands
    numberOfDemands = len(demands)
    global maxPathNumber
    maxPathNumber = 7
    global generationNum
    generationNum = 0

    modularity = 1
    DEalgorithm = DE(demands, modularity=modularity)
    population = DEalgorithm.run()

    best = population[0]
    for specimen in population:
        if DE.evaluationFunction(specimen,modularity) < DE.evaluationFunction(best,modularity):
            best = specimen

    print(best)
    print(DE.evaluationFunction(best,modularity))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
