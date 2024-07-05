import random,sys
import numpy as np
from typing import Optional

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget,QGridLayout,QLineEdit
from PySide6.QtGui import QIcon 
from PySide6.QtCore import QTimer

import gymnasium as gym
import gymnasium.spaces as spaces
from gymnasium.envs.registration import register


register(
    id="sudoku",
    entry_point="environment:ENVI"
)
app = QApplication.instance()
if app is None:
    app = QApplication([])

class Gui(QWidget):
    def __init__(self ):
        super().__init__()

        self.setWindowTitle("Sudoku") 
        self.setMaximumSize(700,700)
        self.setWindowIcon(QIcon("media/icons8-sudoku-96_2.png"))

        self.grid = QGridLayout(self)
        self.grid.setSpacing(0)
        self.size = 49 
        self.cells = [
            [QLineEdit(self) for _ in range(self.size)] 
            for _ in range (self.size)
        ]
        random.seed(42) # TODO : to be removed 

        # layout for cells 
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].setMaximumSize(20,20)
                self.cells[x][y].setReadOnly(True)
                self.cells[x][y].setStyleSheet(f"background-color: #{''.join([random.choice('0123456789ABCDEF') for _ in range(6)])};border: 1px solid balck; color: white;")
                self.cells[x][y].setText(str(random.randint(1,self.size)))
                self.cells[x][y].setAlignment(QtCore.Qt.AlignCenter)
                self.grid.addWidget(self.cells[x][y],x,y)
    
    def updated(self,action: tuple = None ) -> list[list[int]]: 
        """
        This method update update cells via the "action" parameter and return a matrix
        of the updated grid
        """
        if action is not None:
            row,column,value = action
            self.cells[row][column].setText(str(value))
            self.cells[row][column].setStyleSheet(f"background-color: black;border: 1px solid black; color: white;")
            #self.cells[row][column].setStyleSheet(f"background-color: #{''.join([random.choice('0123456789ABCDEF') for _ in range(6)]
                                        # )};border: 1px solid balck; color: white;") # random color 
        list_text = [] 
        for rw in self.cells :
            for cells in rw:
                list_text.append(cells.text())        
        list_text = [int(element) for element in list_text]

        matrix = [
            list_text[i:i+self.size] 
            for i in range(0,len(list_text),49)
        ]
        return matrix
    
    def Subgrid(self,subgrid) -> list[list[list[int]]]:
        """ 
        Sugrid takes our 2D matrix then divide it into regions.
                Each region is a small (7,7) matrix since our sudoku board is size(49,49). 
                That means that we have 49 region in our Sudoku board.
        * If our Sudoku game was size(9,9), 3*3 = 9 so we would have 9 region of size (3,3) on our board.
        """
        self.CONST = 7
        self.MAX_COLUMN_END = 56
        self.ZERO = 0
        matrix = self.updated()

        row_start = self.ZERO
        row_end = self.CONST
        col_start = self.ZERO
        col_end = self.CONST

        subgrid = []

        while len(subgrid) < len(matrix) :
            subgrid.append([
                row[col_start:col_end] 
                for row in matrix[row_start:row_end] ]
            )
            col_start += self.CONST
            col_end += self.CONST
            if col_end == self.MAX_COLUMN_END :
                col_start = self.ZERO
                col_end = self.CONST
                row_start += self.CONST
                row_end += self.CONST

        assert len(subgrid) == len(matrix)
        return subgrid
 
    def solved(self) -> list[bool] :
        """ 
        For the Sudoku game to be solved, each element(number) on the board should:
            - Be unique on the x axis
            - Be unique on the y axis 
            - Be unique in it region
         """
        matrix  = self.updated()
        unique = lambda lisst : len(lisst) == len(set(lisst))  
        
        def x_validation(board=matrix) -> bool: 
            x_done = None      
            for line in board:
                    if not unique(line):
                        x_done = False
            return x_done
        
        def y_validation(board=matrix) -> bool:
            y_list = [[row[i] for row in board] for i in range(self.size)]
            y_done = None
            for sublist in y_list:
                    if not unique(sublist):
                        y_done = False
            return y_done
                    
        def region_validation(board=matrix) -> bool:
            board = np.array(board)
            Sub = self.Subgrid(board)
            Sub = [np.concatenate(sublist) for sublist in Sub]
            assert len(Sub) == self.size

            Sub = [arr.tolist() for arr in Sub]
            region_done = None
            for subarr in Sub:
                if not unique(subarr):
                    region_done = False
            return region_done
        
        completion = [x_validation(),y_validation(),region_validation()]
        assert len(completion) == 3
        return completion


class ENVI(gym.Env):
    def __init__(self):
        super().__init__()

        self.gui = None
        self.size = 49
        self.action_space = spaces.Tuple((spaces.Discrete(self.size),
                                          spaces.Discrete(self.size),
                                          spaces.Discrete(self.size)))
        self.observation_space = spaces.Box(low=0,high=self.size,
                                            shape=(self.size,self.size),
                                            dtype=float)
        self.gui = Gui()
        
    def step(self,action):
        def reward_function(liste : list) :
            assert all(isinstance(element,bool) for element in liste)
            assert len(liste) == 3
            reward = 0
            if sum(liste) == 1:
                reward = 2
            elif sum(liste) == 2:
                reward = 4
            elif all(liste):
                reward = 6
            return reward
        
        self.gui.updated(action = action) # The action
        new_state = self.gui.updated()

        reward_list = self.gui.solved()
        reward = reward_function(reward_list)

        terminated_list = reward_list
        terminated = (True if all(terminated_list) else False)

        return  np.array(new_state),reward,terminated,False,{}

    def reset(self, *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,) -> tuple[np.array, dict]:
        super().reset(seed=seed)
        state =  self.gui.updated() 
        return np.array(state),{}
            
    def render(self) -> None:
        self.gui.updated()
        self.gui.show()
        

class Test:  
    def __init__(self, epi : int, render : bool) -> None:    
        if not isinstance(epi,int) or not epi > 0:
            raise ValueError("Epi should be a positif int instance")
        if not isinstance(render,bool):
            raise ValueError("The render param should be a bool")
        self.epi = epi
        self.render = render
        
        self.test = ENVI( )
        self.timer = QTimer() 
        self.counter = 0

    def main(self):
        if self.counter < self.epi :
            action = self.test.action_space.sample()
            print(f"updating...{action}")
            self.test.step(action=action)
            if self.render:
                self.test.render() 
            self.counter += 1 
        else :
            self.timer.stop()
            sys.exit()

    def run(self):
        self.timer.timeout.connect(self.main)
        self.timer.start(100)
        app.exec()
    
    def state(self):
        print(self.test.reset())


if __name__ == "__main__":
    pass
     
 
 
     
            


 
 
 