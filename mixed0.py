# -*- coding: utf-8 -*-  
from os import system

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

# Entry a_ij of adjacency matrix A
def a(i,j):
    assert 0 <= i and i < n
    assert 0 <= j and j < n
    return 'a'+str(i*n+j)

# Entry u_ij of underlying adjacency matrix
def u(i,j):
    assert 0 <= i and i < n
    assert 0 <= j and j < n
    return 'u'+str(i*n+j)

# Entry p_ij of permutation matrix
def p(i,j):
    assert 0 <= i and i < n
    assert 0 <= j and j < n
    return 'p'+str(i*n+j)

# Auxiliary variable for the constraint of the number of symmetric 1's in rows
def s(i,j):
    assert 0 <= i and i < n
    assert 0 <= j and j < n
    return 's'+str(i*n+j)

# Auxiliary variable to compute A^2
def t(i,j,s):
    assert 0 <= i and i < n
    assert 0 <= j and j < n
    assert 0 <= s and s < n
    return 't'+str(i*n*n+j*n+s)

# Sum of a vector of variables
def sum(v):
    q = '+1'+'*'+v[0];
    for x in v[1:]:
        q += '+1'+'*'+x;
    return q

# Sum of a vector of variables without coefficients
def sum_ncf(v):
    q = '+'+v[0];
    for x in v[1:]:
        q += '+'+x;
    return q

# Subtraction of a vector of variables
def sub(v):
    q = '-1'+'*'+v[0];
    for x in v[1:]:
        q += '-1'+'*'+x;
    return q

# Subtraction of a vector of variables without coefficients
def sub_ncf(v):
    q = '-'+v[0];
    for x in v[1:]:
        q += '-'+x;
    return q

# Lexicographic symmetry break with first k variables
def leq(i,j):
    k = n-d-1
    q = range(k); 
    opb.write(sum_ncf([str(2**(k-1-t))+'*'+u(j,t) for t in q])+sub_ncf([str(2**(k-1-t))+'*'+u(i,t) for t in q])+'>=0;\n')

