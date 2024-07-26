#Names: Sarah Li & Ashley Ezail Mojica
#COURSE CODE: ICS3U1 - 02
#DATE: June 14, 2024
#PROGRAM: Catch Sunjae!

import pygame, random
from tkinter import messagebox

skip = False
#Output a little welcome messagebox
messagebox.showinfo('Welcome', f'Use wasd to move, you have been given 3 chances to save Sunjae.')

#Initialize all the modules required for Pygame
pygame.init()
pygame.mixer.init()
#Load the music and play the music infinitely until an event happens that requires the music to be stopped. (The music played from the show)
pygame.mixer.music.load('runrun.mp3')
pygame.mixer.music.play(loops = -1)
soundeffects = [pygame.mixer.Sound('soundeffect1.mp3')]

#Set the number of lives the player has
lives = 3
#Set the font of the life counter
fLives = pygame.font.Font("Tiny5.ttf", 40)
#Setting the text
livesoutput = fLives.render(f'Time Travels left: {lives}.', True, '#420420')

#Set the number of speed ups a person has
speedups = 2
#Create a timer of 3 minutes for each time travel
pygame.time.set_timer(pygame.USEREVENT +2, 180000)

yo1, yo2, yo3, yo4 = False, False, False, False

#Set the drawing surfaces to 1000 pixals wide and 700 pixals high, and make it resizable.
surface = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)

#Set the caption and the game icon, as well as create the background image. 
pygame.display.set_caption("Catch Sunjae!!")
pygame.display.set_icon(pygame.image.load('icon.jpeg'))
background_image = pygame.image.load('background1.jpeg')
background = pygame.transform.smoothscale(background_image, (surface.get_width(), surface.get_height()))
background2 = pygame.image.load('background2.jpeg')
background2 = pygame.transform.smoothscale(background2, (surface.get_width(), surface.get_height()))
background3 = pygame.image.load('background3.jpeg')
background3 = pygame.transform.smoothscale(background3, (surface.get_width(), surface.get_height()))
background4 = pygame.image.load('background4.jpeg')
background4 = pygame.transform.smoothscale(background4, (surface.get_width(), surface.get_height()))

#Set the bot's image
taesung = pygame.image.load('taesung.png')
taesung = pygame.transform.smoothscale(taesung, (taesung.get_width()*0.35, taesung.get_height()*0.35))

#Set the x and y variables
def settingVariables():
    global xblock, yblock, keys, index, index2, direction, taesungx, taesungy, imsolspeed, collided
    xblock, yblock = 0, 0
    keys = [False, False, False, False]
    index = 0
    index2 = 0
    direction = 'down'
    imsolspeed = 3
    taesungx = random.randint(0, surface.get_width() - taesung.get_width())
    taesungy = random.randint(0, surface.get_height() - taesung.get_height())
    collided = False

#Define the rectangles list
obstacles = []
sunjaeU, sunjaeD, sunjaeR, sunjaeL = [], [], [], []
sunjae = []
imsolU, imsolD, imsolR, imsolL = [], [], [], []
moveimsol = False
#Create timer with 10 second intervals
pygame.time.set_timer(pygame.USEREVENT, 10000)


#Add the bot player images to the list, after resizing.
for index in range(4):
    img_sunjaeR = pygame.image.load(f'right/sunjae{index}.webp')
    img_sunjaeR = pygame.transform.smoothscale(img_sunjaeR, (img_sunjaeR.get_width() * 3, img_sunjaeR.get_height() * 3))
    sunjaeR.append(img_sunjaeR)
    
    img_sunjaeL = pygame.image.load(f'left/sunjae{index}.webp')
    img_sunjaeL = pygame.transform.smoothscale(img_sunjaeL, (img_sunjaeL.get_width() * 3, img_sunjaeL.get_height() * 3))
    sunjaeL.append(img_sunjaeL)
    
    img_sunjaeU = pygame.image.load(f'up/sunjae{index}.webp')
    img_sunjaeU = pygame.transform.smoothscale(img_sunjaeU, (img_sunjaeU.get_width() * 3, img_sunjaeU.get_height() * 3))
    sunjaeU.append(img_sunjaeU)
    
    img_sunjaeD = pygame.image.load(f'down/sunjae{index}.png')
    img_sunjaeD = pygame.transform.smoothscale(img_sunjaeD, (img_sunjaeD.get_width() * 2.25, img_sunjaeD.get_height() * 2.25))
    sunjaeD.append(img_sunjaeD)



