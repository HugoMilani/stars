
import pygame
from pygame.locals import *
from tkinter import Tk, simpledialog
import os
pygame.init()
tamanho = (800, 600)
branco = (255, 255, 255)
preto = (0, 0, 0)
display = pygame.display.set_mode((tamanho))
pygame.display.set_caption("Space Marker")
fundo = pygame.image.load("bg.png") 
dados_fornecidos = {}
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1) 
icon = pygame.image.load("icon2.png")
pygame.display.set_icon(icon)

#Funções para o jogo
def salvar_marcacoes():
    with open("dados.txt", "w") as arquivo:
        for posicao, nome in dados_fornecidos.items():
            arquivo.write(f"{posicao[0]},{posicao[1]},{nome}\n")
    print("Marcações salvas com sucesso!")
def carregar_marcacoes():
    dados_fornecidos.clear()
    if os.path.exists("dados.txt"):
        with open("dados.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                x, y, nome = linha.strip().split(",")
                posicao = (int(x), int(y))
                dados_fornecidos[posicao] = nome
        print("Marcações carregadas com sucesso!")
    else:
        print("Nenhum arquivo de marcações encontrado.")
def excluir_marcacoes():
    dados_fornecidos.clear()
    if os.path.exists("dados.txt"):
        os.remove("dados.txt")
        print("Todas as marcações foram excluídas.")
    else:
        print("Nenhum arquivo de marcações encontrado.")
        
def calcular_diferenca_pontos(ponto1, ponto2):
    diferenca_x = abs(ponto1[0] - ponto2[0])
    diferenca_y = abs(ponto1[1] - ponto2[1])
    diferenca_total = diferenca_x + diferenca_y
    return diferenca_total
executando = True
while executando:
    for evento in pygame.event.get():
        if evento.type == QUIT:
            executando = False
        elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
            executando = False
        elif evento.type == KEYDOWN and evento.key == K_F10:
            salvar_marcacoes()
        elif evento.type == KEYDOWN and evento.key == K_F11:
            carregar_marcacoes()
        elif evento.type == KEYDOWN and evento.key == K_F12:
            excluir_marcacoes()
        elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            posicao_mouse = pygame.mouse.get_pos()
            root = Tk()
            root.withdraw()
            estrela = simpledialog.askstring("Nome da Estrela", "Digite o nome da estrela:")
            if estrela.strip() == "":
                estrela = "desconhecido"
            dados_fornecidos[posicao_mouse] = estrela
    display.blit(fundo, (0, 0))  
    for posicao, nome in dados_fornecidos.items():
        pygame.draw.circle(display, branco, posicao, 5)   
        texto = pygame.font.SysFont(None, 20).render(nome, True, branco)
        texto_coordenadas = pygame.font.SysFont(None, 16).render(f"({posicao[0]}, {posicao[1]})", True, branco)
        display.blit(texto, (posicao[0] + 10, posicao[1] - 10)) 
        display.blit(texto_coordenadas, (posicao[0] + 10, posicao[1] + 5)) 
    pontos = list(dados_fornecidos.keys())
    if len(pontos) >= 2:
        for i in range(len(pontos) - 1):
            ponto1 = pontos[i]
            ponto2 = pontos[i + 1]
            pygame.draw.line(display, branco, ponto1, ponto2)
            diferenca = calcular_diferenca_pontos(ponto1, ponto2)
            texto_diferenca = pygame.font.SysFont(None, 16).render(str(diferenca), True, branco)
            posicao_texto = ((ponto1[0] + ponto2[0]) // 2, (ponto1[1] + ponto2[1]) // 2)
            display.blit(texto_diferenca, posicao_texto)
    instrucoes = [
        "Pressione F10 para Salvar os pontos",
        "Pressione F11 para carregar os pontos",
        "Pressione F12 para deletar os pontos"
    ]
    for i, instrucao in enumerate(instrucoes):
        texto_instrucao = pygame.font.SysFont(None, 16).render(instrucao, True, branco)
        display.blit(texto_instrucao, (10, 10 + i * 20))
        
    pygame.display.update()
    
salvar_marcacoes()
pygame.quit()
        