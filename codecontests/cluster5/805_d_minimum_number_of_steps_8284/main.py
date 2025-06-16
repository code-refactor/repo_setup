#!/usr/bin/env python3

def mess():
    String=input()
    count_it=0
    Counter=0

    for i in String:
        if i=='a':
            count_it = (count_it * 2) % Modulo
            count_it+=1

        elif i=='b':
            Counter+=count_it
            #count_it =(count_it* 2)%Modulo
    return Counter

if __name__ == "__main__":
    Modulo = 1000000007
    print(mess()%Modulo)