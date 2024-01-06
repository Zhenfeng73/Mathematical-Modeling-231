from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense
import numpy as np
import sys
import gamspy as gp

n = 8
m = 5
A = []
u = 1
v = 10

for i in range(0, 8, 1):
    temper = np.random.randint(u, v, m)
    A.insert(i, temper)

D = [np.random.binomial(10, 0.5, n), np.random.binomial(10, 0.5, n)]

B = [4500, 2000, 3150, 3800, 7000]
L = [760000, 150000, 190000, 741000, 353000, 450000, 630000, 152000]
S = [1500, 1300, 1850, 2500, 2000]
Q = [900000, 250000, 300000, 800000, 750000, 850000, 900500, 200000]


C= []
for i in range(n):
    C.insert(i, L[i] - Q[i])

print(C)
print(D)
print(L)
print(Q)
print(B)
print(S)

container = gp.Container()
i = gp.Set(container,"i",description="warehouses",
           records=["1", "2", "3", "4", "5", "6", "7", "8"])
j = gp.Set(container,"j",description="suppliers",
           records=["1", "2", "3", "4", "5"])
a = gp.Parameter(container,"a",
                 description="unit of product i requires of part j",domain=[i, j], records=np.asanyarray(A))
l = gp.Parameter(container,"l",
                 description="cost to produce at location j",domain=i, records=np.asanyarray(L))
q = gp.Parameter(container,"q",
                 description="cost to sell at location i",domain=i, records=np.asanyarray(Q))
b = gp.Parameter(container,"b",
                 description="preorder cost of the supplier j",domain=j, records=np.asanyarray(B))
c = gp.Parameter(container,"c",
                 description="cost coefficients",domain=i, records=np.asanyarray(C))
s = gp.Parameter(container,"s",
                 description="salvage values in the supplier j",domain=j, records=np.asanyarray(S))
d1 = gp.Parameter(container,"d1",
                  description="demand at first scenario",domain=i, records=np.asanyarray(D[0]))
d2 = gp.Parameter(container,"d2",
                  description="demand at second scenaario",domain=i, records=np.asanyarray(D[1]))

d1.records
d2.records

x = gp.Variable(container, "x", domain=j, type="positive",
                description="numbers of portions have been ordered ")
y1 = gp.Variable(container, "y1", domain=j, type="positive",
                 description="numbers of portions have been left in inventory in day one")
y2 = gp.Variable(container, "y2", domain=j, type="positive",
                 description="numbers of portions have been left in inventory in day two")
z1 = gp.Variable(container, "z1", domain=i, type="positive",
                 description="number of portions need to be produced in day one")
z2 = gp.Variable(container, "z2", domain=i, type="positive",
                 description="number of portions need to be produced in day two")

demand1 = Equation(
    container=container, name="demand1", domain=i,
    definition= z1[i] <= d1[i])
demand2 = Equation(
    container=container, name="demand2", domain=i,
    definition = z2[i] <= d2[i])
constraint1 = Equation(
    container=container, name="constraint1", domain=j,
    definition = y1[j] == x[j] - Sum(i,a[i,j]*z1[i]))
constraint2 = Equation(
    container=container, name="constraint2", domain=j,
    definition = y2[j] == x[j] - Sum(i,a[i,j]*z2[i]))

obj_func = Sum(j, b[j] * x[j]) + 1/2 * (Sum(i, c[i] * z1[i]) - Sum(j, s[j] * y1[j])) + 1/2 * (Sum(i, c[i] * z2[i]) - Sum(j, s[j] * y2[j]))

problem = gp.Model(container, "problem",  "LP", container.getEquations(), Sense.MIN, obj_func)
problem.solve(output=sys.stdout)