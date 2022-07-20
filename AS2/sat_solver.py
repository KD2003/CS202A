import os
import time
start_time=time.time()

def read_cnf(filename):                     #reads cnf file and returns a list of lists and total number of literals
    directory = os.path.dirname(os.path.abspath(__file__))
    pre,ext=os.path.splitext(filename)
    new=directory+"\\"+pre+".txt"
    old=directory+"\\"+filename
    os.rename(old,new)
    formula=[]
    with open(new,"r") as f:
        lines=f.readlines()
        for line in lines:
            temp=[]
            line=line.strip()
            if(line[0].isdigit()) or (line[0].startswith("-")):
                substrs=line.split()
                for num in substrs:
                    num_int=int(num)
                    if num_int!=0:
                        temp.append(num_int)
                formula.append(temp)
            elif(line[0]=='p'):
                substr=line.split()
                variables=int(substr[2])
        # print(formula)
    os.rename(new,old)
    return formula,variables;

def remov(formula, unit):                   #assumes unit to be true and simplifies the formula accordingly
    new=[]
    for clause in formula:
        if unit in clause:
            continue;
        if -unit in clause:
            temp=[]
            for i in clause:
                if(i!=-unit):
                    temp.append(i)
            if temp==[]:
                return -1;
            new.append(temp)
        else:
            new.append(clause)
    return new;

def propogate_units(formula):               #simplifies for unit clauses
    assignment=[]
    unit_clauses=[]
    for i in formula:
        if(len(i)==1):
            unit_clauses.append(i[0])
    while(unit_clauses):
        unit=unit_clauses[0]
        formula=remov(formula,unit)
        assignment.append(unit)
        if(formula==-1):
            return -1,[];
        if formula==[]:
            return formula,assignment
        unit_clauses=[]
        for i in formula:
            if(len(i)==1):
                unit_clauses.append(i[0])
    return formula,assignment;

# def propogate_units(formula):           #simplifies for unit clauses
#     a=0
#     while(1):
#         i=formula[a]
#         if(len(i)==1):
#             v=i[0]
#             new.append(v)
#             assignment[abs(v)-1]=v/abs(v)
#             formula.remove(i)
#             a-=1
#         a+=1
#         if(a>=len(formula)):
#             break
#     for i in new:
#         a=0
#         while(1):
#             clause=formula[a]
#             for v in clause:
#                 if(v==i):
#                     formula.remove(clause)
#                     a-=1
#                     break
#                 elif(v==-i):
#                     clause.remove(v)
#                     break
#             a+=1
#             if(a>=len(formula)):
#                 break
#     return formula

# def pure_elim(formula,literals):        #simplifies for pure literal
#     for v in literals:
#         flag,val=0,0
#         for clause in formula:
#             if(v in clause):
#                 if(val==-1):
#                     flag=1
#                     break
#                 val=1
#             elif(-v in clause):
#                 if(val==1):
#                     flag=1
#                     break
#                 val=-1
#         if(flag==0 and val!=0 and assignment[v-1]!=val):
#             a=0
#             while(1):
#                 clause=formula[a]
#                 for i in clause:
#                     if(i==v or i==-v):
#                         formula.remove(clause)
#                         a-=1
#                 a+=1
#                 if(a>=len(formula)):
#                     break
#             assignment[v-1]=val
#     return formula

def dpll(formula,assignment):
    formula,unit_assign=propogate_units(formula)
    assignment+=unit_assign
    if formula==-1:
        return []
    if formula==[]:
        return assignment
    literals=set()
    for clause in formula:
        for l in clause:
            literals.add(abs(l))
    literals=list(literals)
    dict1=dict.fromkeys(literals,0)
    for clause in formula:
        for l in clause:
            dict1[abs(l)]+=1
    x=max(dict1, key=dict1.get)                 #selects most occuring literal
    solution=dpll(remov(formula,x), assignment+[x])
    if solution==[]:
        solution=dpll(remov(formula,-x), assignment+[-x])
    return solution

file=input("Enter name of the file(e.g. test.cnf): ")
cnf,total_literals=read_cnf(file)
solution=dpll(cnf,[])
ans=[x for x in range(1,total_literals+1)]
if solution!=[]:
    for i in range(0,total_literals):
        if(-ans[i] in solution):
            ans[i]=-ans[i]
    print("SATISFIABLE")
    print(ans)
else:
    print("UNSATISFIABLE")
print("Process finished --- %s seconds ---" % (time.time() - start_time))