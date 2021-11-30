import itertools

class Rule:
    def __init__(self,precedent,preSupport):
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
    
    def addAnti(self,anti,support):
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
secondLine = 0

output = open("./result/rules/all_accident_rules.txt",'w')
input = open("./result/all_accidents.txt",'r')
lines = input.readlines()
for line in reversed(lines):
    # start at last line
    line = line.split(',')
    support = line.pop()
    support = support[1:len(support)-1]
    newRule = Rule(line,int(support))
    # create precident rule with the target line
    # then create new subfile of all the lines except the target
    currLine -= 1
    secondLine = currLine
    newLines = list(lines[0:currLine])
    newLines = reversed(newLines)

    #now we have everything up to our current line in newLines
    for newLine in newLines:
        newLine = newLine.split(',')
        newSupport = newLine.pop()
        newSupport = newSupport[1:len(newSupport)-1]
        preLength = len(newRule.getPre())
        antiLength = len(newLine)
        for x in range(0,preLength):
            if ( antiLength >= preLength and compare(newLine[x],newRule.getPre()[x])):
                result = True
            else:
                result = False
                break
        if ( result ):
            antiRules = newLine
            for x in range(0,preLength):
                antiRules.pop(0)
            newRule.addAnti(antiRules,int(newSupport))
            newRule.printRule()

        secondLine -= 1
        

input.close()
output.close()            
