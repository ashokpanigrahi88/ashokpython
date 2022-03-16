"""A set of exercises with matplotlib"""
import numpy as np
import matplotlib.pyplot as plt


def draw_co2_plot():
    """
    Here is some chemistry data

      Time (decade): 0, 1, 2, 3, 4, 5, 6
      CO2 concentration (ppm): 250, 265, 272, 260, 300, 320, 389

    Create a line graph of CO2 versus time, the line should be a blue dashed
    line. Add a title and axis titles to the plot.
    """
    time = np.array([0, 1, 2, 3, 4, 5, 6])
    co2 = np.array([250, 265, 272, 260, 300, 320, 389])
    plt.plot(time, co2, color="blue", ls='dashed')
    plt.title("CO2 versus time ")
    plt.xlabel('Time (decade)')
    plt.ylabel('CO2 concentration (ppm)')
    plt.show()


def draw_equations_plot():
    """
    Plot the following lines on the same plot

      y=cos(x) coloured in red with dashed lines
      y=x^2 coloured in blue with linewidth 3
      y=exp(-x^2) coloured in black

    Add a legend, title for the x-axis and a title to the curve, the x-axis
    should range from -4 to 4 (with 50 points) and the y axis should range
    from 0 to 2. The figure should have a size of 8x6 inches.

    NOTE: Make sure you create the figure at the beginning as doing it at the 
    end will reset any plotting you have done.
    """

    y_cos = lambda x: np.cos(x)
    y_squared = lambda x: x**2
    y_exp = lambda x: np.exp(-x**2)
    xaxis = np.linspace(-4, 4, 50)
    fig = plt.figure(figsize=(8, 6))
    plt.plot(xaxis, y_cos(xaxis), xaxis, y_squared(xaxis), xaxis, y_exp(xaxis))
    plt.ylim(0, 2)
    plt.legend(['Line1', 'Line2', 'Line3'])
    plt.title('Equations Plot')
    plt.show()
