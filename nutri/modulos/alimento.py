import csv
import json

def dadoscsv():
    with open('teste.csv', encoding='utf-8') as csvfile:
        leitor = csv.DictReader(csvfile, delimiter=';')
        l = []
        for linha in leitor:
            l.append(linha)
        return l

class Refeicao:
    def __init__(self,nome_da_refeição:str):
        self.__nome_da_refeição = nome_da_refeição
        self.__proteinas = 0
        self.__carboidrato = 0
        self.__gordura = 0
        self.__calorias = 0
        self.__alimentos_quantidades = []
    def altear_nome_da_refeição(self,novo_nome_da_refeição:str) -> None:
        self.__nome_da_refeição = novo_nome_da_refeição
    def get_nome_da_refeição(self) -> str:
        return self.__nome_da_refeição
    def get_proteina(self) -> float:
        return round(self.__proteinas,2)
    def get_carboidrato(self) -> float:
        return round(self.__carboidrato,2)
    def get_gordura(self) -> float:
        return round(self.__gordura,2)
    def get_calorias(self) -> float:
        return round(self.__calorias,2)
    def get_macros(self) ->list:
        '''Retorna Gordura,Proteinas,Carboidrato,Calorias'''
        return [round(self.__gordura,2),round(self.__proteinas,2),round(self.__carboidrato,2),round(self.__calorias,2)]
    def get_historico(self) -> list:
        return self.__alimentos_quantidades
    def adicionar_alimento(self,alimento):
        if not isinstance(alimento, Alimento):
            print('O parâmetro precisa ser uma instância da classe Alimento')
        self.__proteinas += alimento.get_proteina()
        self.__carboidrato += alimento.get_carboidrato()
        self.__gordura += alimento.get_gordura()
        self.__calorias += alimento.get_calorias()
        self.__alimentos_quantidades.append((alimento.get_nome(),alimento.get_quantidade()))

class Alimento:
    def __init__(self):
        self.__nome = ''
        self.__quantidade = 0
        self.__protaina = 0
        self.__gordura = 0
        self.__carboidrato = 0
        self.__calorias = 0
    def get_nome(self) -> str:
        return self.__nome
    def get_quantidade(self) -> float:
        return self.__quantidade
    def get_proteina(self) -> float:
        return self.__protaina
    def get_gordura(self) -> float:
        return self.__gordura
    def get_carboidrato(self) -> float:
        return self.__carboidrato
    def get_calorias(self) -> float:
        return self.__calorias
    def set_nome(self,nome:str) -> None:
        self.__nome = nome
    def set_quantidade(self,quantidade:float) ->None:
        self.__quantidade = quantidade
    def set_proteina_em_100_gramas(self,proteina:float) -> None:
        self.__protaina = proteina
    def set_gordura_em_100_gramas(self,gordura:float) -> None:
        self.__gordura = gordura
    def set_carboidrato_em_100_gramas(self,carboidrato:float) -> None:
        self.__carboidrato = carboidrato
    def set_calorias_em_100_gramas(self,calorias:float) -> None:
        self.__calorias = calorias

    def dicionario(self) -> dict:
        return {
            'nome': self.__nome,
            'proteina': self.__protaina,
            'gordura': self.__gordura,
            'carboidrato': self.__carboidrato,
            'calorias': self.__calorias
        }
    def adicionar_alimento_ao_json(self,nome_do_alimento:str,proteinas_em_100g:float,gorduras_em_100g:float,carboidratos_em_100g:float,calorias_em_100g:float) -> None:
        self.set_nome(nome_do_alimento.upper())
        self.set_proteina_em_100_gramas(proteinas_em_100g)
        self.set_gordura_em_100_gramas(gorduras_em_100g)
        self.set_carboidrato_em_100_gramas(carboidratos_em_100g)
        self.set_calorias_em_100_gramas(calorias_em_100g)
        with open('modulos/db_alimentos.json', "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        dados["alimentos"].append(self.dicionario())
        with open('modulos/db_alimentos.json', "w") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    def adicionar_alimento_ja_cadastrado(self,nome_busca:str,quantidade:float):
        self.set_quantidade(quantidade)
        try:
            with open('modulos/db_alimentos.json', 'r', encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            print("Arquivo JSON não encontrado.")
            return self
        for alimento in dados.get("alimentos", []):
            if str(alimento['nome']).lower() == nome_busca.lower():
                self.set_nome(nome_busca.upper())
                self.__gordura = alimento['gordura']*self.__quantidade/100
                self.__calorias = alimento['calorias']*self.__quantidade/100
                self.__carboidrato = alimento['carboidrato']*self.__quantidade/100
                self.__protaina = alimento['proteina']*self.__quantidade/100
                break
        if self.__nome == '':
            print('alimento nao cadastrado em nossa base')
            print('Vamos cadastrar ele agora ?')
            proteina = float(input('Quantidade de proteina em 100g :'))
            gordura= float(input('Quantidade de gordura em 100g :'))
            carboidrato = float(input('Quantidade de carboidrato em 100 g :'))
            calorias= float(input('Quantidade de calorias em 100 g :'))
            self.adicionar_alimento_ao_json(nome_busca,proteina,gordura,carboidrato,calorias)
        return self