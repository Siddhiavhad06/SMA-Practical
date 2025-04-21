import plotly.express as px
import pandas as pd
import bokeh.plotting as bp
from bokeh.models import ColumnDataSource

# Load dataset
df = pd.read_csv("C:/Users/Siddhi Avhad/Desktop/Dataset.csv")

# Display first few rows to verify the dataset
print(df.head())

# Scatter plot: Likes vs Shares
fig_scatter = px.scatter(df, x='likes', y='shares', title='Likes vs. Shares',
                         labels={'likes': 'Number of Likes', 'shares': 'Number of Shares'})
fig_scatter.show()

# Boxplot: Distribution of Likes
fig_box = px.box(df, y='likes', title='Distribution of Likes',
                 labels={'likes': 'Number of Likes'})
fig_box.show()

# Bokeh scatter plot
source = ColumnDataSource(df)
fig_bokeh = bp.figure(title="Bokeh Plot: Likes vs Shares", x_axis_label="Likes", y_axis_label="Shares")
fig_bokeh.circle(x='likes', y='shares', source=source, size=8, color="navy", alpha=0.5)
bp.show(fig_bokeh)

# Average Likes
average_likes = df['likes'].mean()
print("Average Likes:", average_likes)