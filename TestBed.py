import os
import sys
#
# kb1=["Pradeep","Adiga", "Poornima"]
# kb2=["Adiga","Poornima"]
# kb3=["Hitesh","Chouhan", "Ravi"]

#print(list(set(kb1)-set(kb2)))
# kblist=[kb1, kb2, kb3]

# totalitems = len(kblist)

# i=0

# while i<totalitems:
#     print(set(list(kblist[i]))-set(list(kblist[i-1])))
#     print (i)
#     i=i+1

str = "Pradeep"
l = []
f=[]
l.append(str)
f.append(l)

str1 ="Adiga"
l.append(str1)
f.append(l)
print(l)
print(f)
print(type(f),type(l))