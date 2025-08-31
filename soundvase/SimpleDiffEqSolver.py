#Carl Osborne, Honors PreCalc, 5/18/22
#Special Topics Project: DiffEq Solver part II
#Program generates and checks a curve of a chosen differential equation using Euler's method with some specifications from the user.


#imports
import numpy as np
import matplotlib.pyplot as plt
import math


#printed description
print("This program finds a curve that is described by a differential equation.")
print("The approximation is then compared to the equation's actual solution")
print("Choose from the differential equations below:")
print("Equation 1: dy/dx = .25*y")
print("Equation 2: dy/dx = 1/y")
print("Equation 3: dy/dx = (1-y/5)*y")
print("Equation 4: dy/dx = x + y ")
print("")


#inputs
print("Enter the number of the option you want to see: ")
equation = int(input())
print("Enter a value between -10 and 10 for the initial x-coordinate: ")
initialx = float(input())
print("Enter a value between -10 and 10 for the initial y-coordinate: ")
initialy = float(input())

if equation == 1 or equation == 2 or equation == 3: #I don't have an actual solution to equation 4
    print("Plot points of the actual solution? T/F: ")
    toplot = input()
    if toplot == "T" or toplot == "t":
        toplot = True
    elif toplot == "F" or toplot == "f":
        toplot = False
else:
    toplot = False

if toplot: #only if they want to plot points
    print("Enter the number of points to plot: ")
    numpoints = int(input())

resolution = 50000 #sets how many points Euler's method uses


#processing
if equation == 1:
    A = initialy/math.e**(initialx/4) #determine unknowns from the user's initial point
    print("An actual solution to this differential equation that contains the point ("+str(initialx)+","+str(initialy)+") is y = "+str(A)+"e^(x/4).") #give the user an equation if possible
    realcurvex = np.arange(initialx,10,((11-initialx)/numpoints)) #x values of actual function's curve
    realcurvey = A*math.e**(realcurvex/4) #y values of actual function's curve
    eulersx = np.arange(initialx,10,((10-initialx)/resolution)) #x values of the curve made by Euler's method
    eulersx = eulersx[0:resolution] #ensure it is a proper length
    eulersy = np.array([initialy]) #initiate an array for the y values of the curve made by Euler's method
    y = initialy #initiate the y variable
    for i in range(resolution-1):
        y = y + 0.25*y*((10-initialx)/resolution) #use Euler's method to find the next point
        eulersy = np.append(eulersy,y) #add the y value of the point to the array holding the y values of the curve made by Euler's method

if equation == 2:
    A = initialy**2 - 2*initialx #determine unknowns from the user's initial point
    print("An actual solution to this differential equation that contains the point ("+str(initialx)+","+str(initialy)+") is y = +/- (2x+"+str(A)+")^(1/2).") #give the user an equation if possible
    realcurvex = np.arange(initialx,10,((11-initialx)/numpoints)) #x values of actual function's curve
    realcurvey = (2*realcurvex+A)**(1/2) #y values of actual function's curve
    eulersx = np.arange(initialx,10,((10-initialx)/resolution)) #x values of the curve made by Euler's method
    eulersx = eulersx[0:resolution] #ensure it is a proper length
    eulersy = np.array([initialy]) #initiate an array for the y values of the curve made by Euler's method
    y = initialy #initiate the y variable
    for i in range(resolution-1):
        y = y + 1/y*((10-initialx)/resolution) #use Euler's method to find the next point
        eulersy = np.append(eulersy,y) #add the y value of the point to the array holding the y values of the curve made by Euler's method

if equation == 3:
    A = (5-initialy)/initialy/math.e**(-initialx) #determine unknowns from the user's initial point
    print("An actual solution to this differential equation that contains the point ("+str(initialx)+","+str(initialy)+") is y = 5/(1+"+str(A)+"e^-x).") #give the user an equation if possible
    realcurvex = np.arange(initialx,10,((11-initialx)/numpoints)) #x values of actual function's curve
    realcurvey = 5/(1+A*math.e**(0-realcurvex)) #y values of actual function's curve
    eulersx = np.arange(initialx,10,((10-initialx)/resolution)) #x values of the curve made by Euler's method
    eulersx = eulersx[0:resolution] #ensure it is a proper length
    eulersy = np.array([initialy]) #initiate an array for the y values of the curve made by Euler's method
    y = initialy #initiate the y variable
    for i in range(resolution-1):
        y = y + (1-y/5)*y*((10-initialx)/resolution) #use Euler's method to find the next point
        eulersy = np.append(eulersy,y) #add the y value of the point to the array holding the y values of the curve made by Euler's method

if equation == 4:
    eulersx = np.arange(initialx,10,((10-initialx)/resolution)) #x values of the curve made by Euler's method
    eulersx = eulersx[0:resolution] #ensure it is a proper length
    eulersy = np.array([initialy]) #initiate an array for the y values of the curve made by Euler's method
    y = initialy #initiate the y variable
    for i in range(resolution-1):
        y = y + (y+eulersx[i+1])*((10-initialx)/resolution) #use Euler's method to find the next point
        eulersy = np.append(eulersy,y) #add the y value of the point to the array holding the y values of the curve made by Euler's method


#outputs
if toplot: #display the actual solution's curve and change the title if appropriate
    if equation == 2:
        plt.plot(realcurvex,-realcurvey,"x") #equation 2 has two possible outcomes
    plt.plot(realcurvex,realcurvey,"x")
    plt.title("The curve shows the result of Euler's method\nand the x's are the outputs of the actual solution.")
else:
    plt.title("The curve shows the result of Euler's method.")
plt.plot(eulersx,eulersy) #plot the curve made by Euler's method
plt.grid() #turn on the grid
plt.xlim([-10,10]) #set the x bounds
plt.ylim([-10,10]) #set the y bounds
plt.show() #show the graph