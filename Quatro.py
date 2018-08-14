import pygame
import random
import numpy as np
from time import sleep

# 게임에 사용되는 전역변수 정의
BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
WhiteBox = (255, 255, 255)
quattro_width = 1280  # 게임화면의 가로크기
quattro_height = 720  # 게임화면의 세로크기
quattro_map = np.zeros([4,4]) # 콰트로 맵은 왼쪽의 실제 게임 맵이다.
pick_map = np.zeros([4,4]) # pick_map은 남은 패들을 그린 맵이다.
img_list = [] # 실제 이미지를 저장한 것들
select_img_list = [] # 선택된 이미지를 저장을 한다.
background_img = pygame.image.load("img/background.png")
turn = pygame.image.load("img/turn.png")
click = -1
picked_mal = 0
previous_select = -1
player = 0
player_text = ""

for i in range(1, 17):
    file_name = "img/" + str(i) + ".PNG"
    img_list.append(pygame.image.load(file_name))
    file_name = "select_img/" + str(i) + ".png"
    select_img_list.append(pygame.image.load(file_name))

def initData():
    global pick_map, quattro_map, player

    player = 0
    for i in range(4):
        for j in range(4):
            pick_map[i][j] = i * 4 + j
            quattro_map[i][j] = -1

def drawObject(obj, x, y):
    global background
    background.blit(obj, (x, y))

def dispMessage(text):
    global background
    textfont = pygame.font.Font('freesansbold.ttf', 40)
    text = textfont.render(text, True, RED)
    textpos = text.get_rect()
    textpos.center = (quattro_width / 2, quattro_height / 2)
    background.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

# 게임 초기화 함수
def initGame():
    global background, clock, pick_map, quattro_map  # 게임이 진행될 게임 화면, 게임의 초당 프레임(FPS), 비행기 변수 선언, 적 선언

    pygame.init()
    background = pygame.display.set_mode((quattro_width, quattro_height))  # 게임화면의 가로세로크기를 설정
    pygame.display.set_caption('Quatro')  # 게임화면의 제목 지정
    clock = pygame.time.Clock()  # 초당 프레임수를 설정할 수 있는 Clock객체 생성

def my_bin(num):
    temp = bin(int(num))[2:]
    if(len(temp) == 4):
        pass
    elif(len(temp) == 3):
        temp = "0" + temp
    elif(len(temp) == 2):
        temp = "00" + temp
    elif(len(temp) == 1):
        temp = "000" + temp
    return temp

def bin_check(num1, num2, num3, num4):#같지 않으면 False 반환 하나라도 같으면 True
    if(num1 < 0 or num2 < 0 or num3 < 0 or num4 < 0):
        return False
    for k in range(1, 5):
        if(my_bin(int(num1))[-k] == my_bin(int(num2))[-k] == my_bin(int(num3))[-k] == my_bin(int(num3))[-k]):
            return True
    return False

def CheckWin():
    global quattro_map

    for i in range(4):
        if(bin_check(quattro_map[i][0], quattro_map[i][1], quattro_map[i][2], quattro_map[i][3])):
            return True
        if (bin_check(quattro_map[0][i], quattro_map[1][i], quattro_map[2][i], quattro_map[3][i])):
            return True
    if(bin_check(quattro_map[0][0], quattro_map[1][1], quattro_map[2][2], quattro_map[3][3])):
        return True
    if (bin_check(quattro_map[3][0], quattro_map[2][1], quattro_map[1][2], quattro_map[0][3])):
        return True
    return False

