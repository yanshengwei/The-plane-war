import pygame
import sys
import random
import time
from pygame.locals import *
# 定义常量(定义后,不再改值)
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 500
bullet_list = []
enemy_bullet_list = []
enemy_list = []
bigbullet_list = []
score = 0
bigbullet_num1 = 0
bigbullet_num = 0


class Item:
    window = None

    def __init__(self, img, x, y, self_x, self_y):
        self.img = pygame.image.load(img)
        self.self_x = self_x
        self.self_y = self_y
        self.x = x
        self.y = y


class BasePlane(Item):
        pass#占位语句


def big_shoot():#定义导弹发射
    global bigbullet_num#导弹数
    if bigbullet_num >= 1:
        for x in range(0, 501, 20):
            bullet = BigBullet('res/bullet_14.png', x, WINDOW_HEIGHT, 20, 56)
            bigbullet_list.append(bullet)
        bigbullet_num -= 1

#########################################################################################
class HeroPlane(BasePlane):#定义主机

    def __init__(self, img, img2, x, y, self_x, self_y):
        BasePlane.__init__(self, img, x, y, self_x, self_y)
        self.img2 = pygame.image.load(img2)

    def display(self):
        self.bullet_fly()
        self.bigbullet_fly()
        self.window.blit(self.img2, (self.x, self.y))#主机本身图片

    #######"W""A""S""D"控制飞机的上下左右
    def move_lift(self):
        if self.x > 0:
            self.x -= 7

    def move_right(self):
        if self.x < WINDOW_WIDTH - self.self_x:
            self.x += 7

    def move_up(self):
        if self.y > 0:
            self.y -= 7

    def move_down(self):
        if self.y < WINDOW_HEIGHT - self.self_y:
            self.y += 7

    def shoot(self):  # 主机发射三个等级的子弹
        if score <= 5000:  # 当积分达到5000分时，子弹升级
            bullet = Bullet('res/bullet_9.png', self.x + self.self_x / 2 - 10, self.y, 20, 31)
            bullet_list.append(bullet)
        elif 5000 < score <= 10000:
            bullet = Bullet('res/bullet_12.png', self.x + self.self_x - 20, self.y + 29, 20, 29)
            bullet1 = Bullet('res/bullet_12.png', self.x + 20, self.y + 29, 20, 29)
            bullet_list.append(bullet)
            bullet_list.append(bullet1)
        else:
            bullet = Bullet('res/bullet_10.png', self.x + self.self_x - 20, self.y + 29, 20, 29)
            bullet1 = Bullet('res/bullet_10.png', self.x + self.self_x, self.y + 29, 20, 29)
            bullet2 = Bullet('res/bullet_10.png', self.x + self.self_x + 20, self.y + 29, 20, 29)
            bullet_list.append(bullet)
            bullet_list.append(bullet1)
            bullet_list.append(bullet2)

    @staticmethod
    def bigbullet_fly():
        del_bullet = []
        for bullet in bigbullet_list:
            if bullet.y >= 0:
                bullet.display()
                bullet.move()
            else:
                del_bullet.append(bullet)
        for db in del_bullet:
            bigbullet_list.remove(db)

    @staticmethod
    def bullet_fly():
        del_bullet = []
        for bullet in bullet_list:
            if bullet.y >= 0:
                bullet.display()
                bullet.move()
            else:
                del_bullet.append(bullet)
        for db in del_bullet:
            bullet_list.remove(db)

    def hurt(self):
        pass
        for enemy in enemy_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(enemy.x, enemy.y, enemy.self_x, enemy.self_y)):
                enemy.x = random.randint(0, WINDOW_WIDTH - self.self_x)
                enemy.y = 0
                return True
        for enemy_bullet in enemy_bullet_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(enemy_bullet.x, enemy_bullet.y, enemy_bullet.self_x,
                                                   enemy_bullet.self_y)):
                enemy_bullet_list.remove(enemy_bullet)
                return True
