import streamlit as st
import matplotlib.pyplot as plt

def graph_pie(bot1,bot2,bot3,bot4):
    summary_wealth = bot1 + bot2 + bot3 + bot4
    ras1 = bot1 * 100 / summary_wealth
    ras2 = bot2 * 100 / summary_wealth
    ras3 = bot3 * 100 / summary_wealth
    ras4 = bot4 * 100 / summary_wealth
    labels = 'Agent1', 'Agent2', 'Agent3', 'Agent4'
    sizes = [ras1, ras2, ras3, ras4]
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    # explode1 = (0,0,0.1,0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