# Writes the Pseudo-Boolean encoding of the problem to file opb
def write_opb():
    # Set 1: The number of 1's in rows and columns of A
    for i in range(n):
        opb.write(sum([a(i,j) for j in range(n)])+'='+str(r+z)+';\n')
    for j in range(n):                       
        opb.write(sum([a(i,j) for i in range(n)])+'='+str(r+z)+';\n')
            
    # Set 2: Loops are not allowed
    for i in range(n):
        opb.write('1'+'*'+a(i,i)+'=0;\n')
    
    # Definition of s_ij. s_ij <=> a_ij && a_ji
    for i in range(n):
        for j in range(n):
            opb.write('-1'+'*'+a(i,j)+'-1'+'*'+a(j,i)+'+1'+'*'+s(i,j)+'>-2;\n')
            opb.write('-1'+'*'+s(i,j)+'+1'+'*'+a(i,j)+'>-1;\n')
            opb.write('-1'+'*'+s(i,j)+'+1'+'*'+a(j,i)+'>-1;\n')
    
    # Definition of t_ijk. t_ijk <=> a_ik && a_kj
    for i in range(n):
        for j in range(n):
            for k in range(n):
                opb.write('-1'+'*'+a(i,k)+'-1'+'*'+a(k,j)+'+1'+'*'+t(i,j,k)+'>-2;\n')
                opb.write('-1'+'*'+t(i,j,k)+'+1'+'*'+a(i,k)+'>-1;\n')
                opb.write('-1'+'*'+t(i,j,k)+'+1'+'*'+a(k,j)+'>-1;\n')

    if almost == 0:
        # Set 3: Each vertex has r edges (I)
        for j in range(n):
            opb.write(sum([s(i,j) for i in range(n)])+'='+str(r)+';\n')
    
        # Set 4: Each vertex has r edges (II)
        for i in range(n):
            opb.write(sum([t(i,i,k) for k in range(n)])+'='+str(r)+';\n')
    
        # Set 5: Every vertex reach all other vertices with trails of length at most 2
        for i in range(n):
            for j in range(n):
                if i != j:
                    opb.write('1'+'*'+a(i,j)+sum([t(i,j,k) for k in range(n)])+'=1;\n')

    if almost == 1:
        # Set 6: P is a permutation matrix
        for i in range(n):
            opb.write(sum([p(i,j) for j in range(n)])+'=1;\n')
        for j in range(n):                       
            opb.write(sum([p(i,j) for i in range(n)])+'=1;\n')

        # Set 7: Encoding of equation I + A + A^2 = J + rI + P 
        for i in range(n):
            opb.write(sum([t(i,i,k) for k in range(n)])+'='+str(r)+';\n')
            
        for i in range(n):
            opb.write(sum([s(i,j) for j in range(n)])+'='+str(r)+';\n')
    
        for i in range(n):
            for j in range(n):
                if i != j:
                    opb.write('-1'+'*'+p(i,j)+'+1'+'*'+a(i,j)+sum([t(i,j,k) for k in range(n)])+'=1;\n')

        # Set 8: There are no selfrepeats
        for i in range(n):
            opb.write('1'+'*'+p(i,i)+'=0;\n')

    if lex == 1:
        # Set 9: Link underlying matrix
        for i in range(n):
          for j in range(n):
            opb.write('1'+'*'+u(i,j)+'-1'+'*'+a(i,j)+'>=0;\n')
            opb.write('1'+'*'+u(j,i)+'-1'+'*'+a(i,j)+'>=0;\n')
            opb.write('1'+'*'+a(i,j)+'+1'+'*'+a(j,i)+'-1'+'*'+u(i,j)+'>=0;\n')

        # Set 10: Underlying matrix is symmetric
        for i in range(n):
            for j in range(i+1,n):
                opb.write('1'+'*'+u(i,j)+'-1'+'*'+u(j,i)+'=0;\n')
    
        if almost == 0:
            # Set 11: Partitioned lexicographic symmetry break (for mixed Moore graphs)
            k = 0
            for i in range(r):
                for j in range(r-2):
                    leq(k,k+1)
                    k += 1
                if r >= 2: k += 1
                for j in range(z-1):
                    leq(k,k+1)
                    k += 1
                k += 1
            for i in range(z):
                for j in range(r-1):
                    leq(k,k+1)
                    k += 1
                k += 1
                for j in range(z-1):
                    if closed == 0 or j != z-2:
                        leq(k,k+1)
                    k += 1
                k += 1
        else: # almost == 1
            # Set 11: Partitioned lexicographic symmetry break (for mixed almost Moore graphs)
            k = 0
            for i in range(r):
                nr = r-2
                nz = z-1
                if i == 0:
                    if repeat == 0:
                        nr = r-3
                    if repeat == 1:
                        nz = z-2
                for j in range(nr):
                    leq(k,k+1)
                    k += 1
                if i == 0:
                    if r >= 2 and repeat != 0: k += 1
                    elif r >= 3 and repeat == 0: k += 1
                elif r >= 2: k += 1
                for j in range(nz):
                    leq(k,k+1)
                    k += 1
                if i == 0:
                    if repeat != 1: k += 1
                    elif z >= 2: k += 1
                else:
                    k += 1
            for i in range(z):
                nr = r-1
                nz = z-1
                if i == 0:
                    if repeat == 2:
                        nr = r-2
                    if repeat == 3:
                        nz = z-2
                for j in range(nr):
                    leq(k,k+1)
                    k += 1
                if i == 0:
                    if repeat != 2: k += 1
                    elif r>=2: k += 1
                else:
                    k += 1
                for j in range(nz):
                    leq(k,k+1)
                    k += 1
                if i == 0:
                    if repeat != 3: k += 1
                    elif z>=2: k += 1
                else: 
                    k += 1

    if almost == 0:
        # Define predetermined a_ij entries for mixed Moore graphs
        if closed == 1:
            pre = 'predetermined-entries/closed/'
        else:
            pre = 'predetermined-entries/free/'
        
        f = open(pre + str(n),'r')
        i = 0
        for line in f:
            j = 0
            for x in line:
                if x == '0' or x == '1':
                    opb.write('1'+'*'+a(i,j)+'='+x+';\n')
                if x != ' ':
                    j += 1
            i += 1
        f.close()


    else:
        # Define predetermined a_ij entries for mixed almost Moore graphs
        pre = 'predetermined-entries/almost/'
        
        f = open(pre + str(n) + '-' + str(repeat),'r')
        i = 0
        for line in f:
            j = 0
            for x in line:
                if x == '0' or x == '1':
                    opb.write('1'+'*'+a(i,j)+'='+x+';\n')
                if x != ' ':
                    j += 1
            i += 1
        f.close()


