import numpy as np

def federaltax(pay1):
    tax1=0
    if pay1>0 and pay1<9950:
        tax1=pay1*0.1
    elif pay1>9951 and pay1<40525:
        tax1=pay1*0.12
    elif pay1>40526 and pay1<86375:
        tax1=pay1*0.22
    elif pay1>86376 and pay1<164925:
        tax1=pay1*0.24
    elif pay1>164926 and pay1<209425:
        tax1=pay1*0.32
    elif pay1>209426 and pay1<523600:
        tax1=pay1*0.35
    elif pay1>523601:
        tax1=pay1*0.37

    aftertax = pay1 - tax1
    return aftertax