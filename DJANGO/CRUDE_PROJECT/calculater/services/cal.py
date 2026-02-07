def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def kaprekar(num_str):
    old=-1
    if num_str:
            num=int(num_str)
            digits=len(num_str)
            first=True
            if digits != 2:
                for _ in range(20):
                    if old != num:
                        old=num
                        s=str(num).zfill(digits)
                        small =int(''.join(sorted(str(s))))
                        big=int(''.join(sorted(str(s),reverse=True)))
                        num=big-small
                    elif old== num:
                        return num
            elif digits <=2:
                for _ in range(20):
                    if old != num:
                        old=num
                        s=str(num).zfill(digits)
                        small =int(''.join(sorted(str(s))))
                        big=int(''.join(sorted(str(s),reverse=True)))
                        num=big-small
                        # print(f"old{old}")
                        # print(f"new{num}")
                        return num

                    
                
