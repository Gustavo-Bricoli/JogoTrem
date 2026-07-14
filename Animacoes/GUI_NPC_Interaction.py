# Seção para teste a partir da root:
#//////////////////////////////////////////////////////////////////////////////////
""" import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.estacao import estacoes
from Sistemas.gerarNpc import criarNpcs
from pyperclip import copy """
#//////////////////////////////////////////////////////////////////////////////////

import os
import getpass
from math import ceil
from Classes.NPC import NPC
from Sistemas.terminalCleaner import clean
from Sistemas.bgGeneratorNpcGroq import gerarBackstory, chatNPC
from Animacoes.ascii_npc.portraits import IMAGE_WOMAN, IMAGE_MAN

terminal_width, terminal_lines = os.get_terminal_size()

def gerarCaixaDialog():
    content = []

    # Versão legada da caixa de diálogo:
    """ content.append(os.get_terminal_size()[0]*'-')
    for i in range(19): #terminal_lines-6, 13 para centralizar imagem ascii mockup acima
        content.append('|'+(os.get_terminal_size()[0]-2)*' '+'|')
    content.append(os.get_terminal_size()[0]*'-')
    print(''.join(content)) """

    # Nova versão da caixa de diálogo:
    content.append('╔'+(terminal_width-2)*'═'+'╗')
    for i in range(len(IMAGE_WOMAN)+2): #terminal_lines-6, 13 para centralizar imagem ascii mockup, 19 (17+2) para arte ascii Roberto
        content.append('║'+(terminal_width-2)*' '+'║')
    content.append('╚'+(terminal_width-2)*'═'+'╝')

    return content

