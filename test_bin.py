quattro_map = ((1,1,1,1),
               (1,2,2,2),
               (1,4,2,1),
               (2,2,3,4))

def bin_check(num1, num2, num3, num4):#같지 않으면 False 반환 하나라도 같으면 True
    for k in range(1, 5):
        if(bin(num1)[-k] == "b" or bin(num2)[-k] == "b" or bin(num3)[-k] == "b" or bin(num4)[-k] == "b"):
            break
        if(bin(num1)[-k] == bin(num2)[-k] == bin(num3)[-k] == bin(num3)[-k]):
            return True
    return False

for n in range(4):
    if(bin_check(quattro_map[n][0], quattro_map[n][1], quattro_map[n][2], quattro_map[n][3])):
        print(n, quattro_map[n][0], quattro_map[n][1], quattro_map[n][2], quattro_map[n][3])
        print("1Game End")
    if(bin_check(quattro_map[0][n], quattro_map[1][n], quattro_map[2][n], quattro_map[3][n])):
        print(n, quattro_map[n][0], quattro_map[n][1], quattro_map[n][2], quattro_map[n][3])
        print("2Game End")