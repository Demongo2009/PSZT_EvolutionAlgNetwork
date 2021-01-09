# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import xml.etree.ElementTree as ET
import xml.dom.minidom
import numpy as np
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def func(y):
    return sum([ x**2 for x in y ])

class Link:

    def __init__(self, name, numberOfFlows):
        self.name = name
        self.numberOfFlows = numberOfFlows


def evaluationFunction(specimen):
    numberOfSystems = 0

    listOfLinks = []

    # TODO: finish
    for i,flowsForDemand in enumerate(specimen):
        print(i)




    return numberOfSystems



class DE:

    def __init__(self, demands, populationSize = 100, crossoverProbability = 0.9,
                 differentialWeight = 0.8, penaltyFactor = 0.1, maxfes = 2000, evaluationFunction = staticmethod(func)):
        self.populationSize = populationSize
        self.crossoverProbability = crossoverProbability
        self.differentialWeight = differentialWeight
        self.penaltyFactor = penaltyFactor
        self.maxfes = maxfes
        self.evaluationFunction = evaluationFunction
        self.demands = demands

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
        value = sumOfFlows - self.demands[indexOfDemand].demandValue

        if -sumOfFlows > value:
            value = -sumOfFlows

        # TODO: finnish
        for path in self.demands[indexOfDemand].admissiblePaths:
            print(path)


        return value


    def penalty(self, specimen):
        arr = np.array([self.penaltyFactor * max(0, self.constraintViolation(i,x)) for i,x in enumerate(specimen)])
        penaltyValue = arr.sum()
        return penaltyValue


    def evaluate(self, trialVector, specimen, population):
        x_val = self.evaluationFunction(specimen)
        y_val = self.evaluationFunction(trialVector)

        x_val += self.penalty(specimen)
        y_val += self.penalty(trialVector)
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
            generationNum+=1
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
        print("DemandValue: " + self.demandValue)
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
                              d.getElementsByTagName('demandValue')[0].firstChild.data,
                              pathList
                              ))
    return demands

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    doc = xml.dom.minidom.parse('data.xml')

    demands = getDemandsFromDoc(doc)

    for d in demands:
        d.print()

    global minValue
    minValue = 0
    global maxValue
    maxValue = max([ x.demandValue for x in demands ])
    global numberOfDemands
    numberOfDemands = len(demands)
    global maxPathNumber
    maxPathNumber = 7


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