def inserirConteudoCaixa(content:list, text:str, portrait:tuple=None):
    if portrait is None:
        line_size = terminal_width-2-10

        breaks = [index for index, char in enumerate(text) if char == "\n"]

        while text.find('\n') != -1:
            text = text.replace('\n', ' '*(line_size-(breaks[0]%line_size)), 1)
            breaks = [index for index, char in enumerate(text) if char == "\n"]

        total_lines = ceil(len(text)/line_size)

        if len(text) > line_size:
            lines_ok = 0
            temp_text = []
            i = 0
            offset = 0
            while lines_ok != total_lines:
                if text[line_size*i+offset:line_size*(i+1)+offset][:3] == '   ':
                    temp_text.append(text[line_size*i:line_size*(i+1)])
                    offset -= 1
                    lines_ok += 1
                    i += 1
                elif text[line_size*i+offset:line_size*(i+1)+offset][0] != ' ':
                    temp_text.append(text[line_size*i+offset:line_size*(i+1)+offset])
                    lines_ok += 1
                    i += 1
                else:
                    offset += 1

            text = ''.join(temp_text)
            del temp_text, lines_ok, i, offset # 'inútil' por causa do garbage collector do python, mas funcionar funciona

        max_size_text = line_size*(len(IMAGE_WOMAN))
        if len(text) > max_size_text:
            temp_text = []
            for i in range(ceil(len(text)/max_size_text)):
                temp_text.append(text[max_size_text*i:max_size_text*(i+1)])
            text = temp_text
            del temp_text # 'inútil' por causa do garbage collector do python, mas funcionar funciona

            for i in range(len(text)): # tratativa para textos muito longos
                textBox(text=text[i])
                if i != len(text)-1:
                    getpass.getpass(f'\n({i+1}/{len(text)})\nPressione enter para continuar. ')
                else:
                    print(f'\n({i+1}/{len(text)})', end='')
                
            return
            
        total_lines = ceil(len(text)/line_size) # para caso tenha sido adicionado linhas, após as tratativas acima

        for i in range(total_lines):
            len_linha = len(text[line_size*i:line_size*(i+1)])
            content[i+2] = content[i+2].replace(' ', '', len_linha)
            content_list = list(content[i+2])
            if '\033[0m' in text[line_size*i:line_size*(i+1)]:
                content_list.insert(6, text[line_size*i:line_size*(i+1)]+' '*11)
            else:
                content_list.insert(6, text[line_size*i:line_size*(i+1)])
            content[i+2] = ''.join(content_list)

        return ''.join(content)
    
    else:
        portrait_size = len(IMAGE_MAN[0])
        line_size = terminal_width-2-15-portrait_size

        text = text.replace('\n\n', '\n#\n').replace('\r','') # tratamento para não quebrar na verificação de linha para inserção do portrait

        breaks = [index for index, char in enumerate(text) if char == "\n"]

        while text.find('\n') != -1:
            text = text.replace('\n', ' '*(line_size-(breaks[0]%line_size)), 1)
            breaks = [index for index, char in enumerate(text) if char == "\n"]

        total_lines = ceil(len(text)/line_size)

        if len(text) > line_size:
            lines_ok = 0
            temp_text = []
            i = 0
            offset = 0
            while lines_ok != total_lines:
                if text[line_size*i+offset:line_size*(i+1)+offset][:3] == '   ':
                    temp_text.append(text[line_size*i:line_size*(i+1)])
                    offset -= 1
                    lines_ok += 1
                    i += 1
                elif text[line_size*i+offset:line_size*(i+1)+offset][0] != ' ':
                    temp_text.append(text[line_size*i+offset:line_size*(i+1)+offset])
                    lines_ok += 1
                    i += 1
                else:
                    offset += 1

            text = ''.join(temp_text)
            del temp_text, lines_ok, i, offset # 'inútil' por causa do garbage collector do python, mas funcionar funciona

        max_size_text = line_size*(len(IMAGE_WOMAN))
        if len(text) > max_size_text:
            temp_text = []
            for i in range(ceil(len(text)/max_size_text)):
                temp_text.append(text[max_size_text*i:max_size_text*(i+1)])
            text = temp_text
            del temp_text # 'inútil' por causa do garbage collector do python, mas funcionar funciona

            for i in range(len(text)): # tratativa para textos muito longos
                textBox(text=text[i], portrait=portrait)
                if i != len(text)-1:
                    getpass.getpass(f'\n({i+1}/{len(text)})\nPressione enter para continuar. ')
                else:
                    print(f'\n({i+1}/{len(text)})', end='')
                
            return
            
        total_lines = ceil(len(text)/line_size) # para caso tenha sido adicionado linhas, após as tratativas acima

        #content = list(content) # esta linha não funciona porque o content é criado como uma lista com as respectivas linhas a serem printadas. Enquanto que o list() retorna todos os caracteres individualizados
        
        for i in range(total_lines):
            len_linha = len(text[line_size*i:line_size*(i+1)])
            #if len_linha != 0: # não é mais um bug por causa do uso de ceil()
            content[i+2] = content[i+2].replace(' ', '', len_linha+portrait_size)
            content_list = list(content[i+2])
            content_list.insert(6, text[line_size*i:line_size*(i+1)])
            content[i+2] = ''.join(content_list)

        for i in range(len(portrait)):
            if content[i+2][6] == ' ' and content[i+2][7] == ' ':
                content[i+2] = content[i+2].replace(' ', '', len(portrait[0]))
            content_list = list(content[i+2].replace('#', ' '))
            content_list.insert(line_size+11, portrait[i])
            content[i+2] = ''.join(content_list)

        return ''.join(content)
    
def textBox(text:str, portrait:tuple=None):
    clean()
    content = gerarCaixaDialog()
    content = inserirConteudoCaixa(content, text, portrait)

    if content is not None: # retornará None para os casos de texto maior que 1 tela
        print(content)