########################################################################################################################

class EnemyPlane(BasePlane):#定义敌机
    def __init__(self, img, boom_img, boom2_img, boom_sound, x, y, self_x, self_y):
        BasePlane.__init__(self, img, x, y, self_x, self_y)
        self.boom_img = pygame.image.load(boom_img)
        self.boom2_img = pygame.image.load(boom2_img)
        self.boom_sound = pygame.mixer.Sound(boom_sound)
        enemy_list.append(self)

    def move(self):
        if self.y >= WINDOW_HEIGHT:
            self.y = random.randint(-300, -68)
            self.x = random.randint(0, WINDOW_WIDTH - self.self_x)
            self.img = pygame.image.load('res/img-plane_%d.png' % random.randint(1, 6))
        if score < 10000:
            self.y += 1
        if 10000 <= score < 20000:
            self.y += 2
        if 20000 <= score:
            self.y += 3

    def display(self):
        self.window.blit(self.img, (self.x, self.y))
        self.move()
        self.hurt()

    def boom_display(self):
        self.boom_sound.play()
        self.window.blit(self.boom_img, (self.x, self.y))
        self.window.blit(self.boom2_img, (self.x, self.y))

    def hurt(self):
        global score
        global bigbullet_num1
        for bullet in bullet_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(bullet.x, bullet.y, bullet.self_x, bullet.self_y)):
                self.boom_display()
                score += 100
                bigbullet_num1 += 1
                self.y = random.randint(-300, -68)
                self.x = random.randint(0, WINDOW_WIDTH - self.self_x)
                self.img = pygame.image.load('res/img-plane_%d.png' % random.randint(1, 6))
                bullet_list.remove(bullet)
        for bullet in bigbullet_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(bullet.x, bullet.y, bullet.self_x, bullet.self_y)):
                self.boom_display()
                score += 100
                bigbullet_num1 += 1
                self.y = random.randint(-300, -68)
                self.x = random.randint(0, WINDOW_WIDTH - self.self_x)
                self.img = pygame.image.load('res/img-plane_%d.png' % random.randint(1, 6))


class BigEnemyPlane(EnemyPlane):
    def __init__(self, img, boom_img, boom2_img, boom_sound, x, y, self_x, self_y):
        EnemyPlane.__init__(self, img, boom_img, boom2_img, boom_sound, x, y, self_x, self_y)
        self.enemy_bullet()

    def display(self):
        EnemyPlane.display(self)
        self.enemy_bullet_display()

    def hurt(self):
        global score
        global bigbullet_num1
        for bullet in bullet_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(bullet.x, bullet.y, bullet.self_x, bullet.self_y)):
                self.boom_display()
                score += 100
                bigbullet_num1 += 1
                self.y = WINDOW_HEIGHT
                self.enemy_bullet()
                bullet_list.remove(bullet)
        for bullet in bigbullet_list:
            if pygame.Rect.colliderect(pygame.Rect(self.x, self.y, self.self_x, self.self_y),
                                       pygame.Rect(bullet.x, bullet.y, bullet.self_x, bullet.self_y)):
                self.boom_display()
                score += 200
                bigbullet_num1 += 2
                self.y = WINDOW_HEIGHT
                self.enemy_bullet()

    def move(self):
        if self.y >= WINDOW_HEIGHT * 2:
            self.y = 0
            self.x = random.randint(0, WINDOW_WIDTH - self.self_x)
            self.enemy_bullet()
        if score < 10000:
            self.y += 1
        if 10000 <= score < 20000:
            self.y += 2
        if 20000 <= score:
            self.y += 3

    def enemy_bullet(self):
        enemy_bullet = EnemyBullet('res/bullet_3.png',
                                   self.x + self.self_x/2 - 10, self.y + self.self_y, 20, 40)
        enemy_bullet_list.append(enemy_bullet)

    @staticmethod
    def enemy_bullet_display():
        del_bullet = []
        for enemy_bullet in enemy_bullet_list:
            if enemy_bullet.y <= WINDOW_HEIGHT:
                enemy_bullet.display()
                enemy_bullet.move()
            else:
                del_bullet.append(enemy_bullet)
        for db in del_bullet:
            enemy_bullet_list.remove(db)


