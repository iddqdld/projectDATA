import pandas as pd
import numpy as np

df = pd.read_csv(
    'cars.csv',
    dtype={
        'id': 'int32',
        'title': 'string',
        'price': 'float32',
        'mileage': 'Int32',
        'year': 'Int64',
        'link': 'string'
    },
    parse_dates=['scraped_at'],
    na_values=['', 'NA', 'N/A', 'NULL'],
    keep_default_na=False
)

# setting de parametrage de output (terminal)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_colwidth', 30)


# import year from title
df['year'] = df['title'].str.extract(r'\b(\d{4})\b').astype('Int64')

# print(df[['title', 'year']].head())

# sort a propos de prix
# df_sorted = df.sort_values(by='price', ascending=True)

# sort a prp de km
# df_sorted_mil = df.sort_values(by='mileage', ascending=True)
# output
# print(df_sorted_mil.head(15))

import matplotlib.pyplot as plt
import seaborn as sns

# style des charts
plt.style.use('seaborn-v0_8')
plt.figure(figsize=(15, 8))

# 1. Pie chart years
plt.subplot(1, 2, 1)
year_counts = df['year'].value_counts().sort_index()
year_counts = year_counts[year_counts > 0]  # ignore de nan

patches, texts, autotexts = plt.pie(
    year_counts,
    labels=year_counts.index.astype(str),
    autopct='%1.1f%%',
    startangle=90,
    pctdistance=0.85,
    wedgeprops={'edgecolor': 'w', 'linewidth': 1}
)

plt.title('Pie chart a porpos de lanne de production', fontsize=14)
plt.axis('equal')


# 2. prix vs km
plt.subplot(1, 2, 2)
scatter = sns.scatterplot(
    data=df,
    x='mileage',
    y='price',
    hue='year',
    palette='viridis',
    size='year',
    sizes=(20, 200),
    alpha=0.7,
    edgecolor='none'
)

# axes
plt.xlabel('km (mil)', fontsize=12)
plt.ylabel('prix ($)', fontsize=12)
plt.title('Dependence de prix a propos de kilometrage et date de production', fontsize=14)


# grid
plt.grid(True, linestyle='--', alpha=0.5)

# legende
handles, labels = scatter.get_legend_handles_labels()
plt.legend(
    handles[1:6],
    labels[1:6],
    title='anne',
    bbox_to_anchor=(1.05, 1),
    loc='upper left'
)

# setting gen
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)

# sauvgarde et visual
plt.savefig('cars_visualization.png', dpi=300, bbox_inches='tight')
plt.show()
