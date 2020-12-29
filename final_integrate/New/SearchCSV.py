import csv

def get_name(num):
    data=[]
    with open('StaffList.csv') as list:
        search = csv.reader(list)
        for row in search:
            data.append(row)

    nums= [x[0] for x in data]
    names=[x[1] for x in data]
    #print(names[nums.index(num)])
    try:
        name=names[nums.index(num)]
    except ValueError as e:
        return(num)
    else:
        return(name)

#print(get_name('HELLO'))