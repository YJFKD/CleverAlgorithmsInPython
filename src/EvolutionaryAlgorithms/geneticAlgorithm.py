import random

def getPopulation(numOfBits, popSize):
    population = [{"bitstring":None,"fitness":None}]*popSize
    for i in range(popSize):
        temp = ''.join( '1' if random.random() < 0.5 else '0' for i in range(numOfBits))
        population[i] = {"bitstring":temp,"fitness":oneMax(temp)}
    return population

def oneMax(temp):
    return temp.count('1')

def binaryTournament(population, popSize):
    i, j = random.randrange(popSize), random.randrange(popSize)
    while j==i:
        j = random.randrange(popSize)
    return population[i] if population[i]["fitness"]>population[j]["fitness"] else population[j]

def crossOver(parent1, parent2, popCrossOver):
    if random.random()> popCrossOver:
        return parent1
    point = 1 + random.randint(1,len(parent1) - 2)
    return parent1[0:point]+parent2[point:len(parent1)]

def pointMutation(bitstring, popMutation):#popMutation
    child = ""
    bLen = len(bitstring)
    for i in range(bLen):
        bit = bitstring[i]
        child += "0" if bit=='1' else "1" if (random.random() < popMutation) else bit
    return child

def reproduce(selected, popSize, popCrossOver, popMutation):
    children = [None]*popSize
    child = {}
    for index, parent1 in enumerate(selected):
        parent2 = selected[index-1] if index%2 else selected[index+1]
        if index == len(selected)-1:
            parent2 = selected[0]
        child = {}
        child["bitstring"] = crossOver(parent1["bitstring"], parent2["bitstring"], popCrossOver)
        child["bitstring"] = pointMutation(child["bitstring"], popMutation)
        child["fitness"] = oneMax(child["bitstring"])
        children[index] = child                
    return children

def geneticAlgorithm(maxNoGenes, numOfBits, popSize, popCrossOver, popMutation):
    population =  getPopulation(numOfBits, popSize)
    best  = sorted(population, key = lambda x: x['fitness'], reverse=True)[0]
    for i in range(maxNoGenes):
        selected = [binaryTournament(population, popSize) for j in range(popSize) ]
        children = reproduce(selected, popSize, popCrossOver, popMutation)
        bestFromChildren = sorted(children, key = lambda x: x['fitness'], reverse=True)[0]
        if bestFromChildren["fitness"] >= best['fitness']:
            best  = bestFromChildren
        print " Generation ",i,
        print " Best ",best["fitness"],best["bitstring"]
        if best["fitness"] == numOfBits:
            break
    return best