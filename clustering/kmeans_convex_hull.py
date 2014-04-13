import numpy as np
import random

# Constants
POINTS_FILE = 'point.txt'
HULLS_FILE = 'hulls.txt'

############################################################################################################
# KMeans clustering from http://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/ #
############################################################################################################

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

############################################################################################################
# Creating convex hull using QuickHull algorithm.
# Source: members.home.nl/wim.h.bakker/python/quickhull2d.py
############################################################################################################

def qhull(sample):
    link = lambda a,b: np.concatenate((a,b[1:]))
    edge = lambda a,b: np.concatenate(([a],[b]))

    def dome(sample, base): 
        h, t = base
        dists = np.dot(sample-h, np.dot(((0,-1),(1,0)),(t-h)))
        outer = np.repeat(sample, dists>0, axis=0)
        
        if len(outer):
            pivot = sample[np.argmax(dists)]
            return link(dome(outer, edge(h, pivot)),
                        dome(outer, edge(pivot, t)))
        else:
            return base

    if len(sample) > 2:
        axis = sample[:][0]
        base = np.take(sample, [np.argmin(axis), np.argmax(axis)], axis=0)
        return link(dome(sample, base),
                    dome(sample, base[::-1]))
    else:
        return sample

def plot_hull(hull, sample):
    from pylab import plot
    import pylab

    for s in sample:
        plot([s[0]], [s[1]], 'b.')

    i = 0
    while i < len(hull)-1:
        plot([hull[i][0], hull[i+1][0]], [hull[i][1], hull[i+1][1]], color='k')
        i = i + 1

    plot([hull[-1][0], hull[0][0]], [hull[-1][1], hull[0][1]], color='k')

    pylab.show()

############################################################################################################

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

def empty_file(file_loc):
    open(file_loc, 'w').close()

def write_to_files(cens, clus):
    empty_file(POINTS_FILE)
    empty_file(HULLS_FILE)

    for i in range(0, len(cens)):
        cluster = clus[i]
        hull = qhull(cluster)

        for clu in cluster:
            pt_code = 'L.circleMarker([' + str(clu[0]) + ', ' + str(clu[1]) + '], {radius: r, color: \'' + get_color(i) + '\', opacity: o}).addTo(map);\n'
            append_to_file('points.txt', pt_code)

        hull_code = 'L.polygon([['
        for vertex in hull:
            hull_code += str(vertex[0]) + ', ' + str(vertex[1]) + '], ['
        hull_code = hull_code[:-3] + ']).addTo(map);\n'
        append_to_file('hulls.txt', hull_code)

def get_coordi(lines):
    coordi = []
    for line in lines:
        tokens = line.strip().split()
        if len(tokens) >= 3:
            coordi.append([float(tokens[1].strip()), float(tokens[2].strip())])
    return coordi

def read_file(file_loc):
    content = []
    try:
        with open(file_loc, 'r') as inp:
            content = inp.readlines()
    except IOError:
        print 'Cannot read file: ' + file_loc
    return content

def main():
    lines = read_file('CX.txt')
    X = get_coordi(lines)
    K = 15
    cens, clus = find_centers(X, K)
    write_to_files(cens, clus)

if __name__ == '__main__':
    main()
