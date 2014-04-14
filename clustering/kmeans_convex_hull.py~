#from __future__ import division
import numpy as np
import random, re

# Constants
POINTS_FILE = 'points.txt'
HULLS_FILE = 'hulls.txt'
CLUS_FILE = 'clusters.txt'

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
# Prediction
############################################################################################################

def predict(ys, index, data):
    y_predicted = 0
    for i in range(index, 1, -1):
        y_predicted += data[str(i - 1)] * (i - 1)
    return y_predicted / sum(range(1, index))

def predict_all(drugs_per_clus, index):
    epsilons = {}

    clusters = drugs_per_clus.keys()
    clusters.sort()
    for i in range(0, len(clusters)):
        cluster = clusters[i]
        ys = drugs_per_clus[cluster].keys()
        ys.sort()
        data = drugs_per_clus[cluster]
        prediction = predict(ys, index, data)
        drugs_per_clus[cluster][str(index)] = prediction

        epsilon = 0
        for j in range(3, index):
            epsilon += data[str(j + 1)] - predict(ys, j + 1, data)
        epsilons[i + 1] = int(epsilon)

    return drugs_per_clus, epsilons

############################################################################################################

def append_to_file(file_loc, data):
    with open(file_loc, 'a') as output:
        output.write(data)

def get_color(i):
    if i < 5000:
        return '#1a9850'
    elif i < 10000:
        return '#66bd63'
    elif i < 15000:
        return '#a6d96a'
    elif i < 20000:
        return '#fee08b'
    elif i < 25000:
        return '#fdae61'
    elif i < 30000:
        return '#f46d43'
    else:
        return '#d73027'

def empty_file(file_loc):
    open(file_loc, 'w').close()

def write_to_files(cens, clus, counts):
    empty_file(POINTS_FILE)
    empty_file(HULLS_FILE)

    for i in range(0, len(cens)):
        cluster = clus[i]
        hull = qhull(cluster)

        for clu in cluster:
            pt_code = 'L.circleMarker([' + str(clu[0]) + ', ' + str(clu[1]) + '], {radius: r, color: \'' + get_color(counts[str(clu[0]) + '|' + str(clu[1])]) + '\', opacity: o}).addTo(map);\n'
            append_to_file(POINTS_FILE, pt_code)

        hull_code = 'L.polygon([['
        for vertex in hull:
            hull_code += str(vertex[0]) + ', ' + str(vertex[1]) + '], ['
        hull_code = hull_code[:-3] + ']).addTo(map);\n'
        append_to_file('hulls.txt', hull_code)

def reformat_aggr(drugs_per_clus):
    reformat = {}

    for clus in drugs_per_clus:
        clus_str = str(clus + 1)
        start = False
        first = 0
        if clus_str not in reformat:
            reformat[clus_str] = {}
            reformat[clus_str]['label'] = 'Cluster ' + clus_str
            reformat[clus_str]['data'] = []
        qtrs = drugs_per_clus[clus].keys()
        qtrs.sort()
        for qtr in qtrs:
            if not start:
                first = int(drugs_per_clus[clus][qtr])
                start = True
            reformat[clus_str]['data'].append([qtr, first - int(drugs_per_clus[clus][qtr])])

    return reformat

def get_clus_aggr(lines, clus, zips):
    drug_by_zip = {}
    drugs_per_clus = {}

    for line in lines:
        qtr, zip_c, cnt = re.split('\t|\|', line)
        if zip_c not in drug_by_zip:
            drug_by_zip[zip_c] = {}
        drug_by_zip[zip_c][qtr] = float(cnt)
    for i in range(0, len(clus)):
        for coordi in clus[i]:
            zip_code = zips[str(coordi[0]) + '|' + str(coordi[1])]
            drug = drug_by_zip[zip_code]
            qtrs = drug.keys()
            qtrs.sort()
            for qtr in qtrs:
                if i in drugs_per_clus:
                    if qtr in drugs_per_clus[i]:
                        drugs_per_clus[i][qtr] += drug[qtr]
                    else:
                        drugs_per_clus[i][qtr] = drug[qtr]
                else:
                    drugs_per_clus[i] = {}
                    drugs_per_clus[i][qtr] = drug[qtr]

    return drugs_per_clus

def get_coordi(lines):
    coordi = []
    counts = {}
    zips = {}

    for line in lines:
        tokens = line.strip().split()
        if len(tokens) >= 4:
            x = float(tokens[1].strip())
            y = float(tokens[2].strip())
            coordi.append([x, y])
            counts[str(x) + '|' + str(y)] = int(tokens[3].strip())
            zips[str(x) + '|' + str(y)] = tokens[0]

    return coordi, counts, zips

def read_file(file_loc):
    content = []
    try:
        with open(file_loc, 'r') as inp:
            content = inp.readlines()
    except IOError:
        print 'Cannot read file: ' + file_loc
    return content

def main():
    lines = read_file('zip_coordi_lkp')
    X, counts, zips = get_coordi(lines)
    K = 7
    cens, clus = find_centers(X, K)
    lines = read_file('../mapreduce/drug_by_quarter')
    drugs_per_clus = get_clus_aggr(lines, clus, zips)
    drugs_per_clus, epsilons = predict_all(drugs_per_clus, 5)
    print reformat_aggr(drugs_per_clus)
    print epsilons
    write_to_files(cens, clus, counts)

if __name__ == '__main__':
    main()
