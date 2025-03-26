from .alimento import Refeicao,Alimento
import json
from typing import Literal

class Usuario:
    def __init__(self):
        self.__nome = ''
        self.__idade = ''
        self.__sexo = ''
        self.__altura = ''
        self.__peso = ''
        self.__objetivo = ''
        self.__metasdiarios = {'Calorias':0,'Proteinas':0,'Carboidratos':0,'Gordura':0}
        self.__macros_consumidos_dia = {'Calorias':0,'Proteinas':0,'Carboidratos':0,'Gordura':0}
        self._refeicao = ''
        self.__historico_refeicao = []
        self.__nivel_de_atividade_fisica = ''
    def dicionario(self) -> dict:
        return {
            "nome": self.__nome,
            "idade": self.__idade,
            "sexo": self.__sexo,
            "altura": self.__altura,
            "peso": self.__peso,
            "objetivo": self.__objetivo,
            "metasdiarios": self.__metasdiarios,
            "macros_consumidos": self.__macros_consumidos_dia,
            'refeicao':self._refeicao,
            'historico':self.__historico_refeicao,
            'nivel':self.__nivel_de_atividade_fisica
        }
    def set_nome(self,novo_nome:str) -> None:
        self.__nome = novo_nome
    def set_idade(self,nova_idade:int)-> None:
        self.__idade = nova_idade
    def set_sexo(self,novo_sexo:Literal['F','M','f','m'])->None:
        self.__sexo = novo_sexo.upper()
    def set_altura(self,nova_altura:int)->None:
        self.__altura = nova_altura
    def set_peso(self,novo_peso:float) -> None:
        self.__peso = novo_peso
    def set_objetivo(self,novo_objetivo):
        self.__objetivo = novo_objetivo
    def set_meta_macro_nutriente(self,proteina:float,gordura:float,carboidratos:float,calorias:float):
        self.__metasdiarios['Proteinas'] = proteina
        self.__metasdiarios['Gordura'] = gordura
        self.__metasdiarios['Carboidratos'] = carboidratos
        self.__metasdiarios['Calorias'] = calorias
    def set_macro_nutriente_consumido_hoje(self,proteina:float,gordura:float,carboidratos:float,calorias:float):
        self.__macros_consumidos_dia['Proteinas'] = proteina
        self.__macros_consumidos_dia['Gordura'] = gordura
        self.__macros_consumidos_dia['Carboidratos'] = carboidratos
        self.__macros_consumidos_dia['Calorias'] = calorias
    def set_nivel_de_atividade_fisica(self,lvl):
        if lvl == 'S' or 1.2:
            self.__nivel_de_atividade_fisica = 1.2
        elif lvl == 'LA' or 1.375:
            self.__nivel_de_atividade_fisica = 1.375
        elif lvl == 'MA' or 1.55:
            self.__nivel_de_atividade_fisica = 1.55
        elif lvl == 'AA' or 1.725:
            self.__nivel_de_atividade_fisica = 1.725
        elif lvl == 'MA' or 1.9:
            self.__nivel_de_atividade_fisica = 1.9
    def set_historico(self,hist):
        self.__historico_refeicao = hist
    def get_nome(self):
        return self.__nome
    def get_idade(self):
        return self.__idade
    def get_sexo(self):
        return self.__sexo
    def get_altura(self):
        return self.__altura
    def get_peso(self):
        return self.__peso
    def get_objetivo(self):
        return self.__objetivo
    def get_refeicao(self) -> str:
        return self._refeicao.get_nome_da_refeição()
    def get_historico(self) -> list:
        return self.__historico_refeicao
    def get_nivel(self):
        return self.__nivel_de_atividade_fisica
    def get_meta_consumo_diario(self):
        return self.__metasdiarios
    def get_macros_consumidos_no_dia(self):
        return self.__macros_consumidos_dia
    def criar_refeição(self,nome_da_refeicao):
        self._refeicao = Refeicao(nome_da_refeicao)
    def adiciona_alimentos_na_refeicao(self,nome_do_alimento,quant):
        self._refeicao.adicionar_alimento(Alimento().adicionar_alimento_ja_cadastrado(nome_do_alimento,quant))
    def contabilizar_os_macros_refeição(self):
        g,p,carb,calo = self._refeicao.get_macros()
        self.__macros_consumidos_dia['Gordura'] += round(g,2)
        self.__macros_consumidos_dia['Proteinas'] += round(p,2)
        self.__macros_consumidos_dia['Carboidratos'] += round(carb,2)
        self.__macros_consumidos_dia['Calorias'] += round(calo,2)
        self.__historico_refeicao.append([self._refeicao.get_nome_da_refeição(),self._refeicao.get_historico()])
        self._refeicao= ''
    def status_macros_diarios_zerar(self):
        self.__metasdiarios = {'Calorias': 2200, 'Proteinas': 50, 'Carboidratos': 200, 'Gordura': 100}
        self.__macros_consumidos = {'Calorias': 0, 'Proteinas': 0, 'Carboidratos': 0, 'Gordura': 0}
    def calculo_tmp(self):
        #Local de onde eu peguei a formula
        #https://www.calculadora.app/nutricao/taxa-metabolica-basal#google_vignette
        return round((66+(13.8*self.get_peso())+(5*self.get_altura())-(6.8*self.get_idade())),2)
    def calculo_get(self):
        return round((self.calculo_tmp()*self.get_nivel()),2)
