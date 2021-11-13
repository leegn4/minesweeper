from random import randint
from sys import stdin as r
import os

#! 제출 형식 때문에 global 키워드 많이 사용함

def tutorial():
    clear()
    print("""
    Simple CLI minesweeper 실행을 환영합니다.

    게임판의 가로세로 길이는 최소 3 이상이며, <가로길이 세로길이> 형태로 입력하셔야 합니다.

    또한, 게임 시작 후 좌표를 입력할 때에는 <행 열> 형태로 입력하셔야 합니다.

    게임은 모든 지뢰를 찾아내거나 지뢰를 밟게 되면 종료되며, exit을 입력하여 조기 종료할 수 있습니다.

    점수는 좌표 입력 표시 왼쪽에, 현재까지 밝혀낸 타일의 개수로 표시됩니다.

    이제 게임을 시작하겠습니다. 시작하려면 엔터 키를 눌러주세요.
    """)
    r.readline()

def clear(): #* clear prompt
    os.system("cls" if os.name=='nt' else "clear")

def getgridsize(): #* get grid size
    print("Grid size(MxN): ",end="")
    row,col=map(int,r.readline().strip().split()) #* Size of board
    print("Maximum number of mines(at least 3): ",end="")
    m=int(r.readline().strip()) #* Number of mines
    return row,col,m

def gettile():
    print(f"[{score}] >> ",end='')
    R=r.readline().strip()
    if R=="exit": return (None,None) #* exit
    else: return map(int,R.split()) #* user input(row,col) - in natural numbers

def createmine(q,p,m):
    mine=""
    for k in range(m):
        mine+=str(randint(0,q*p-1))+" "
    return (mine.rstrip().split()) #* list of mine indexes

def createboard(q, p, mine):
    global ref
    ref=0
    for j in range(q): #* page 0: whether mine: 0 or 1
        for k in range(p):
            if str(j*q+k) in mine: board[0][j][k]="1"; ref+=1 #* string index = col*q + row
            else: board[0][j][k]="0" #! by division theorem of integers, no collision

    for y in range(q): #* page 1: surrounding number of mines
        for x in range(p):
            count=0
            for j in range(-1,1+1):
                for i in range(-1,1+1): #* iterate adjacent indexes
                    if (isvalid(y+j,x+i,q,p) and board[0][y+j][x+i]=="1"): count+=1 #* index is valid & isMine: True
            board[1][y][x]=count    

def printboard(q,p,a=True): #* print board
    if a==True: #* game is rolling
        for j in range(q):
            for i in range(p):
                if board[0][j][i]=="1" or board[0][j][i]=="0": print("-",end="") #* untouched tiles: -
                else: print(board[0][j][i],end="") #* touched tiles(number of surrounding mines)
            print()
    else: #* game has finished,print grid until now + answer
        for j in range(q):
            for i in range(p):
                if board[0][j][i]=="1": print("*",end="") #* untouched tiles,mine: True
                elif board[0][j][i]=="0": print("~",end="") #* untouched tiles,mine: False
                else: print(board[0][j][i],end="") #* touched tiles
            print()

def isvalid(col,row,q,p): #* validate grid index
    return (col>=0 and col<q and row>=0 and row<p)

def opensurrounding(col,row,q,p): #* open surrounding tiles if (col,row) is a free tile
    global score
    for j in range(-1,1+1): #* iterate adjacent indexes - column
        for i in range(-1,1+1): #* iterate adjacent indexes - row
            if isvalid(col+j,row+i,q,p):
                if (board[0][col+j][row+i]=="o" or board[1][col+j][row+i]=="o"): continue #* check if visited
                elif board[1][col+j][row+i]!=0: #* focused tile is not free tile
                    score+=1
                    board[0][col+j][row+i]=board[1][col+j][row+i]
                    board[1][col+j][row+i]="o" #* make visited=True
                elif board[1][col+j][row+i]==0: #* focused tile is free tile
                    board[0][col+j][row+i]="o" #* make visited=True
                    score+=1
                    opensurrounding(col+j,row+i,q,p) #* recursion with the focused free tile

def main():
    tutorial()
    clear()

    while True:
        try:
            clear()
            p,q,m=getgridsize() #* q: column,p: row
        except:
            continue
        else:
            if (not (q>2 and p>2 and m>2 and q*p>m)): #* check grid size
                continue
            break
        
    global score,ref
    score,ref=0,0 #* ref: number of mines,cleared+ref=grid size

    global board
    board=[[["" for row in range(p)] for col in range(q)] for depth in range(2)]

    mine=createmine(q,p,m)

    createboard(q,p,mine)

    clear()
    reset=False
    printboard(q,p)

    global b,a

    while True:
        #* Uncomment to print answer grid
        with open("ans.txt","w") as ans:
            ans.write(str(board[0]))
            ans.write("\n")
            ans.write(str(board[1]))
            ans.write(f"\n{ref}")
        if score==q*p-ref: #* every mine is cleared
            clear()
            printboard(q,p,False)
            print()
            print("ALL CLEAR")
            print(f"Score: {score}")
            break
        if reset: #* reset board until 1st try success
            mine=createmine(q,p,m)
            createboard(q,p,mine)
            clear()
        else:
            try:
                clear()
                printboard(q,p)
                b,a=gettile()
            except:
                continue
            else:
                if (b,a)==(None,None): quit() #* exit
                if not isvalid(b-1,a-1,q,p): #* check user input index
                    continue
        if board[0][b-1][a-1]=="1": #* user selected mine tile
            if score==0: #* in 1st try -> reset board
                reset=True
            else: #* not in 1st try -> game over
                clear()
                printboard(q,p,False)
                print()
                print("BOOM")
                print(f"Score: {score}")
                break
        elif board[0][b-1][a-1]=="0" and board[1][b-1][a-1]==0: #* user selected non-mine tile,with 0 surrounding mines
            clear()
            opensurrounding(b-1,a-1,q,p) #* open surrounding tiles of current position
            printboard(q,p)
            reset=False
        elif board[0][b-1][a-1]=="0" and board[1][b-1][a-1]!=0: #* user selected non-mine tile,surrounding mines exist
            clear()
            board[0][b-1][a-1]=board[1][b-1][a-1] #* change selected tile with number of surrounding mines
            score+=1
            printboard(q,p)
            reset=False
        else: #* in case of repetitive input
            clear()
            printboard(q,p)

    r.readline() #* prevent closing too fast

main()