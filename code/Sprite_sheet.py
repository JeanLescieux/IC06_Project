import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((800, 600))

# 加载贴图集
sprite_sheet = pygame.image.load('../graphics/Tilemap.png').convert_alpha()

# Floor
sprite_rect = pygame.Rect(0, 0, 16, 16)
sprite_Floor1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 16, 16, 16)
sprite_Floor2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80, 0, 16, 16)
sprite_Floor3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80, 16, 16, 16)
sprite_Floor4 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 64, 16, 16)
sprite_Floor5 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 80, 16, 16)
sprite_Floor6 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 128, 16, 16)
sprite_Floor7 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80, 128, 16, 16)
sprite_Floor7_mirror = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 128, 16, 16)
sprite_Floor8 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 128, 16, 16)
sprite_Floor9 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 128, 16, 16)
sprite_Floor10 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 176, 16, 16)
sprite_Floor11 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 176, 16, 16)
sprite_Floor12 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 192, 16, 16)
sprite_Floor13 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 192, 16, 16)
sprite_Floor14 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 192, 16, 16)
sprite_Floor15 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 192, 16, 16)
sprite_Floor16 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 192, 16, 16)
sprite_Floor17 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 208, 16, 16)
sprite_Floor18 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 208, 16, 16)
sprite_Floor19 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 208, 16, 16)
sprite_Floor20 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 224, 16, 16)
sprite_Floor21 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 224, 16, 16)
sprite_Floor22 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 224, 16, 16)
sprite_Floor23 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80, 80, 16, 16)
sprite_Floor24 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 48, 16, 16)
sprite_Floor25 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 48, 16, 16)
sprite_Floor26 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80, 64, 16, 16)
sprite_Floor27 = sprite_sheet.subsurface(sprite_rect)

#Bricks
sprite_rect = pygame.Rect(16, 0, 16, 16)
sprite_Brick1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 0, 16, 16)
sprite_Brick1_mirror = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 0, 16, 16)
sprite_Brick2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 0, 16, 16)
sprite_Brick2_mirror = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 16, 16, 16)
sprite_Brick3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 64, 16, 16)
sprite_Brick3_mirror = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 16, 16, 16)
sprite_Brick4 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 64, 16, 16)
sprite_Brick4_mirror = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 80, 16, 16)
sprite_Brick5 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 64, 16, 16)
sprite_Brick6 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 80, 16, 16)
sprite_Brick7 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 80, 16, 16)
sprite_Brick7_mirror = sprite_sheet.subsurface(sprite_rect)


#Walls
sprite_rect = pygame.Rect(32, 16, 16, 32)
sprite_Wall1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 16, 16, 32)
sprite_Wall2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 96, 16, 32)
sprite_Wall3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 96, 16, 32)
sprite_Wall4 = sprite_sheet.subsurface(sprite_rect)

#Pool
sprite_rect = pygame.Rect(0, 144, 16, 16)
sprite_Pool1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16, 144, 16, 16)
sprite_Pool2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0,160, 16, 16)
sprite_Pool3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16,160, 16, 16)
sprite_Pool4 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 144, 16, 16)
sprite_Pool5 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 144, 16, 16)
sprite_Pool6 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 144, 16, 16)
sprite_Pool7 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 160, 16, 16)
sprite_Pool8 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 160, 16, 16)
sprite_Pool9 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 160, 16, 16)
sprite_Pool10 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32, 176, 16, 16)
sprite_Pool11 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(48, 176, 16, 16)
sprite_Pool12 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64, 176, 16, 16)
sprite_Pool13 = sprite_sheet.subsurface(sprite_rect)


#Stairs
sprite_rect = pygame.Rect(0, 32, 32, 32)
sprite_Dstairs_L = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64,32, 32, 32)
sprite_Dstairs_R = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0, 208, 32, 32)
sprite_Ustairs_L = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0,240, 32, 32)
sprite_Ustairs_R = sprite_sheet.subsurface(sprite_rect)

#Trap
sprite_rect = pygame.Rect(0,272, 16, 16)
sprite_Trap_Open = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16,272, 16, 16)
sprite_Trap_Close = sprite_sheet.subsurface(sprite_rect)

#Key
sprite_rect = pygame.Rect(80,144, 16, 16)
sprite_Key = sprite_sheet.subsurface(sprite_rect)