class Usuario_feminino(Usuario):
    def calculo_tmp(self):
        return round((651.1 + (9.6 * self.get_peso()) + (1.85 * self.get_altura()) - (4.676 * self.get_idade())), 2)

def carregar_usuario(nome_usuario):
    """
    Lê o JSON e procura o usuário com o nome especificado.
    Retorna a instância do usuário e também uma tupla (dados_json, indice)
    para posterior atualização no arquivo.
    """
    try:
        with open('modulos/usuarios.json', 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        print("Arquivo JSON não encontrado!")
        return None, None
    usuario_dict = None
    indice = None
    for idx, usuario in enumerate(dados.get("usuarios", [])):
        if usuario.get("nome", "").lower() == nome_usuario.lower():
            usuario_dict = usuario
            indice = idx
            break

    if usuario_dict is None:
        print(f"Usuário '{nome_usuario}' não encontrado no JSON.")
        return None, None
    if usuario_dict['sexo'] == 'M':
        u = Usuario()
        u.set_nome(usuario_dict['nome'])
        u.set_idade(usuario_dict['idade'])
        u.set_sexo(usuario_dict['sexo'])
        u.set_altura(usuario_dict['altura'])
        u.set_peso(usuario_dict['peso'])
        u.set_objetivo(usuario_dict['objetivo'])
        u.set_macro_nutriente_consumido_hoje(usuario_dict['macros_consumidos']['Proteinas'],
                                             usuario_dict['macros_consumidos']['Gordura'],
                                             usuario_dict['macros_consumidos']['Carboidratos'],
                                             usuario_dict['macros_consumidos']['Calorias'])
        u.set_meta_macro_nutriente(usuario_dict['metasdiarios']['Proteinas'],
                                   usuario_dict['metasdiarios']['Gordura'],
                                   usuario_dict['metasdiarios']['Carboidratos'],
                                   usuario_dict['metasdiarios']['Calorias'])
        u.set_historico(usuario_dict['historico'])
        u.set_nivel_de_atividade_fisica(usuario_dict['nivel'])
        return u, (dados, indice)
    elif usuario_dict['sexo'] == 'F':
        u = Usuario_feminino()
        u.set_nome(usuario_dict['nome'])
        u.set_idade(usuario_dict['idade'])
        u.set_sexo(usuario_dict['sexo'])
        u.set_altura(usuario_dict['altura'])
        u.set_peso(usuario_dict['peso'])
        u.set_objetivo(usuario_dict['objetivo'])
        u.set_macro_nutriente_consumido_hoje(usuario_dict['macros_consumidos']['Proteinas'],
                                             usuario_dict['macros_consumidos']['Gordura'],
                                             usuario_dict['macros_consumidos']['Carboidratos'],
                                             usuario_dict['macros_consumidos']['Calorias'])
        u.set_meta_macro_nutriente(usuario_dict['metasdiarios']['Proteinas'], usuario_dict['metasdiarios']['Gordura'],
                                   usuario_dict['metasdiarios']['Carboidratos'],
                                   usuario_dict['metasdiarios']['Calorias'])
        u.set_historico(usuario_dict['historico'])
        u.set_nivel_de_atividade_fisica(usuario_dict['nivel'])
        return u, (dados,indice)
def salvar_usuario(dados_e_indice, usuario_instancia):
    """
    Atualiza os dados do usuário no JSON e grava o arquivo.
    """
    dados, indice = dados_e_indice
    dados["usuarios"][indice] = usuario_instancia.dicionario()
    with open('modulos/usuarios.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