#Add the images to the list, after resizing them. 
for index in range(8):
    img_imsolD = pygame.image.load(f'down/imsol{index}.jpeg')
    img_imsolD = pygame.transform.smoothscale(img_imsolD, (img_imsolD.get_width() * 1.2, img_imsolD.get_height()*1.2))
    imsolD.append(img_imsolD)
    
    img_imsolR = pygame.image.load(f'right/imsol{index}.jpeg')
    img_imsolR = pygame.transform.smoothscale(img_imsolR, (img_imsolR.get_width()*1.2, img_imsolR.get_height()*1.2))
    imsolR.append(img_imsolR)
    
    img_imsolU = pygame.image.load(f'up/imsol{index}.jpeg')
    img_imsolU = pygame.transform.smoothscale(img_imsolU, (img_imsolU.get_width()*1.2, img_imsolU.get_height()*1.2))
    imsolU.append(img_imsolU)
    
    img_imsolL = pygame.image.load(f'left/imsol{index}.jpeg')
    img_imsolL = pygame.transform.smoothscale(img_imsolL, (img_imsolL.get_width()*1.2, img_imsolL.get_height()*1.2))
    imsolL.append(img_imsolL)
#Randomize the players' coordinates, and the bot's coordinates.
def randomizing():
    global ximsol, yimsol, xsunjae, ysunjae
    ximsol, yimsol = random.randint(0, surface.get_width() - img_imsolU.get_width()), random.randint(0, surface.get_height() - img_imsolU.get_height())

    xsunjae, ysunjae = random.randint(0, surface.get_width() - img_sunjaeU.get_width()), random.randint(0, surface.get_height() - img_sunjaeU.get_height())
        
def collision_check2():
    #Create Rect objects to represent both the player and the bot
    sunjae_rect = pygame.Rect(xsunjae + 50, ysunjae + 40, sunjaeD[index2].get_width() - 80, sunjaeD[index2].get_height() - 70)
    imsol_rect = pygame.Rect(ximsol, yimsol, imsolD[index].get_width(), imsolD[index].get_height())
    #Return a bool value which indicates whether the 2 objects collided
    return imsol_rect.colliderect(sunjae_rect)

def collision_check():
    #Create a Rect object to represent the character controlled by the player
    imsol_rect = pygame.Rect(ximsol, yimsol, imsolD[index].get_width(), imsolD[index].get_height())
    
    #Create a Rect object to represent the obstacle
    taesung_rect = pygame.Rect(taesungx + 17, taesungy + 40, taesung.get_width() - 50, taesung.get_height() - 90)
    
    #Return a bool value which indicates whether the 2 objects collided
    return imsol_rect.colliderect(taesung_rect)
    
def sunjaeRun():
    global xspeed, yspeed, sunjaeWay
    #Create a dictionary
    # sunjae.append({'xspeed': random.randint(5, 10), 'yspeed': random.randint(5,10), 'sunjaeWay': random.randint(1,4)})
    xspeed = 4
    yspeed = 4
    sunjaeWay = random.randint(1,4)
    pygame.time.set_timer(pygame.USEREVENT + 1, 100)

