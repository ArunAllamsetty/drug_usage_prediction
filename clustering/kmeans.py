import numpy as np
import random
 
def cluster_points(X, mu):
    clusters  = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm([x[0]-mu[i[0]][0], x[1]-mu[i[0]][1]])) for i in enumerate(mu)], key=lambda t:t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters
 
def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis = 0))
    return newmu
 
def has_converged(mu, oldmu):
    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])
 
def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        print 'Iterating'
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return(mu, clusters)

def append_to_file(file_loc, data):
    with open(file_loc, 'a') as output:
        output.write(data)

def get_color(i):
    if i == 0:
        return '#FF0000'
    elif i == 1:
        return '#00FF00'
    elif i == 2:
        return '#0000FF'
    elif i == 3:
        return '#FFFF00'
    elif i == 4:
        return '#00FFFF'
    elif i == 5:
        return '#FF00FF'
    else:
        return '#003300'

def getCoordi(lines):
    coordi = []
    for line in lines:
        tokens = line.strip().split()
        if len(tokens) >= 3:
            coordi.append([float(tokens[1].strip()), float(tokens[2].strip())])
    return coordi

def readFile(file_loc):
    content = []
    try:
        with open(file_loc, 'r') as inp:
            content = inp.readlines()
    except IOError:
        print 'Cannot read file: ' + file_loc
    return content

def main():
    lines = readFile('CX.txt')
    X = getCoordi(lines)
    #X = [[1, 1], [2, 1], [3, 2], [1, 2], [1, 3]]
    K = 7
    cens, clus = find_centers(X, K)
    for i in range(0, len(cens)):
        for clu in clus[i]:
            code = 'L.circleMarker([' + str(clu[0]) + ', ' + str(clu[1]) + '], {radius: r, color: \'' + get_color(i) + '\', opacity: o}).addTo(map);\n'
            append_to_file('points.txt', code)

if __name__ == '__main__':
    main()