def encontroNPC(NPC: NPC):
    if NPC.genero == 'F':
        image = IMAGE_WOMAN
    else:
        image = IMAGE_MAN

    # Primeira tela
    if NPC.genero == 'F':
        texto = 'Você sai da cabine de comando e se depara com uma passageira.'
    else:
        texto = 'Você sai da cabine de comando e se depara com um passageiro.'

    textBox(text=texto)
    # NPC.backstory aqui para a primeira tela ser como uma de carregamento
    NPC.backstory = gerarBackstory(NPC) # -> fazer só passar NPC, gerar aleatório juntamente -> 👌
    #copy(NPC.backstory)
    getpass.getpass('\nPressione enter para continuar. ')

    # Segunda tela
    #geração da NPC.backstory antes do Enter da primeira tela

    # história gerada com \n\n para teste:
    #NPC.backstory = 'Rebeca Pereira, de 38 anos, é uma jornalista experiente que sempre viveu ao sabor do vento. Ela viaja constantemente, em busca de histórias que contar e de lugares que explorar. Com um olhar curioso e uma mente ágil, Rebeca navega pelos trens, ônibus e hotéis, sempre à procura de algo novo.\n\nSua vida é um constante fluxo de ação, com entrevistas, notas de rodapé e prazos a cumprir. Mesmo assim, ela nunca perde a oportunidade de parar e apreciar as pequenas coisas, como o som das rodinhas do trem ou o aroma de um café recém-preparado. Enquanto o trem atravessa um túnel escuro, Rebeca retira um caderno da bolsa e começa a escrever, capturando as impressões do dia.'
    
    textBox(text=NPC.backstory, portrait=image)
    getpass.getpass('\nPressione enter para continuar. ')

    # Terceira tela
    while True:
        texto = [
            f'Mesmo com os demais passageiros te encarando de forma quase hostil, é possível seguir interagindo com {NPC.nome}.\n', # condição de demais passageiros no trem? Futuro
            'Faça uma escolha:\n\n',
            '2. Voltar para a cabine de comando.'
        ]

        if NPC.genero == 'F':
            texto.insert(2, '1. Interagir com a passageira.\n')
        else:
            texto.insert(2, '1. Interagir com o passageiro.\n')

        texto = ''.join(texto)

        textBox(text=texto)

        answer = input('\nO que deseja fazer? (1/2)\n')
        if answer in ['1','2']:
            break

    # Quarta tela
    if answer == '1':
        texto = [
            f'O que deseja fazer com {NPC.nome.split(" ")[0]}?\n',
            '1. Dizer alguma coisa.',
            '2. Examinar.',
            '3. Voltar para a cabine de comando.'
        ]

        answer = ''
        options = ['1','2','3']
        txt_input = '\nO que deseja fazer? (1/2/3)\n'

        while True:        
            while answer not in options:
                textBox(text='\n'.join(texto))

                answer = input(txt_input)
                if answer in options:
                    break
            if answer == '1':
                options.remove('1')
                texto[1] = f'\033[0;90m{texto[1]}\033[0m'
                txt_input = '\nO que deseja fazer? (2/3)\n'

                # seção de pergunta
                textBox(text='RELEMBRANDO: '+NPC.backstory, portrait=image)
                NPC_interaction = input('\nO que deseja dizer?\n')
                textBox(text=chatNPC(NPC, NPC_interaction), portrait=image)
                getpass.getpass('\nPressione enter para continuar. ')
                
            elif answer == '2':
                textBox(text='* Examinando... *')
                answer = ''
                getpass.getpass('\nPressione enter para continuar. ')
            else:
                break

    # Quarta(não aceitou interação)/quinta(aceitou interação) tela
    if NPC.genero == 'F':
        textBox(text=f'Você deixa {NPC.nome.split(" ")[0]} falando sozinha e volta para seu posto.')
    else:
        textBox(text=f'Você deixa {NPC.nome.split(" ")[0]} falando sozinho e volta para seu posto.')

    getpass.getpass('\nPressione enter para continuar. ')
    clean()

# Testando:
#////////////////////////////////
""" npc = criarNpcs(estacoes, 1)
encontroNPC(npc[0]) """
#////////////////////////////////