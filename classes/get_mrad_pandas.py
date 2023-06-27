import pandas as pd
import matplotlib.pyplot as plt

df_1 = pd.read_json('../data/data_inklinometer_1.json', orient='index')
df_2 = pd.read_json('../data/data_inklinometer_2.json', orient='index')
frames = [df_1, df_2]
df = pd.concat(frames, axis=1, join='inner')
print(df)

df_x = df['X']
df_cb = df['CB']

# print(df_x)
# print(df_cb)

relation = df_x / df_cb
print(relation)

print(relation.mean())

df_x.plot()
df_cb.plot()

plt.show()