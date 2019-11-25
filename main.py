#-*-coding:utf8;-*-
#qpy:pygame

import pygame, random
from pygame.locals import *

onAndroid = False

if onAndroid:
    caminho = "/storage/emulated/0/qpython/projects/f/"
else:
    caminho = ""

pygame.init()
pygame.font.init()

fonteMain = pygame.font.SysFont('Comic Sans MS', 30)
fontePontuacao = pygame.font.SysFont('Comic Sans MS', 15)

TELA_ALTURA = 720
TELA_COMPRIMENTO = 400

CANO_ALTURA = 500
CANO_COMPRIMENTO = 60
CANO_DISTANCIA = (TELA_COMPRIMENTO/2)+50

CHAO_ALTURA = 100

tela = pygame.display.set_mode((TELA_COMPRIMENTO, TELA_ALTURA))

relogio = pygame.time.Clock()

background = pygame.image.load(caminho+'background.png')
background = pygame.transform.scale(background, (TELA_COMPRIMENTO, TELA_ALTURA))

class Passaro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in [caminho+'bluebird-midflap.png', caminho+'bluebird-downflap.png', caminho+'bluebird-upflap.png']:
            self.images.append(pygame.image.load(i).convert_alpha())
        self.imagemAtual = 0
        self.image = self.images[self.imagemAtual]
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
        self.velocidade = 0
    def update(self):
        self.velocidade += 1
        self.imagemAtual = (self.imagemAtual + 1) % 3
        self.image = self.images[self.imagemAtual]
        if self.rect[1] + self.velocidade > 0:
            self.rect[1] += self.velocidade
    def pular(self):
        self.velocidade = -10
        
class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(caminho+'base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TELA_COMPRIMENTO,CHAO_ALTURA))
        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = y
    def update(self):
        self.rect[0] -= 5
        if (self.rect[0] <= -TELA_COMPRIMENTO):
            self.rect[0] = TELA_COMPRIMENTO
            
class matadorDeCanos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,TELA_ALTURA))
        self.rect = self.image.get_rect()
        self.rect[0] = -CANO_COMPRIMENTO

class Cano(pygame.sprite.Sprite):
    def __init__(self, x ,y, invertido):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(caminho+'pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (CANO_COMPRIMENTO, CANO_ALTURA))
        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect[1] = y-CANO_ALTURA-100
            self.rect[0] = TELA_COMPRIMENTO+x
        else:
            self.rect = self.image.get_rect()
            self.rect[1] = y
            self.rect[0] = TELA_COMPRIMENTO+x
    def update(self):
        self.rect[0] -= 5
        
def randomCano(param):
    distancia = random.randint(150,600)
    cano1 = Cano(param, distancia, False)
    cano2 = Cano(param, distancia, True)
    return cano1,cano2

def game(pontuacaoAnterior):
    
    pontuacao = 0
    
    textoIniciar = fonteMain.render(("Pressione espaco para iniciar."), 1, (0,0,0))
    textoPontuacao = fontePontuacao.render(("Pontuacao: "+str(pontuacaoAnterior)), 1, (0,0,0))
    
    grupo_passaro = pygame.sprite.Group()
    passaro = Passaro(100, 300)
    grupo_passaro.add(passaro)
    
    grupo_chao = pygame.sprite.Group()
    chao1 = Chao(0, TELA_ALTURA-CHAO_ALTURA)
    chao2 = Chao(TELA_COMPRIMENTO, TELA_ALTURA-CHAO_ALTURA)
    grupo_chao.add(chao1)
    grupo_chao.add(chao2)
    
    grupo_cano = pygame.sprite.Group()
    cano1, cano2 = randomCano(0)
    cano3, cano4 = randomCano(CANO_DISTANCIA)
    grupo_cano.add(cano1)
    grupo_cano.add(cano2)
    grupo_cano.add(cano3)
    grupo_cano.add(cano4)
    
    grupo_matadorCano = pygame.sprite.Group()
    grupo_matadorCano.add(matadorDeCanos())
    
    stopped = True

    while True:
        relogio.tick(30)
        
        # Pausa
        if (stopped):
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        stopped = False
                if event.type == pygame.MOUSEBUTTONUP:
                    stopped = False
            tela.fill((0,0,0))
            tela.blit(background, (0,0)) 
            grupo_passaro.draw(tela)
            grupo_chao.draw(tela)
            tela.blit(textoIniciar, (5,100))
            if pontuacaoAnterior != None:
                tela.blit(textoPontuacao, (20,150))
            pygame.display.update()
            continue
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    passaro.pular()
            if event.type == pygame.MOUSEBUTTONUP:
                passaro.pular()
                    
        if pygame.sprite.groupcollide(grupo_matadorCano, grupo_cano, False, True):
            tempCano1, tempCano2 = randomCano(CANO_DISTANCIA-150)
            grupo_cano.add(tempCano1)
            grupo_cano.add(tempCano2)   

        print(grupo_cano)
        tela.fill((0,0,0))
        tela.blit(background, (0,0)) 
        grupo_chao.update()
        grupo_passaro.update()
        grupo_cano.update()
        
        grupo_passaro.draw(tela)
        grupo_cano.draw(tela)
        grupo_chao.draw(tela)
        
        pygame.display.update()
        
        if (pygame.sprite.groupcollide(grupo_passaro, grupo_chao, False, False)):
            return pontuacao
        if (pygame.sprite.groupcollide(grupo_passaro, grupo_cano, False, False)):
            return pontuacao

mensagem = None
while True:
    mensagem = game(mensagem)