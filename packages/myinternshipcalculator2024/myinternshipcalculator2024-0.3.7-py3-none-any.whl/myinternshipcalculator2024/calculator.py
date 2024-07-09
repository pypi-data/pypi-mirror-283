import statsmodels.api as sm
import scipy.stats as stats
import plotly.express as px
import sklearn.linear_model as lm

def calculate_weekly_hours(daily_hours):
    """
    version 0.3.6
    Calculates total weekly hours based on daily hours.
    Assumes a 5-day work week.

    :param daily_hours: Number of hours worked per day
    :return: Total weekly hours
    """
    return daily_hours * 5

def calculate_monthly_hours(weekly_hours):
    """
    Calculates total monthly hours based on weekly hours.
    Assumes a 5-week month.

    :param weekly_hours: Number of hours worked per week
    :return: Total monthly hours
    """
    return weekly_hours * 5

def perform_ttest(data1, data2):
    """
    Performsss an independent T-test on two datasets.

    :param data1: First dataset
    :param data2: Second dataset
    :return: T-test statistic and p-value
    """
    return stats.ttest_ind(data1, data2)

def create_scatter_plot(data, x, y):
    """
    Create a scatter plot using Plotly.

    :param data: DataFrame containing the data
    :param x: Column name for x-axis
    :param y: Column name for y-axis
    :return: Plotly scatter plot figure
    """
    fig = px.scatter(data, x=x, y=y)
    fig.show()

def train_linear_regression(X, y):
    """
    Train a linear regression model using scikit-learn.

    :param X: Features
    :param y: Target variable
    :return: Trained linear regression model
    """
    model = lm.LinearRegression()
    model.fit(X, y)
    return model
