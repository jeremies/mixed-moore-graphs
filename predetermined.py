# -*- coding: utf-8 -*-  






# Returns the parameters r and z given n for mixed Moore graphs
def rz_mixed(n): 
    nrz = [(6,1,1), (12,1,2), (18,3,1), (20,1,3), (30,1,4), (40,3,3), (42,1,5), (54,3,4), (84,7,2), (88,3,6)]
    for t in nrz:
        if t[0] == n:
            return (t[1],t[2])
    print "the value of n is not in the list" 
    return (0,0)

# Returns the parameters r and z given n for mixed almost Moore graphs
def rz_almost(n):
    nrz = [(26,4,1), (50,6,1), (68,4,4), (84,6,3), (10,2,1), (18,2,2), (28,2,3), (40,2,4), (54,2,5)]
    for t in nrz:
        if t[0] == n:
            return (t[1],t[2])
    print "the value of n is not in the list" 
    return (0,0)

def edge(i,j):
    A[i][j] = 1
    A[j][i] = 1

def arc(i,j):
    A[i][j] = 1
    A[j][i] = 0

# The order of the graph
n = int(raw_input('n: '))

# almost=0: search mixed Moore graphs, almost=1: search mixed almost Moore graphs
almost = int(raw_input('almost: '))

# closed=0: don't close some directed cycles, closed=1: close some directed cycles
closed = int(raw_input('closed: '))

# Four different cases to consider for finding mixed almost Moore graphs (see Section 4.3.2 of the thesis)
repeat = int(raw_input('repeat: '))

print ""

if almost == 0:
    (r,z) = rz_mixed(n)
else:
    (r,z) = rz_almost(n)
d = r+z

# Initialize the matrix with all entries not determined (=2)
A = [[2 for j in range(n)] for i in range(n)]

# Spanning tree of G
for i in range(z):
    arc(n-1,n-1-d+i)

for i in range(r):
    edge(n-1,n-1-r+i)

k = 0
for i in range(r):
    nr = r-1;
    nz = z;
    if i == 0 and almost == 1:
        if repeat == 0:
            nr = r-2; # one edge missing
        elif repeat == 1:
            nz = z-1; # one arc missing
    for j in range(nr):
        edge(n-2-i,k)
        k += 1
    for j in range(nz):
        arc(n-2-i,k)
        k += 1

for i in range(z):
    nr = r;
    nz = z;
    if i == 0 and almost == 1:
        if repeat == 2:
            nr = r-1; # one edge missing
        elif repeat == 3:
            nz = z-1; # one arc missing
    for j in range(nr):
        edge(n-2-r-i,k)
        k += 1
    for j in range(nz):
        arc(n-2-r-i,k)
        k += 1

if almost == 0:
    # A_ii = 0
    i = 0
    k = 0
    for l in range(r):
        for m in range(d-1):
            for j in range(d-1):
                A[i][k+j] = 0
            i += 1
        k += d-1
    for l in range(z):
        for m in range(d):
            for j in range(d):
                A[i][k+j] = 0
            i += 1
        k += d
    
    for i in range(d+1):
        for j in range(n):
            if A[n-1-d+i][j] == 2:
                A[n-1-d+i][j] = 0
                
    for i in range(r*(d-1)):
        for j in range(d+1):
            if A[i][n-1-d+j] == 2:
                A[i][n-1-d+j] = 0
    
    k = r*(d-1)
    for m in range(z):
        for i in range(r):
            A[k+i][n-1] = 0
        k += d
    
    # Some directed cycles closed
    if closed == 1:
        for i in range(z):
            arc(n-1-(i+1)*d-1,n-1)
        for i in range(n):
            if A[i][n-1] == 2:
                A[i][n-1] = 0
        h = n-2-d
        for l in range(z):
            k = 0
            for m in range(r):
                for j in range(r-1):
                    A[h-l*d][k+j] = 0
                    A[k+j][h-l*d] = 0
                k += d-1
        for l in range(z):
            k = r*(d-1)
            for m in range(z):
                for j in range(r):
                    A[h-l*d][k+j] = 0
                A[h-l*d][k+d-1] = 0
                k += d
        for l in range(z):
            k = n-1-d
            for j in range(d):
                A[h-l*d][k+j] = 0

else: # almost == 1
    i = 0
    k = 0
    for l in range(d):
        if l < r:
            nr = r-1
            nd = d-1
            nz = z
            if l == 0:
                if repeat == 0:
                    nr = r-2
                    nd = d-2
                elif repeat == 1:
                    nd = d-2
                    nz = z-1
        else:
            nr = r
            nd = d
            nz = z
            if l == r:
                if repeat == 2:
                    nr = r-1
                    nd = d-1
                elif repeat == 3:
                    nd = d-1
                    nz = z-1
        for m in range(nr):
            for j in range(nd):
                A[i][k+j] = 0
            i += 1
        i += nz
        k += nd

    # a_ii = 0
    for i in range(n):
        A[i][i] = 0

    q = range(d+1)
    if repeat == 0 or repeat == 1:
        q.remove(d-1)
    else:
        q.remove(z-1)
    for i in q:
        for j in range(n):
            if A[n-1-d+i][j] == 2:
                A[n-1-d+i][j] = 0
    
# Print matrix with predetermined entries
for i in range(n):
    for j in range(n):
        print str(A[i][j]) ,
    print ""