#Barrel
sprite_rect = pygame.Rect(80,160, 16, 32)
sprite_Barrel = sprite_sheet.subsurface(sprite_rect)

#Treasure box
sprite_rect = pygame.Rect(96, 64, 48, 48)
sprite_TreasureBox_Close = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(96, 112, 48, 48)
sprite_TreasureBox_Empty = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(96, 160, 48, 48)
sprite_TreasureBox_Full = sprite_sheet.subsurface(sprite_rect)

#Windows
sprite_rect = pygame.Rect(128, 208, 16, 32)
sprite_Windows_Close = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(128, 240, 16, 32)
sprite_Windows_Open = sprite_sheet.subsurface(sprite_rect)

#Torch
sprite_rect = pygame.Rect(80, 256, 16, 32)
sprite_Torch = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(96, 256, 16, 48)
sprite_Torch_L = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(112, 256, 16, 48)
sprite_Torch_R = sprite_sheet.subsurface(sprite_rect)



#Peristele
sprite_rect = pygame.Rect(96,0, 48, 64)
sprite_peristele = sprite_sheet.subsurface(sprite_rect)

#Doors
sprite_rect = pygame.Rect(32,240, 48, 48)
sprite_Door_Close = sprite_sheet.subsurface(sprite_rect)

# sprite_rect1 = pygame.Rect(80,192, 16, 16)
# sprite_rect2 = pygame.Rect(80,208, 48, 48)
# image_part1 = sprite_sheet.subsurface(sprite_rect1.copy()
# image_part2 = sprite_sheet.subsurface(sprite_rect2).copy()
#
# new_surface_width = max(80 + 16, 80 + 48)
# new_surface_height = max(192+ 16, 208 + 48)
# new_surface = pygame.Surface((new_surface_width, new_surface_height), pygame.SRCALPHA)
#
# # 将两个图案部分拼接到新的 Surface 上
# new_surface.blit(image_part1, (x1, y1))
# new_surface.blit(image_part2, (x2, y2))


#COMPONETS

# FLOORS
sprite_rect = pygame.Rect(0,64, 16, 64)
sprite_C_Floor1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(80,64, 16, 64)
sprite_C_Floor2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32,48, 32, 16)
sprite_C_Floor3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(0,128, 32, 16)
sprite_C_Floor4 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(64,128, 32, 16)
sprite_C_Floor5 = sprite_sheet.subsurface(sprite_rect)

#WALLS
sprite_rect = pygame.Rect(16,0, 64, 16)
sprite_C_Wall1 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16,64, 48, 16)
sprite_C_Wall2 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(32,80, 32, 16)
sprite_C_Wall3 = sprite_sheet.subsurface(sprite_rect)

sprite_rect = pygame.Rect(16,96, 64, 32)
sprite_C_Wall4 = sprite_sheet.subsurface(sprite_rect)

