import itertools

input_file = '../result/all_accidents.txt'
output_file = '../result/rules/2/all_accident_rules.txt'

class Rule:
    def __init__(self, precedent, preSupport):
        self.precedent = precedent
        self.anticedent = list()
        self.totalsupport = 0.0
        self.preSupport = preSupport
        self.confidence = 0.0

    def calculateConfidence(self):
        self.confidence = self.totalsupport / self.preSupport

    def getPre(self):
        return self.precedent

    def getConf(self):
        return self.confidence

    def addAnti(self, anti, support):
        self.anticedent = anti
        self.totalsupport = support
        self.calculateConfidence()

    def printRule(self):
        for x in self.precedent:
            output.write(x + ",")
        output.write(" -> ")
        for x in self.anticedent:
            output.write(x + ",")
        output.write(" with confidence " + str(self.confidence) + "\n")


def compare(first, second):
    if first == second:
        return True
    else:
        return False


ruleList = list()
singles = list()
pre = list()
preSupport = 0
anti = list()
antiSupport = 0
support = 0
currLine = 0


with open(input_file, 'r') as inputFile, open(output_file, 'w') as output:
    inp = inputFile.readlines()
    for line in inp:
        line = line.split('|')
        support = line.pop()
        newRule = Rule(line[0].strip(',').split(","), int(support))
        # create precident rule with the target line
        for newLine in inp:
            newLine = newLine.split('|')
            newSupport = newLine.pop()
            if line[0] in newLine[0] and line[0] != newLine[0]:
                antiRules = list(set(newLine[0].strip(',').split(',')) - set(newRule.precedent))
                newRule.addAnti(antiRules, int(newSupport))
                newRule.printRule()
