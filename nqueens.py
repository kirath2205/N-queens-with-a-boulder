import math
def succ(state,boulderX,boulderY):  #this function returns a list of all valid successor states
    n=len(state)
    matrix=list()
    row=list()
    index=0
    for i in range(n):  #creation of a chessboard using nested lists
        for k in range(n):
            if(i==boulderX and k==boulderY):
                row.append(-1)
            else:
                row.append(0)
        matrix.append(row.copy())
        row.clear()
    for i in range(n):
        matrix[state[i]][i]=1
        index=index+1
    list_of_moves=list()
    state_copy=state.copy()

    for row in range(n):  #generating the successor states and storing them in list_of_moves
        for column in range(n):
            if(matrix[row][column]==0):
                state[column]=row
                list_of_moves.append(state.copy())
                state=state_copy.copy()
                matrix[row][column]=1
    return list_of_moves



def f(state,boulderX,boulderY): #   #this function returns an integer score such that the goal state scores 0
    n=len(state)
    matrix=list()
    row=list()
    for i in range(n):
        for k in range(n):
            if(i==boulderX and k==boulderY):
                row.append(-1)
            else:
                row.append(0)
        matrix.append(row.copy())
        row.clear()
    for i in range(n):
        matrix[state[i]][i]=1
    list_of_queens=list()
    for i in range(n):
        list_of_queens.append(0)
    for i in range(n):  #checking for boulders obstructing the path of queens
        for row in range(n): #if a queen gets hit then a 1 is stored in the index of the particular queen's column
            for column in range(n):
                #print("current ",row,"  ",column)
                if((i!=column ) and matrix[row][column]==1):
                    if(matrix[row][column]==1):
                        if((abs(state[i]-i)== abs(row-column)) and (abs(state[i]-i)==abs(boulderY-boulderX)) and (max(i,column)>boulderX) and (max(state[i],row)>boulderY) and boulderX>min(i,column) and boulderY>min(state[i],row)) :

                            continue
                        if(state[i]==row and row==boulderY and max(column,i)>boulderX and min(column,i)<boulderX):

                            continue

                        if(state[i]==row):
                            list_of_queens[i]=1

                        if(abs(column-i)==abs(row-state[i])):
                            list_of_queens[i]=1


    return sum(list_of_queens)


def choose_next(curr,boulderX,boulderY):  #this function is used to generate successors using succ() function and returns the most optimised state
    k=curr.copy()
    list_of_states=succ(curr,boulderX,boulderY)
    list_of_states.append(k.copy())
    list_of_scores=list()
    for i in list_of_states:
        list_of_scores.append(f(i,boulderX,boulderY))

    smallest_f=list_of_scores[0]
    for i in range(len(list_of_states)):
        if(list_of_scores[i]<smallest_f):
            smallest_f=list_of_scores[i]

    new_list_states=list()
    for i in range(len(list_of_states)):
        if(smallest_f==list_of_scores[i]):
            new_list_states.append(list_of_states[i])

    curr=k.copy()

    new_list_states.sort()

    if(new_list_states[0]==k):
        return None #return None or return that same list k
    else:
        return new_list_states[0]



def nqueens(initial_state,boulderX,boulderY): # run the hill-climbing algorithm from a given initial state, return the convergence state
   previous_state=initial_state.copy()  #this function also prints all the selected states using choose_next along with their 'f' values using f() function
   current_state=choose_next(previous_state.copy(),boulderX,boulderY)
   if(current_state==None):
       print(previous_state,"- f=",f(previous_state.copy(),boulderX,boulderY))
   while(previous_state!=current_state or current_state!=None):
       print(previous_state,"- f=",f(previous_state.copy(),boulderX,boulderY))
       if(current_state==None):

           print()
           return previous_state

       previous_state = current_state.copy()
       current_state=choose_next(previous_state.copy(),boulderX,boulderY)

   print()
   return current_state

import random

def generate_random_list(n,boulderX,boulderY): #this is an additional function that generates a list of random states containing n queens for the n*n chessboard
    list_states=list()          #the boulder however can be selected arbitarily
    for i in range(n):
        list_states.append(random.randint(0,n-1))

    for i in range(n):
        if(i==boulderX and list_states[i]==boulderY):
            list_states=generate_random_list(n,boulderX,boulderY).copy()
    return list_states


def nqueens_restart(n,k,boulderX,boulderY):  #Generate a random (valid!) initial state for your n*n board, and use your nqueens() function on that state. If the convergent state does not solve the problem, generate a new random (valid!) initial state and try again. Try again up to k times.

#If  a solution is found before we reach k, print the solution and terminate.

#If we reach k before finding a solution, print the best solution(s) in sorted order.
    new_state=generate_random_list(n,boulderX,boulderY).copy()
    counter=0
    smallest_f=f(new_state.copy(),boulderX,boulderY)
    list_of_smallet_states=list()
    while(counter<k):
        new_state=nqueens(new_state.copy(),boulderX,boulderY).copy()
        if(f(new_state.copy(),boulderX,boulderY)==0):
            return new_state
        else:
            if(f(new_state.copy(),boulderX,boulderY)<smallest_f):
                smallest_f=f(new_state.copy(),boulderX,boulderY)
                list_of_smallet_states.clear()
                list_of_smallet_states.append(new_state.copy())
            if (f(new_state.copy(), boulderX, boulderY) == smallest_f):
                list_of_smallet_states.append(new_state.copy())
            counter=counter+1

        new_state=generate_random_list(n,boulderX,boulderY).copy()
    new_list_final_states=list()
    for i in list_of_smallet_states:
        if(i not in new_list_final_states):
            new_list_final_states.append(i)
    new_list_final_states.sort()
    return (new_list_final_states)

n=int(input("enter value of n "))
k=int(input("enter value of k "))
boulderX=int(input("Enter X co-ordinate in the chessboard for the boulder placement "))
boulderY=int(input("Enter Y co-ordinate in the chessboard for the boulder placement "))
print("final optimised and returned state",nqueens_restart(n,k,boulderX,boulderY))

