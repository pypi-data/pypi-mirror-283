from pregress.modeling.parse_formula import parse_formula
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def barplot(formula=None, data=None, xcolor="blue", ycolor="red", main="Barplots of Variables", xlab="Variable", ylab="Value"):
    """
    Generates and prints bar plots for all numeric variables specified in the formula or all numeric variables in the data if no formula is provided.

    Args:
        formula (str, optional): Formula to define the model (dependent ~ independent).
        data (DataFrame, optional): Data frame containing the data.
        xcolor (str, optional): Color of the bars for the independent variables.
        ycolor (str, optional): Color of the bars for the dependent variable.
        main (str, optional): Title of the plot.
        xlab (str, optional): Label for the x-axis.
        ylab (str, optional): Label for the y-axis.

    Returns:
        None. The function creates and shows bar plots.
    """
    if formula is not None:
        formula = formula + "+0"
        Y_name, X_names, Y_out, X_out = parse_formula(formula, data)

        # Combine Y and X data for bar plots
        plot_data = pd.concat([pd.Series(Y_out, name=Y_name), X_out], axis=1)

        # Melt the DataFrame for easier plotting with seaborn
        plot_data_melted = plot_data.melt(var_name='Variable', value_name='Value')

        # Create a color mapping for columns
        palette = {Y_name: ycolor}
        palette.update({x: xcolor for x in X_names})

    else:
        # If no formula is provided, use all numeric variables in the data
        plot_data = data.select_dtypes(include=[np.number])

        # Melt the DataFrame for easier plotting with seaborn
        plot_data_melted = plot_data.melt(var_name='Variable', value_name='Value')

        # Create a single color mapping for all variables
        palette = {var: xcolor for var in plot_data_melted['Variable'].unique()}

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    barplot = sns.barplot(x='Variable', y='Value', data=plot_data_melted, hue='Variable', dodge=False, palette=palette, errorbar=None, legend=False)

    barplot.set_title(main)
    barplot.set_xlabel(xlab)
    barplot.set_ylabel(ylab)

    plt.show()
