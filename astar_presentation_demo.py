#!/usr/bin/env python

import numpy as np
import time

class mapinfo:
    OBS = 1
    FREE = 0
    START = 2
    DEST = 3
    mapping = {'*':OBS,
               ' ':FREE,
               '#':START,
               '@':DEST}

def dijkstra(map_, start, dest):
    '''
    (y,x)
    '''
    assert isinstance(start,tuple)
    assert isinstance(dest,tuple)
    assert len(start) == len(dest) == 2

    if( map_[start] == mapinfo.OBS or
        map_[dest]  == mapinfo.OBS ):
        print "start or dest is OBS"
        return None

    ysize, xsize = map_.shape

    dire = (( 0,-1),
            ( 0, 1),
            ( 1, 0),
            (-1, 0),
            
            (-1,-1),
            (-1, 1),
            ( 1, 1),
            ( 1,-1),)

    look = []
    
    cost = np.full(map_.shape, np.inf)
    estcost = np.zeros(map_.shape)
    last = np.full(map_.shape+(2,), 0, dtype=int)
    visited = np.full(map_.shape, 0)

    path = []

    #pp = [1.7,-0.7]
    pp = [1 , 0]

    for j in xrange(ysize):
        for i in xrange(xsize):
            last[j,i] = [j,i]
            #e0 = abs(dest[0]-j)+abs(dest[1]-i) 
            e0 = np.sqrt(np.power(dest[0]-j,2)+np.power(dest[1]-i,2)) 
            #e0 = (np.power(dest[0]-j,2)+np.power(abs(dest[1]-i),2))

            e1 = np.sqrt(np.power(start[0]-j,2)+np.power(start[1]-i,2)) 
            estcost[j,i] = pp[0]*e0 + \
                           pp[1]*e1
            

    def printer(pos):
        for j in xrange(ysize):
            print ''.join(map(lambda i: '%s%c\033[0m'%('\033[1m' if (j==pos[0] and i==pos[1]) else ('\033[48;5;243m' if visited[j,i] else ''),
                                                       '+' if (j,i) in path else('O' if (j==pos[0] and i==pos[1]) else (' ' if map_[j,i]==mapinfo.FREE else '*'))),
                              [i for i in xrange(xsize)] ))

    def getnb(a):
        return filter(lambda x: ( x[1]>=0 and x[1]<xsize and 
                                  x[0]>=0 and x[0]<ysize and
                                  map_[x] != mapinfo.OBS ),
                      map(lambda x:(a[0]+x[0], a[1]+x[1]),
                          dire))

    #p = [0.3, 0.7]
    #p = [0, 1]
    p = [1, 0]

    def costcmp(x,y):
        cx = p[0]*cost[x] + p[1]*estcost[x]
        cy = p[0]*cost[y] + p[1]*estcost[y]
        if(cx>cy):
            return 1
        elif(cx<cy):
            return -1
        else:
            return 0

    look.append(start)
    cost[start] = 0

    def getpath(x):
        ret = [x]
        while True:
            #print ret[0]#,x
            if((last[ret[0]] == ret[0]).all()):
                if(ret[0] == start):
                    return ret
                else:
                    #print last[ret[0]]
                    raise Exception("wtf?!")
            else:
                ret = [tuple(last[ret[0]])] + ret
            

    while(look):
        look.sort(cmp = costcmp)
        head = look[0]
        look = look[1:]

        if(True):
            time.sleep(0.05)
            print "\033c"
            printer(head)
            print ""
            print look

        visited[head] = 1
        nbs = getnb(head)

        tmpcost = cost[head] + 1
        for i in nbs:
            if(visited[i] == 1): # if not stop here, may cause loop
                continue
            if i == dest:
                last[i] = head
                path = getpath(i)
                time.sleep(0.05)
                print "\033c"
                printer(i)
                print ""
                print look
                return path

                
            if(#visited[i] == 0 and 
               not(i in look)):
                look.append(i)
            if(tmpcost < cost[i]):
                cost[i] = tmpcost
                last[i] = head
    
    return []

if __name__ == "__main__":
    map_ = "\
                                 ,\
                                 ,\
          ****        ****       ,\
          *  **     @ *  **      ,\
    *******   *********   *      ,\
    *             *       ***    ,\
    *             *         *    ,\
    *    #        *         *    ,\
    *             *              ,\
    *             *         *    ,\
    ******     *********    *    ,\
                                 ,\
                                 \
"
    map__ = np.array(map(lambda x:map(lambda x:mapinfo.mapping[x],x),
                         map_.split(',')))

    print "shape:",map__.shape

    def getstart(m):
        r = np.where(m==mapinfo.START)
        return (r[0][0],r[1][0])

    def getdest(m):
        r = np.where(m==mapinfo.DEST)
        return (r[0][0],r[1][0])

    start = getstart(map__)
    dest = getdest(map__)

    map__[map__==mapinfo.START] = mapinfo.FREE
    map__[map__==mapinfo.DEST] = mapinfo.FREE

    print dijkstra(map__,
                   start,
                   dest)
