import os
import json
import sys
from datetime import datetime, date
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from decimal import Decimal
import traceback

# ==================== CONFIGURAÇÃO INICIAL ====================

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_pastas_necessarias():
    """Cria as pastas necessárias para o sistema"""
    pastas = ['folha_dados', 'documentos', 'relatorios']
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    print("✅ Pastas verificadas com sucesso!")

# ==================== CLASSES DE DADOS ====================

@dataclass
class Endereco:
    logradouro: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    uf: str
    cep: str

@dataclass
class Empresa:
    id: int
    cnpj: str
    razao_social: str
    nome_fantasia: str
    endereco: Endereco
    telefone: str
    email: str
    inscricao_estadual: str
    inscricao_municipal: str
    regime_tributario: str

@dataclass
class Sindicato:
    id: int
    nome: str
    cnpj: str
    endereco: Endereco
    telefone: str
    email: str
    aliquota_sindical: float
    valor_mensalidade: float

@dataclass
class Cargo:
    id: int
    nome: str
    descricao: str
    cbo: str
    salario_base: float
    comissao: float = 0.0
    adicional_insalubridade: float = 0.0
    adicional_periculosidade: float = 0.0

@dataclass
class BaseSalarial:
    id: int
    nome: str
    salario_minimo: float
    piso_salarial: float
    vale_refeicao: float
    vale_transporte: float
    plano_saude: float
    plano_odontologico: float

@dataclass
class Funcionario:
    id: int
    nome: str
    cpf: str
    rg: str
    data_nascimento: str
    endereco: Endereco
    telefone: str
    email: str
    empresa_id: int
    cargo_id: int
    sindicato_id: Optional[int]
    data_admissao: str
    data_demissao: Optional[str]
    salario: float
    base_salarial_id: int
    jornada_trabalho: str
    dependentes: int
    tipo_contrato: str
    vale_transporte_opcao: bool = True
    vale_refeicao_opcao: bool = True
    plano_saude_opcao: bool = False
    plano_odontologico_opcao: bool = False

@dataclass
class Dependente:
    id: int
    funcionario_id: int
    nome: str
    cpf: str
    data_nascimento: str
    parentesco: str

@dataclass
class FolhaPagamento:
    id: int
    funcionario_id: int
    competencia: str
    salario_base: float
    horas_extras: float = 0.0
    horas_extras_valor: float = 0.0
    adicional_noturno: float = 0.0
    comissao: float = 0.0
    dsr: float = 0.0
    adicional_insalubridade: float = 0.0
    adicional_periculosidade: float = 0.0
    vale_transporte: float = 0.0
    vale_refeicao: float = 0.0
    plano_saude: float = 0.0
    plano_odontologico: float = 0.0
    faltas: int = 0
    faltas_desconto: float = 0.0
    atrasos: int = 0
    atrasos_desconto: float = 0.0
    inss: float = 0.0
    irrf: float = 0.0
    fgts: float = 0.0
    pensao_alimenticia: float = 0.0
    outros_descontos: float = 0.0
    outros_proventos: float = 0.0
    salario_liquido: float = 0.0
    data_processamento: str = ""

@dataclass
class Rescisao:
    id: int
    funcionario_id: int
    data_rescisao: str
    data_aviso_previo: str
    tipo_rescisao: str
    aviso_previo_tipo: str
    saldo_salario: float = 0.0
    aviso_previo_valor: float = 0.0
    ferias_vencidas: float = 0.0
    ferias_proporcionais: float = 0.0
    ferias_vencidas_1_3: float = 0.0
    ferias_proporcionais_1_3: float = 0.0
    decimo_terceiro_proporcional: float = 0.0
    multa_fgts: float = 0.0
    fgts_rescisorio: float = 0.0
    indenizacao_adicional: float = 0.0
    outros_valores: float = 0.0
    inss: float = 0.0
    irrf: float = 0.0
    pensao_alimenticia: float = 0.0
    outros_descontos: float = 0.0
    valor_liquido: float = 0.0
    observacoes: str = ""

