import pygame
import random
import customtkinter as ctk

pygame.init()
#screen
width,height = 1400,900
#player 
p_width,p_height = 100,100

#player velocity
player_velocity = 5


#enemy 

enemy_width = 60
enemy_height = 60

hit = False
enemy_list = [] #it will have all the enemy from the screen

#main display screen
window = pygame.display.set_mode((width,height))
pygame.display.set_caption("Space kings")

background = pygame.image.load("assets/bg.jpg")
background = pygame.transform.scale(background,(width,height))

ship1 =pygame.transform.scale(pygame.image.load("assets/ship1.png"),(p_width,p_height))
ship2 =pygame.transform.scale(pygame.image.load("assets/ship2.png"),(p_width + 20,p_height +20))

player_var = random.choice([ship1,ship2])

enemy1 = pygame.transform.scale(pygame.image.load("assets/enemy1.png"),(enemy_width,enemy_height))
enemy2 = pygame.transform.scale(pygame.image.load("assets/enemy2.png"),(enemy_width ,enemy_height))

#font
font = pygame.font.SysFont("Arial",30)

clock = pygame.time.Clock()

def update_screen(player,enemy,score):
    window.blit(background,(0,0))

    window.blit(player_var,(player.x,player.y))

    #enemy drawing
    for e_img, e_data in enemy :
        window.blit(e_img,e_data)
    score_draw = font.render(f"Score: {score}",True,"white")
    window.blit(score_draw,(20,0))


    pygame.display.update() #need to update the display for changes

def main():
    print("main code block") 

    enemy_add_time = 2000
    enemy_spawn_time = 0
    hit = False

        #score
    score = 0
    
    

    #definig the player
    #here is making an rectangle for the player... pos(coordinates(x,y)), width,height
    player = pygame.Rect(0, height - p_height,p_width,p_height)

    run = True
    #bg music
    bg_music = pygame.mixer.Sound("assets/main_song.mp3")
    shoot_music = pygame.mixer.Sound("assets/shoot.mp3")
    end_music = pygame.mixer.Sound("assets/end.mp3")
    bg_music.play(-1)
    bg_music.set_volume(0.3)

    shoot_music.set_volume(0.1)

    while run:

        enemy_spawn_time += clock.tick(60) #getting the time
        if enemy_spawn_time > enemy_add_time:

            for i in range(2):
                enemy_x = random.randint(0,width - enemy_width) #randamising the x corrs
                #initializing the enemy
                _enemy_ = pygame.Rect(enemy_x, 0 ,enemy_width-40,enemy_height-40) #enemy data or creating an rect for the enemys
                enemy_var = random.choice([enemy1,enemy2])

                
                overlap = False
                for _, exist_eme in enemy_list:
                    if _enemy_.colliderect(exist_eme):
                        overlap = True
                        break
                if not overlap :
                    enemy_list.append((enemy_var,_enemy_))
                
        #making the spawn time 0 so that it can resart nd speed up the swapn
            enemy_add_time = max(200,enemy_add_time - 50)
            enemy_spawn_time = 0

        for enemy_image, enemy_pos in enemy_list[:]:
            enemy_pos.y += 2
            if enemy_pos.y >= height:
                enemy_list.remove((enemy_image,enemy_pos))
                #sucessfully passed
                score += 1
            elif enemy_pos.colliderect(player):
                bg_music.stop()
                shoot_music.stop()
                end_music.set_volume(5.0)
                end_music.play()
                enemy_list.remove((enemy_image,enemy_pos))
                hit = True
                break
        if hit:
            dis = ctk.CTk(fg_color="#1E1E1E")  # dark background
            dis.geometry("400x250")
            dis.title("Game Over")
            dis.resizable(False, False)

            # Main frame for padding and rounded effect
            main_frame = ctk.CTkFrame(dis, fg_color="#2C2C2C", corner_radius=20)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # Game Over Label
            label = ctk.CTkLabel(main_frame, text="GAME OVER", text_color="#FF4C4C",
                                fg_color="#2C2C2C", font=("Arial", 30, "bold"))
            label.pack(pady=(10, 10))

            # Score Label
            label2 = ctk.CTkLabel(main_frame, text=f"Your Score: {score}", text_color="white",
                                fg_color="#2C2C2C", font=("Arial", 20))
            label2.pack(pady=(0, 20))

            # Buttons frame
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack()

            # Exit button
            btn_exit = ctk.CTkButton(button_frame, text="Exit", width=120, height=40, 
                                    fg_color="#594AFF", text_color="white",
                                    font=("Arial", 15, "bold"), cursor="hand2",
                                    command=dis.destroy)
            btn_exit.pack(side="left", padx=10)

            # Optional: Play Again button
            btn_play_again = ctk.CTkButton(button_frame, text="Play Again", width=120, height=40,
                                        fg_color="#4CAF50", text_color="white",
                                        font=("Arial", 15, "bold"), cursor="hand2",
                                        command=lambda: [dis.destroy(), main()])
            btn_play_again.pack(side="right", padx=10)

            dis.mainloop()
            pygame.time.delay(200)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and player.x + player_velocity + p_width <= 1400:
            player.x += player_velocity
            shoot_music.play()
        if keys[pygame.K_a] and player.x - player_velocity >= 0:
            player.x -= player_velocity
            shoot_music.play()
        if keys[pygame.K_w] and player.y+ player.height + 10 >= 800:
            player.y -= 10
        if keys[pygame.K_s] and player.y + player.height + 10 <= 900:
            player.y += 10

        

        update_screen(player,enemy_list,score)
    pygame.quit()

def main_screen():
    app = ctk.CTk()
    app.geometry("500x800")
    app.title("Menu")

    frame = ctk.CTkFrame(app, fg_color="#0E0E0E")
    frame.pack(fill="both", expand=True)
    frame.pack_propagate(False)

    # Centering a container frame for buttons
    button_frame = ctk.CTkFrame(frame, fg_color="transparent")
    button_frame.place(relx=0.5, rely=0.5, anchor="center")  # center in parent

    lable = ctk.CTkLabel(button_frame,text="SPACE KINGS",text_color="white",fg_color="transparent",font=("Arial",40,"bold"))
    lable.pack(fill="both")

    def start_game ():
        app.destroy()
        main()


    btn1 = ctk.CTkButton(
        button_frame,
        text="Start Game",
        text_color="black",
        font=("Arial", 20, "bold"),
        fg_color="#594AFF",
        cursor="hand2",
        width=300,
        height=50,
        command= start_game
    )
    btn1.pack(pady=10)  # vertical spacing between buttons

    btn2 = ctk.CTkButton(
        button_frame,
        text="Exit",
        text_color="black",
        font=("Arial", 20, "bold"),
        fg_color="#4CAF50",
        cursor="hand2",
        width=300,
        height=50,
        command= app.destroy
    )
    btn2.pack(pady=10)

    app.mainloop()


if __name__ == "__main__" :
    main_screen()
