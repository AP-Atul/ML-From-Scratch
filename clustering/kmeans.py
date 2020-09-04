import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

TOL = 0.001
ITER = 300
CLUSTER = 2


class KMeans:
    def __init__(self, k=CLUSTER, tol=TOL, max_iter=ITER):
        self.classifications = {}
        self.centroids = {}
        self.k = k
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, data):

        # intializing the centroids to 1st 3 ele
        for i in range(self.k):
            self.centroids[i] = data[i]
            print(self.centroids)

        # iterate for max _iterations
        for i in range(self.max_iter):

            for i in range(self.k):
                self.classifications[i] = []

            # create cluster & cal Euclidean distance
            for featureset in data:
                distances = [np.linalg.norm(featureset - self.centroids[centroid]) for centroid in self.centroids]
                classification = distances.index(min(distances))
                self.classifications[classification].append(featureset)

            prev_centroids = dict(self.centroids)

            # recal mean/centroid
            for classification in self.classifications:
                self.centroids[classification] = np.average(self.classifications[classification], axis=0)

            optimized = True

            # check for tolerance
            for c in self.centroids:
                original_centroid = prev_centroids[c]
                current_centroi = self.centroids[c]
                if np.sum((current_centroi - original_centroid) / original_centroid * 100.0) > self.tol:
                    print("New centroid :: ", np.sum((current_centroi - original_centroid) / original_centroid * 100.0))
                    optimized = False

            if optimized:
                break

    def predict(self, data):
        distances = [np.linalg.norm(data - self.centroids[centroid]) for centroif in self.centroids]
        classification = distances.index(min(distances))
        return classification


############################################################
# Driver code
# Reading the first 2 cols of the dataset
X = pd.read_csv("iris.csv", header=None, usecols=[0, 1, 2, 3])
colors = ['r', 'g', 'b', 'c', 'k', 'o', 'y']

clf = KMeans()
clf.fit(np.array(X))

for i in range(len(X)):
    plt.scatter(np.array(X)[i][0], np.array(X)[i][1],
                color="r", marker="*")
    plt.scatter(np.array(X)[i][2], np.array(X)[i][3],
                color="r", marker="*")
plt.show()

# for sepals
for classification in clf.classifications:
    color = colors[classification]
    for featureset in clf.classifications[classification]:
        plt.scatter(featureset[0], featureset[1],
                    marker=".", color=color, linewidths=5)

for centroid in clf.centroids:
    plt.scatter(clf.centroids[centroid][0], clf.centroids[centroid][1],
                marker="*", color="b", s=100, linewidths=5)

plt.xlabel("Sepals Length")
plt.ylabel("Sepals Width")
plt.title("Sepals")
plt.show()

# for petals
for classification in clf.classifications:
    color = colors[classification]
    color1 = colors[classification + 1]
    for featureset in clf.classifications[classification]:
        plt.scatter(featureset[2], featureset[3],
                    marker=".", color=color, linewidths=5)

for centroid in clf.centroids:
    plt.scatter(clf.centroids[centroid][2], clf.centroids[centroid][3],
                marker="*", color="b", s=100, linewidths=5)

plt.xlabel("Petals Length")
plt.ylabel("Petals Width")
plt.title("Petals")
plt.show()
