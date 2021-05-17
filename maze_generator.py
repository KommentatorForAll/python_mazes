import cv2 as cv
import numpy as np
import random


"""
1/n * 2/3 chance for the line to make a turn
the higher the number, as more 'spirally' the maze becomes
"""
streightness = 1

"""
the furthest distance away from the starting point
"""
furthest_distance = 0

"""
The x coordinate of the furthest spot on the map
"""
furthest_x = 0

"""
The y coordinate of the furthest spot on the map
"""
furthest_y = 0

"""
if the screen should update after every step (requires any key press to continue)
"""
show_steps = True


def create_image(width:int, height:int) -> np.ndarray:
    """
    Creates an empty (black) image of the given width and height.
    """
    return np.zeros((height,width,3), np.uint8)
    
    
def create_maze(start_x:int, start_y:int, image:np.ndarray, num:str) -> None:
    """
    Creates a maze, beginning from the starting position x and y in the image
    start_x: the x position of the maze origin
    start_y: the y position of the maze origin
    image: the image the maze is created on
    """
    
    
    color = (255,255,255) #The paths color. default: white
    
    x = start_x
    y = start_y
    
    direction = random.randrange(0,4) #selects a random direction to start off
    
    create_path(x, y, direction, 0, image, color) #starts the recursive calls for the path creation
    
    image[furthest_y][furthest_x] = (0,0,255) #colors the furthest point red (cv uses BGR notation not RGB)
    image[start_y][start_x] = (255,0,0) #colors the starting point blue (cv uses BGR notation and not RGB)
    
    cv.imwrite(f"imgs/maze_{num}.png", cv.UMat(image)) #saves the image to a file in the imgs folder
    
    pic = cv.UMat(cv.resize(image, (len(image[0])*16, len(image)*16), interpolation = cv.INTER_NEAREST)) #resizes the image to make one able to see it properly
    
    cv.imshow("maze_test.png", pic) # shows the final image to the user
    cv.waitKey(0) #waits until the user pressed any key and then closes the windows
    cv.destroyAllWindows()
    
def create_path(x:int, y:int, direction:int, depth:int, image:np.ndarray, color:tuple) -> None:
    """
    Recursive function to create the path of the maze
    x: the x position where to start off of
    y: the y position where to start off of
    direction: the last direction a line was generated in
    depth: the recursion depth. Used to terminate (avoid errors) and to determine the furthest distance from the start
    image: the image to generate the maze on
    color: the paths color
    """
    
    #makes the function terminate if the depth is greater than 900 to avoid max recursion depth errors
    if (depth > 900):
        return
    
    global furthest_distance, furthest_x, furthest_y #accesses global values
    if (furthest_distance < depth): #checks if this point of the path is further away from the start than any other
        furthest_distance = depth
        furthest_x = x
        furthest_y = y
    
    #setting to make lines streighter. in 1/n cases the direction has the possibility to change.
    if (random.randrange(0,streightness) == 0):
        direction += random.randrange(-1,2)
        direction = direction%4
        
    #checks if any other direction is free to draw a path to, then does so.
    #similar to the code above
    for i in range(0,4):
        direction = (direction + i) %4
        
        #gets the next path position to check if there is already a path
        pos = get_position(x, y, direction , 2)
        
        #checks if the position is out of bounds or if there is already a path
        if (check_position(pos, image) and not (image[pos[1]][pos[0]] == color).all()):
            stamp(x, y, direction, image, color)
            #checks if the user wants to see every step, then shows the image
            if (show_steps):
                cv.imshow("maze_test.png", cv.UMat(cv.resize(image, (len(image[0])*16, len(image)*16), interpolation = cv.INTER_NEAREST)))
                cv.waitKey(0)
            #recursive call of the function if a new path has been created
            create_path(pos[0], pos[1], direction, depth+1, image, color)
        
        

    
def stamp(x:int, y:int, direction:int, image:np.ndarray, color:tuple) -> None:
    """
    stamps a path onto the maze, originating from x and y in the direction direction.
    x: x coordinate of the stamp
    y: y coordinate of the stamp
    direction: the facing of the stamp. must be within range [0:4]
    color: the color of the stamp. must be a three long tuple as brg
    """
    image[y][x] = color
    pos = get_position(x, y, direction)
    image[pos[1]][pos[0]] = color
    pos = get_position(x, y, direction, 2)
    image[pos[1]][pos[0]] = color

def get_position(x:int, y:int, direction:int, distance:int=1) -> (int,int):
    """
    fetches the new position in the given distance of the direction
    x: the current x position
    y: the current y position
    direction: the direction to fetch the new position in
    distance: the amount of spots to go further
    """
    if (direction == 0):
        return (x, y-distance)
    elif (direction == 1):
        return (x+distance, y)
    elif (direction == 2):
        return (x, y+distance)
    elif (direction == 3):
        return (x-distance, y)
    else:
        print(f"Error, invalid direction {direction} not in range [0:4]")
        raise IndexError

def check_position(pos:list, image:np.ndarray) -> bool:
    """
    checks if the position is out of bounds
    """
    return pos[0] > 0 and pos[1] > 0 and pos[0] < len(image[0]) and pos[1] < len(image)

def main():
    while True:
        width = -1
        height = -1
        start_x = -1
        start_y = -1
        global streightness
        
        print("Please input the maze parameters. If you want a random value, type 'random'")
        
        while (width <= 0):
            tmp = input("maze width: ")
            if (tmp.lower() == 'random'):
                width = random.randrange(1,100)
                break
            try:
                width = int(tmp)
                if (width <= 0):
                    raise ValueError
            except ValueError:
                print("Invalid input: input was neither 'random' nor a number > 0")
                
        while (height <= 0):
            tmp = input("maze height: ")
            if (tmp.lower() == 'random'):
                height = random.randrange(1,100)
                break
            try:
                height = int(tmp)
                if (height <= 0):
                    raise ValueError
            except ValueError:
                print("Invalid input: input was neither 'random' nor a number > 0")

        valid = False
        print("Please enter the x position of the start point")
        while (not valid):
            tmp = input("x: ")
            if (tmp.lower() == 'random'):
                tmp = random.randrange(0,width)
                valid = True
                break
            try:
                start_x = int(tmp)
                if (not start_x in range(0,width)):
                    raise ValueError
                valid = True
            except ValueError:
                print(f"Invalid input: input must be 'random' or in range[0,{width}]")
                valid = False
                    
        valid = False
        print("Please enter the y position of the start point")
        while (not valid):
            tmp = input("y: ")
            if (tmp.lower() == 'random'):
                tmp = random.randrange(0,height)
                valid = True
                break
            try:
                start_y = int(tmp)
                if (not start_y in range(0,height)):
                    raise ValueError
                valid = True
            except ValueError:
                print(f"Invalid input: input must be 'random' or in range[0,{height}]")

        print("Please enter the streigthness of the maze")
        print("There is a 1/n * 2/3 chance of the line doing a turn")
        valid = False
        while (not valid):
            tmp = input("streightness: ")
            if (tmp.lower() == 'random'):
                streightness = random.randrange(1,5)
                valid = True
                break
            try:
                streightness = int(tmp)
                if (streightness < 1):
                    raise ValueError
                valid = True
            except ValueError:
                print("Invalid input: input must be 'random' or in range [1,[")
                valid = False
        
        maze_name = input("maze name (will be saved as maze_[name].png): ")
        
        global show_steps
        show_steps = input("shall the steps be shown?[yes/no]").lower().startswith('y')
        
        create_maze(start_x, start_y, create_image(width, height), maze_name)
        
    
if (__name__ == '__main__'):
    main()
