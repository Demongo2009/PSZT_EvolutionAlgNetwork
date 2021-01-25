# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np
import random
import math
import copy

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

    def __init__(self, demands, populationSize = 100, crossoverProbability = 0.7,
                 differentialWeight = 0.2, penaltyFactor = 100, maxGeneration = 2000,
                 penaltyForBadFlow = 100, modularity = 500, aggregateFlows = True):
        self.populationSize = populationSize
        self.crossoverProbability = crossoverProbability
        self.differentialWeight = differentialWeight
        self.penaltyFactor = penaltyFactor
        self.maxGeneration = maxGeneration
        self.demands = demands
        self.penaltyForBadFlow = penaltyForBadFlow
        self.aggregateFlows = aggregateFlows
        self.modularity = modularity
        self.maxPathNumber = 7
        self.minValue = 0
        self.maxValue = max([x.demandValue for x in demands])
        self.numberOfDemands = len(demands)


    def evaluationFunction(self, specimen):
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
                            break

                    if linkExists:
                        listOfLinks[linkIndex].flowLoad += flow
                    else:
                        listOfLinks.append(Link(link, flow))

        # for every loaded link add system depending on modularity
        for link in listOfLinks:
            numberOfSystems += math.ceil(link.flowLoad / self.modularity)

        return numberOfSystems




    def initialization(self):
        return np.random.randint(self.minValue, self.maxValue, (self.populationSize, self.numberOfDemands, self.maxPathNumber))


    def generate(self, population, index):
        indexSet = {index}
        individuals = [population[i] for i in random.sample(set(range(self.populationSize)) - indexSet, 3)]
        return individuals


    def mutationDE(self, individuals):
        donorVector = np.add(individuals[0],
                             self.differentialWeight * np.array(np.subtract(individuals[1], individuals[2])))

        return donorVector

    def mutation(self, specimen):
        donorVector = copy.deepcopy(specimen)

        i = random.randint(0,self.numberOfDemands-1)
        j = random.randint(0,self.maxPathNumber-1)

        indexOfFlow =0
        for index, flow in enumerate(specimen[i]):
            if flow > 0:
                indexOfFlow = index

        donorVector[i][indexOfFlow] = 0

        donorVector[i][j] = specimen[i][indexOfFlow]

        return donorVector


    def crossover(self, specimen, donorVector):
        randomI = random.sample(range(self.numberOfDemands), 1)
        trialVector = [
            donorVector[i] if random.uniform(0, 1) <= self.crossoverProbability or i == randomI else specimen[i] for i
            in range(self.numberOfDemands)]
        return np.array(trialVector)


    def constraintViolation(self, indexOfDemand, flows):
        sumOfFlows = flows.sum()
        value = int(sumOfFlows) - self.demands[indexOfDemand].demandValue

        if -sumOfFlows > value:
            value = -sumOfFlows

        return value


    def penalty(self, specimen):
        arr = np.array([self.penaltyFactor * max(0, self.constraintViolation(i,x)) for i,x in enumerate(specimen)])
        penaltyValue = arr.sum()
        return penaltyValue


    def evaluate(self, trialVector, specimen, population, index):
        x_val = self.evaluationFunction(specimen)
        y_val = self.evaluationFunction(trialVector)

        # print(x_val)
        # print(y_val)
        if y_val <= x_val:
            population[index] = trialVector




    def repair(self, specimen):
        for demand in specimen:
            for i, flow in enumerate(demand):
                if demand[i] < 0:
                    demand[i] *= -1

        if self.aggregateFlows:
            for i, demand in enumerate(specimen):
                maxIndex = 0
                max = -1
                for j, flow in enumerate(demand):
                    if flow > max:
                        maxIndex = j
                        max = flow
                    demand[j] = 0
                demand[maxIndex] = demands[i].demandValue

        else:
            for i, demand in enumerate(specimen):
                # demands[i].demandValue # suma do ktorej dazymy
                ratio = demands[i].demandValue / np.sum(demand)



                for j, flow in enumerate(demand):
                    demand[j] = round(demand[j] * ratio)






        return specimen

    def run(self):
        population = self.initialization()
        for i, specimen in enumerate(population.tolist()):
            population[i] = self.repair(specimen)
        generation = 0
        while generation < self.maxGeneration:
            for i, specimen in enumerate(population.tolist()):
                specimenIndex = i
                if self.aggregateFlows:
                    donorVector = self.mutation(specimen)
                else:
                    individuals = self.generate(population, specimenIndex)
                    donorVector = self.mutationDE(individuals)
                    donorVector = self.repair(donorVector)
                trialVector = self.crossover(specimen, donorVector)
                self.evaluate(trialVector, specimen, population, specimenIndex)
            generation+=1
            print_hi(generation)

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

    # value = 0
    # for d in demands:
    #     value += d.demandValue
    # print(value)


    DEalgorithm = DE(demands)
    population = DEalgorithm.run()

    best = population[0]
    for specimen in population:
        if DE.evaluationFunction(DEalgorithm,specimen) < DE.evaluationFunction(DEalgorithm,best):
            best = specimen

    print(best)
    print(DE.evaluationFunction(DEalgorithm,best))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
