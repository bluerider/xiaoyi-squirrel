##!/bin/python3

import random
import sys

## Xiaoyi's squirrel problem
## There's a squirrel, tree, and scattered nuts
## The squirrel must retrieve a nut, take it to the tree, and repeat
## find the minimum number of steps the squirrel will have to take
## to obtain all nuts (can only grab one nut at a time)
## The squirrel also must take the closest nut to them in order of
## preference : up/down, left/right
## I think what they are saying is that they want the top left-most
## closest nut
## function also returns the total distance as value
## return total distance : int
def main(test: int = 0,
         squirrel: tuple = (),
         tree: tuple = (),
         nuts: list = [],
         plot: bool = False) -> int:
    ## generate the game
    if test == 0:
        ## if passing in values, use those
        squirrel, tree, nuts = genGame(squirrel = squirrel,
                                       tree = tree,
                                       nuts = nuts)
    else:
        ## run some unit tests if called
        squirrel, tree, nuts = unitTests(test)
    ## sanity check
    if squirrel == 0:
        print("Missing initial values")
        return
    ## get the initial step
    initial_step, rest_of_nuts = getInitialStep(squirrel = squirrel, 
                                                tree = tree, 
                                                nuts = nuts)
    ## get the distance for the squirrel -> nut -> tree
    ## for the initial step
    first_route = distance(origin = squirrel, 
                           nut = initial_step) + distance(origin = tree,
                                                          nut = initial_step)
    ## get the distances for the rest of the nuts from the tree
    rest_route_distance = getDistances(tree = tree,
                                       nuts = rest_of_nuts)
    ## get the total distance
    total_distance = first_route + rest_route_distance
    ## print some values
    print(f"Squirrel: {squirrel}\nTree: {tree}\nNuts: {nuts}\nInitial Step: {initial_step}\nDistance: {total_distance}\n")
    ## plot some stuff if requested
    if plot == True:
        from matplotlib import pyplot as plt
        from matplotlib import patches as mpatches
        plt.scatter(x = [nut[0] for nut in rest_of_nuts],
                    y = [nut[1] for nut in rest_of_nuts],
                    color = "orange",
                    marker = 'h')
        plt.suptitle(f"Total Distance : {total_distance}")
        plt.scatter(x = initial_step[0],
                    y = initial_step[1],
                    marker = "h",
                    color = "red")
        plt.scatter(x = squirrel[0], y = squirrel[1], color = "brown", marker="v")
        plt.scatter(x = tree[0], y = tree[1], color = "green", marker="P")
        red_patch = mpatches.Patch(color='red', label='initial nut')
        orange_patch = mpatches.Patch(color='orange', label='nuts')
        brown_patch = mpatches.Patch(color='brown', label='squirrel')
        green_patch = mpatches.Patch(color='green', label='tree')
        plt.legend(handles=[red_patch, orange_patch, green_patch, brown_patch])
    ## return the total distance
    return(total_distance)

## generate a unit test1
def unitTests(test: int) -> tuple:
    if test == 1:
        squirrel = (4,4)
        tree = (1,3)
        nuts = [(2,2), (1,3)]
    elif test == 2:
        squirrel = (0,0)
        tree = (5,5)
        nuts = [(5,5), (1,4), (3, 2), (9, 10), (12, 12)]
    elif test == 3:
        squirrel = (0,0)
        tree = (4,4)
        nuts = [(-2,-3), (4,8), (-1,-1), (5,5), (-2,0)]
    elif test == 4:
        squirrel = (2,2)
        tree = (3,3)
        nuts = [(3,3), (1,1), (0,0), (4,4)]
    elif test == 5:
        squirrel = (2,2)
        tree = (2,3)
        nuts = [(2,1), (2,3), (3,2), (1,2)]
    elif test == 6:
        squirrel = (2,2)
        tree = (4,4)
        nuts = [(4,4), (0,0), (0,4), (4,0)]
    else:
        ## set dummy values
        squirrel = 0
        tree = 0
        nuts = 0
        print("No unit test available!")
    return((squirrel, tree, nuts))
    
## generate the squirrel, tree, and nuts position
## squirrel = tuple : (x, y)
## tree = tuple : (x, y)
## num_nuts = int
## nuts = list : [(x,y), ...]
## currently using 2**32 for maximum random int
## returns a list : [ squirrel(x,y), tree(x,y), nuts[(x,y), ...]]
def genGame(squirrel: tuple = (),
            tree: tuple = (),
            num_nuts: int = 0,
            nuts: list = []) -> tuple:
    ## set a max integer
    if not num_nuts:
        max_int = random.randint(1, int(1e3))
    ## check if we need to generate values
    if not squirrel:
        squirrel = (random.randint(0, max_int),
                    random.randint(0, max_int))
    if not tree:
        tree = (random.randint(0, max_int),
                random.randint(0, max_int))
    ## if we don't pass in the nuts coordinates
    if not nuts:
        if num_nuts == 0:
            ## generate the number of nuts such that
            ## is bound by max_int
            num_nuts = random.randint(1, max_int)
        ## set a random # of nuts taken from a 32-bit integer
        nuts = zip(random.sample(range(max_int), num_nuts),
                   random.sample(range(max_int), num_nuts))
        ## return tuples for nuts
        nuts = [coord for coord in nuts]
    ## return the game
    return((squirrel, tree, nuts))

## find the distance between two points
## returns an int
def distance(origin: tuple,
             nut: tuple) -> int :
    ## since distance is step wise, we don't use the normal
    ## sqrt(diff(x)^2 + diff(y)^2)
    ## just take the absolute value of the differences between
    ## nut and origin coordinates
    y_diff = abs(nut[1] - origin[1])
    x_diff = abs(nut[0] - origin[0])
    ## distance is just the sum of these steps
    distance = x_diff + y_diff
    ## return the distance
    return(distance)

## get the total number of distance travelled
## between tree and nut
## returns an int
def getDistances(tree: tuple,
                 nuts: list) -> int:
    ## calculate the distance for each tree nut combination
    ## since the squirrel has to travel to the nut then back
    ## distance travelled per trip is actually twice the
    ## distance from tree to nut
    distances = sum([2*distance(tree, nut) for nut in nuts])
    ## return the distance
    return(distances)

## problem can be split up into a matter of squirrel finding
## the optimal location for the first nut
## then the rest of the problem is simply movement
## between the tree and nuts
## returns a tuple : (coord(), rest_of_nuts[])
def getInitialStep(squirrel: tuple,
                   tree: tuple,
                   nuts: list) -> tuple:
    ## we need to first get all the distances from nuts to the squirrel
    ## returns a list of tuples : [(x,y, distance), ...]
    distances = [(nut, distance(squirrel, nut)) for nut in nuts]
    ## let's sort the list by the x values (sort for lower x values)
    distances = sorted(distances, key = lambda x: x[0][0])
    ## let's sort the list by the y values (sort for higher y values)
    distances = sorted(distances, key = lambda x: x[0][1], reverse = True)
    ## let's sort the list by distance (sort for lower distance values)
    distances = sorted(distances, key = lambda x: x[1])
    ## get the coord of the first nut
    initial_step = distances[0][0]
    ## get a list of nuts without the first sorted element from distances
    truncated_nuts = list(nuts)
    truncated_nuts.remove(initial_step)
    ## return some values
    return(initial_step, truncated_nuts)
    
## cookie cutter main call
if __name__ == '__main__':
    main()