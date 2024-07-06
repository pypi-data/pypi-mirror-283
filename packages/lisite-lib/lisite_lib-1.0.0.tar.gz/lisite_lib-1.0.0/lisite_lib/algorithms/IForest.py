# lisite_lib/lisite_lib/algorithms/IForest.py

import numpy as np
import pandas as pd
import random
from lisite_lib.utils import consts as ue

"""This class implements the core logic of the isolated forest algorithm."""
class IsolationForest:
    def __init__(self, sample_size, n_trees=100):
        """
        sample_size: the sample size of each tree.
        n_trees: number of trees, default is 100.
        height_limit: height limit of the tree, the logarithm of the sample size.
        trees: Store the generated trees.
        samples: Store the sample index of each tree.
        n_dimensions: dimensions of the training data.
        """
        self.sample_size = sample_size
        self.n_trees = n_trees
        self.height_limit = np.log2(sample_size)
        self.trees = []
        self.samples = []
        self.n_dimensions = 0

    def fit(self, X: np.ndarray):
        """
        X: input training data.
        self.n_dimensions: set to the number of columns in the data.
        The fit method generates multiple isolated trees by random sampling and stores them in self.trees.
        """
        self.n_dimensions = X.columns
        # Check if the data is in DataFrame format, if so, convert to numpy array
        if isinstance(X, pd.DataFrame):
            X = X.values
            # Sample size for obtaining data
            len_x = len(X)
            # Number of features to acquire data
            col_x = X.shape[1]
            # Initialize tree list
            self.trees = []
            # If sample size is larger than the data size, adjust the sample size
            if self.sample_size > len_x:
                self.sample_size = len_x
        # Loop to generate each tree
        for i in range(self.n_trees):
            sample_idx = random.sample(list(range(len_x)), self.sample_size) # Randomly sample indices
            self.samples.append(sample_idx) # Save sample indices
            temp_tree = IsolationTree(self.height_limit, 0).fit(X[sample_idx, :]) # Train isolated tree with sample
            self.trees.append(temp_tree) # Add generated tree to tree list

        return self

    def fit_with_bias(self, sample: np.ndarray): # Given training sample
        """This method trains a tree using the given sample and adds it to the tree list."""
        temp_tree = IsolationTree(self.height_limit, 0).fit(sample) # Train isolated tree with sample
        self.trees.append(temp_tree) # Add generated tree to tree list
        return self

    def path_length(self, X: np.ndarray) -> np.ndarray: # Input data
        """
        X: input data.
        The path_length method calculates the path length of the input data in each tree.
        """
        pl_vector = [] # Initialize path length list
        # Check if the data is in DataFrame format, if so, convert to numpy array
        if isinstance(X, pd.DataFrame):
            X = X.values

        for x in X:
            pl = np.array([path_length_tree(x, t, 0) for t in self.trees])
            pl = pl.mean()
            pl_vector.append(pl)

        pl_vector = np.array(pl_vector).reshape(-1, 1)
        return pl_vector

    """
    Given the dataset X, calculate the prediction values for all data in x.
    Use each tree in self.trees to calculate the path length of x_i, and stop calculation when n_trees/2 + 1 decides if x is normal or abnormal.
    Return an ndarray: prediction values of all x data in X and the number of trees that made the decision.
    """
    def prediction_for_majority_voting(self, X: np.ndarray, threshold: float, return_pathLength=False) -> np.ndarray:
        prediction = []
        decision_trees_number = []
        scores = []
        paths_length = []
        if isinstance(X, pd.DataFrame):
            X = X.values
        c_val = c(len(X))
        for x in X:
            anomaly_number = 0
            normal_number = 0
            found = False
            anomalies_score = 0
            normals_scores = 0
            score = 0
            anomalies_pathLength = 0
            normals_pathLength = 0
            pathLength = 0
            for t in self.trees:
                if found == False:
                    p = path_length_tree(x, t, 0)
                    s = 2.0 ** (-1.0 * p / c_val)
                    if s >= threshold:
                        anomaly_number = anomaly_number + 1
                        anomalies_score = anomalies_score + s
                        anomalies_pathLength = anomalies_pathLength + p
                        if anomaly_number > self.n_trees / 2:
                            pred = ue._OUTLIER_PREDICTION_LABEL # Anomaly
                            decision_trees_number.append(anomaly_number + normal_number)
                            score = anomalies_score / (self.n_trees / 2 + 1)
                            pathLength = anomalies_pathLength / (self.n_trees / 2 + 1)
                            found = True
                    else:
                        normal_number = normal_number + 1
                        normals_scores = normals_scores + s
                        normals_pathLength = normals_pathLength + p
                        if normal_number > self.n_trees / 2:
                            pred = ue._NORMAL_PREDICTION_LABEL # Normal
                            decision_trees_number.append(normal_number + anomaly_number)
                            score = normals_scores / (self.n_trees / 2 + 1)
                            pathLength = normals_pathLength / (self.n_trees / 2 + 1)
                            found = True
                else:
                    break
            if normal_number == anomaly_number:
                score = (normals_scores + anomalies_score) / self.n_trees
                pathLength = (normals_pathLength + anomalies_pathLength) / self.n_trees
                if score >= threshold:
                    pred = ue._OUTLIER_PREDICTION_LABEL # Anomaly
                    decision_trees_number.append(anomaly_number + normal_number)
                else:
                    pred = ue._NORMAL_PREDICTION_LABEL # Normal
                    decision_trees_number.append(normal_number + anomaly_number)

            prediction.append(pred)
            scores.append(score)
            paths_length.append(pathLength)

        if return_pathLength == True:
            return prediction, decision_trees_number, scores, paths_length
        else:
            return prediction, decision_trees_number, scores

    def anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """
        Given a 2D matrix of observations X, calculate the anomaly score for each x_i and return an ndarray.
        """
        pathLength = self.path_length(X)
        return (2.0 ** (-1.0 * pathLength / c(len(X)))), pathLength

    def anomaly_score_with_details(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly score and data path length.
        """
        # TODO Delete before compute memory consumption
        return 2.0 ** (-1.0 * self.path_length(X) / c(len(X)))

    def anomaly_score_from_pathLength(self, pathLength: np.ndarray, X: np.ndarray) -> np.ndarray:
        """
        Calculate the anomaly score based on the given path length.
        """
        # TODO Delete before compute memory consumption
        return 2.0 ** (-1.0 * pathLength / c(len(X)))

    def predict_from_anomaly_scores(self, scores: np.ndarray, threshold: float) -> np.ndarray:
        """
        Given an array of scores and a score threshold, return an array of predictions:
        return -1 if the score is greater than or equal to the threshold, otherwise return 1.
        """
        predictions = [-1 if p[0] >= threshold else 1 for p in scores]
        return predictions

    def predict(self, X: np.ndarray, threshold: float) -> np.ndarray:
        "Shorthand for calling anomaly_score() and predict_from_anomaly_scores()."
        scores, pathLength = self.anomaly_score(X)
        predictions = self.predict_from_anomaly_scores(scores, threshold)
        return predictions, scores

    def predict_from_pathLength(self, X: np.ndarray, threshold: float, pathLength: np.ndarray) -> np.ndarray:
        """
        Shortcut for calling anomaly_score() and predict_from_anomaly_scores().
        Use the given path length and threshold to make predictions.
        """

        scores = self.anomaly_score_from_pathLength(pathLength, X)
        predictions = self.predict_from_anomaly_scores(scores, threshold)
        return predictions, scores

    def predict_and_get_pathLength(self, X: np.ndarray, threshold: float) -> np.ndarray:
        "Shorthand for calling anomaly_score() and predict_from_anomaly_scores()."
        scores = self.anomaly_score(X)
        predictions = self.predict_from_anomaly_scores(scores, threshold)
        return predictions, scores

    def fit_predict(self, X: np.ndarray, threshold: float) -> np.ndarray:
        "Fit to create a random forest"
        self.fit(X)
        "Calculate and return anomaly scores"
        return self.predict(X, threshold)


class IsolationTree:
    """This class implements the logic of a single isolated tree."""
    def __init__(self, height_limit, current_height):
        """
        height_limit: height limit of the tree.
        current_height: current height of the node.
        left, right: left and right subtrees.
        split_by, split_value: split feature and split value.
        exnodes: leaf node flag.
        size: number of samples contained in the node.
        n_nodes: number of nodes.
        """
        self.height_limit = height_limit
        self.current_height = current_height
        self.split_by = None
        self.split_value = None
        self.right = None
        self.left = None
        self.size = 0
        self.exnodes = 0
        self.n_nodes = 1
        self.node_sample = np.ndarray

    def fit(self, X: np.ndarray):
        """
        X: input data.
        The fit method recursively builds the tree, selects a feature to split, and splits the data into left and right subtrees based on the split value.
        """
        self.node_sample = X
        if len(X) <= 1 or self.current_height >= self.height_limit: # If the data size is less than or equal to 1 or the current height exceeds the height limit, set it as a leaf node and return
            self.exnodes = 1
            self.size = X.shape[0]
            return self

        split_by = random.choice(np.arange(X.shape[1])) # Randomly choose a feature to split
        X_col = X[:, split_by] # Get the column of the chosen feature
        # Get the minimum and maximum values of the feature
        min_x = X_col.min()
        max_x = X_col.max()
        # If the minimum value equals the maximum value, set it as a leaf node and return
        if min_x == max_x:
            self.exnodes = 1
            self.size = len(X)
            return self
        else:
            # Randomly choose a split value
            split_value = min_x + random.betavariate(0.5, 0.5) * (max_x - min_x)
            # Split the data into left and right subtrees based on the split value
            w = np.where(X_col < split_value, True, False)
            del X_col

            self.size = X.shape[0]
            self.split_by = split_by
            self.split_value = split_value
            # Recursively build the left subtree
            self.left = IsolationTree(self.height_limit, self.current_height + 1).fit(X[w])
            # Recursively build the right subtree
            self.right = IsolationTree(self.height_limit, self.current_height + 1).fit(X[~w])
            # Update the number of nodes
            self.n_nodes = self.left.n_nodes + self.right.n_nodes + 1

        return self


def c(n):
    """This function calculates the logarithmic correction term for path length, used to adjust the path length of leaf nodes to make the calculated path length more realistic."""
    if n > 2: # If the sample size is greater than 2, calculate the logarithmic correction term
        return 2.0 * (np.log(n - 1) + 0.5772156649) - (2.0 * (n - 1.) / (n * 1.0))
    elif n == 2: # If the sample size equals 2, return correction term 1
        return 1
    if n == 1: # If the sample size equals 1, return correction term 0
        return 0


def path_length_tree(x, t, e):
    """
    x: input data point.
    t: current node.
    e: current path length.
    The path_length_tree function recursively calculates the path length of the input data point in the tree.
    """
    e = e
    if t.exnodes == 1: # If the current node is a leaf node, add the correction term and return the path length
        e = e + c(t.size)
        return e
    else:
        a = t.split_by # Get the split feature
        if x[a] < t.split_value: # If the data point is in the left subtree, recursively calculate the path length of the left subtree
            return path_length_tree(x, t.left, e + 1)
        if x[a] >= t.split_value: # If the data point is in the right subtree, recursively calculate the path length of the right subtree
            return path_length_tree(x, t.right, e + 1)
