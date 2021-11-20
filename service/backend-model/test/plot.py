import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

train = pd.read_csv('test_result.csv')
colors_list = ["brownish green", "pine green", "ugly purple",
               "blood", "deep blue", "brown", "azure"]

palette = sns.xkcd_palette(colors_list)

x = train.iloc[:, 1:].sum()

plt.figure(figsize=(9, 6))
ax = sns.barplot(x.index, x.values, palette=palette)
plt.title("Class")
plt.ylabel('Occurrences', fontsize=12)
plt.xlabel('Type ')
rects = ax.patches
labels = x.values
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 10, label,
            ha='center', va='bottom')

plt.show()
