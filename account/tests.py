from django.test import TestCase

# Create your tests here.
# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Generate random data for monthly sales:
# Here, we generate random sales values between 50 and 200 for 12 months (a whole year).
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
sales = np.random.randint(50, 200, size=12)

# Create a line chart for monthly sales:
plt.plot(months, sales)  # Plot the sales data
plt.title("Monthly Sales Over a Year (Line Chart)")  # Set the title of the plot
plt.xlabel("Month")  # Set the x-axis label
plt.ylabel("Sales")  # Set the y-axis label
plt.show()  # Display the plot

# Create a bar chart for monthly sales:
plt.figure(figsize=(10, 6))  # Set the figure size
plt.bar(months, sales, color='g')  # Create a bar chart with the sales data
plt.title("Monthly Sales Over a Year (Bar Chart)")  # Set the title of the plot
plt.xlabel("Month")  # Set the x-axis label
plt.ylabel("Sales")  # Set the y-axis label
plt.tight_layout()  # Ensure layout looks good
plt.show()  # Display the plot

# Create a pie chart for the distribution of sales across months:
plt.figure(figsize=(10, 6))  # Set the figure size
plt.pie(sales, labels=months, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)  # Create a pie chart
plt.title("Sales Distribution Across Months (Pie Chart)")  # Set the title of the plot
plt.tight_layout()  # Ensure layout looks good
plt.show()  # Display the plot

# Create a histogram to see the distribution of sales values:
plt.figure(figsize=(10, 6))  # Set the figure size
plt.hist(sales, bins=8, color='m', alpha=0.7)  # Create a histogram with 8 bins
plt.title("Distribution of Sales (Histogram)")  # Set the title of the plot
plt.xlabel("Sales")  # Set the x-axis label
plt.ylabel("Number of Months")  # Set the y-axis label
plt.tight_layout()  # Ensure layout looks good
plt.show()  # Display the plot
