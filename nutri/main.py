from modulos.usuario import Usuario,Usuario_feminino,carregar_usuario,salvar_usuario
from modulos.alimento import Alimento,Refeicao
import json

class app:
    def __init__(self):
        self._usuario_selecionado = ''
        self._dados_indice = ''
    def inicio_menu(self):
        print('---- Sejá bem vindo ao Programa de calculo nutricional ----')
        while True:
            print('     Para selecionar um usuario digite 1')
            print('     Para adicionar um usuario digite 2')
            print('     Para cadastro de alimentos 3 ')
            print('     Para sair do programa digite 0')
            print('     Selecione uma opção das acima')
            resposta_input = input('R: ')
            if resposta_input == '1':
                print('-----------------------------------------------------------')
                resp = input('Digite o nome do Usuario :')
                self.f_selecio_usuario(resp)
            elif resposta_input == '2':
                self.f_menu_criar_usuario()
                return self.inicio_menu()
            elif resposta_input == '3':
                break
            elif resposta_input == '0':
                break
            else:
                print('Selecione uma opção valida')
    def selec_menu(self):
        while True:
            print('-----------------------------------------------------------')
            print(f'Voce esta com o usuario {self._usuario_selecionado.get_nome()} Selecionado')
            print('-----------------------------------------------------------')
            print('     Para criar refeição digite 1')
            print('     Para ver realizado x meta digite 2')
            print('     Para calculos de GET e TMP digite 3')
            print('     Para zerar os macros do dia digite 4')
            print('     Para ver o historico de refeições digite 5')
            print('     Para para voltar ao menu anterior digite 0')
            resp = input('Selecione uma opção das acima R: ')
            if resp == '1':
                print('-----------------------------------------------------------')
                print('Qual o nome da refeição: ')
                resp = input('R = ')
                self._usuario_selecionado.criar_refeição(resp)
                self.menu_refeicao()
            elif resp == '2':
                print('-----------------------------------------------------------')
                print(f' Usuario {self._usuario_selecionado.get_nome()}  Consumo x meta de macro nutriente')
                print('-----------------------------------------------------------')
                print(f'''
Usuario {self._usuario_selecionado.get_nome()} 
Consumo X Meta
Calorias:   {self._usuario_selecionado.get_macros_consumidos_no_dia()['Calorias']} X {self._usuario_selecionado.get_meta_consumo_diario()['Calorias']}
Gordura:    {self._usuario_selecionado.get_macros_consumidos_no_dia()['Gordura']} X {self._usuario_selecionado.get_meta_consumo_diario()['Gordura']}
Proteina:   {self._usuario_selecionado.get_macros_consumidos_no_dia()['Proteinas']} X {self._usuario_selecionado.get_meta_consumo_diario()['Proteinas']}
Carboidrato:{self._usuario_selecionado.get_macros_consumidos_no_dia()['Carboidratos']} X {self._usuario_selecionado.get_meta_consumo_diario()['Carboidratos']}
''')
            elif resp == '3':
                print('-----------------------------------------------------------')
                print(f' Usuario {self._usuario_selecionado.get_nome()}  Calculo de GET E TMP')
                print('-----------------------------------------------------------')
                print(f' Sue TMP é de = {self._usuario_selecionado.calculo_tmp()}')
                print('-----------------------------------------------------------')
                print(f' Sue GET é de = {self._usuario_selecionado.calculo_get()}')
                print('-----------------------------------------------------------')
            elif resp == '4':
                print('-----------------------------------------------------------')
                print(f' Usuario {self._usuario_selecionado.get_nome()}  Zerado o consumo do dia')
                self._usuario_selecionado.set_macro_nutriente_consumido_hoje(0,0,0,0)
                print('-----------------------------------------------------------')
            elif resp == '5':
                historico =self._usuario_selecionado.get_historico()
                for hist in range(len(historico)):
                    ref, alimento_quant = historico[hist]
                    print(f'Na refeição {ref} voce comeu:')
                    for alimento in alimento_quant:
                        nome = alimento[0]
                        quantidade = alimento[1]
                        print(f"{nome} {quantidade}G")
            elif resp == '0':
                salvar_usuario(self._dados_indice, self._usuario_selecionado)
                print('-----------------------------------------------------------')
                print(f'Voce saiu do usuario selecionado {self._usuario_selecionado.get_nome()}')
                self._usuario_selecionado = ''
                self._dados_indice = ''
                return self.inicio_menu()
    def menu_refeicao(self):
        while True:
            print('-----------------------------------------------------------')
            print(f'Voce esta com o usuario {self._usuario_selecionado.get_nome()} Selecionado e na refeição {self._usuario_selecionado.get_refeicao()}')
            print('-----------------------------------------------------------')
            print('             Para adicionar alimento da refeição digite 1')
            print('             Para mostras dados da refeição digite 2')
            print('             Se já adicionaou todos os alimentos da refeição Digite 3')
            print('             Para mostrar alimentos e quantidade já adicionada na refeição Digite 4')
            resp = input('Selecione uma opção das acima R: ')
            if resp == '1':
                self.f_adicinar_alimento_na_refeição()
            elif resp == '2':
                print('-----------------------------------------------------------')
                print(f'Segue os dados dos macros nutriente da refeição')
                print(f'''1
Usuario {self._usuario_selecionado.get_nome()}
Calorias {self._usuario_selecionado._refeicao.get_calorias()}
Gordura {self._usuario_selecionado._refeicao.get_gordura()}
Proteina {self._usuario_selecionado._refeicao.get_proteina()}
Carboidrato {self._usuario_selecionado._refeicao.get_carboidrato()}
                ''')
            elif resp == '3':
                self._usuario_selecionado.contabilizar_os_macros_refeição()
                print('-----------------------------------------------------------')
                print('Macro nutriente da refeição contabilizados no usuario com sucesso')
                break
            elif resp == '4':
                print('-----------------------------------------------------------')
                print(f' Na refeição :{self._usuario_selecionado._refeicao.get_nome_da_refeição()} voce ja adicionou os seguintes alimentos')
                for i in self._usuario_selecionado._refeicao.get_historico():
                    a,q = i
                    print(f'Alimento {a}, quantidade {q}G')
    def f_adicinar_alimento_na_refeição(self):
        print('-----------------------------------------------------------')
        print(
            f'Voce esta adiconando alimento na refeição:{self._usuario_selecionado.get_refeicao()} do usuario {self._usuario_selecionado.get_nome()}')
        alimento_input = input('        Qual o nome do alimento ?')
        quantidade_em_gramas = input('        Qual a quantidade desse alimento em gramas :')
        print('-----------------------------------------------------------')
        self._usuario_selecionado.adiciona_alimentos_na_refeicao(alimento_input, int(quantidade_em_gramas))
        print('Alimento adicionado na refeição, voce foi redirecionado para o menu da refeição')
    def f_menu_criar_usuario(self):
        print('---------------- Vamos Criar um usuario da plataforma ------------- ')
        nome = input('Qual é o nome :')
        idade = int(input('Qual é o idade (numero inteiro):'))
        sexo = input('Qual é o sexo M ou F:')
        altura = int(input('Qual é o altura em cm (numero inteiro) :'))
        peso = int(input('Qual é o peso (numero inteiro) :'))
        objetivo = input('Qual é o objetivo :')
        meta_calorias = input('Qual é a mata de calorias para um dia (numero inteiro) :')
        meta_proteinas = input('Qual é a meta de proteinas para um dia (numero inteiro) :')
        meta_carboidratos  = input('Qual é a meta de carboidratos para um dia (numero inteiro) :')
        meta_gordura = input('Qual é a meta de gordura para um dia (numero inteiro) :')
        nivel_atividade_fisica = input('''qual o seu nivel de atividade ficica opçoes de resposta
Sedentário: S
Levemente ativo: LA
Moderadamente ativo: M
Altamente ativo: AA
Muito ativo: MA
Resposta = ''')
        if sexo.upper() == "M":
            novo_usuario = Usuario()
            novo_usuario.set_nome(nome)
            novo_usuario.set_idade(idade)
            novo_usuario.set_sexo(sexo)
            novo_usuario.set_altura(altura)
            novo_usuario.set_peso(peso)
            novo_usuario.set_objetivo(objetivo)
            novo_usuario.set_meta_macro_nutriente(meta_proteinas,meta_gordura,meta_carboidratos,meta_calorias)
            novo_usuario.set_nivel_de_atividade_fisica(nivel_atividade_fisica.upper())
        elif sexo.upper() == "F":
            novo_usuario = Usuario_feminino()
            novo_usuario.set_nome(nome)
            novo_usuario.set_idade(idade)
            novo_usuario.set_sexo(sexo)
            novo_usuario.set_altura(altura)
            novo_usuario.set_peso(peso)
            novo_usuario.set_objetivo(objetivo)
            novo_usuario.set_meta_macro_nutriente(meta_proteinas, meta_gordura, meta_carboidratos, meta_calorias)
            novo_usuario.set_nivel_de_atividade_fisica(nivel_atividade_fisica.upper())
        try:
            with open('modulos/usuarios.json', "r") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            dados = {"usuarios": []}
        dados["usuarios"].append(novo_usuario.dicionario())
        with open('modulos/usuarios.json', "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
        print('Voltamos para o menu inicial')
    def f_selecio_usuario(self,nome):
        self._usuario_selecionado,self._dados_indice = carregar_usuario(nome)
        self.selec_menu()

teste = app().inicio_menu()