# ==================== SISTEMA DE ARMAZENAMENTO ====================

class Database:
    def __init__(self):
        self.data_dir = "folha_dados"
        criar_pastas_necessarias()
        
    def _get_file_path(self, collection):
        return os.path.join(self.data_dir, f"{collection}.json")
    
    def load(self, collection):
        try:
            file_path = self._get_file_path(collection)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"⚠️ Erro ao carregar {collection}: {e}")
            return []
    
    def save(self, collection, data):
        try:
            file_path = self._get_file_path(collection)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"⚠️ Erro ao salvar {collection}: {e}")
            return False

# ==================== SISTEMA PRINCIPAL ====================

class SistemaFolhaPagamento:
    def __init__(self):
        self.db = Database()
        self.next_id = {}
        self.carregar_ids()
    
    def carregar_ids(self):
        """Carrega os próximos IDs disponíveis"""
        collections = ['empresas', 'sindicatos', 'cargos', 'bases_salariais', 
                      'funcionarios', 'dependentes', 'folhas', 'rescisoes']
        
        for collection in collections:
            data = self.db.load(collection)
            if data:
                try:
                    max_id = max(item['id'] for item in data if 'id' in item)
                    self.next_id[collection] = max_id + 1
                except:
                    self.next_id[collection] = 1
            else:
                self.next_id[collection] = 1
    
    def obter_proximo_id(self, collection):
        """Obtém o próximo ID para uma coleção"""
        if collection not in self.next_id:
            self.next_id[collection] = 1
        id_atual = self.next_id[collection]
        self.next_id[collection] += 1
        return id_atual
    
    def input_com_voltar(self, mensagem, obrigatorio=False):
        """Input que permite voltar digitando '0'"""
        while True:
            valor = input(mensagem)
            if valor == '0':
                return None
            if obrigatorio and not valor.strip():
                print("❌ Campo obrigatório! Digite 0 para cancelar.")
                continue
            return valor
    
    def input_float(self, mensagem, obrigatorio=False):
        """Input para valores float com validação"""
        while True:
            valor = self.input_com_voltar(mensagem, obrigatorio)
            if valor is None:
                return None
            try:
                # Substitui vírgula por ponto e remove espaços
                valor_limpo = valor.replace(',', '.').strip()
                return float(valor_limpo)
            except:
                print("❌ Valor inválido! Digite um número (ex: 1500.50)")
    
    def input_int(self, mensagem, obrigatorio=False):
        """Input para valores int com validação"""
        while True:
            valor = self.input_com_voltar(mensagem, obrigatorio)
            if valor is None:
                return None
            try:
                return int(valor.strip())
            except:
                print("❌ Valor inválido! Digite um número inteiro")
    
    def input_data(self, mensagem, obrigatorio=False):
        """Input para datas com validação"""
        while True:
            valor = self.input_com_voltar(mensagem, obrigatorio)
            if valor is None:
                return None
            try:
                data = datetime.strptime(valor.strip(), "%d/%m/%Y")
                return data.strftime("%Y-%m-%d")
            except:
                print("❌ Data inválida! Use o formato DD/MM/AAAA")
    
    def input_boolean(self, mensagem):
        """Input para valores booleanos (S/N)"""
        while True:
            valor = input(mensagem).upper().strip()
            if valor == 'S':
                return True
            elif valor == 'N':
                return False
            else:
                print("❌ Digite S para Sim ou N para Não")
    
    # ========== CRUD EMPRESAS ==========
    def cadastrar_empresa(self):
        limpar_tela()
        print("\n" + "="*60)
        print("📋 CADASTRO DE EMPRESA")
        print("="*60)
        print("(Digite 0 a qualquer momento para cancelar)\n")
        
        try:
            # Coleta dados do endereço
            print("--- Endereço da Empresa ---")
            logradouro = self.input_com_voltar("Logradouro: ", True)
            if logradouro is None: return
            
            numero = self.input_com_voltar("Número: ", True)
            if numero is None: return
            
            complemento = self.input_com_voltar("Complemento: ", False) or ""
            
            bairro = self.input_com_voltar("Bairro: ", True)
            if bairro is None: return
            
            cidade = self.input_com_voltar("Cidade: ", True)
            if cidade is None: return
            
            uf = self.input_com_voltar("UF (sigla): ", True)
            if uf is None: return
            
            cep = self.input_com_voltar("CEP: ", True)
            if cep is None: return
            
            endereco = Endereco(
                logradouro=logradouro,
                numero=numero,
                complemento=complemento,
                bairro=bairro,
                cidade=cidade,
                uf=uf.upper(),
                cep=cep
            )
            
            print("\n--- Dados da Empresa ---")
            cnpj = self.input_com_voltar("CNPJ (apenas números): ", True)
            if cnpj is None: return
            
            razao_social = self.input_com_voltar("Razão Social: ", True)
            if razao_social is None: return
            
            nome_fantasia = self.input_com_voltar("Nome Fantasia: ", True)
            if nome_fantasia is None: return
            
            telefone = self.input_com_voltar("Telefone: ", True)
            if telefone is None: return
            
            email = self.input_com_voltar("Email: ", True)
            if email is None: return
            
            inscricao_estadual = self.input_com_voltar("Inscrição Estadual: ", True)
            if inscricao_estadual is None: return
            
            inscricao_municipal = self.input_com_voltar("Inscrição Municipal: ", True)
            if inscricao_municipal is None: return
            
            regime_tributario = self.input_com_voltar("Regime Tributário (Simples Nacional/Lucro Presumido/Lucro Real): ", True)
            if regime_tributario is None: return
            
            # Cria o objeto empresa
            empresa = Empresa(
                id=self.obter_proximo_id('empresas'),
                cnpj=cnpj,
                razao_social=razao_social,
                nome_fantasia=nome_fantasia,
                endereco=endereco,
                telefone=telefone,
                email=email,
                inscricao_estadual=inscricao_estadual,
                inscricao_municipal=inscricao_municipal,
                regime_tributario=regime_tributario
            )
            
            # Salva no banco de dados
            empresas = self.db.load('empresas')
            empresas.append(asdict(empresa))
            
            if self.db.save('empresas', empresas):
                print("\n" + "="*60)
                print("✅ EMPRESA CADASTRADA COM SUCESSO!")
                print("="*60)
                print(f"\nID da Empresa: {empresa.id}")
                print(f"Razão Social: {empresa.razao_social}")
                print(f"CNPJ: {empresa.cnpj}")
                print("\n" + "="*60)
            else:
                print("\n❌ Erro ao salvar empresa!")
                
        except Exception as e:
            print(f"\n❌ Erro durante o cadastro: {e}")
    
    def listar_empresas(self):
        limpar_tela()
        empresas = self.db.load('empresas')
        
        print("\n" + "="*60)
        print("📋 LISTA DE EMPRESAS CADASTRADAS")
        print("="*60)
        
        if not empresas:
            print("\n📭 Nenhuma empresa cadastrada.")
            print("\nUse a opção 1 do menu principal para cadastrar.")
        else:
            for i, emp in enumerate(empresas, 1):
                print(f"\n{i}. ID: {emp['id']}")
                print(f"   Razão Social: {emp['razao_social']}")
                print(f"   Nome Fantasia: {emp['nome_fantasia']}")
                print(f"   CNPJ: {emp['cnpj']}")
                print(f"   Cidade: {emp['endereco']['cidade']}/{emp['endereco']['uf']}")
                print(f"   Telefone: {emp['telefone']}")
                print("-"*40)
            
            print(f"\nTotal de empresas: {len(empresas)}")
        
        print("="*60)
    
    # ========== CRUD SINDICATOS ==========
    def cadastrar_sindicato(self):
        limpar_tela()
        print("\n" + "="*60)
        print("📋 CADASTRO DE SINDICATO")
        print("="*60)
        print("(Digite 0 a qualquer momento para cancelar)\n")
        
        try:
            print("--- Endereço do Sindicato ---")
            endereco = Endereco(
                logradouro=self.input_com_voltar("Logradouro: ", True),
                numero=self.input_com_voltar("Número: ", True),
                complemento=self.input_com_voltar("Complemento: ", False) or "",
                bairro=self.input_com_voltar("Bairro: ", True),
                cidade=self.input_com_voltar("Cidade: ", True),
                uf=self.input_com_voltar("UF: ", True),
                cep=self.input_com_voltar("CEP: ", True)
            )
            
            if None in [endereco.logradouro, endereco.numero, endereco.bairro, 
                       endereco.cidade, endereco.uf, endereco.cep]:
                print("\n❌ Operação cancelada.")
                return
            
            print("\n--- Dados do Sindicato ---")
            nome = self.input_com_voltar("Nome do Sindicato: ", True)
            if nome is None: return
            
            cnpj = self.input_com_voltar("CNPJ: ", True)
            if cnpj is None: return
            
            telefone = self.input_com_voltar("Telefone: ", True)
            if telefone is None: return
            
            email = self.input_com_voltar("Email: ", True)
            if email is None: return
            
            aliquota = self.input_float("Alíquota Sindical (%): ", True)
            if aliquota is None: return
            
            mensalidade = self.input_float("Valor da Mensalidade: R$ ", True)
            if mensalidade is None: return
            
            sindicato = Sindicato(
                id=self.obter_proximo_id('sindicatos'),
                nome=nome,
                cnpj=cnpj,
                endereco=endereco,
                telefone=telefone,
                email=email,
                aliquota_sindical=aliquota / 100,
                valor_mensalidade=mensalidade
            )
            
            sindicatos = self.db.load('sindicatos')
            sindicatos.append(asdict(sindicato))
            
            if self.db.save('sindicatos', sindicatos):
                print(f"\n✅ Sindicato cadastrado com sucesso! ID: {sindicato.id}")
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    def listar_sindicatos(self):
        limpar_tela()
        sindicatos = self.db.load('sindicatos')
        
        print("\n" + "="*60)
        print("📋 LISTA DE SINDICATOS")
        print("="*60)
        
        if not sindicatos:
            print("\n📭 Nenhum sindicato cadastrado.")
        else:
            for sind in sindicatos:
                print(f"\nID: {sind['id']}")
                print(f"Nome: {sind['nome']}")
                print(f"CNPJ: {sind['cnpj']}")
                print(f"Telefone: {sind['telefone']}")
                print(f"Cidade: {sind['endereco']['cidade']}")
                print(f"Alíquota: {sind['aliquota_sindical']*100:.1f}%")
                print(f"Mensalidade: R$ {sind['valor_mensalidade']:.2f}")
                print("-"*40)
        
        print("="*60)
    
    # ========== CRUD CARGOS ==========
    def cadastrar_cargo(self):
        limpar_tela()
        print("\n" + "="*60)
        print("📋 CADASTRO DE CARGO")
        print("="*60)
        print("(Digite 0 a qualquer momento para cancelar)\n")
        
        try:
            nome = self.input_com_voltar("Nome do Cargo: ", True)
            if nome is None: return
            
            descricao = self.input_com_voltar("Descrição: ", True)
            if descricao is None: return
            
            cbo = self.input_com_voltar("CBO: ", True)
            if cbo is None: return
            
            salario_base = self.input_float("Salário Base: R$ ", True)
            if salario_base is None: return
            
            comissao = self.input_float("Comissão (%): ", False) or 0
            
            insalubridade = self.input_float("Adicional de Insalubridade (%): ", False) or 0
            
            periculosidade = self.input_float("Adicional de Periculosidade (%): ", False) or 0
            
            cargo = Cargo(
                id=self.obter_proximo_id('cargos'),
                nome=nome,
                descricao=descricao,
                cbo=cbo,
                salario_base=salario_base,
                comissao=comissao,
                adicional_insalubridade=insalubridade,
                adicional_periculosidade=periculosidade
            )
            
            cargos = self.db.load('cargos')
            cargos.append(asdict(cargo))
            
            if self.db.save('cargos', cargos):
                print(f"\n✅ Cargo cadastrado com sucesso! ID: {cargo.id}")
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    def listar_cargos(self):
        limpar_tela()
        cargos = self.db.load('cargos')
        
        print("\n" + "="*60)
        print("📋 LISTA DE CARGOS")
        print("="*60)
        
        if not cargos:
            print("\n📭 Nenhum cargo cadastrado.")
        else:
            for cargo in cargos:
                print(f"\nID: {cargo['id']}")
                print(f"Nome: {cargo['nome']}")
                print(f"CBO: {cargo['cbo']}")
                print(f"Salário Base: R$ {cargo['salario_base']:.2f}")
                if cargo['comissao'] > 0:
                    print(f"Comissão: {cargo['comissao']}%")
                if cargo['adicional_insalubridade'] > 0:
                    print(f"Insalubridade: {cargo['adicional_insalubridade']}%")
                if cargo['adicional_periculosidade'] > 0:
                    print(f"Periculosidade: {cargo['adicional_periculosidade']}%")
                print("-"*40)
        
        print("="*60)
    
    # ========== CRUD BASES SALARIAIS ==========
    def cadastrar_base_salarial(self):
        limpar_tela()
        print("\n" + "="*60)
        print("📋 CADASTRO DE BASE SALARIAL")
        print("="*60)
        print("(Digite 0 a qualquer momento para cancelar)\n")
        
        try:
            nome = self.input_com_voltar("Nome da Base: ", True)
            if nome is None: return
            
            salario_minimo = self.input_float("Salário Mínimo: R$ ", True)
            if salario_minimo is None: return
            
            piso = self.input_float("Piso Salarial da Categoria: R$ ", True)
            if piso is None: return
            
            vale_refeicao = self.input_float("Vale Refeição (diário): R$ ", True)
            if vale_refeicao is None: return
            
            vale_transporte = self.input_float("Vale Transporte (diário): R$ ", True)
            if vale_transporte is None: return
            
            plano_saude = self.input_float("Plano de Saúde (mensal): R$ ", False) or 0
            
            plano_odonto = self.input_float("Plano Odontológico (mensal): R$ ", False) or 0
            
            base = BaseSalarial(
                id=self.obter_proximo_id('bases_salariais'),
                nome=nome,
                salario_minimo=salario_minimo,
                piso_salarial=piso,
                vale_refeicao=vale_refeicao,
                vale_transporte=vale_transporte,
                plano_saude=plano_saude,
                plano_odontologico=plano_odonto
            )
            
            bases = self.db.load('bases_salariais')
            bases.append(asdict(base))
            
            if self.db.save('bases_salariais', bases):
                print(f"\n✅ Base salarial cadastrada! ID: {base.id}")
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    def listar_bases(self):
        limpar_tela()
        bases = self.db.load('bases_salariais')
        
        print("\n" + "="*60)
        print("📋 LISTA DE BASES SALARIAIS")
        print("="*60)
        
        if not bases:
            print("\n📭 Nenhuma base salarial cadastrada.")
        else:
            for base in bases:
                print(f"\nID: {base['id']}")
                print(f"Nome: {base['nome']}")
                print(f"Salário Mínimo: R$ {base['salario_minimo']:.2f}")
                print(f"Piso Salarial: R$ {base['piso_salarial']:.2f}")
                print(f"Vale Refeição: R$ {base['vale_refeicao']:.2f}")
                print(f"Vale Transporte: R$ {base['vale_transporte']:.2f}")
                if base['plano_saude'] > 0:
                    print(f"Plano Saúde: R$ {base['plano_saude']:.2f}")
                if base['plano_odontologico'] > 0:
                    print(f"Plano Odonto: R$ {base['plano_odontologico']:.2f}")
                print("-"*40)
        
        print("="*60)

