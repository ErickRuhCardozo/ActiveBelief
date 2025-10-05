import numpy as np
import matplotlib.pyplot as plt

# 1. Definição do Agente com uma Crença Central
class AgenteCrenca:
    def __init__(self, crenca_inicial, viabilidade_crenca=0.5):
        # Crença é um valor entre 0.0 (Ceticismo Total) e 1.0 (Convicção Total)
        self.crenca = crenca_inicial
        # A 'viabilidade' representa o quão facilmente a crença pode ser alterada.
        # Um valor mais alto significa mais teimosia (viés mais forte).
        self.viabilidade = viabilidade_crenca
        self.historico_crenca = [crenca_inicial]

    def processar_realidade(self, informacao_bruta):
        """
        Simula o Viés de Confirmação: A Crença distorce a informação bruta.
        """
        # A informação é "filtrada" pela Crença. 
        # A distorção é maior quanto mais forte for a crença (self.crenca).
        
        # O Viés de Confirmação amplifica a informação que está alinhada à Crença
        # e atenua a informação que a contradiz.
        distorcao = (informacao_bruta - 0.5) * self.crenca  # 0.5 é o ponto neutro
        
        informacao_percebida = informacao_bruta + distorcao
        
        # Limita o valor percebido entre 0 e 1
        informacao_percebida = np.clip(informacao_percebida, 0.0, 1.0)
        
        return informacao_percebida

    def atualizar_crenca(self, informacao_percebida):
        """
        A informação Percebida (viés) atualiza a Crença para o próximo passo.
        """
        # A crença se move em direção à informação percebida, mas a "viabilidade" 
        # (teimosia) impede que a mudança seja total de uma vez.
        delta = informacao_percebida - self.crenca
        
        # A atualização é suavizada pela 'viabilidade' (quanto menor, mais suave a mudança)
        nova_crenca = self.crenca + delta * (1 - self.viabilidade)
        
        self.crenca = np.clip(nova_crenca, 0.0, 1.0)
        self.historico_crenca.append(self.crenca)


# 2. Simulação do Sistema
def simular_crenca_atuante(agente, passos):
    # Geramos uma "Realidade Neutra" (aleatória)
    informacao_bruta = np.random.rand(passos) 
    
    for i in range(passos):
        # 1. A Crença (output passado) age como INPUT no processamento da Realidade
        percepcao = agente.processar_realidade(informacao_bruta[i])
        
        # 2. O resultado (percepção) se torna o INPUT para atualizar a Crença
        agente.atualizar_crenca(percepcao)
        
    return informacao_bruta

# 3. Execução e Visualização

# Agente 1: Crença Forte (Ex: "O mundo é perigoso")
agente1 = AgenteCrenca(crenca_inicial=0.8, viabilidade_crenca=0.2) 

# Agente 2: Crença Neutra/Fraca (Ex: "O mundo é equilibrado")
agente2 = AgenteCrenca(crenca_inicial=0.5, viabilidade_crenca=0.5)

passos = 100
realidade = simular_crenca_atuante(agente1, passos)
simular_crenca_atuante(agente2, passos)


# Plotagem dos resultados
plt.figure(figsize=(12, 6))
plt.plot(agente1.historico_crenca, label=f'Agente 1 (Crença Inicial: {agente1.historico_crenca[0]:.1f}, Viés Forte)', linewidth=2)
plt.plot(agente2.historico_crenca, label=f'Agente 2 (Crença Inicial: {agente2.historico_crenca[0]:.1f}, Viés Neutro)', linestyle='--', alpha=0.7)
plt.axhline(0.5, color='gray', linestyle=':', label='Realidade Neutra (Média)')

plt.title('A Crença (Output Passado) Agindo como Filtro (Input Atual)')
plt.xlabel('Passos de Interação com a Realidade')
plt.ylabel('Força da Crença (0.0 a 1.0)')
plt.legend()
plt.grid(True, alpha=0.5)
plt.show()
