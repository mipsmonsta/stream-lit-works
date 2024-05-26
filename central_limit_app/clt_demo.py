import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# central limit theorem: states that if we randomly sample with replacement
# enough from any distribution, then the distribution of the mean of 
# our samples will approximate the normal distribution

binomial_dist = np.random.binomial(1, 0.5, 100) # n = 1, p = 0.5

list_of_means = []

for i in range(0, 1000):
    list_of_means.append(np.random.choice(binomial_dist, 100, replace=True).mean())

fig, ax = plt.subplots()
ax = plt.hist(list_of_means)
st.pyplot(fig)