class Bullet(Item):

    def display(self):
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y -= 5


class EnemyBullet(Bullet):
    def move(self):#敌机子弹移动速度
        if score < 10000:
            self.y += 2
        if 10000 <= score < 20000:
            self.y += 3
        if 20000 <= score:
            self.y += 4


class BigBullet(Bullet):
    def move(self):
        self.y -= 2


class BeiJing:
    def __init__(self, window, bj_img, start_img, stop_img, hero_plane):
        self.window = window
        self.start_img = pygame.image.load(start_img)
        self.stop_img = pygame.image.load(stop_img)
        self.hero_plane = hero_plane
        self.bj_img = pygame.image.load(bj_img)

    def start(self):
        """开始时等待输入界面"""
        while True:
            self.window.blit(self.start_img, (0, 0))
            font_obj = pygame.font.Font("res/SIMHEI.TTF", 42)
            font_obj2 = pygame.font.Font("res/SIMHEI.TTF", 60)
            text_obj = font_obj.render("ENTER开始  ESC退出", 1, (255, 255, 255))
            text_obj2 = font_obj2.render("飞机大战", 1, (0, 255, 0))
            text_rect = text_obj.get_rect(centerx=260, centery=380)
            text_rect2 = text_obj.get_rect(centerx=300, centery=280)
            self.window.blit(text_obj, text_rect)
            self.window.blit(text_obj2, text_rect2)
            pygame.display.update()
            for event in pygame.event.get():
                # 1. 鼠标点击关闭窗口事件
                if event.type == QUIT:
                    print("点击关闭窗口按钮")
                    sys.exit()  # 关闭程序
                # 2. 键盘按下事件
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return
                    elif event.key == K_ESCAPE:
                        sys.exit()

    def die(self):
        """死亡后停止界面"""
        while True:
            global score
            global bigbullet_num1
            global bigbullet_num
            pygame.mixer.music.stop()
            bullet_list.clear()
            bigbullet_list.clear()
            enemy_bullet_list.clear()
            self.hero_plane.x = 190
            self.hero_plane.y = 500
            for enemy in enemy_list:
                enemy.y = 0
            score = 0
            bigbullet_num1 = 0
            bigbullet_num = 0
            self.window.blit(self.stop_img, (0, 0))
            font_obj = pygame.font.Font("res/SIMHEI.TTF", 42)
            font_obj2 = pygame.font.Font("res/SIMHEI.TTF", 60)
            text_obj = font_obj.render("按ENTER重新开始,ESC退出", 1, (255, 255, 255))
            text_obj2 = font_obj2.render("游戏结束", 1, (0, 255, 0))
            text_rect = text_obj.get_rect(centerx=260, centery=380)
            text_rect2 = text_obj.get_rect(centerx=380, centery=280)
            self.window.blit(text_obj, text_rect)
            self.window.blit(text_obj2, text_rect2)
            pygame.display.update()
            for event in pygame.event.get():
                # 1. 鼠标点击关闭窗口事件
                if event.type == QUIT:
                    print("点击关闭窗口按钮")
                    sys.exit()  # 关闭程序
                # 2. 键盘按下事件
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pygame.mixer.music.play(-1)
                        return
                    elif event.key == K_ESCAPE:
                        sys.exit()

    def num(self):
        """分数与大招数量"""
        global bigbullet_num
        global bigbullet_num1
        font_obj = pygame.font.Font("res/SIMHEI.TTF", 30)
        text_obj = font_obj.render("得分: %d" % score, 1, (255, 255, 255))
        text_rect = text_obj.get_rect(centerx=80, centery=20)
        if bigbullet_num1 >= 60:#击落敌机数达到100时，得到一枚导弹
            bigbullet_num += 1
            bigbullet_num1 -= 60#敌机击落数清零
        font_obj = pygame.font.Font("res/SIMHEI.TTF", 30)
        text_obj1 = font_obj.render("* %d" % bigbullet_num, 1, (0, 255, 0))
        text_rect1 = text_obj1.get_rect(centerx=60, centery=80)
        self.window.blit(text_obj, text_rect)
        self.window.blit(text_obj1, text_rect1)
        pygame.display.update()


