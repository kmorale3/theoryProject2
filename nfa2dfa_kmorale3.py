#!/usr/bin/env python3

# Katie Morales
# Theory of Computing Project 2
# team kmorale3

# NFA to DFA

import sys

class NFA: 
    def __init__(self, name, states, chars, start, final, trans ):
        self.name       = name             # the NFA name
        self.states     = states           # set of states of the NFA
        self.chars      = chars            # set of possible inputs
        self.start      = start            # start state of NFA
        self.final      = final            # set of final states
        self.trans      = trans            # dictionary of transitions

class DFA: 
    def __init__(self, name, states, chars, start, final, trans ):
        self.name       = name             # the NFA name
        self.states     = states           # states of the NFA
        self.chars      = chars            # array of possible inputs
        self.start      = start            # start state of NFA
        self.final      = final            # array of final states
        self.trans      = trans            # dictionary of transitions

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

def build_dfa(myNFA):
    ''' This function takes an NFA object and converts it to a DFA object,
        then returns the DFA
    '''
    name  = "DFA for " + myNFA.name 
    chars = myNFA.chars
    Efunc = {}
    states = set() # set has unique members


    # calculate E(R)
    for s in myNFA.states:
        if (s, '~') in myNFA.trans:
            Efunc[s] = [s] + myNFA.trans[(s, '~')]
        else:
            Efunc[s] = [s]

    # use E(R) to get new initial state
    start = '+'.join(Efunc[myNFA.start])

    # transitions and final states
    trans = {}
    final = set() # set has unique members

    # check if the initial state needs to be changed to a final state
    for y in myNFA.final:
        if y in Efunc[myNFA.start]:
            start = "*" + start
            final.add(start)
            break

    # the list of states to calculate transitions for
    newstates = [start]

    while(newstates):
        state = newstates.pop(0)
        # remove the final state designation for indexing purposes
        if state[0] == "*":
            tempName = state[1:]
        else:
            tempName = state

        # trap state remains in trap state
        if state =="TRAP":
            for c in chars:
                trans[(state,c)] = state
            states.add(state)
            continue

        # only process transitions if state has not already been processed
        if state not in states:
            # add transitions for all characters from a state
            for c in chars:
                # get all the possible states the NFA can go to and form a superstate
                nextstate = set()
                for x in tempName.split("+"):
                    if (x, c) in myNFA.trans:
                        for s in myNFA.trans[(x, c)]:
                            for st in Efunc[s]:
                                nextstate.add(st)
                # trap state if the NFA can't go anywhere
                if not nextstate:
                    statename = "TRAP"
                # new statename of the superstate
                else:
                    statename = '+'.join(sorted(nextstate, key=lambda x: x[-1]))
                # check if it should be a final state, final states start with *
                for y in myNFA.final:
                    if y in nextstate:
                        statename = "*" + statename
                        final.add(statename)
                        break
                # add the transitions 
                trans[(state,c)] = statename
                # make sure the newly formed state will be processed
                newstates.append(statename)
        # add state being processedto states for DFA
        states.add(state)

    return DFA(name, sorted(states), chars, start, sorted(final), trans )

def output(myDFA):
    ''' This functions takes a DFA object and outputs it as follows
            Line 1: Name of machine
            Line 2: List of state names for Q
            Line 3: List of characters from Σ
            Line 4: The start state
            Line 5: List of final states, accepting state names start with *

            Transitions Lines:
                The name of a state that the machine might be in.
                A character from Σ
                The name of a state that the machine may go into if that character was found next
                on the input.
    '''
    print(myDFA.name)

    states = ",".join(myDFA.states)
    print(states)

    chars = ",".join(myDFA.chars)
    print(chars)

    print(myDFA.start)

    final = ",".join(myDFA.final)
    print(final)

    for key, val in myDFA.trans.items():
        print(f'{key[0]},{key[1]},{val}')

def main():
    file_name  = sys.argv[1]
    input_file = open(file_name, "r") 
    # read NFA
    myNFA = read_nfa(input_file)
    # build DFA
    myDFA = build_dfa(myNFA)
    # print out DFA
    output (myDFA)

if __name__ == '__main__':
    main()