# ==================== MENUS ====================

def menu_cadastros(sistema):
    while True:
        limpar_tela()
        print("\n" + "="*60)
        print("📋 MENU DE CADASTROS")
        print("="*60)
        print("1 - Cadastrar Empresa")
        print("2 - Cadastrar Sindicato")
        print("3 - Cadastrar Cargo")
        print("4 - Cadastrar Base Salarial")
        print("5 - Cadastrar Funcionário (em breve)")
        print("0 - Voltar ao menu principal")
        print("-"*60)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            sistema.cadastrar_empresa()
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            sistema.cadastrar_sindicato()
            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            sistema.cadastrar_cargo()
            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            sistema.cadastrar_base_salarial()
            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")

def menu_listagens(sistema):
    while True:
        limpar_tela()
        print("\n" + "="*60)
        print("📋 LISTAGENS")
        print("="*60)
        print("1 - Listar Empresas")
        print("2 - Listar Sindicatos")
        print("3 - Listar Cargos")
        print("4 - Listar Bases Salariais")
        print("5 - Listar Funcionários (em breve)")
        print("0 - Voltar ao menu principal")
        print("-"*60)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            sistema.listar_empresas()
            input("\nPressione Enter para continuar...")
        elif opcao == '2':
            sistema.listar_sindicatos()
            input("\nPressione Enter para continuar...")
        elif opcao == '3':
            sistema.listar_cargos()
            input("\nPressione Enter para continuar...")
        elif opcao == '4':
            sistema.listar_bases()
            input("\nPressione Enter para continuar...")
        elif opcao == '5':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")