class BjCri(Item):
    """背景循环"""
    def display(self):
        """背景显示"""
        self.move()
        self.window.blit(self.img, (self.x, self.y - WINDOW_HEIGHT))
        self.window.blit(self.img, (self.x, self.y))

    def move(self):
        """背景移动"""
        if self.y == WINDOW_HEIGHT:
            self.y = 0
        else:
            self.y += 1


def main():
    pygame.init()
    # 创建窗口
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    Item.window = window
    # 加载图片文件，返回图片对象
    pygame.mixer.music.load("res/bg3.mp3")#背景音乐
    bigbulletnum_img = pygame.image.load("res/bullet_14.png")#导弹图标
    hero_plane = HeroPlane('res/hero.png', 'res/hero2.png', 190, 500, 100, 68)
    beijing = BeiJing(window, "res/img_bg_level_1.jpg", 'res/img_bg_level_3.jpg',
                      'res/img_bg_level_2.jpg', hero_plane)
    bj_circulation = BjCri("res/img_bg_level_0.jpg", 0, 0, 500, 700)#游戏进入初始背景设置
    for _ in range(4):
        enemy_plane = EnemyPlane('res/img-plane_%d.png' % random.randint(1, 6),
                                 'res/bomb-1.png',
                                 'res/bomb-2.png', "res/bomb.wav", random.randint(0, WINDOW_WIDTH-100),
                                 random.randint(-300, -68), 100, 68)
        enemy_list.append(enemy_plane)
    enemy_plane2 = BigEnemyPlane('res/img-plane_7.png',
                                 'res/bomb-1.png', 'res/bomb-2.png', "res/bomb.wav",
                                 random.randint(0, WINDOW_WIDTH - 100), random.randint(-300, -68), 100, 68)
    enemy_list.append(enemy_plane2)
    # 设置窗口标题
    pygame.display.set_caption("飞机大战")
    pygame.mixer.music.play(-1)
    # 设置窗口图标
    image = pygame.image.load("res/game.ico")
    pygame.display.set_icon(image)
    beijing.start()
    while True:
        # # 贴图（指定坐标，将图片绘制到窗口）
        bj_circulation.display()
        window.blit(bigbulletnum_img, (5, 50))
        hero_plane.display()
        for enemy_plane in enemy_list:
            enemy_plane.display()
        beijing.num()
        if hero_plane.hurt():
            beijing.die()
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()
        # 获取新事件
        for event in pygame.event.get():
            # 1. 鼠标点击关闭窗口事件
            if event.type == QUIT:
                sys.exit()  # 关闭程序
            # 2. 键盘按下事件
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    hero_plane.shoot()
                if event.key == K_f:
                    big_shoot()
        # 获取当前键盘所有按键的状态（按下/没有按下），返回bool元组  (0, 0, 0, 0, 1, 0, 0, 0, 0)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            hero_plane.move_lift()
        if pressed_keys[K_w] or pressed_keys[K_UP]:
            hero_plane.move_up()
        if pressed_keys[K_s] or pressed_keys[K_DOWN]:
            hero_plane.move_down()
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            hero_plane.move_right()
        # if pressed_keys[K_SPACE]:
        #     hero_plane.shoot()
        time.sleep(0.01)


if __name__ == '__main__':
    main()