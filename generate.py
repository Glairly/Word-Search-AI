import random
def generate_word_list():
    file=open("words.txt","r")
    words_list=[]
    for line in file.readlines():
	    words_list.append(line.rstrip())
    return words_list

def check_possiblity(matrice,word,index,fitting_orders,fitting_order):
    x,y=index
    ix,iy=fitting_orders[fitting_order]
    try:
        for i in range(len(word)):
            if 0<=y<=14 and 0<=x<=14:
                if matrice[y][x]!="0":
                    return False
                x+=ix
                y+=iy
            else :
                return False
    except IndexError:
        return False

    return True

def put_in_word(matrice,word,index,fitting_orders,fitting_order):
    x,y=index
    ix,iy=fitting_orders[fitting_order]
    for _ in range(len(word)):
        matrice[y][x]=word[_]
        y+=iy
        x+=ix

def generate_words(words):
    for i in range(10): 
        random_word=random.choice(lst_words)
        words.append(random_word)
        lst_words.remove(random_word)
    return words

grid=[]
alphabet="ABCDFEFGHIJKLMNOPQRSTUVWXYZ"
alphabet=list(alphabet)
for i in range(15):
    grid.append(list("0"*15))
lst_words=generate_word_list()
words=generate_words([])
words_copy=words[::]


possibilites={"f":(1,0),"b":(-1,0),"u":(0,-1),"d":(0,1)}
moves=["f","b","u","d"]

while(True):
    if words==[]:
        break
    word=random.choice(words)
    words.remove(word)
    x_coordinate=random.randint(0,14)
    y_coordinate=random.randint(0,14)
    index=(x_coordinate,y_coordinate)
    pattern=random.choice(moves)
    while(check_possiblity(grid,word,index,possibilites,pattern)!=1):
        x_coordinate=random.randint(0,14)
        y_coordinate=random.randint(0,14)
        index=(x_coordinate,y_coordinate)
    put_in_word(grid,word,index,possibilites,pattern)
for i in range(15):
    for j in range(15):
        if grid[i][j]=="0":
            grid[i][j]=random.choice(alphabet)

