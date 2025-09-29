name=input("enter name:")
sub1=int(input("enter markes:"))
sub2=int(input("enter markes:"))
sub3=int(input("enter markes:"))

total=sub1+sub2+sub3
average=(sub1+sub2+sub3/3)
Per=(total/300)*100

if Per>90:
    Grade= "A"
elif Per>75:
   Grade= "B"
elif Per>60:
   Grade= "C"
elif Per>=35:
   Grade= "D"
else:
    Grade= "E"
    
if Per>35 and Grade != "E":
    print(f"{name} has pass")
else:
    print(f"{name} has fail")
    

    
    