"""
PATCH SIMPLIFICADO para game_logic.py
APENAS: Veterinário Obrigatório + Teto de Preço (SEM INFLAÇÃO)

⚠️  INSTRUÇÕES:
1. Adicione isto ao topo de game_logic.py (na seção de imports):
   - TETO_PRECO_CAVALOS
   - CUSTO_CONSULTA_VETERINARIA, CUSTO_CRUZAMENTO, CUSTO_TOTAL_CRUZAMENTO
   - VETERINARIO_SISTEMA

2. Adicione estes atributos à classe Jogo.__init__():
   - self.veterinario_contratado_semana = {}
   - self.consultas_veterinarias = 0

3. Substitua ou adicione estes métodos na classe Jogo:
   - pode_fazer_cruzamento()
   - fazer_cruzamento()
   - aplicar_teto_preco() ← IMPORTANTE!
"""

# ══════════════════════════════════════════════════════════════════════════════
#  1. ADICIONAR AOS IMPORTS (linha ~14)
# ══════════════════════════════════════════════════════════════════════════════

"""
from config import (NOMES, CORES, CORES_CRINA, RACAS, RACAS_LISTA, PRECO_CAVALOS,
                    VEL_BASE, STAMINA_BASE, MEDALHAS, EVENTOS_SEMANAIS,
                    PATROCINADORES_DISPONIVEIS, OPCOES_EMPRESTIMO,
                    CAMP_N_CORRIDAS, CAMP_PONTOS, CAMP_PREMIO_CORRIDA,
                    CAMP_PREMIO_FINAL, CAMP_NOME_NPC, gerar_id, PRECO_BAIA,
                    ESTRELAS_VEL, PRECO_MAX_ESTRELA, PRECO_MIN_ESTRELA,
                    VEL_MAX_GLOBAL, COMPETICOES,
                    HARAS_TIPOS, HARAS_NIVEL_BAIAS, HARAS_BAIAS_GRATIS,
                    CUSTO_MANUTENCAO_BASE, MAX_PATROCINADORES_TEMPORADA,
                    CAVALOS_LENDARIOS, LEILAO_INTERVALO_SEMANAS,
                    LEILAO_DURACAO_SEMANAS, LEILAO_N_LOTES, LEILAO_ESTRELA_MIN,
                    LEILAO_LANCE_INICIAL_PCT, LEILAO_INCREMENTO_PCT,
                    LEILAO_MAX_LANCES,
                    # ← ADICIONE ESTAS LINHAS:
                    TETO_PRECO_CAVALOS,
                    CUSTO_CONSULTA_VETERINARIA, CUSTO_CRUZAMENTO, 
                    CUSTO_TOTAL_CRUZAMENTO, VETERINARIO_SISTEMA)
"""

# ══════════════════════════════════════════════════════════════════════════════
#  2. ADICIONAR À CLASSE JOGO.__init__() (após linha ~312)
# ══════════════════════════════════════════════════════════════════════════════

"""
        self.semana_ultimo_leilao = 0
        
        # ← ADICIONE ESTAS LINHAS:
        # Sistema de veterinário para cruzamento
        self.veterinario_contratado_semana = {}
        self.consultas_veterinarias = 0
"""

# ══════════════════════════════════════════════════════════════════════════════
#  3. ADICIONAR ESTES MÉTODOS À CLASSE JOGO
# ══════════════════════════════════════════════════════════════════════════════

class JogoMethods:
    """Métodos para adicionar à classe Jogo"""

    def aplicar_teto_preco(self, cavalo):
        """
        Aplica teto de preço baseado nas estrelas do cavalo.
        Cavalos lendários ignoram o teto.
        """
        # Se é lendário, ignora teto
        if getattr(cavalo, 'lendario', False):
            return cavalo.preco  # Mantém preço original
        
        # Obter número de estrelas
        from game_logic import estrelas
        num_estrelas = estrelas(cavalo.vel_base)
        
        # Obter teto para essa estrela
        teto = TETO_PRECO_CAVALOS.get(str(num_estrelas), 50_000)
        
        # Aplicar teto (não pode ser maior)
        preco_final = min(cavalo.preco, teto)
        
        return preco_final

    def pode_fazer_cruzamento(self):
        """Verifica se o jogador pode fazer um cruzamento (tem dinheiro e veterinário)."""
        custo = CUSTO_TOTAL_CRUZAMENTO
        
        if self.dinheiro < custo:
            return False, f"❌ Você precisa de R${custo:,} para o cruzamento!\n\n🏥 Consulta Veterinária: R${CUSTO_CONSULTA_VETERINARIA:,}\n⚙️  Cruzamento: R${CUSTO_CRUZAMENTO:,}"
        
        return True, "✅ Você pode fazer o cruzamento!"

    def fazer_cruzamento(self, pai, mae, nome_filhote, cor_filhote, raca_filhote):
        """
        Faz um cruzamento OBRIGATORIAMENTE com veterinário.
        
        Parâmetros:
        - pai: Cavalo macho
        - mae: Cavalo fêmea
        - nome_filhote: Nome do potro
        - cor_filhote: Cor do potro
        - raca_filhote: Raça do potro
        
        Retorna: (sucesso, mensagem)
        """
        
        # Verificar custo
        custo = CUSTO_TOTAL_CRUZAMENTO
        if self.dinheiro < custo:
            return False, f"❌ Dinheiro insuficiente!\nPrecisa de R${custo:,}, você tem R${self.dinheiro:,}"
        
        # Verificar se fêmea não está grávida
        if mae.em_gestacao():
            return False, f"❌ {mae.nome} já está grávida!\nEspere dar à luz primeiro."
        
        # Verificar sexo
        if not hasattr(mae, 'sexo') or mae.sexo != 'F':
            return False, f"❌ {mae.nome} não é uma fêmea!"
        if not hasattr(pai, 'sexo') or pai.sexo != 'M':
            return False, f"❌ {pai.nome} não é um macho!"
        
        # ✅ COBRAR CUSTOS
        self.dinheiro -= custo
        self.consultas_veterinarias += 1
        
        # ✅ FAZER CRUZAMENTO
        mae.gestacao_semana = self.semana
        mae.filho_pendente = {
            'nome': nome_filhote,
            'cor': cor_filhote,
            'raca': raca_filhote,
            'pai': pai,
            'mae': mae,
        }
        
        # Adicionar ao histórico
        self.historico.append({
            'semana': self.semana,
            'tipo': 'cruzamento',
            'pai': pai.nome,
            'mae': mae.nome,
            'filhote': nome_filhote,
            'custo': custo
        })
        
        mensagem = f"""
✅ CRUZAMENTO BEM-SUCEDIDO!

🏥 Consulta Veterinária Realizada
   Custo: R${CUSTO_CONSULTA_VETERINARIA:,}

👨 Pai: {pai.nome} ({pai.raca})
👩 Mãe: {mae.nome} ({mae.raca})

🐴 Filhote: {nome_filhote} ({raca_filhote})
⏱️  Nascerá em 8 semanas!

💰 Custo Total: R${custo:,}
💾 Saldo: R${self.dinheiro:,}

⚠️  {mae.nome} não pode correr enquanto grávida!
"""
        
        return True, mensagem

    def calcular_preco_com_teto(self, cavalo):
        """
        Calcula o preço final do cavalo aplicando o teto de preço.
        Usa para mostrar preço correto no mercado.
        """
        return self.aplicar_teto_preco(cavalo)
