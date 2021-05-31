import pickle
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib import mlab
from scipy.special import erf

"""
We approximate concentrated and relaxed brain wave data sets each as normal Gaussian distributions.

The cross point of the two gaussians give the best V0 (threshold voltage which separates relazed and concentrated data) which minimizes over all error.

The overlap area divided by 2 give the probability of wrong classification

The ratio of overlap area left of V0 to right of V0 gives the percentage of wrong estimation being we guessed concentrated but is actually relaxed.
"""

# read np.array object from pickle file
# data[0]: relaxed data voltage
# data[1]: concentrated data voltage

filename = ''
file = open(filename, 'rb')
data = pickle.load(file)
file.close()

relaxed = data[0]
concentrated = data[1]


# calculate mean and std to construct the gaussian normal distributions

r_mean = np.mean(relaxed)
c_mean = np.mean(concentrated)
r_std = np.std(relaxed)
c_std = np.std(concentrated)

# Solve for cross point of the two normal distributions

def solve(m1,m2,std1,std2):
    a = 1/(2*std1**2) - 1/(2*std2**2)
    b = m2/(std2**2) - m1/(std1**2)
    c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
    return np.roots([a,b,c])

results = solve(r_mean, c_mean, r_std, c_std)
intersection = []

# Select the cross point in the middle of the two mean values.

for i in range(len(results)):
    if results[i] < r_mean and results[i] > c_mean:
        intersection.append(results[i])
V0 = intersection[0]
print("V0 should be: ", V0)

# plot the normal distributions and the cross point

x = np.linspace(c_mean-7*c_std,r_mean+7*r_std,10000)
plot1=plt.plot(x,norm.pdf(x,r_mean,r_std))
plot2=plt.plot(x,norm.pdf(x,c_mean,c_std))
plot3=plt.plot(result,norm.pdf(result,r_mean,r_std),'o')

# Calculate the overlap area using erf function
r_z = (V0 - r_mean)/(r_std * math.sqrt(2))
r_overlap = (1-abs(erf(r_z)))/2
c_z = (V0 - c_mean)/(c_std* math.sqrt(2))
c_overlap = (1-abs(erf(c_z)))/2

overlap = r_overlap + c_overlap
prob = overlap/2
prob_percent = r_overlap/(c_overlap+r_overlap)
print("probability of wrong classification is: ", prob)
print("percentage of wrong classification being predicted is concentrated but is actually relaxed: ", prob_percent)
