import pandas as pd

import pandas_datareader as web


import matplotlib.pyplot as plt

import datetime as dt


ticker = "TSLA"                   # Stock Symbol used in the market.


start = dt.datetime(2020,1,1)

end = dt.datetime.now()           # The latest possible timestamp.


data = web.DataReader(ticker, "yahoo", start, end)              # This is a pandas.core.frame.DataFrame object



closing_data = data["Adj Close"]



# Now, let's calculate the difference between the adjusted closing prices of today and yesterday. (let's check if it is positive or negative)



delta_closing_data = closing_data.diff(1)


# delta_closing_data => What is the difference between today's closing price and yesterday's closing price.



delta_closing_data = delta_closing_data.dropna(inplace = False)                     # just drop "not available" values from the DataFrame object.




# If inplace keyword argument equals True, the method, object.dropna() returns None. It becomes an "inplace method". By default, inplace equals False, that means by default, dropna() returns a DataFrame object.



positive = delta_closing_data.copy()

negative = delta_closing_data.copy()




positive[positive < 0 ] = 0


negative[negative > 0] = 0


days = 14                   # This is the timeframe of the RSI graph. You can alter this to get different results.



average_gain = positive.rolling(window = days).mean()             # We are gonna take the rolling sum of the positive differences in the "passed-in" timeframe and simultaneously take its mean


average_loss = abs(negative.rolling(window = days).mean())        # We are gonna take the rolling sum of the negative differences in the "passed-in" timeframe  and simultaneously calculate its mean and finally take the absolute value of the resultant.


# We require only the magnitude of the average_loss. Hence, we are taking the absolute value of the final value.


relative_strength = average_gain / average_loss


rsi = 100.0 - (100.0 / (1.0 + relative_strength))                # relative_strength = average_gain/average_loss


# rsi = relative strength index



# Now, let's create a combined dataframe.


combined = pd.DataFrame()


combined['Adj Close'] = data['Adj Close']

combined['rsi'] = rsi


plt.figure(figsize = (12, 8))


axis_1 = plt.subplot(211)



axis_1.plot(combined.index, combined["Adj Close"], color = "lightgray")                  # combined.index refers to the dates. (time)  (x_axis)


axis_1.set_title("Closing Share Price", color = "white")


axis_1.grid(True, color = "#555555")             # Yes, we want gridlines on the graph.



axis_1.set_axisbelow(True)


axis_1.set_facecolor("black")

axis_1.tick_params(axis = "x", colors = "black")                # Highlight the axis "x" parameters (numbers)


axis_1.tick_params(axis = "y", colors = "black")                  # Highlight the axis "y" parameters (numbers)













axis_2 = plt.subplot(212, sharex = axis_1)                      # The rsi graph will be sharing its x_axis with the adjusted closing price graph.



axis_2.plot(combined.index, combined["rsi"], color = "lightgray")                  # combined.index refers to the dates. (time)  (x_axis)



axis_2.axhline(0, linestyle = "--", alpha = 0.5, color = "#ff0000")


axis_2.axhline(10, linestyle = "--", alpha = 0.5, color = "#ffaa00")



axis_2.axhline(20, linestyle = "--", alpha = 0.5, color = "#00ff00")



axis_2.axhline(30, linestyle = "--", alpha = 0.5, color = "#cccccc")



axis_2.axhline(70, linestyle = "--", alpha = 0.5, color = "#cccccc")


axis_2.axhline(80, linestyle = "--", alpha = 0.5, color = "#00ff00")


axis_2.axhline(90, linestyle = "--", alpha = 0.5, color = "#ffaa00")


axis_2.axhline(100, linestyle = "--", alpha = 0.5, color = "#ff0000")






axis_2.set_title("Relative Strength Index", color = "White")


axis_2.grid(False)             # No, we don't want gridlines on the graph.



axis_2.set_axisbelow(True)


axis_2.set_facecolor("black")




axis_2.tick_params(axis = "x", colors = "black")               # Highlight/color the axis "x" parameters (numbers)


axis_2.tick_params(axis = "y", colors = "black")              # Highlight/color the axis "y" parameters (numbers)



plt.show()                               # Display the two graphs.
