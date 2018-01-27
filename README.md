# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: We loop over each unit from the unitlist and check if there are two boxes which have the exact same values and each have only 2 digits in it and add them in a list of twins. for example, A1: '24' and B1:'24' would be counted as twins and added to the list of twins, but A4: '123' and B5: '123' would not be counted as twins since they have 3 digits each so they are not twins (they would be considered triplets if there were a third box in the same unit with the same digits).
Then we loop over the twins list and find the peers common between the pair of each twins, for example, A1: '24' and B1:'24' are twins so we find the peers common between them (in other words we find the units in which both of them exist) and remove the digits of the twins from all the boxes in those peers in this case the digits are '2' and '4'. This ensures that no digits from the twins is allowed in the possible digits for other boxes in the same unit, and Thus enforcing the constraint.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Simply we add the diagonals as units to the unitlist. Thus it is added automatically to the list of peers for the boxes along the diagonal. Meaning unlike standard suduko where each box has peers from the same row, column, and 3x3 square only, now boxes existing on the diagonal will also have peers from the diagonal. So later in the eliminate function when it is checking the peers it will prevent dulicates from foriming on the diagonals. Thus enforcing the constraints that no duplicates should exist on the diagonals.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

