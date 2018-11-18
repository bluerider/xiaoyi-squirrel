##!/bin/python3

import random

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
         nuts: list = []) -> int:
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
    ## return the total distance
    return(total_distance)

## generate a unit test1
def unitTests(test: int) -> tuple:
    if test == 1:
        squirrel = (4,4)
        tree = (1,3)
        nuts = [(2,2), (1,3)]
        return((squirrel, tree, nuts))
    elif test == 2:
        squirrel = (0,0)
        tree = (5,5)
        nuts = [(5,5), (1,4), (3, 2), (9, 10), (12, 12)]
        return((squirrel, tree, nuts))
    else:
        print("No unit test available!")
        ## return dummy values
        return(0,0,0)
    
## generate the squirrel, tree, and nuts position
## squirrel = tuple : (x, y)
## tree = tuple : (x, y)
## num_nuts = int
## nuts = list : [(x,y), ...]
## currently using 2^32 for maximum random int
## returns a list : [ squirrel(x,y), tree(x,y), nuts[(x,y), ...]]
def genGame(squirrel: tuple = (),
            tree: tuple = (),
            num_nuts: int = 0,
            nuts: list = []) -> tuple:
    ## check if we need to generate values
    if not squirrel:
        squirrel = (random.randint(0, 2^32),
                   random.randint(0, 2^32))
    if not tree:
        tree = (random.randint(0, 2^32),
               random.randint(0, 2^32))
    ## if we don't pass in the nuts coordinates
    if not nuts:
        if num_nuts == 0:
            num_nuts = random.randint(1, 2^32)
        ## set a random # of nuts taken from a 32-bit integer
        nuts = zip(random.sample(range(2^32), num_nuts),
                   random.sample(range(2^32), num_nuts))
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
## returns a tuple : (distance, rest_of_nuts[])
def getInitialStep(squirrel: tuple,
                   tree: tuple,
                   nuts: list) -> tuple:
    ## we need to first get all the distances from nuts to the squirrel
    ## returns a list of tuples : [(x,y, distance), ...]
    distances = [(nut, distance(squirrel, nut)) for nut in nuts]
    ## let's sort the list by the y values (sort for higher y values)
    distances = sorted(distances, key = lambda x: x[0][1], reverse = True)
    ## let's sort the list by the x values (sort for lower x values)
    distances = sorted(distances, key = lambda x: x[0][0])
    ## let's sort the list by distance (sort for lower distance values)
    distances = sorted(distances, key=lambda x: x[1])
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