def runGame():
    global click, player, player_text, pick_map, background_img, picked_mal, previous_select, quattro_map

    initData()
    player_text = "GameStart"
    ongame = False
    while not ongame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 마우스로 창을 닫는 이벤트
                exit()
            elif(event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                if( pygame.mouse.get_pos()[0] > 1160 and pygame.mouse.get_pos()[1] < 80):
                    if (player == 3 and click != -1): # Computer 가 패를 놓음
                        if (CheckWin()):
                            dispMessage("Computer Win")

                        else:
                            player_text = "Computer Choice time"
                            player = 4
                            click = -1
                            previous_select = -1

                    elif (player == 1 and click != -1): # 플레이어가 패를 놓음
                        if(CheckWin()):
                            dispMessage("Player Win")

                        else:
                            player_text = "Player Choice time"
                            player = 2
                            click = -1
                            previous_select = -1

                    elif (player == 4 and click != -1 and pick_map[int(click/4)][click%4] != -1): # 컴퓨터가 상대방 패를 골라줌
                        picked_mal = click
                        pick_map[int(click/4)][click%4] = -1
                        player_text = "Player turn"
                        player = 1
                        click = -1
                        previous_select = -1

                    elif (player == 2 and click != -1 and pick_map[int(click/4)][click%4] != -1): # 플레이어가 상대방 패를 골라줌
                        picked_mal = click
                        pick_map[int(click/4)][click%4] = -1
                        player_text = "Computer turn"
                        player = 3
                        click = -1
                        previous_select = -1

                    elif(player == 0):
                        player = 2
                        player_text = "Player Choice time"
                        click = -1
                        previous_select = -1

                if(player == 2 and 640 < pygame.mouse.get_pos()[0] and 80 < pygame.mouse.get_pos()[1]): # pick_map을 선택한 경우
                    click = int((pygame.mouse.get_pos()[0]-640)/160) + 4 * (int((pygame.mouse.get_pos()[1]-80)/160))
                if (player == 4 and 640 < pygame.mouse.get_pos()[0] and 80 < pygame.mouse.get_pos()[1]):  # pick_map을 선택한 경우
                    click = int((pygame.mouse.get_pos()[0] - 640) / 160) + 4 * (int((pygame.mouse.get_pos()[1] - 80) / 160))

                if(player == 1 and pygame.mouse.get_pos()[0] < 640 and 80 < pygame.mouse.get_pos()[1]):
                    click = int((pygame.mouse.get_pos()[0]) / 160) + 4 * (int((pygame.mouse.get_pos()[1] - 80) / 160))
                if (player == 3 and pygame.mouse.get_pos()[0] < 640 and 80 < pygame.mouse.get_pos()[1]):
                    click = int((pygame.mouse.get_pos()[0]) / 160) + 4 * (int((pygame.mouse.get_pos()[1] - 80) / 160))

            elif(event.type == pygame.KEYUP):
                if(event.key == pygame.K_SPACE):
                    dispMessage("Quatro test")
        background.fill(BLACK)

        drawObject(turn, 1160,0)
        for i in range(4):
            for j in range(4):
                if (pick_map[i][j] != -1):
                    drawObject(img_list[int(pick_map[i][j])], 640 + 160 * (j), 80 + 160 * int(i))
                else:
                    drawObject(background_img, 640 + 160 * (j), 80 + 160 * int(i))

                if (quattro_map[i][j] != -1):
                    drawObject(img_list[int(quattro_map[i][j])], 160 * (j), 80 + 160 * int(i))
                else:
                    drawObject(background_img, 160 * (j), 80 + 160 * int(i))

        if(click != -1 and player == 2):
            if(pick_map[int(click/4)][click%4] != -1):
                drawObject(select_img_list[click], 640 + 160 * (click % 4), 80 + 160 * int((click / 4)))
        if (click != -1 and player == 4):
            if (pick_map[int(click / 4)][click % 4] != -1):
                drawObject(select_img_list[click], 640 + 160 * (click % 4), 80 + 160 * int((click / 4)))

        if(click != -1 and player == 1):
            if(quattro_map[int(click/4)][click%4] == -1):
                if(previous_select != -1):
                    quattro_map[int(previous_select / 4)][previous_select % 4] = -1
                quattro_map[int(click/4)][click%4] = picked_mal
                previous_select = click

        if(click != -1 and player == 3):
            if (quattro_map[int(click / 4)][click % 4] == -1):
                if (previous_select != -1):
                    quattro_map[int(previous_select / 4)][previous_select % 4] = -1
                quattro_map[int(click / 4)][click % 4] = picked_mal
                previous_select = click

        #텍스트 출력하는 코드
        textfont = pygame.font.Font('freesansbold.ttf', 20)
        text = textfont.render(player_text, True, (255,255,255))
        textpos = text.get_rect()
        textpos.center = (quattro_width / 2, 40)
        background.blit(text, textpos)


        pygame.display.update()  # 게임화면을 다시그림
        clock.tick(60)  # 게임화면의 초당 프레임수를 60으로 설정
    pygame.quit()


initGame()
initData()
runGame()