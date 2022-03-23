import time
import numpy as np
from copy import deepcopy

"""
The file Question1.2.3.py solved the 8-puzzle problem using two different heuristic functions 
which can be chosen by the user. These functions are admissible and include:
--> Manhattan Distance
--> Euclidean Distance
"""

def findSolution(distance, initialPosition, finalPosition):
    """
    This function is used to find the solution for the puzzle. It includes
    three different arguments, including: distance( which indicates the type of distance; either
    Manhattan or euclidean distance to choose), another argument is the initialPosition(which
    represents the position on the grid at the start of the movement) and the finalPosition( which
    indicates the final goal position on the grid).

    Import numpy to create a numpy array of the grids rows and columns. The time taken for the function
    to start and end is recorded to reflect on the efficiency of the heuristic functions. Also, it checks
    the positions on the grid are not already achieved from the start.
    """

    # uses timer to evaluate the time taken for the heuristic functions to reach the final solution.
    start = time.time()

    # checks if the initial grid tile numbers match the exact end goal solution.
    # if the initial and final position are exactly the same then process is terminated.
    if np.array_equal(initialPosition, finalPosition):
        return finalPosition, time.time() - start


    # dtype suggests how the the bytes in the fixed-size block of memory corresponding to an array item should be interpreted.
    columns = np.array([("moveLeft", [0, 3, 6], -1),("moveRight", [2, 5, 8], 1),("moveUpwards", [0, 1, 2], -3),("moveDownwards", [6, 7, 8], 3)],
                     dtype=[("movement", str, 1),("gridPlacement", list),("first", int)])

    grid = [("puzzleProblem", list), ("mainBranch", int), ("fpoints", int), ("epoints", int)]

    # user inputs 1 for solving the problem using the Manhattan distance function
    # user inputs 2 for solving the problem using the Euclidean distance function
    if distance == "1":
        epoints = manhattanDistance(initialPosition, finalPosition)
    else:
        epoints = euclideanDistance(initialPosition, finalPosition)

    gridArrangement = np.array([(initialPosition, -1, 0, epoints)], grid)

    order = np.array([(0, epoints)], [("gridPlacement", int), ("pointsSum", int)])

    solutionFound = False

    while not solutionFound:
        # This rearranges the list of integers
        # They are ordered by havin the lower integres first and moving up to the bigger ones
        # This depends on their pointsSum
        order = np.sort(order, order=["pointsSum", "gridPlacement"], kind="mergesort")


        # This line of code chooses a specific grid
        # The choosing depends on the pointsSum value
        # The smallest integer is chosen
        gridPlacement, pointsSum=order[0]
        order=np.delete(order, 0, 0)
        puzzleProblem, mainBranch, fpoints, epoints=\
            gridArrangement[gridPlacement]

        # Locate the empty tile
        # Increase the fpoints by 1
        emptyTile=int(np.where(puzzleProblem == 0)[0])
        fpoints += 1

        # This for loop will go through all the tiles that are not an empty tile
        for column in columns:
            if not emptyTile in column["gridPlacement"]:
                freePositions=deepcopy(puzzleProblem)
                change = freePositions[emptyTile + column["first"]]
                freePositions[emptyTile + column["first"]] = freePositions[emptyTile]
                freePositions[emptyTile] = change

                if not (np.all(list(gridArrangement["puzzleProblem"]) == freePositions, 1)).any():
                    # Allows user to input integer (either 1 or 2)
                    # User decides between performing the heuristic function to solve the puzzle
                    # Either using Manhattan or Euclidean distance
                    if distance=="1":
                        epoints=manhattanDistance(freePositions, finalPosition)
                    else:
                        epoints=euclideanDistance(freePositions, finalPosition)
                    queue=np.array([(freePositions, gridPlacement, fpoints, epoints)], grid)
                    gridArrangement=np.append(gridArrangement, queue, 0)

                    # Performs overall calculation of total cost of the function.
                    # each movement is 1
                    pointsSum=epoints+fpoints

                    queue=np.array([(len(gridArrangement) - 1, pointsSum)], [("gridPlacement", int),("pointsSum", int)])
                    order=np.append(order, queue, 0)

                    # This if statement makes sure the 8-puzzle problem has an exact solution and makes sure solution matches with the goal solution which is the final position
                    if np.array_equal(freePositions, finalPosition):
                        solutionFound = True
                        break
    print("Success! Solution found! \n")
    return freePositions,\
           time.time() - start

# This function displays the final correct grid
# final grid will be equivalent to the final positions variable grid
def showGrid(gridArrangement):
    print(str(gridArrangement.reshape(-1, 3, 3)).replace("]", "") .replace("  [", "") .replace("[", ""))

def manhattanDistance(initialPosition, finalPosition):
    """
    This function is used to perform the corresponding calculations to
    achieve the total cost of the Manhattan distance. It holds two arguments,
    including: initialPosition (which indicates the ing position on the grid
    of the 8 puzzle problem). And the finalPosition (which indicates the last end goal
    position on the grid of the puzzle).
    """

    othersSum=abs(initialPosition % 3 - finalPosition % 3)
    factorSum=abs(initialPosition // 3 - finalPosition // 3)

    sumOfCost=factorSum + othersSum
    return sum(sumOfCost)

def euclideanDistance(initialPosition, finalPosition):
    """
    This function is used to perform the corresponding calculations to
    achieve the total cost of the Euclidean distance. It holds two arguments,
    including: initialPosition (which indicates the starting position on the grid
    of the 8 puzzle problem). And the finalPosition (which indicates the last end goal
    position on the grid of the puzzle).
    """

    othersSum=abs(initialPosition % 3 - finalPosition % 3) ** 2
    factorSum=abs(initialPosition // 3 - finalPosition // 3) ** 2

    sumOfCost=np.sqrt(factorSum + othersSum)
    return sum(sumOfCost)

def main():
    """
    The main function where all functions above are combined
    to successfully find the solution to the 8 puzzle problem.

    The initial and final positions wanted by the user can be
    modified here.

    This function also allows the printing of the grids so it
    becomes more accessible for users to visualise the empty tiles
    and the procedure to get to the goal end grid arrangement.
    """
    # This line of code lets the user decide what heuristic function to implement
    # Makes sure it is either the Manhattan distance or the euclidean distance
    # no other heuristic functions can be chosen
    distance = ""
    while distance != "1" and distance != "2":
        distance = input( "Input either 1 or 2 to solve the puzzle using a distinct function:\n 1. Manhattan Distance 2. Euclidean Distance")
    # states initial position
    initialPosition=np.array([7, 2, 4, 5, 0, 6, 8, 3, 1])
    # states final position aiming for
    finalPosition=np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    # Prints the initial position of grid
    print("Initial Position:")
    showGrid(initialPosition)
    # Prints the final position of grid
    print("Final Position:")
    showGrid(finalPosition)

    freePositions, time = findSolution(distance, initialPosition, finalPosition)
    print("The time taken for the function to perform solution of puzzle: " + str(round(time, 4)) + " s")

if __name__ == "__main__":
    main()