# Read the solution given by glucose SAT solver
def get_solution():
    line = sol.readline()

    if line != 'UNSAT\n':
        res = ''
        v = []
        i = 0
        for x in line:
            if i == n*n:
                break
            if x != ' ':
                res += x
            else:
                res = int(res)
                if(res > 0): v.append(1)
                else: v.append(0)
                res = ''
                i += 1
        k = 0
        A = [] 
        for i in range(n):
            A.append([v[i*n+j] for j in range(n)])

        if output == 0:
            for a in A:
                print a

        elif output == 1:
            print A

        else:
            if almost == 0:
                path = 'solved.nosinc/graphs/'
                if closed == 1 and lex == 0:
                    path += 'moore/closed/'
                elif closed == 0 and lex == 1:
                    path += 'moore/lex1/'
                elif closed == 1 and lex == 1:
                    path += 'moore/lex2/'
                else:
                    return 'SAT'

            out = open(path + str(n),'w')
            for i in range(n):
                for j in range(n):
                    out.write(str(A[i][j]) + ' ')
                out.write('\n')
            out.close()

        return 'SAT'

    else:
        return 'UNSAT'


# The order of the graph
n = int(raw_input('n: '))

# almost=0: search mixed Moore graphs, almost=1: search mixed almost Moore graphs
almost = int(raw_input('almost: '))

# lex=0: no symmetry break, lex=1: lexicographic symmetry break
lex = int(raw_input('lex: '))

# closed=0: don't close some directed cycles, closed=1: close some directed cycles
closed = int(raw_input('closed: '))

# suffix added at the end of output files
suffix = int(raw_input('suffix: '))

# more=0: don't configure more options, more=1: to configure more options
more = int(raw_input('more: '))

sfx = str(n) + '-' + str(almost) + '-' + str(lex) + '-' + str(closed) + '-' + str(more) + '-'

# different outputs for adjacency matrix
output = 0

# sols=1: search for the first solution found, sols=0: search all solutions
sols = 1

if more == 1:
    # output = int(raw_input('output: '))
    sols = int(raw_input('sols: '))

sfx += str(output) + '-' + str(sols) + '-' + str(suffix)

if almost == 0:
    (r,z) = rz_mixed(n)
    d = r+z

    # Write Pseudo-Boolean problem to file opb
    opb = open('fopb'+sfx+'.nosinc','w')
    write_opb()
    opb.close()
    
    system('rm cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc')

    if sols == 1:
        minisat = './minisat+/minisat+_bignum_static '
        glucose = './glucose-3.0.nosinc/simp/glucose_static '

        # Translate the Pseudo-Boolean problem to CNF using minisat+
        system(minisat + 'fopb'+sfx+'.nosinc -cnf=cnf'+sfx+'.nosinc')
        # Solve the CNF problem using Glucose SAT solver
        system(glucose + 'cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc')

        # Read solution given by Glucose SAT solver
        sol = open('fsol'+sfx+'.nosinc','r')
        get_solution()
        sol.close()

        system('rm fopb'+sfx+'.nosinc cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc')

    if sols == 0:
        minisat = './minisat+/minisat+_bignum_static -all '
        # Translate the Pseudo-Boolean problem to CNF using minisat+ and solve the CNF problem using minisat SAT solver
        system(minisat + 'fopb'+sfx+'.nosinc > all-solutions.nosinc')
        # Count the number of solutions found
        system('grep -c -E "^c MODEL" all-solutions.nosinc')

        system('rm fopb'+sfx+'.nosinc')
        

else: # almost == 1
    (r,z) = rz_almost(n)
    d = r+z

    for i in range(4):
        # repeat: a number in the interval [0,1,2,3]. Four different cases to consider for finding mixed almost Moore graphs (see Section 4.3.2 of the thesis)
        repeat = i
        print "repeat = " + str(repeat)

        # Write Pseudo-Boolean problem to file opb
        opb = open('fopb'+sfx+'.nosinc','w')
        write_opb()
        opb.close()

        minisat = './minisat+/minisat+_bignum_static '
        glucose = './glucose-3.0.nosinc/simp/glucose_static '

        system('rm cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc')
        # Translate the Pseudo-Boolean problem to CNF using minisat+
        system(minisat + 'fopb'+sfx+'.nosinc -cnf=cnf'+sfx+'.nosinc')
        # Solve the CNF problem using Glucose SAT solver
        system(glucose + 'cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc')

        # catch read error when minisat+ says that the problem is trivially unsatisfiable 
        result='UNSAT'
        try:
            # Read solution given by Glucose SAT solver
            sol = open('fsol'+sfx+'.nosinc','r')
            result=get_solution()
            sol.close()
        except:
            print "Read solution error"

        system('rm cnf'+sfx+'.nosinc fsol'+sfx+'.nosinc fopb'+sfx+'.nosinc')

        if result == 'SAT' and sols == 1:
            break

# Local Variables:
# python-indent-offset: 4
# End:
