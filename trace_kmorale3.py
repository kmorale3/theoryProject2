#!/usr/bin/env python3

# Katie Morales
# Theory of Computing Project 2
# team kmorale3

# Tracing NFA Behavior 

import sys

class NFA: 
    def __init__(self, name, states, chars, start, final, trans ):
        self.name       = name             # the NFA name
        self.states     = states           # set of states of the NFA
        self.chars      = chars            # set of possible inputs
        self.start      = start            # start state of NFA
        self.final      = final            # set of final states
        self.trans      = trans            # dictionary of transitions

        self.paths      = []               # list of possible paths for the NFA for the input string

def read_nfa(input_file):
    ''' This function reads in an NFA from an input file, assuming the NFA is formatted as follows:

    Line 1: Name of machine
    Line 2: List of state names for Q
    Line 3: List of characters from Σ
    Line 4: The start state
    Line 5: List of final states, accepting state names start with *

    Transitions Lines:
        The name of a state that the machine might be in.
        A character from Σ, or an ε, represented by ~
        The name of a state that the machine may go into if that character was found next
        on the input.
    '''

    # read the header
    name   = input_file.readline().rstrip().split(",")[0]
    states = set(filter(None, input_file.readline().rstrip().split(",")))
    chars  = set(filter(None, input_file.readline().rstrip().split(",")))
    start  = input_file.readline().rstrip().split(",")[0]
    final  = set(filter(None, input_file.readline().rstrip().split(",")))

    # read the transitions into a dictionary
    trans = {}
    transition = list(filter(None, input_file.readline().rstrip().split(",")))
    source, char, target = transition[0], transition[1], transition[2]
    while(source and char and target):        
        trans[(source, char)] = trans.get((source, char), []) + [target]
        transition = list(filter(None, input_file.readline().rstrip().split(",")))
        if len(transition) > 2:
            source, char, target = transition[0], transition[1], transition[2]
        else:
            source, char, target = None, None, None

    # return an NFA project with the read in attributes   
    return NFA(name, states, chars, start, final, trans)

def trace_nfa(myNFA, input_str, currState, path):
    ''' this recursive function takes in an NFA object, input string, state, and path 
        to trace all the paths of an NFA and add them to a list of paths attributed to 
        the NFA object
        it prints out the accepted paths and returns how many accepted paths there are
    '''
    #base case
    if not len(input_str):
        paths = 0
        if currState in myNFA.final:
            myNFA.paths.append(path)
            pathStr = ', '.join(path)
            print("**ACCEPTED:")
            print(pathStr)
            print()
            paths += 1
        # check if there are anymore epsilon transitions
        elif (currState, '~') in myNFA.trans:
            for t in myNFA.trans[(currState, '~')]: 
                newPath = path + [t]
                myNFA.paths.append(newPath)
                if t in myNFA.final:
                    pathStr = ', '.join(newPath)
                    print("**ACCEPTED:")
                    print(pathStr)
                    print()
                    paths += 1
        else:
            myNFA.paths.append(path)
        return paths

    # recursive step
    accepted = 0
    # take the input
    if (currState, input_str[0]) in myNFA.trans:
        for t in myNFA.trans[(currState, input_str[0])]:
            accepted += trace_nfa(myNFA, input_str[1:], t, path + [t])
    # take the epsilon
    if (currState, '~') in myNFA.trans:
        for t in myNFA.trans[(currState, '~')]:
            accepted += trace_nfa(myNFA, input_str, t, path + [t])
    return accepted

def main():
    file_name  = sys.argv[1]
    # assume empty string if input not provided
    if len(sys.argv) < 3:
        input_str = ""
    else:
        input_str  = str(sys.argv[2])
    input_file = open(file_name, "r") 

    # build the NFA
    myNFA = read_nfa(input_file)

    # print the terminal command and provided string and machine 
    terminalStr = ' '.join(sys.argv)
    print(terminalStr)
    print(f'Tracing Paths of String \'{input_str}\' on Machine \'{myNFA.name}\'')
    print()

    # trace the paths and get the number of accepted strings 
    accepted = trace_nfa(myNFA, input_str, myNFA.start, [myNFA.start])
    print(f'{accepted} accepted paths')
    total = len(myNFA.paths)
    print(f'{total} total paths\n')

    # comment to mute printing all paths 
    print("all paths: ")
    for path in myNFA.paths:
        string = ', '.join(path)
        print(f'{string}')

    print('\n#########################################################################\n')

if __name__ == '__main__':
    main()