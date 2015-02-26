#-------------------------------------------------------------------------------
# Name:        htmljavascriptgrammarcheckerbyCFG
# Purpose:     Educational
#
# Author:      TRINITI
#
# Created:     26-08-2014
# Copyright:   (c) TRINITI 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def addtochart(theset,index,elt):
    if not (elt in theset[index]):
        theset[index]=theset[index]+[elt]
        return True
    else:
        False


def closure(grammar,i,x,ab,cd,j):
    next_states=[ (rule[0],[],rule[1],i) \
     for rule in grammar  if  cd<>[] and rule[0]==cd[0] ]
    return next_states


def shift(tokens,i,x,ab,cd,j):
    if cd<>[] and tokens[i]==cd[0]:
        return (x,ab+[cd[0]],cd[1:],j) #return (x, ab + cd[:1], cd[1:], j) cd[:1]==[cd[0]]
    else:
        return None

def reduction(chart,i,x,ab,cd,j):
    return [ (jstate[0], jstate[1]+[x],(jstate[2])[1:],jstate[3])
            for jstate in chart[j]
            if cd==[] and jstate[2] <> [] and (jstate[2])[0]==x]

def parse(tokens,grammar):
    tokens=tokens+ ["end_of_input_marker"]
    chart={}
    start_rule=grammar[0] #s->p
    for i in range(len(tokens)+1):
        chart[i]=[]
    start_state=(start_rule[0],[],start_rule[1],0)
    chart[0]=[start_state]
    for i in range(len(tokens)):
        while True:
            changes=False
            for state in chart[i]:
                #state==x->ab.cd,j
                x=state[0]
                ab=state[1]
                cd=state[2]
                j=state[3]
                #current state == x->ab.cd,j
                #option 1: for each grammar rule c->pqr  where the c's match
                #make a next state c->.pqr,i
                #ENGLISH : We're about to start parsing a "c", but "c" may be
                #something like exp with mpre production rules. we will bring those production rules in
                next_states=closure(grammar,i,x,ab,cd,j)
                for next_state in next_states:
                    changes=addtochart(chart,i,next_state) or changes

                #current state == x->ab.cd,j
                #option2 if token[i]==c
                #make a new state x->abc.d,j in chart[i+1]
                #ENGLISH: we are looking for to parse token c next and the
                #current token is exactly c! Arent we lucky!
                #So we can parse over and move to j+1

                next_state=shift(tokens,i,x,ab,cd,j)
                if next_state<> None:
                    any_change=addtochart(chart,i+1,next_state) or any_change

                #Current State == x->ab.cd.j
                #Option 3: if cd is [], the state is just c->ab. ,j
                #foe each p->q.xr,l in chart[j]
                #make a new state     p->qx.r,l
                #in chart[i]
                #ENGLISH: We just finished parsing an "x" with this token,
                #but that may have been a sub-step (like matching "exp->2"
                 #in "2+3" ). we should update the higher-level rules as well.
                next_states=reduction(chart,i,x,ab,cd,j)
                for next_state in next_states:
                    changes=addtochart(chart,i,next_state) or changes


            if not changes:
                break
    for i in range(len(tokens)):#print out the chart
        print "== chart"+str(i)
        for state in chart[i]:
            x=state[0]
            ab=state[1]
            cd=state[2]
            j=state[3]
            print "    "+x+" ->",
            for sym in ab:
                print " "+ sym,
            print " .",
            for sym in cd:
                print " "+sym,
            print " from " +str(j)

    accepting_state=(start_rule[0],start_rule[1],[],0)
    return accepting_state in chart[len(tokens)-1]

def main():
    x=raw_input()
    count=0
    tokens=list(x)
    tokens = [x for x in tokens if x != 'P']
    print tokens
    grammar=[
    ("S",["P"]),
    ("P",["{","Fe","M","}"]),
    ("P",["{","M","Fe","}"]),# we have to write here the whole grammar for HTML and JAVASCRIPT
   # ("Fe",["Fe","F"]),
    ("Fe",["F","Fe"]),
    ("Fe",[]),
    ("M",["<","Ls",">"]),
    ("F",["(","Ls",")"]),
    #("Ls",["Ls","L"]),
    ("Ls",["L","Ls"]),
    ("Ls",[]),
    ("L",["{","L","}"]),
    ("L",[]),

    ]
    result=parse(tokens,grammar)
    print result
    pass

if __name__ == '__main__':
    main()
