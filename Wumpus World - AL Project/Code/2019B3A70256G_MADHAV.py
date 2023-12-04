from Agent import * # See the Agent.py file
from pysat.solvers import Glucose3
import numpy as np

def out_of_bounds_index(ix, iy):
    if ix<1 or iy<1 or ix>5 or iy>5:
        return True
    else:
        return False

def add_clauses(game, percept, adj_cells):
    # Covering all possible valid number of adjacent cells and percept combinations
    adj_arr_len = len(adj_cells)

    if percept == 0: # 2-0, 3-0, 4-0
        for cell in adj_cells:
            game.add_clause([cell])

    elif adj_arr_len == percept: # 2-2, 3-3, 4-4
        for cell in adj_cells:
            game.add_clause([-cell])

    elif percept == 1: # 2-1, 3-1, 4-1 covered
        neg_adj_cells = []
        for cell in adj_cells:
            neg_adj_cells.append(-1*cell)

        game.add_clause(neg_adj_cells)
        for i in range(adj_arr_len):
            for j in range(i+1, adj_arr_len):
                game.add_clause([adj_cells[i], adj_cells[j]])

    elif (adj_arr_len==3 and percept==2) or (adj_arr_len==4 and percept==3): # 3-2, 4-3 covered
        game.add_clause(adj_cells)
        for i in range(adj_arr_len):
            for j in range(i+1, adj_arr_len):
                game.add_clause([-adj_cells[i], -adj_cells[j]])

    elif adj_arr_len == 4 and percept == 2: # 4-2 covered
        for i in range(adj_arr_len):
            for j in range(i+1, adj_arr_len):
                for k in range(i+1, adj_arr_len):
                    game.add_clause([-adj_cells[i], -adj_cells[j], -adj_cells[k]])
                    game.add_clause([adj_cells[i], adj_cells[j], adj_cells[k]])

def output(safe_arr):

    valid_gold_positions = [[2,2], [3,2], [4,2], [2,3], [3,3], [4,3], [2,4], [3,4], [4,4]]
    move = [[0, 1], [0, -1], [-1, 0], [1, 0]]

    for i in range(9):
        gold_check = True
        g_ix, g_iy = valid_gold_positions[i]
        for j in range(4):
            m_ix = g_ix + move[j][0]
            m_iy = g_iy + move[j][1]
            if safe_arr[m_ix][m_iy] == 2:
                continue
            else:
                gold_check = False
                break
        if gold_check == True:
            print("Gold is present in room [" + str(g_ix) + "," + str(g_iy) + "].")
            break
    if gold_check == False:
       print("Gold could not be detected after visting all the safe rooms.")

def main():
    agent = Agent()
    game = Glucose3()

    safe_arr = np.zeros((6, 6), dtype=int) # 0 if unknown, 1 if safe_arr, 2 if unsafe
    visit_arr = np.zeros((6, 6), dtype=int) 
    
    safe_arr[1][1] = 1  
    game.add_clause([1])    
    

    while True:
        ix, iy = agent.FindCurrentLocation()
        visit_arr[ix][iy] = 1

        adj_cells = []
        move = [[0, 1], [0, -1], [-1, 0], [1, 0]]
        for i in range(4):
            new_ix = ix + move[i][0]
            new_iy = iy + move[i][1]
            if out_of_bounds_index(new_ix, new_iy) or safe_arr[new_ix][new_iy] == 1:
                continue
            adj_cells.append(new_ix + 5 * (new_iy - 1))

        percept = agent.PerceiveCurrentLocation()
        add_clauses(game, percept, adj_cells)

        # Safe cell and mine cell inference
        for i in range(1,6):
            for j in range(1,6):
                if safe_arr[i][j]==0:
                    literal=i+5*(j-1)
                    if game.solve([-literal]) == False:
                        safe_arr[i][j] = 1
                    if game.solve([literal]) == False:
                        safe_arr[i][j] = 2


        route_plan_arr = np.full((6, 6), 9999999, dtype=int)
        route_plan_arr[ix][iy] = 0
        cell_queue = [[ix, iy]]
        next_action = False
        na_cell = [0,0]

        while len(cell_queue) > 0 and next_action == False:
            c_ix, c_iy = cell_queue.pop(0)
            for i in range(4):
                new_ix = c_ix + move[i][0]
                new_iy = c_iy + move[i][1]
                if out_of_bounds_index(new_ix, new_iy) or route_plan_arr[new_ix][new_iy]!= 9999999:
                    continue

                if safe_arr[new_ix][new_iy] == 0 or safe_arr[new_ix][new_iy] == 2:
                    continue

                if visit_arr[new_ix][new_iy] == 1:
                    route_plan_arr[new_ix][new_iy] = route_plan_arr[c_ix][c_iy] + 1
                    cell_queue.append([new_ix, new_iy])

                elif visit_arr[new_ix][new_iy] == 0:
                    route_plan_arr[new_ix][new_iy] = route_plan_arr[c_ix][c_iy] + 1
                    next_action = True
                    na_cell = [new_ix, new_iy]
                    break


        if not next_action:
            break


        action = ['Up','Down','Left','Right']
        action_list = []
        path_length=route_plan_arr[na_cell[0], na_cell[1]]
        c_ix = na_cell[0]
        c_iy = na_cell[1]

        while path_length>0:
            for i in range(4):
                new_ix = c_ix+move[i][0]
                new_iy = c_iy+move[i][1]
                if out_of_bounds_index(new_ix, new_iy):
                    continue
                if route_plan_arr[new_ix][new_iy] == path_length - 1:
                    if i==0:
                        action_list.append(action[1])
                    elif i==1:
                        action_list.append(action[0])
                    elif i==2:
                        action_list.append(action[3])
                    elif i==3:
                        action_list.append(action[2])
                    c_ix = new_ix
                    c_iy = new_iy
                    break
            path_length -= 1

        for i in range(len(action_list)):
            agent.TakeAction(action_list.pop())

    output(safe_arr)
    
if __name__=='__main__':
    main()




