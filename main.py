import pygame
import sys
import myplane
import enemy
import bullet
import supply
from pygame.locals import *
from random import *

#初始化pygame和pygame混音器模块
pygame.init()
pygame.mixer.init()

#设置窗口尺寸和标题
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战 -- 小坨Demo")

#加载背景图片
background = pygame.image.load("images/background4.jpg").convert()

#颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

# 添加敌机到对应敌机组
def add_small_enemies(group1, group2, num):
	for i in range(num):
		e1 = enemy.SmallEnemy(bg_size)
		group1.add(e1)
		group2.add(e1)

def add_mid_enemies(group1, group2, num):
	for i in range(num):
		e2 = enemy.MidEnemy(bg_size)
		group1.add(e2)
		group2.add(e2)

def add_big_enemies(group1, group2, num):
	for i in range(num):
		e3 = enemy.BigEnemy(bg_size)
		group1.add(e3)
		group2.add(e3)

def add_speed(target,add_speed):
	for each in target:
		each.speed += add_speed
				
def main():
	#设置背景音乐循环播放
	pygame.mixer.music.play(-1)

	# 实例化我方飞机
	me = myplane.Plane(bg_size)

	enemies = pygame.sprite.Group()

	# 实例化敌方小型飞机并添加到对应敌机组
	small_enemies = pygame.sprite.Group()
	add_small_enemies(small_enemies, enemies, 15)

	# 实例化敌方中型飞机并添加到对应敌机组
	mid_enemies = pygame.sprite.Group()
	add_mid_enemies(mid_enemies, enemies, 4)

	# 实例化敌方大型飞机并添加到对应敌机组
	big_enemies = pygame.sprite.Group()
	add_big_enemies(big_enemies, enemies, 2)

	# 生成普通子弹
	bullet1 = []
	bullet1_index = 0
	BULLET1_NUM = 4
	for i in range(BULLET1_NUM):
		bullet1.append(bullet.Bullet1(me.rect.midtop))

	# 生成超级子弹
	bullet2 = []
	bullet2_index = 0
	BULLET2_NUM = 8
	for i in range(BULLET2_NUM // 2):
		bullet2.append(bullet.Bullet2((me.rect.centerx - 33,me.rect.centery)))
		bullet2.append(bullet.Bullet2((me.rect.centerx + 33,me.rect.centery)))
		
	clock = pygame.time.Clock()

	# 中弹图片索引
	e1_destroy_index = 0
	e2_destroy_index = 0
	e3_destroy_index = 0
	me_destroy_index = 0
	
	#统计分数
	score = 0
	score_font = pygame.font.Font("font/font.ttf",36)
	
	paused = False
	pause_nor_img = pygame.image.load("images/pause_nor.png").convert_alpha()
	pause_pressed_img = pygame.image.load("images/pause_pressed.png").convert_alpha()
	resume_nor_img = pygame.image.load("images/resume_nor.png").convert_alpha()
	resume_pressed_img = pygame.image.load("images/resume_pressed.png").convert_alpha()
	paused_rect = pause_nor_img.get_rect()
	paused_rect.left,paused_rect.top = (width - paused_rect.width - 10,10)
	paused_img = pause_nor_img
	
	#设置难度等级
	level = 1
	
	#全屏炸弹
	bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
	bomb_rect = bomb_image.get_rect()
	bomb_num = 3
	bomb_font = pygame.font.Font("font/font.ttf",48)
	
	#补给包
	bullet_supply = supply.Bullet_Supply(bg_size)
	bomb_supply = supply.Bomb_Supply(bg_size)
	SUPPLY_TIME = USEREVENT
	pygame.time.set_timer(SUPPLY_TIME,30 * 1000)
	
	#超级子弹
	SUPPER_BULLET = USEREVENT + 1
	#超级子弹使用标记
	is_supper_bullet = False
	
	#生命数量
	life_image = pygame.image.load("images/life.png").convert_alpha()
	life_rect = life_image.get_rect()
	life_num = 3
	
	#解除无敌状态事件
	SAFE_TIME = USEREVENT + 2
	
	#用于阻止重复打开文件
	recorded = False
	
	#游戏结束画面
	gameover_font = pygame.font.Font("font/STHUPO.ttf",36)
	again_image = pygame.image.load("images/again.png").convert_alpha()
	again_rect = again_image.get_rect()
	gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
	gameover_rect = gameover_image.get_rect()
	
	# 用于切换图片
	switch_image = True

	# 用于延迟
	delay = 100

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1 and paused_rect.collidepoint(event.pos):
					paused = not paused
					if paused:
						pygame.time.set_timer(SUPPLY_TIME,0)
						pygame.mixer.music.pause()
						pygame.mixer.pause()
					else:
						pygame.time.set_timer(SUPPLY_TIME,30 * 1000)
						pygame.mixer.music.unpause()
						pygame.mixer.unpause()
			elif event.type == MOUSEMOTION:
				if paused_rect.collidepoint(event.pos):
					if paused:
						paused_img = resume_pressed_img
					else:
						paused_img = pause_pressed_img
				else:
					if paused:
						paused_img = resume_nor_img
					else:
						paused_img = pause_nor_img
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					if bomb_num:
						bomb_num -= 1
						bomb_sound.play()
						for each in enemies:
							if each.rect.bottom > 0:
								each.active = False
			elif event.type == SUPPLY_TIME:
				supply_sound.play()
				if choice([True,False]):
					bullet_supply.reset()
				else:
					bomb_supply.reset()
			elif event.type == SUPPER_BULLET:
				is_supper_bullet = False
				pygame.time.set_timer(SUPPER_BULLET,0)
			elif event.type == SAFE_TIME:
				me.safe_time = False
				pygame.time.set_timer(SAFE_TIME,0)
						
		if level == 1 and score > 500:
			level = 2
			upgrade_sound.play()
			#增加三架小型敌机、两架小型敌机、一架小型敌机
			add_small_enemies(small_enemies,enemies,3)
			add_mid_enemies(mid_enemies,enemies,2)
			add_big_enemies(big_enemies,enemies,1)
			#提升小型机的速度
			add_speed(small_enemies,1)
		elif level == 2 and score > 2000:
			level = 3
			upgrade_sound.play()
			#增加三架小型敌机、两架小型敌机、一架小型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升小型机的速度
			add_speed(small_enemies,1)
			add_speed(mid_enemies,1)
		elif level == 3 and score > 5000:
			level = 4
			upgrade_sound.play()
			#增加三架小型敌机、两架小型敌机、一架小型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升小型机的速度
			add_speed(small_enemies,1)
			add_speed(mid_enemies,1)        
		elif level == 4 and score > 10000:
			level = 5
			upgrade_sound.play()
			#增加三架小型敌机、两架小型敌机、一架小型敌机
			add_small_enemies(small_enemies,enemies,5)
			add_mid_enemies(mid_enemies,enemies,3)
			add_big_enemies(big_enemies,enemies,2)
			#提升小型机的速度
			add_speed(small_enemies,1)
			add_speed(mid_enemies,1)        
									
		screen.blit(background, (0, 0))
						
		if life_num and not paused:
			# 检测用户的键盘操作
			key_pressed = pygame.key.get_pressed()

			if key_pressed[K_w] or key_pressed[K_UP]:
				me.moveUp()
			if key_pressed[K_s] or key_pressed[K_DOWN]:
				me.moveDown()
			if key_pressed[K_a] or key_pressed[K_LEFT]:
				me.moveLeft()
			if key_pressed[K_d] or key_pressed[K_RIGHT]:
				me.moveRight()
				
			#绘制全屏炸弹并检测是否获得
			if bomb_supply.active:
				bomb_supply.move()
				screen.blit(bomb_supply.image,bomb_supply.rect)
				if pygame.sprite.collide_mask(bomb_supply,me):
					get_bomb_sound.play()
					if bomb_num < 3:
						bomb_num += 1
					bomb_supply.active = False  

			if bullet_supply.active:
				bullet_supply.move()
				screen.blit(bullet_supply.image,bullet_supply.rect)
				if pygame.sprite.collide_mask(bullet_supply,me):
					get_bullet_sound.play()
					is_supper_bullet = True
					pygame.time.set_timer(SUPPER_BULLET,18 * 1000)
					bullet_supply.active = False    

			# 发射子弹
			if not(delay % 10):
				bullet_sound.play()
				if is_supper_bullet:
					bullets = bullet2
					bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
					bullets[bullet2_index+1].reset((me.rect.centerx+33, me.rect.centery))
					bullet2_index = (bullet2_index + 2) % BULLET2_NUM
				else:
					bullets = bullet1
					bullets[bullet1_index].reset(me.rect.midtop)
					bullet1_index = (bullet1_index + 1) % BULLET1_NUM

			# 检测子弹是否击中敌机
			for b in bullets:
				if b.active:
					b.move()
					screen.blit(b.image, b.rect)
					enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
					if enemy_hit:
						b.active = False
						for e in enemy_hit:
							if e in mid_enemies or e in big_enemies:
								e.hit = True
								e.energy -= 1
								if e.energy == 0:
									e.active = False
							else:
								e.active = False
			
			# 绘制大型敌机
			for each in big_enemies:
				if each.active:
					each.move()
					if each.hit:
						screen.blit(each.image_hit, each.rect)
						each.hit = False
					else:
						if switch_image:
							screen.blit(each.image1, each.rect)
						else:
							screen.blit(each.image2, each.rect)

					# 绘制血槽
					pygame.draw.line(screen, BLACK, \
									 (each.rect.left, each.rect.top - 5), \
									 (each.rect.right, each.rect.top - 5), \
									 2)
					# 当生命大于20%显示绿色，否则显示红色
					energy_remain = each.energy / enemy.BigEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, \
									 (each.rect.left, each.rect.top - 5), \
									 (each.rect.left + each.rect.width * energy_remain, \
									  each.rect.top - 5), 2)
						
					# 即将出现在画面中，播放音效
					if each.rect.bottom == -50:
						enemy3_fly_sound.play(-1)
				else:
					# 毁灭
					if not(delay % 3):
						if e3_destroy_index == 0:
							enemy3_down_sound.play()
						screen.blit(each.destroy_images[e3_destroy_index], each.rect)
						e3_destroy_index = (e3_destroy_index + 1) % 6
						if e3_destroy_index == 0:
							enemy3_fly_sound.stop()
							score += 100
							each.reset()

			# 绘制中型敌机：
			for each in mid_enemies:
				if each.active:
					each.move()
					if each.hit:
						screen.blit(each.image_hit, each.rect)
						each.hit = False
					else:
						screen.blit(each.image, each.rect)

					# 绘制血槽
					pygame.draw.line(screen, BLACK, \
									 (each.rect.left, each.rect.top - 5), \
									 (each.rect.right, each.rect.top - 5), \
									 2)
					# 当生命大于20%显示绿色，否则显示红色
					energy_remain = each.energy / enemy.MidEnemy.energy
					if energy_remain > 0.2:
						energy_color = GREEN
					else:
						energy_color = RED
					pygame.draw.line(screen, energy_color, \
									 (each.rect.left, each.rect.top - 5), \
									 (each.rect.left + each.rect.width * energy_remain, \
									  each.rect.top - 5), 2)
				else:
					# 毁灭
					if not(delay % 3):
						if e2_destroy_index == 0:
							enemy2_down_sound.play()
						screen.blit(each.destroy_images[e2_destroy_index], each.rect)
						e2_destroy_index = (e2_destroy_index + 1) % 4
						if e2_destroy_index == 0:
							score += 20
							each.reset()

			# 绘制小型敌机：
			for each in small_enemies:
				if each.active:
					each.move()
					screen.blit(each.image, each.rect)
				else:
					# 毁灭
					if not(delay % 3):
						if e1_destroy_index == 0:
							enemy1_down_sound.play()
						screen.blit(each.destroy_images[e1_destroy_index], each.rect)
						e1_destroy_index = (e1_destroy_index + 1) % 4
						if e1_destroy_index == 0:
							score += 10
							each.reset()

			# 检测我方飞机是否被撞
			enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
			if enemies_down and not me.safe_time:
				me.active = False
				for e in enemies_down:
					e.active = False
			
			# 绘制我方飞机
			if me.active:
				if switch_image:
					screen.blit(me.image1, me.rect)
				else:
					screen.blit(me.image2, me.rect)
			else:
				# 毁灭
				if not(delay % 3):
					if me_destroy_index == 0:
						me_down_sound.play()
					screen.blit(me.destroy_images[me_destroy_index], me.rect)
					me_destroy_index = (me_destroy_index + 1) % 4
					if me_destroy_index == 0:
						life_num -= 1
						me.reset()
						pygame.time.set_timer(SAFE_TIME,3 * 1000)
						
			#绘制剩余炸弹数量
			bomb_text = bomb_font.render("× {0}".format(str(bomb_num)),True,(255,255,255))
			text_rect = bomb_text.get_rect()
			screen.blit(bomb_image,(10,height - bomb_rect.height - 10))
			screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))
			
			score_text = score_font.render("score:{0}".format(str(score)),True,(128,128,128))
			screen.blit(score_text,(10,5))
			
			#绘制剩余生命数量
			if life_num:
				for i in range(life_num):
					screen.blit(life_image,(width - 10 - (i + 1) * life_rect.width,height - 10 - life_rect.height))
					
		elif life_num == 0:
			pygame.mixer.music.stop()
			pygame.mixer.stop()
			pygame.time.set_timer(SUPPLY_TIME,0)
			if not recorded:
				recorded = True
				with open ("record.txt","r") as f:
					record_score = int(f.read())
				if score > record_score:
					with open ("record.txt","w") as f:
						f.write(str(score))
				
			#绘制结束画面
			record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
			screen.blit(record_score_text, (10, 10))
			
			gameover_text1 = gameover_font.render("小坨，失败乃成功之母", True, (255, 255, 255))
			gameover_text1_rect = gameover_text1.get_rect()
			gameover_text1_rect.left, gameover_text1_rect.top = \
								 (width - gameover_text1_rect.width) // 2, height // 3
			screen.blit(gameover_text1, gameover_text1_rect)
			
			gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
			gameover_text2_rect = gameover_text2.get_rect()
			gameover_text2_rect.left, gameover_text2_rect.top = \
								 (width - gameover_text2_rect.width) // 2, \
								 gameover_text1_rect.bottom + 10
			screen.blit(gameover_text2, gameover_text2_rect)

			again_rect.left, again_rect.top = \
							 (width - again_rect.width) // 2, \
							 gameover_text2_rect.bottom + 50
			screen.blit(again_image, again_rect)

			gameover_rect.left, gameover_rect.top = \
								(width - again_rect.width) // 2, \
								again_rect.bottom + 10
			screen.blit(gameover_image, gameover_rect)

			# 检测用户的鼠标操作
			# 如果用户按下鼠标左键
			if pygame.mouse.get_pressed()[0]:
				# 获取鼠标坐标
				pos = pygame.mouse.get_pos()
				# 如果用户点击“重新开始”
				if again_rect.left < pos[0] < again_rect.right and \
				   again_rect.top < pos[1] < again_rect.bottom:
					# 调用main函数，重新开始游戏
					main()
				# 如果用户点击“结束游戏”            
				elif gameover_rect.left < pos[0] < gameover_rect.right and \
					 gameover_rect.top < pos[1] < gameover_rect.bottom:
					# 退出游戏
					pygame.quit()
					sys.exit()    			
			
		
		#绘制暂停按钮
		screen.blit(paused_img,paused_rect)

		# 切换图片
		if not(delay % 5):
			switch_image = not switch_image

		delay -= 1
		if not delay:
			delay = 100

		pygame.display.flip()
		clock.tick(60)
		
if __name__ == "__main__":
	main()
	input()
