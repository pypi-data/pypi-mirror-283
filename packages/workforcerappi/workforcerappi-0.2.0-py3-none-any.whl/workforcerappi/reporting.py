import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_time_series(df, x, y):
    """
    Plot the proportion of orders by country.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    y (str): The column name for the ORDERS. 
    x (str): The column name for the FECHA.
    """
    # Group by the country column and sum the orders
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x=x, y=y)#, marker='o'
    plt.title(f'{y} Over Time')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.show()

# Average orders by interval
def plot_general_orders_curve(df, x, y):
    """
    Plot the average orders by interval.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    x (str): The column name for the x-axis (intervals).
    y (str): The column name for the y-axis (orders).
    """
    #df['DATETIME'] = pd.to_datetime(df['FECHA'].astype(str) + ' ' + df['INTERVALO'].astype(str))
    interval_avg_orders = df.groupby(x)[y].mean().reset_index()
    interval_avg_orders.columns = [x, 'AVG_ORDERS']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=interval_avg_orders, x=x, y='AVG_ORDERS', palette='viridis')
    plt.title('Average Orders by Interval')
    plt.xlabel('Interval')
    plt.ylabel('Average Number of Orders')
    plt.xticks(rotation=45)
    plt.show()


#Proportion of Orders by Country
def plot_proportion_of_orders_by_country(df, orders_col, country_col):
    """
    Plot the proportion of orders by country.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    orders_col (str): The column name for the orders.
    country_col (str): The column name for the countries.
    """
    # Group by the country column and sum the orders
    df_grouped = df.groupby(country_col)[orders_col].sum().reset_index()
    
    # Sort the DataFrame by orders in descending order
    df_ordered = df_grouped.sort_values(by=orders_col, ascending=False)
    
    # Plot the proportion of orders by country
    plt.figure(figsize=(10, 6))
    plt.pie(df_ordered[orders_col], labels=df_ordered[country_col], autopct='%1.1f%%', startangle=140, 
            colors=sns.color_palette('viridis', len(df_ordered)))
    plt.title('Proportion of Orders by Country')
    plt.show()



#Total Number of Orders per Country

def plot_total_orders_per_country(df, x, y):
    """
    Plot the proportion of orders by country.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the data.
    y (str): The column name for the ORDERS. 
    x (str): The column name for the COUNTRY.
    """
    # Group by the country column and sum the orders
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=x, y=y, palette='viridis')
    plt.title('Total Number of Orders per Country')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()


# Plot raw data vs predictions
def plot_raw_data_vs_prediction(data,X_test,test,model):
    test['prediction'] = model.predict(X_test)
    data = data.merge(test[['prediction']], how='left', left_index=True, right_index=True)
    ax = data[['SS']].plot(figsize=(15, 5))
    data['prediction'].plot(ax=ax)
    plt.legend(['Truth Data', 'Predictions'])
    ax.set_title('Raw Dat and Prediction')
    plt.show()
    

# Plot raw data vs forecasted
def plot_raw_data_vs_forecasted(data,month_to_predict):
    month_to_predict2=pd.DataFrame(month_to_predict)
    data2 = pd.concat([data["SS"],month_to_predict2])
    ax = data2[0].plot(figsize=(15, 5))
    data2['prediction'].plot(ax=ax)
    plt.legend(['Truth Data', 'Predictions'])
    ax.set_title('Raw Dat and Prediction')
    plt.show()


def plot_orders_curve(curva_ordenes):
    x_labels = [str(time) for time in curva_ordenes.index]
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(20, 18))
    axes = axes.flatten()
    for i, (col, ax) in enumerate(zip(curva_ordenes.columns, axes)):
        ax.plot(x_labels, curva_ordenes[col], linestyle='-', color='b')
        ax.set_title(col)
        ax.set_xlabel('Interval')
        ax.set_ylabel('Value')
        ax.tick_params(axis='x', rotation=70)

    plt.tight_layout()
    plt.show()
