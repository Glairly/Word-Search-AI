import pygame
import generate

pygame.init()
screen=pygame.display.set_mode((800,600))
selected=[]


def game_over_screen(screen,list_copy):
    game_over_format=pygame.font.Font("freesansbold.ttf", 100)

    if list_copy==[]:
        screen.fill((255,255,255))
        display_word=game_over_format.render("YOU WIN",True,"Green")
        screen.blit(display_word,(175,200))




def refine_list(lst):
    for i in range(len(lst)):
        lst[i]=remove_duplicate(lst[i])
    return lst


def remove_duplicate(word):
    try:
        s=""
        s+=word[0]
        for i in range(1,len(word)):
            if word[i]!=s[-1]:
                s+=word[i]
        return s
    except IndexError:
        return 0

def display_board():
    x_start=0
    y_start=0
    for i in range(15):
        for j in range(15):
            if [x_start,y_start] in guessed_indexes:
                pygame.draw.rect(screen,"green",(x_start,y_start,40,40),0)
                pygame.draw.rect(screen,"black",(x_start,y_start,40,40),1)
            elif [x_start,y_start] in selected:
                pygame.draw.rect(screen,"cyan",(x_start,y_start,40,40),0)
                pygame.draw.rect(screen,"black",(x_start,y_start,40,40),1)
                
            else:
                pygame.draw.rect(screen,"blue",(x_start,y_start,(40),(40)),1)
            x_start+=40
        x_start=0
        y_start+=40
    

def print_search():
    y=25
    search_format=pygame.font.Font("Quicksilver.ttf",30)
    for line in generate.grid:
        x=21
        for i in range(15):
            search_render=search_format.render(line[i].upper(),True,(0,0,0))
            width=search_render.get_width()
            height=search_render.get_height()
            screen.blit(search_render,(x-width//2,y-height//2))
            x+=40
        y+=40

def display_words():
    x=625
    y=80
    word_format=pygame.font.Font("freesansbold.ttf", 25)
    title_words_format=pygame.font.Font("freesansbold.ttf", 35)

    title_words=title_words_format.render("WORDS",True,(255,0,255))
    screen.blit(title_words,(x,25))
    for word in generate.words_copy:
        display_word=word_format.render(word,True,(0,0,0))
        screen.blit(display_word,(x,y))
        y+=33


def search_btn():
    x = 625
    y = 500
    pygame.draw.rect(screen,"green",(x,y,250,40),0)
    title_words_format=pygame.font.Font("freesansbold.ttf", 25)
    title_words=title_words_format.render("Search",True,(255,0,255))
    screen.blit(title_words,(x + 5,y + 7.5))


def dfs(x, y, i, w, ans = []):
    board = generate.grid
    if i == len(w):
        ans += [[x*40,y*40]]
        return True

    movements = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for xm, ym in movements:
        if len(board[0]) <= x+xm or x+xm < 0:
            continue
        if len(board) <= y+ym or y+ym < 0:
            continue
        if board[y+ym][x+xm] != w[i]:
            continue
        tmp = board[y][x]
        ans += [[x*40,y*40]]
        # board[y][x] = '#'
        if dfs(x+xm, y+ym, i+1, w):
            return ans
        board[y][x] = tmp
        ans.pop(-1)
    return False

def exist(w):
    board = generate.grid
    print(w)
    ans = []
    for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != w[0]:
                    continue
                ans = dfs(j, i, 1, w)
                if ans:
                    return ans
    return False


drag=False
guessed=[]
word=""
running=True
guessed_indexes=[]
words_to_guess=refine_list(generate.words_copy[::])

def corrected(idx,w):
    if remove_duplicate(w) in words_to_guess:
            selected+=(idx)
            index=words_to_guess.index(remove_duplicate(word))
            words_to_guess.remove(remove_duplicate(word))
            generate.words_copy.pop(index)


while(running):
    
    screen.fill((255,255,255))
    
    display_board()
    display_words()
    print_search()
    search_btn()
    game_over_screen(screen,words_to_guess)

    for event in pygame.event.get():
        if (event.type!=pygame.MOUSEBUTTONUP):
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.MOUSEBUTTONDOWN):       
                drag=True
                x, y = pygame.mouse.get_pos()
                if x<=600:
                    word+=generate.grid[(y//40%600)][(x//40)%600]
                elif x >= 625 and y <= 540 and y >= 500 and len(generate.words_copy):
                    # print(exist(words_to_guess[searched_word]))
                    sel_word = generate.words_copy[0]
                    ans = exist(sel_word)
                    
                    if (ans):
                        if remove_duplicate(sel_word) in words_to_guess:
                            selected+=ans
                            index=words_to_guess.index(remove_duplicate(sel_word))
                            words_to_guess.remove(remove_duplicate(sel_word))
                            generate.words_copy.pop(index)

            if event.type==pygame.MOUSEMOTION and drag:
                x, y = pygame.mouse.get_pos()
                if x<=600:
                    word+=generate.grid[(y//40%600)][(x//40)%600]
                    
                    guessed_indexes.append([x//40*40,y//40*40])
        else:
            drag=False
            if remove_duplicate(word) in words_to_guess:
                selected+=(guessed_indexes)
                index=words_to_guess.index(remove_duplicate(word))
                words_to_guess.remove(remove_duplicate(word))
                generate.words_copy.pop(index)
            
            word=""
            guessed_indexes=[]
        pygame.display.update()