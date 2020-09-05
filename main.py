import pygame
import random
import time


from pygame import mixer
#import auto_py_to_exe
mixer.init()
pygame.font.init()
WIDTH=900
HEIGHT=650
WIN=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')
m=random.randint(0, WIDTH - 100)
n=random.randint(-1500, -100)

#sound

bullet_hit_enemy_sound=mixer.Sound('star_war_game_external_files/invaderkilled.wav')
bullet_shoot_sound=mixer.Sound('star_war_game_external_files/shoot.wav')
explosion_of_player_sound=mixer.Sound('star_war_game_external_files/explosion.wav')



# images
menu_pic=pygame.image.load('star_war_game_external_files/menu pic.jpg')
star_wars=pygame.image.load('star_war_game_external_files/star wars text.png')
background_img=pygame.image.load('star_war_game_external_files/starships2.jpg')
player_img=pygame.image.load('star_war_game_external_files/aircraft.png')
player_img_1=pygame.image.load('star_war_game_external_files/jet.png')
enemy_1_img=pygame.image.load('star_war_game_external_files/easy alien.png')
enemy_2_img=pygame.image.load('star_war_game_external_files/medium alien.png')
enemy_3_img=pygame.image.load('star_war_game_external_files/hard alien.png')
player_laser_img=pygame.image.load('star_war_game_external_files/bullets1.png')
enemy_1_laser_img=pygame.image.load('star_war_game_external_files/easy laser.png')
enemy_2_laser_img=pygame.image.load('star_war_game_external_files/medium laser.png')
enemy_3_laser_img=pygame.image.load('star_war_game_external_files/hard laser.png')

bullet_1_img=pygame.image.load('star_war_game_external_files/bullet.png')


class Laser:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.img=enemy_3_laser_img
        self.mask=pygame.mask.from_surface(self.img)
        self.lasers=[]

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel,height):
        self.y+=vel
        if(self.y>height):
            self.x=random.randint(0,650)
            self.y=random.randint(-1500,-1000)

    def collision(self,obj):
        return collide(self,obj)

    def off_screen(self,height):
        return(self.y<=height)




class Ship:
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.ship_img=None
        self.laser_img=None
        self.lasers=[]
        self.cool_down_counter=0

    def draw(self,window):
        window.blit(self.ship_img,(self.x,self.y))

    def get_height(self):
        return self.ship_img.get_height()

    def get_width(self):
        return self.ship_img.get_width()

class Player(Ship):
    def __init__(self,x,y,health=100):
        Ship.__init__(self,x,y,health)
        self.ship_img=player_img
        self.laser_img=player_laser_img
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.max_health=health

    def health_bar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y+self.get_height()+10,self.get_width(),10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.get_height() + 10, (self.get_width()*self.health)/100, 10))


class Bullet:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.bullet_image=player_laser_img
        self.bullet_state='ready'
        self.mask=pygame.mask.from_surface(self.bullet_image)
        self.did_it_hit_enemy=False

    def draw_of_bullet(self, window):
            window.blit(self.bullet_image, (self.x, self.y))

    def shooting_of_player(self, vel):
        self.bullet_state = 'fire'
        if self.did_it_hit_enemy==False:
            self.y -= vel
        else:
            self.y=1000

    def bullet_boundary(self):
        if(self.y<0):
            return True


class Enemy(Ship):
    diffulty_map = {'easy': (enemy_1_img,enemy_1_laser_img) ,'medium': (enemy_2_img,enemy_2_laser_img) ,'hard': (enemy_3_img,enemy_3_laser_img)}
    def __init__(self,x,y,diffulty,health=100):
        Ship.__init__(self,x,y,health=100)
        self.ship_img,self.laser_img=self.diffulty_map.get(diffulty)
        self.mask=pygame.mask.from_surface(self.ship_img)
        self.laser_x=self.x
        self.laser_y=self.y

    def move(self,vel):
        self.y+=vel













def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    lol=(obj1.mask.overlap(obj2.mask,(offset_x,offset_y)))
    #!= None returns tuple of cordinates
    if(lol):
        return True
    else:
        return False