def menu_calculos(sistema):
    while True:
        limpar_tela()
        print("\n" + "="*60)
        print("🧮 CÁLCULOS")
        print("="*60)
        print("1 - Calcular Folha de Pagamento")
        print("2 - Calcular Rescisão")
        print("3 - Calcular 13º Salário")
        print("4 - Calcular Férias")
        print("0 - Voltar ao menu principal")
        print("-"*60)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '2':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '3':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '4':
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")

def menu_documentos(sistema):
    while True:
        limpar_tela()
        print("\n" + "="*60)
        print("📄 EMISSÃO DE DOCUMENTOS")
        print("="*60)
        print("1 - Ficha de Registro")
        print("2 - Contrato de Trabalho")
        print("3 - Declaração de Dependentes")
        print("4 - Declaração de Vale Transporte")
        print("5 - Termo de Rescisão")
        print("6 - Requerimento Seguro Desemprego")
        print("0 - Voltar ao menu principal")
        print("-"*60)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao in ['1','2','3','4','5','6']:
            print("\n🚧 Funcionalidade em desenvolvimento...")
            input("Pressione Enter para continuar...")
        elif opcao == '0':
            break
        else:
            print("\n❌ Opção inválida!")
            input("Pressione Enter para continuar...")

# ==================== PROGRAMA PRINCIPAL ====================

