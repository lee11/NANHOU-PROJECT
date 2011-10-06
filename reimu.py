import EntityTypes

class PlayerClass (EntityTypes.Player):
    def __init__(self):
        super(PlayerClass, self).__init__(controlState):
        animator = animation.Animator([''], '.png', '.playeranim')
    def shoot(self):
        b = []
        b.append(EntityTypes.Bullet(animation.Animator(dirStr="./playerbulletanim"), (self.x, self.y), vel=(0,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        
        
        b.append(EntityTypes.Bullet(animation.Animator(dirStr="./playerbulletanim"), (self.x, self.y), vel=(self.bulletSpeed*-1,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        
        
        b.append(EntityTypes.Bullet(animation.Animator(dirStr="./playerbulletanim"), (self.x, self.y), vel=(self.bulletSpeed,self.bulletSpeed*-1), radius=self.bulletRadius, damage=self.bulletDamage))
        
        self.lastShot = 0
        return b


name = "Hakurei Reimu"
portrait = pygame.image.load('reimu.png')
desc = "The lazy, care free, shrine maiden."
longDesc = "The wonderful shrine maiden of Gensokyo. She loves exterminating youkai, and strange people love her."

