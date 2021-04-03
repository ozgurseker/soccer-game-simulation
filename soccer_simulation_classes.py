import autograd.numpy as np2
from autograd import grad
import scipy.optimize as op
from scipy.optimize import Bounds

class team:
    def __init__(self, Pa, Pd, W, D, Opp):
        self.OffPow = Pa
        self.DefPow = Pd
        self.PayoffW = W
        self.PayoffD = D
        self.Opponent = Opp
        self.T = 1
        self.N = 1
        self.effort_allocation = dict()
        self.n = 1
        self.Utilities = dict()


    def __init__(self, Pa, Pd, W, D):
        self.OffPow = Pa
        self.DefPow = Pd
        self.PayoffW = W
        self.PayoffD = D
        self.T = 1
        self.N = 1
        self.n = 1
        self.Opponent = None
        self.effort_allocation = dict()
        self.Utilities = dict()


    def ProbToScore(self, e1, e2):
        return e1*self.OffPow / (self.T * (e1*self.OffPow + (2-e2)*self.Opponent.DefPow))

    def ProbToScoreOpp(self, e1, e2):
        return e2 * self.Opponent.OffPow / (self.T * (2-e1) * self.DefPow + self.T * e2 * self.Opponent.OffPow)

    def ProbNtoLead(self, e1, e2, N):
        pA = self.ProbToScore(e1, e2)
        pB = self.ProbToScoreOpp(e1, e2)
        return (1-pA)*(1-pB)*pA**N / (1-pA*pB)

    def ProbNtoBack(self, e1, e2, N):
        pA = self.ProbToScore(e1, e2)
        pB = self.ProbToScoreOpp(e1, e2)
        return (1 - pA) * (1 - pB) * pB ** N / (1 - pA * pB)

    def ProbMoreThanLead(self, e1, e2, N):
        pA = self.ProbToScore(e1, e2)
        pB = self.ProbToScoreOpp(e1, e2)
        return (1 - pB) * pA ** (N+1) / (1 - pA * pB)

    def ProbMoreThanBack(self, e1, e2, N):
        pA = self.ProbToScore(e1, e2)
        pB = self.ProbToScoreOpp(e1, e2)
        return (1 - pA) * pB ** (N + 1) / (1 - pA * pB)

    def ExpectedPayoff(self, t, n, e1, e2):

        if t == self.T - 1 and n > 0:
            payoff = (1 - self.ProbMoreThanBack(e1,e2,n-1)) * self.PayoffW + self.ProbNtoBack(e1,e2,n) * self.PayoffD
            return payoff

        elif t == self.T - 1 and n <= 0:
            payoff = self.ProbMoreThanLead(e1, e2, n) * self.PayoffW + self.ProbNtoLead(e1, e2,n) * self.PayoffD
            return payoff

        else:
            payoff = 0
            for i in range(self.n):
                payoff = payoff + self.ProbNtoLead(e1,e2, i+1)*self.Utilities[int(2*(t+1)*self.N + n+i+1)]
                payoff = payoff + self.ProbNtoBack(e1,e2,i+1)*self.Utilities[int(2*(t+1)*self.N + n-i-1)]

            payoff = payoff + self.ProbNtoLead(e1,e2,0)*self.Utilities[int(2*(t+1)*self.N + n)]

            return payoff

    def Utility(self, t, n):
        if t >= self.T:
            if n > 0 :
                return self.PayoffW
            elif n < 0 :
                return 0
            else:
                return self.PayoffD

        else:
            return self.Utilities[2*t*self.N +n]

    def addeffortallocation(self, t, s, allocation):
        self.effort_allocation[int(2*t*self.N + s)] = allocation

    def getEffortAllocation(self, t, s):
        return self.effort_allocation[int(2*t*self.N + s)]

    def addUtilities(self,t,s,Util):
        self.Utilities[int(2*t*self.N +s)] = Util

    def showEffortAllocations(self):
        for t in range(self.T):
            for s in range(t*self.n):
                print("term: " + str(t) + "")

class Game:
    def __init__(self, team_home, team_away, T, N):
        self.team_h = team_home
        self.team_a = team_away
        self.team_a.Opponent = self.team_h
        self.team_h.Opponent = self.team_a
        self.team_h.N = N
        self.team_a.N = N
        self.team_h.n = int(N/T)
        self.team_a.n = int(N/T)
        self.team_h.T = T
        self.team_a.T = T
        self.T = T
        self.N = N
        self.n = int(N/T)

    def setEffortAllocations(self):
        for i in range(self.T):
            t = self.T - i - 1
            for s in range(self.n * t + 1):
                foc1 = grad(self.team_h.ExpectedPayoff, 2)
                foc2 = grad(self.team_a.ExpectedPayoff, 2)
                def foc_all(effs):
                    f1 = foc1(t, s, effs[0], effs[1])
                    f2 = foc2(t, -s, effs[1], effs[0])
                    return [f1, f2]

                alloc = op.root(foc_all, np2.array([0.5,0.5]))
                alloc = alloc.x
                self.team_h.addeffortallocation(t,s,alloc[0])
                self.team_a.addeffortallocation(t, -s, alloc[1])
                Util = self.team_h.ExpectedPayoff(t,s, alloc[0], alloc[1])
                self.team_h.addUtilities(t, s, Util)
                Util = self.team_a.ExpectedPayoff(t, -s, alloc[1], alloc[0])
                self.team_a.addUtilities(t, -s, Util)

                s = -s
                def foc_all(effs):
                    f1 = foc1(t, s, effs[0], effs[1])
                    f2 = foc2(t, -s, effs[1], effs[0])
                    return [f1, f2]

                alloc = op.root(foc_all, np2.array([0.5, 0.5]))
                alloc = alloc.x
                self.team_h.addeffortallocation(t,s,alloc[0])
                self.team_a.addeffortallocation(t, -s, alloc[1])
                Util = self.team_h.ExpectedPayoff(t,s, alloc[0], alloc[1])
                self.team_h.addUtilities(t, s, Util)
                Util = self.team_a.ExpectedPayoff(t, -s, alloc[1], alloc[0])
                self.team_a.addUtilities(t, -s, Util)

    def showAllocations(self, t, s):
        e_h = self.team_h.getEffortAllocation(t,s)
        e_a = self.team_a.getEffortAllocation(t,-s)
        return [e_h, e_a]


team_h = team(4, 3, 3, 1)
team_a = team(1, 1, 3, 1)

newGame = Game(team_h, team_a, 3, 6)

newGame.setEffortAllocations()


newGame.showAllocations(2, 3) #Effort allocations when period is 2, and team_h leads by 3

 