from collections import defaultdict
from math import inf
import random
import csv
import math

def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    length =  len(points)
    centre = []
    
    for point in zip(*points):
        centre.append(sum(point)/length)
    return centre


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    centroid = []
    centre = defaultdict(list)
    for index, point in zip(assignments,data_set):
        centre[index].append(point)
        
    for key in centre.keys():
        centroid.append(point_avg(centre[key]))
    return centroid


def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(x, y):
    """
    Returns the Euclidean distance between a and b
    """
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):
    
    dataset = []
    with open(dataset_file) as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            datapoint = []
            for index in range(0,len(row)):
                datapoint.append(int(row[index]))
            dataset.append(datapoint)
    
    return dataset


def cost_function(clustering):
    
    cost =0
    for key in clustering.keys():
        values = clustering[key]
        centre = point_avg(values)
        for value in values:
            cost += distance(value, centre)
    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