def main():
    try:
        # Configuração inicial
        criar_pastas_necessarias()
        sistema = SistemaFolhaPagamento()
        
        while True:
            limpar_tela()
            print("="*60)
            print("💰 SISTEMA DE FOLHA DE PAGAMENTO")
            print("   DEPARTAMENTO PESSOAL")
            print("="*60)
            print("\n1️⃣  - CADASTROS")
            print("2️⃣  - CÁLCULOS")
            print("3️⃣  - DOCUMENTOS")
            print("4️⃣  - LISTAGENS")
            print("0️⃣  - SAIR")
            print("-"*60)
            print(f"📊 Status: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            print("="*60)
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                menu_cadastros(sistema)
            elif opcao == '2':
                menu_calculos(sistema)
            elif opcao == '3':
                menu_documentos(sistema)
            elif opcao == '4':
                menu_listagens(sistema)
            elif opcao == '0':
                print("\n" + "="*60)
                print("👋 Obrigado por usar o sistema!")
                print("   Desenvolvido para Departamento Pessoal")
                print("="*60)
                input("\nPressione Enter para sair...")
                break
            else:
                print("\n❌ Opção inválida!")
                input("Pressione Enter para continuar...")
                
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrompido pelo usuário!")
        input("Pressione Enter para sair...")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        traceback.print_exc()
        input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()