# # 游戏主循环
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # 清屏
#     screen.fill((0, 0, 0))
#
#     # units
#     screen.blit(sprite_Floor1, (0, 0))
#     screen.blit(sprite_Floor2, (32, 0))
#     screen.blit(sprite_Floor3, (64, 0))
#     screen.blit(sprite_Floor4, (96, 0))
#     screen.blit(sprite_Floor5, (128, 0))
#     screen.blit(sprite_Floor6, (160, 0))
#     screen.blit(sprite_Floor7, (192, 0))
#     screen.blit(sprite_Floor7_mirror, (224, 0))
#     screen.blit(sprite_Floor8, (256, 0))
#     screen.blit(sprite_Floor9, (288, 0))
#     screen.blit(sprite_Floor10, (320, 0))
#     screen.blit(sprite_Floor11, (352, 0))
#     screen.blit(sprite_Floor12, (384, 0))
#     screen.blit(sprite_Floor13, (416, 0))
#     screen.blit(sprite_Floor14, (448, 0))
#     screen.blit(sprite_Floor15, (480, 0))
#     screen.blit(sprite_Floor16, (512, 0))
#     screen.blit(sprite_Floor17, (544, 0))
#     screen.blit(sprite_Floor18, (576, 0))
#     screen.blit(sprite_Floor19, (608, 0))
#     screen.blit(sprite_Floor20, (640, 0))
#     screen.blit(sprite_Floor21, (672, 0))
#     screen.blit(sprite_Floor22, (704, 0))
#     screen.blit(sprite_Floor23, (736, 0))
#     screen.blit(sprite_Floor24, (768, 0))
#     screen.blit(sprite_Floor25, (384, 32))
#     screen.blit(sprite_Floor26, (416, 32))
#     screen.blit(sprite_Floor27, (448, 32))
#
#
#     screen.blit(sprite_Brick1, (0, 32))
#     screen.blit(sprite_Brick1_mirror, (32, 32))
#     screen.blit(sprite_Brick2, (64, 32))
#     screen.blit(sprite_Brick2_mirror, (96, 32))
#     screen.blit(sprite_Brick3, (128, 32))
#     screen.blit(sprite_Brick3_mirror, (160, 32))
#     screen.blit(sprite_Brick4, (192, 32))
#     screen.blit(sprite_Brick4_mirror, (224, 32))
#     screen.blit(sprite_Brick5, (256, 32))
#     screen.blit(sprite_Brick6, (288, 32))
#     screen.blit(sprite_Brick7, (320, 32))
#     screen.blit(sprite_Brick7_mirror, (352, 32))
#
#     screen.blit(sprite_Pool1, (0, 64))
#     screen.blit(sprite_Pool2, (32, 64))
#     screen.blit(sprite_Pool3, (64, 64))
#     screen.blit(sprite_Pool4, (96, 64))
#     screen.blit(sprite_Pool5, (128, 64))
#     screen.blit(sprite_Pool6, (160, 64))
#     screen.blit(sprite_Pool7, (192, 64))
#     screen.blit(sprite_Pool8, (224, 64))
#     screen.blit(sprite_Pool9, (256, 64))
#     screen.blit(sprite_Pool10, (288, 64))
#     screen.blit(sprite_Pool11, (320, 64))
#     screen.blit(sprite_Pool12, (352, 64))
#     screen.blit(sprite_Pool13, (384, 64))
#
#
#
#     screen.blit(sprite_Wall1, (0, 96))
#     screen.blit(sprite_Wall2, (32, 96))
#     screen.blit(sprite_Wall3, (64, 96))
#     screen.blit(sprite_Wall4, (96, 96))
#
#     screen.blit(sprite_Key, (128, 96))
#     screen.blit(sprite_Barrel, (160, 96))
#
#     screen.blit(sprite_Dstairs_L, (0, 144))
#     screen.blit(sprite_Dstairs_R, (48, 144))
#     screen.blit(sprite_Ustairs_L, (96, 144))
#     screen.blit(sprite_Ustairs_R, (144, 144))
#     screen.blit(sprite_Trap_Open, (192, 144))
#     screen.blit(sprite_Trap_Close, (224, 144))
#
#     screen.blit(sprite_peristele, (0, 180))
#     screen.blit(sprite_Door_Close, (64, 180))
#     screen.blit(sprite_TreasureBox_Close, (128, 180))
#     screen.blit(sprite_TreasureBox_Empty, (192, 180))
#     screen.blit(sprite_TreasureBox_Full, (240, 180))
#     screen.blit(sprite_Windows_Close, (304, 180))
#     screen.blit(sprite_Windows_Open, (336, 180))
#     screen.blit(sprite_Torch, (368, 180))
#     screen.blit(sprite_Torch_L, (400, 180))
#     screen.blit(sprite_Torch_R, (432, 180))
#
#
#
#     #Components
#     screen.blit(sprite_C_Floor1, (0,260 ))
#     screen.blit(sprite_C_Floor2, (32, 260))
#     screen.blit(sprite_C_Floor3, (64, 260))
#     screen.blit(sprite_C_Floor4, (112, 260))
#     screen.blit(sprite_C_Floor5, (160, 260))
#
#     screen.blit(sprite_C_Wall1, (0, 348))
#     screen.blit(sprite_C_Wall2, (80, 348))
#     screen.blit(sprite_C_Wall3, (160, 348))
#     screen.blit(sprite_C_Wall4, (240, 348))
#
#     # 更新屏幕
#     pygame.display.flip()
#
# # 退出 Pygame
# pygame.quit()
# sys.exit()
