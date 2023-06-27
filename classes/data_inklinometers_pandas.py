import pandas as pd
import matplotlib.pyplot as plt

df_1 = pd.read_json('../data/data_inklinometer_1.json', orient='index')
df_2 = pd.read_json('../data/data_inklinometer_2.json', orient='index')
frames = [df_1, df_2]
df = pd.concat(frames, axis=1, join='inner')
print(df)
print(df['X'])
print(df['CB'])

print(df['CB'].corr(-df['X']))

df_x = -df['X']
df_CB = df['CB']

a = (df_x - df_x.min()) / (df_x.max() - df_x.min())
b = (df_CB - df_CB.min()) / (df_CB.max() - df_CB.min())

a.plot(label='NIVEL220')
b.plot(label='Наш')
plt.xlabel('t, с', fontsize=14)
plt.ylabel('Смещение', fontsize=14)
plt.legend(fontsize=14)
plt.show()

