import EntityTypes, player, pygame.image, animation

FRAME_INTERVAL = 10

class PlayerClass (player.Player):
    def __init__(self, controlState):
        super(PlayerClass, self).__init__(controlState)
        #for i in range(0,player.N_STATES):
        #    self.animations[i] = animation.Animator(['', 'u', 'd', 'l', 'r', 'i'], '.png', './playeranim')
        #    self.animations[i].setAnimation('', FRAME_INTERVAL)
        self.animator = animation.Animator(['u', 'd', 'l', 'r', 'i'], '.png', './playeranim')
        self.animator.setFrameInterval(FRAME_INTERVAL)
        self.animator.setAnimation('i')
        self.x = 320
        self.y = 240

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