randomizing()
settingVariables()
sunjaeRun()
endgame = False
sunjaePic = sunjaeD[index2]
previousx = ximsol
previousy = yimsol
walksu, walksr, walksl, walksd = 0, 0, 0, 0
while endgame == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            endgame = True
        
        #Setting the text again
        livesoutput = fLives.render(f'Time Travels left: {lives}.', True, '#420420')

        #Making the player move based off which key they press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys[0] = True
            if event.key == pygame.K_d:
                keys[1] = True
            if event.key == pygame.K_s:
                keys[2] = True
            if event.key == pygame.K_a:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            if event.key == pygame.K_d:
                keys[1] = False
            if event.key == pygame.K_s:
                keys[2] = False
            if event.key == pygame.K_a:
                keys[3] = False
            if event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d:
                index = 0
        if keys[0] == True:
            # yimsol -=5
            
            direction = 'up'
            if yimsol <=0:
                yimsol -=0
            else:
                yimsol-=imsolspeed
            index +=1
            if index == len(imsolU):
                index = 0
        
        if keys[2] == True:
            # yimsol +=5
            
            direction = 'down'
            if yimsol + imsolD[index].get_height() >= surface.get_height():
                yimsol +=0
            else:
                yimsol +=imsolspeed
            index +=1
            if index == len(imsolD):
                index = 0
        if keys[1] == True:
            # ximsol +=5
            direction = 'right'
            
            if ximsol + imsolR[index].get_width() >=surface.get_width():
                ximsol +=0
            else:
                ximsol +=imsolspeed
            index +=1
            if index == len(imsolR):
                index = 0
                
        if keys[3] == True:
            # ximsol -= 5
            direction = 'left'

            if ximsol <=0:
                ximsol -=0
            else:
                ximsol -=imsolspeed
            index +=1
            if index == len(imsolL):
                index = 0
                
        #Allowing the bot to move based off of the player's positions
        if event.type == pygame.USEREVENT+1:
                sunjaeRun()
                
                if ysunjae < yimsol:
                    ysunjae -= yspeed
                    if ysunjae <= 0:
                        ysunjae = 0
                    index2+=1
                    if index2 == len(sunjaeU):
                        index2 = 0
                    sunjaePic = sunjaeU[index2]
                elif ysunjae> yimsol:
                    ysunjae+= yspeed
                    if ysunjae + sunjaePic.get_height() >= surface.get_height():
                        ysunjae = surface.get_height() - sunjaePic.get_height()
                    index2+=1
                    if index2 == len(sunjaeD):
                        index2 = 0
                    sunjaePic = sunjaeD[index2]
                    
                if xsunjae < ximsol:
                    xsunjae -= xspeed
                    if xsunjae <= 0:
                        xsunjae = 0
                    index2 +=1
                    if index2 == len(sunjaeL):
                        index2 = 0
                    sunjaePic = sunjaeL[index2]
                    
                elif xsunjae> ximsol:
                    xsunjae+=xspeed
                    if xsunjae + sunjaePic.get_width() >= surface.get_width():
                        xsunjae = surface.get_width() - sunjaePic.get_width()
                    index2 +=1
                    if index2 == len(sunjaeR):
                        index2 = 0
                    sunjaePic = sunjaeR[index2]
        surface.blit(sunjaePic, (xsunjae, ysunjae))
        
        if event.type == pygame.USEREVENT:
            #Prevent the player from moving after the timer is done
            collided = True
            taesungx = random.randint(0, surface.get_width() - taesung.get_width())
            taesungy = random.randint(0, surface.get_height() - taesung.get_height())
        #Check if the character hits the obstacle
        previousy = yimsol
        previousx = ximsol
        collision_check()
        collision_check2()
        #If yes, then stop the character from moving for 2 seconds, while playing an audio.
        if collision_check() == True:
            ximsol = previousx
            yimsol = previousy

            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(soundeffects[0])

            pygame.time.delay(3500)
            pygame.mixer.music.unpause()
            pygame.time.set_timer(pygame.USEREVENT, 10000)
            taesungx = random.randint(0, surface.get_width() - taesung.get_width())
            taesungy = random.randint(0, surface.get_height() - taesung.get_height())
            pygame.time.delay(1000)
            walksu, walksd, walksr, walksl = 0, 0, 0, 0
            # collided = False
        if event.type == pygame.USEREVENT +2:
            lives -= 1
            
            #Variables for how many lives are left, which will result in which image is uploaded
            if lives == 2:
                yo1 = True
            elif lives == 1:
                yo2 = True

            elif lives == 0:
                yo3 = True

            if lives >=0:
                #Takeout a life from the total
                livesoutput = fLives.render(f'Time Travels left: {lives}.', True, '#420420')
                #Make the player faster after each life lost
                imsolspeed +=1
                #output a messagebox warning
                messagebox.showwarning("Time Ran Out!", f'Sunjae died. You only have {lives} time travels left!')
                #Reset the variables and randomize the placements
                settingVariables()
                randomizing()
            #If they have no more remaining rebirths, they end the game
            elif lives < 0:
                pygame.mixer.music.unload()
                messagebox.showerror("GAME OVER!", 'You were unable to save Sunjae...')
                pygame.quit()
                endgame = True
                quit()
                
                
            
            
        #If the player collides with sunjae, say that the player has won.
        if collision_check2() == True:
            pygame.mixer.music.unload()
            pygame.mixer.music.load('SpringSnow.mp3')
            pygame.mixer.music.play(-1)

            answer = messagebox.askyesno("Congratulations!", 'Would you like to play again?')
            if answer == True:
                pygame.mixer.music.load('runrun.mp3')
                randomizing()
                settingVariables
                pygame.mixer.music.play(-1)
            #Dont wanna play, then end game.
            if answer == False:
                messagebox.showinfo('Thank you!', "Thank you for playing, we hope to see you next time!")
                pygame.quit()
                endgame = True
                exit()
                
    #If they have 2, 1, 0 rebirths, then display the death of sunjae.
    if yo1 == True:
        surface.blit(background2, (0,0))
        pygame.time.delay(5000)
        yo1 = False
    elif yo2 == True:
        surface.blit(background3, (0,0))
        pygame.time.delay(5000)
        yo2 = False
    elif yo3 == True:
        surface.blit(background4, (0,0))
        pygame.time.delay(5000)
        surface.blit(background, (0,0))
        yo3 = False
    else:
        surface.blit(background, (0,0))
    surface.blit(taesung, (taesungx, taesungy))
    if direction == 'right':
        surface.blit(imsolR[index], (ximsol, yimsol))
    elif direction == 'left':
        surface.blit(imsolL[index], (ximsol, yimsol))
    elif direction == 'up':
        surface.blit(imsolU[index], (ximsol, yimsol))
    elif direction == 'down':
        surface.blit(imsolD[index], (ximsol, yimsol))
        

    #Outputting sunjae
    surface.blit(sunjaePic, (xsunjae, ysunjae))
    
    #Outputting the text
    surface.blit(livesoutput, (surface.get_width() - livesoutput.get_width(), 0))
    #Display everything
    pygame.display.update()

    