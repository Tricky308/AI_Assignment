
from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3



#### All your code can go here.

#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.


def main():
    ag = Agent()
    print('curLoc',ag.FindCurrentLocation())
    print('Percept ',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept ',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept ',ag.PerceiveCurrentLocation())

if __name__=='__main__':
    main()