def main():

    run=True
    FPS=60
    clock=pygame.time.Clock()
    level=1
    lives=5
    main_font=pygame.font.SysFont('comicsans',40)
    lost_font = pygame.font.SysFont('comicsans', 40)
    player_vel=8
    enemy_vel=1
    laser_vel=5
    enemies=[]
    lasers=[]
    wave_length=5
    player_bullet_speed=4

    player=Player(150,560)
    bullet = Bullet(player.x+12,player.y)
    for i in range(level):
        laser=Laser(random.randint(0, WIDTH - 100), random.randint(-1500, -100))
        lasers.append(laser)




    lost=False
    lost_count=0


    def redraw_window():


        WIN.blit(background_img,(0,0))
        lives_label=main_font.render('Lives : ' +str(lives), 1 ,(255,255,255))
        level_label = main_font.render('Level : ' + str(level-1), 1, (255, 255, 255))

        if(level>2):
            player.ship_img=player_img_1

        WIN.blit(lives_label,(10,10))
        WIN.blit(level_label,(WIDTH-level_label.get_width()-10,10))

        if lost == True:
            lost_label = lost_font.render('You Lost !', 1, (255, 255, 200))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2,300))

        for enemy in enemies:
            enemy.draw(WIN)



        player.draw(WIN)
        for laser in lasers:
            laser.draw(WIN)

        if(bullet.bullet_state=='fire'):
            bullet.draw_of_bullet(WIN)

        player.health_bar(WIN)
        pygame.display.update()

    while run:
        clock.tick(FPS)

        redraw_window()
        bullet.draw_of_bullet(WIN)
        bullet.shooting_of_player(player_bullet_speed)

        for laser in lasers:
            laser.move(laser_vel,HEIGHT)
            fire_ball_hit=collide(bullet,laser)
            if fire_ball_hit==True:
                laser.y= random.randint(-1500, -100)
                laser.x= random.randint(0, WIDTH - 100)
                bullet.did_it_hit_enemy=True




        if(lives <= 0) or player.health<0:
            lost=True
            lost_count+=1
        if lost:
            if (lost_count > FPS * 3):
                run = False
            else:
                continue


        if len(enemies)==0:
            level+=1
            wave_length+=5

            for i in range(wave_length):
                if level==1:
                    enemy = Enemy(random.randint(0, WIDTH - 100), random.randint(-1500, -100),'easy')
                    enemy_obj=enemy
                elif level==2:
                    enemy = Enemy(random.randint(0, WIDTH - 100), random.randint(-1500, -100),random.choice(['easy', 'medium']))
                    enemy_obj = enemy
                else:
                    enemy=Enemy(random.randint(0,WIDTH-100),random.randint(-1500,-100),random.choice(['easy','medium','hard']))
                    enemy_obj = enemy
                enemies.append(enemy)

        for enemy in enemies:
                enemy.move(enemy_vel)
                enemy_player_hit=collide(player,enemy)
                if enemy_player_hit==True:
                    explosion_of_player_sound.play()
                    enemies.remove(enemy)
                    player.health-=10
                    print(player.health)
                if(enemy.y+enemy.get_height()>HEIGHT):
                    lives-=1
                    enemies.remove(enemy)
                condition=collide(bullet,enemy)
                if condition==True:
                    bullet_hit_enemy_sound.play()
                    enemies.remove(enemy)
                    bullet.did_it_hit_enemy=True

        for laser in lasers:
            condition_laser=collide(player,laser)
            if condition_laser==True:
                player.health-=20
                explosion_of_player_sound.play()
                laser.x = random.randint(0, 650)
                laser.y = random.randint(-1500, -1000)
                print(player.health)





        if bullet.bullet_state=='fire':
            bullet.shooting_of_player(player_bullet_speed)






        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_vel >0:
            player.y-=player_vel
            if bullet.bullet_state=='ready':
                bullet.y-=player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel +25< 590:
            player.y += player_vel
            if bullet.bullet_state == 'ready':
                bullet.y += player_vel
        if keys[pygame.K_RIGHT]and player.x + player_vel < 840:
            player.x+=player_vel
            if bullet.bullet_state == 'ready':
                bullet.x += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
            if bullet.bullet_state == 'ready':
                bullet.x -= player_vel
        if keys[pygame.K_SPACE]:
            bullet.bullet_state = 'fire'
            bullet_shoot_sound.play()
            if bullet.bullet_boundary() or bullet.did_it_hit_enemy:
                bullet=Bullet(player.x+12,player.y)


def main_menu():
    run=True
    title_font=pygame.font.SysFont('comicsans',30)
    while run:
        WIN.blit(menu_pic,(-200,-100))
        WIN.blit(star_wars,(130,190))
        title_label=title_font.render('Press any button to begin',1,(255,255,255))
        WIN.blit(title_label,(100,450))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                main()
            elif event.type==pygame.QUIT:
                run=False
    pygame.quit()
main_menu()
