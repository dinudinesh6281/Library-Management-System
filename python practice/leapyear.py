year=int(input("enter a year:"))
if year%400==0 or year%100!=0 and year%4==0:
    print("leap year")
else:
    print("not leap year")