import tkinter as tk
import random
import time

class SpaceInvaders:
    def __init__(self, master):
        self.master = master
        self.master.title("Space Invaders")
        self.canvas = tk.Canvas(master, width=600, height=400, bg='black')
        self.canvas.pack()

        # Création des boutons et placement dans un conteneur Frame
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)

        self.replay_button = tk.Button(self.button_frame, text="Rejouer", command=self.restart_game)
        self.replay_button.pack(side=tk.RIGHT, padx=5)

        self.pause_button = tk.Button(self.button_frame, text="Mettre en pause", command=self.pause_game)
        self.pause_button.pack(side=tk.RIGHT, padx=5)

        self.resume_button = tk.Button(self.button_frame, text="Continuer à jouer", command=self.resume_game)
        self.resume_button.pack(side=tk.RIGHT, padx=5)
        self.resume_button.config(state=tk.DISABLED)  # Le bouton "Continuer à jouer" est désactivé au début

        self.quit_button = tk.Button(self.button_frame, text="Quitter", command=self.quit_game)
        self.quit_button.pack(side=tk.RIGHT, padx=5)

        self.ship = self.canvas.create_rectangle(280, 360, 320, 380, fill='blue')
        self.projectiles = []
        self.invader_projectiles = []
        self.invaders = []
        self.obstacles = []
        self.obstacle_health = 100  # Points de vie de l'obstacle
        self.score = 0
        self.score_label = self.canvas.create_text(50, 20, text="Score: 0", fill="white", anchor="nw")
        self.game_over_text = None
        self.game_over = False  # Variable d'état du jeu

        self.create_invaders()
        self.create_obstacles()

        # Initialisation de l'attribut paused
        self.paused = False

        self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        self.canvas.bind_all('<KeyRelease-space>', self.fire)

        self.animate()
        self.invader_fire_loop()
        

    def create_invaders(self):
        x = 50
        y = 50
        for _ in range(18):
            invader = self.canvas.create_rectangle(x, y, x+30, y+20, fill='red')
            self.invaders.append(invader)
            x += 40
            if x > 570:
                x = 50
                y += 30
    
    def destroy_invader(self, invader):
        self.canvas.delete(invader)
        self.invaders.remove(invader)

    def pause_game(self):
        self.paused = True
        self.resume_button.config(state=tk.NORMAL)  # Activer le bouton "Continuer à jouer"
        self.pause_button.config(state=tk.DISABLED)  # Désactiver le bouton "Mettre en pause"

    def resume_game(self):
        self.paused = False
        self.pause_button.config(state=tk.NORMAL)  # Activer le bouton "Mettre en pause"
        self.resume_button.config(state=tk.DISABLED)  # Désactiver le bouton "Continuer à jouer"

    def quit_game(self):
        self.master.destroy()  # Fermer la fenêtre du jeu

    def create_obstacles(self):
        for _ in range(4):
            obstacle = self.canvas.create_rectangle(200, 250, 400, 270, fill='green')
            self.obstacles.append(obstacle)

    def move_left(self, event):
        if not self.game_over:  # Vérifier si le jeu est en cours
            self.canvas.move(self.ship, -20, 0)

    def move_right(self, event):
        if not self.game_over:  # Vérifier si le jeu est en cours
            self.canvas.move(self.ship, 20, 0)

    def fire(self, event):
        if not self.game_over:  
            x1, y1, x2, y2 = self.canvas.coords(self.ship)
            projectile = self.canvas.create_rectangle(x1+15, y1, x1+25, y1-10, fill='yellow')
            self.projectiles.append(projectile)

        for projectile in self.projectiles:
            if self.detect_collision(projectile, self.obstacles[1]):
                self.damage_obstacle(self.obstacles[1])
                self.projectiles.remove(projectile) 

    def invader_fire(self, invader):
        x1, y1, x2, y2 = self.canvas.coords(invader)
        projectile = self.canvas.create_rectangle(x1+15, y1+20, x1+25, y1+30, fill='white')
        self.invader_projectiles.append(projectile)

    def invader_fire_loop(self):
        for invader in self.invaders:
            chance = random.randint(1, 20)  # Chance de tirer à chaque itération
            if chance == 1:
                self.invader_fire(invader)
        if not self.game_over:  # Vérifier si le jeu est en cours
            self.master.after(1000, self.invader_fire_loop)

    def animate(self):
        if not self.game_over:
            if not self.paused:  # Vérifier si le jeu est en cours et non en pause
                for _ in range(10):
                    self.move_invaders()
                    self.move_projectiles()
                    self.move_invader_projectiles()
                    self.check_collisions()
                    self.master.update()
                    time.sleep(0.1)
                self.master.after(100, self.animate)
            else:
                self.master.after(100, self.animate)  # Si le jeu est en pause, attendez et vérifiez à nouveau

    def move_invaders(self):
        if not self.paused:  # Vérifier si le jeu n'est pas en pause
            for invader in self.invaders:
                dx = random.randint(-5, 5)
                dy = random.randint(0, 3)
                self.canvas.move(invader, dx, dy)

    def show_game_over(self):
        if not self.game_over_text:  # Vérifie si le message n'est pas déjà affiché
            self.game_over_text = self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Helvetica", 32))

    def hide_game_over(self):
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)


    def move_projectiles(self):
        for projectile in self.projectiles:
            self.canvas.move(projectile, 0, -20)

    def move_invader_projectiles(self):
        for projectile in self.invader_projectiles:
            self.canvas.move(projectile, 0, 5)

    def check_collisions(self):
        if self.projectiles: 
            for projectile in self.projectiles[:]:
                for invader in self.invaders:
                    if self.detect_collision(projectile, invader):
                        self.canvas.delete(projectile)
                        self.canvas.delete(invader)
                        self.projectiles.remove(projectile)
                        self.invaders.remove(invader)
                        self.score += 10
                        self.canvas.itemconfig(self.score_label, text=f"Score: {self.score}")

                for invader in self.invaders[:]:
                    if self.detect_collision(projectile, invader):
                        self.destroy_invader(invader)
                        self.projectiles.remove(projectile)
                        break  # Quitter la boucle après la collision avec un invader

                for projectile in self.invader_projectiles[:]:
                    if self.detect_collision(projectile, self.ship):
                        self.game_over = True
                        self.show_game_over()
                        break  # Quitter la boucle après la collision avec le vaisseau joueur

    def damage_obstacle(self, obstacle):
        # L'obstacle du milieu subit 5% de dommages
        current_damage = int(self.canvas.itemcget(obstacle, 'fill').split('#')[-1], 16)
        new_damage = current_damage + 0.05 * 255
        hex_damage = int(min(255, new_damage))
        self.canvas.itemconfig(obstacle, fill=f'#{hex(hex_damage)[2:]:>02}')

        self.obstacle_health -= 10
        if self.obstacle_health <= 0:
            # Supprimer l'obstacle s'il n'a plus de points de vie
            self.canvas.delete(self.obstacles[1])
            self.obstacles.pop(1)
        else:
            # Mettre à jour l'apparence de l'obstacle en fonction des points de vie restants
            green_value = int(255 * (self.obstacle_health / 100))
            obstacle_color = f'#{green_value:02x}ff00'
            self.canvas.itemconfig(self.obstacles[1], fill=obstacle_color)

    def detect_collision(self, item1, item2):
        coords_item1 = self.canvas.coords(item1)
        coords_item2 = self.canvas.coords(item2)
        if coords_item1 and coords_item2:
            x1, y1, x2, y2 = coords_item1
            x3, y3, x4, y4 = coords_item2
            if (x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3):
                return True
        return False

    def show_game_over(self):
        self.game_over_text = self.canvas.create_text(300, 200, text="Game Over", fill="white", font=("Helvetica", 32))

        # Demander au joueur s'il souhaite rejouer
        self.replay_button = tk.Button(self.master, text="Rejouer", command=self.restart_game)
        self.replay_button.pack()

    def restart_game(self):
        # Arrêter l'animation en cours
        self.game_over = False
        self.score = 0
        self.canvas.itemconfig(self.score_label, text="Score: 0")
        if self.game_over_text:
            self.canvas.delete(self.game_over_text)
            self.replay_button.destroy()
            self.hide_game_over()  # Cacher le texte "Game Over"
        # Supprimer tous les projectiles, ennemis et obstacles existants
        self.clear_canvas()
        # Recréer de nouveaux ennemis et obstacles
        self.create_invaders()
        self.create_obstacles()
        # Relancer le jeu
        self.animate()
        self.invader_fire_loop()
        self.obstacle_health = 100


    def clear_canvas(self):
        # Supprimer tous les projectiles
        for projectile in self.projectiles:
            self.canvas.delete(projectile)
        self.projectiles = []
        # Supprimer tous les projectiles des ennemis
        for projectile in self.invader_projectiles:
            self.canvas.delete(projectile)
        self.invader_projectiles = []
        # Supprimer tous les ennemis
        for invader in self.invaders:
            self.canvas.delete(invader)
        self.invaders = []
        # Supprimer tous les obstacles
        for obstacle in self.obstacles:
            self.canvas.delete(obstacle)
        self.obstacles = []

def main():
    root = tk.Tk()
    game = SpaceInvaders(root)
    root.mainloop()

if __name__ == "__main__":
    main()
