import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('race_results.csv')

scaler = StandardScaler()
df[['finish_time', 'num_participants']] = scaler.fit_transform(df[['finish_time', 'num_participants']])

# Kreiraj karakteristike za klasterovanje
X = df[['finish_time', 'num_participants', 'course_type', 'season']]

# Primeni K-means klasterovanje
kmeans = KMeans(n_clusters=5, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Analiziraj rezultate
for cluster in range(5):
    cluster_data = df[df['cluster'] == cluster]
    print(f"Cluster {cluster}:")
    print(cluster_data.describe())

# Pretpostavimo da trkač ima PR koji želimo analizirati
runner_pr = 3000  # primer vrednost u sekundama

# Pronađi klastere gde bi PR bio među top 10
for cluster in range(5):
    cluster_data = df[df['cluster'] == cluster]
    top_10_threshold = cluster_data['finish_time'].quantile(0.1)
    if runner_pr <= top_10_threshold:
        print(f"Runner PR of {runner_pr} would be in top 10 in cluster {cluster}")
