'''
    Title: classify.py
    Author: Guillem Camats Felip, Adrià Juvé Sánchez, Martí La Rosa Ramos, Xavier Nadal Reales
    Date: 25-5-2020
    Code version: 1.0.0
    Availability: https://github.com/santo0/algorithms_and_complexity_challenge
'''
import random


def calculate_min_puntuation(new_cluster, score_matrix):
    '''Calculates minimum punutation of cluster'''
    new_points = []
    for key in new_cluster:
        new_min = -1
        for number in new_cluster[key]:
            new_puntuation = -1
            for i in range(len(new_cluster[key])):
                new_puntuation += score_matrix[number][new_cluster[key][i]]
            if new_min == -1 or new_min > new_puntuation:
                new_min = new_puntuation
                new_min_number = number
        new_points.append(new_min_number)
    return new_points


def create_clustering(points, score_matrix):
    '''Creates clustering'''
    new_clusters = {str(point): [] for point in points}
    for i in range(len(score_matrix)):
        new_min = -1
        for point in points:
            if i == point or new_min == -1 or new_min > score_matrix[i][point]:
                new_min = score_matrix[i][point]
                closest_point = point
        new_clusters[str(closest_point)].append(i)
    next_centers = calculate_min_puntuation(new_clusters, score_matrix)
    if all(elem in next_centers for elem in points):
        return new_clusters

    return create_clustering(next_centers, score_matrix)


def clustering(median_sample_list, score_matrix):
    '''Does clustering and replaces numbers with country names'''
    points = []
    i = 0
    while i < 6:
        element = random.randrange(0, 30, 1)
        if element not in points:
            points.append(element)
            i += 1
    clustering_with_geolocalitation = {}
    result_clusters = create_clustering(points, score_matrix)
    for key in result_clusters.keys():
        clustering_with_geolocalitation.update(
            {median_sample_list[int(key)].geolocation: []})
        for value in result_clusters[key]:
            clustering_with_geolocalitation[median_sample_list[int(key)].geolocation].append(
                median_sample_list[value].geolocation)
    return clustering_with_geolocalitation
