"""
Testes de Auditoria Contábil
Audiper - Sistema de Auditoria Digital

Testes implementados:
- Saldos Invertidos (Ativo Credor / Passivo Devedor)

Arquitetura JSON-first: todos os testes retornam List[Dict] para flexibilidade no frontend.
"""

import polars as pl
from typing import List, Dict, Any, Tuple
from enum import Enum


class Severidade(Enum):
    """Níveis de severidade dos achados"""
    CRITICO = "CRÍTICO"
    ATENCAO = "ATENÇÃO"
    INFO = "INFO"
    OK = "OK"


def get_cor_severidade(severidade: str) -> str:
    """Retorna cor para exibição baseado na severidade"""
    cores = {
        "CRÍTICO": "#DC2626",   # Vermelho
        "ATENÇÃO": "#F59E0B",   # Amarelo
        "INFO": "#3B82F6",      # Azul
        "OK": "#10B981",        # Verde
    }
    return cores.get(severidade, "#6B7280")


def get_emoji_severidade(severidade: str) -> str:
    """Retorna emoji para exibição"""
    emojis = {
        "CRÍTICO": "🔴",
        "ATENÇÃO": "🟡",
        "INFO": "🔵",
        "OK": "🟢",
    }
    return emojis.get(severidade, "⚪")


def teste_saldos_invertidos(df_saldos: pl.DataFrame) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    TESTE: Saldos com Natureza Invertida
    
    Regras:
    - ATIVO deve ter saldo DEVEDOR (D)
    - PASSIVO deve ter saldo CREDOR (C)
    - PL deve ter saldo CREDOR (C)
    - RECEITAS deve ter saldo CREDOR (C)
    - DESPESAS deve ter saldo DEVEDOR (D)
    
    Exceções (contas retificadoras):
    - Depreciação, Amortização, Exaustão
    - Provisões (PDD, etc)
    - Prejuízos Acumulados
    
    Returns:
        Tupla com (lista de achados em JSON, estatísticas)
    """
    
    if df_saldos.is_empty():
        return [], {"total": 0, "criticos": 0, "atencao": 0, "info": 0}
    
    # Filtrar apenas contas analíticas com saldo
    df_analiticas = df_saldos.filter(
        (pl.col("tipo_conta") == "A") & 
        (pl.col("saldo_final") != 0)
    )
    
    if df_analiticas.is_empty():
        return [], {"total": 0, "criticos": 0, "atencao": 0, "info": 0}
    
    # Definir saldo esperado por natureza
    saldo_esperado = {
        "ATIVO": "D",
        "PASSIVO": "C",
        "PATRIMÔNIO LÍQUIDO": "C",
        "RESULTADO": None,  # Depende se é receita ou despesa
        "COMPENSAÇÃO": None,
        "OUTRAS": None,
    }
    
    # Termos que identificam contas retificadoras
    termos_retificadoras = [
        "DEPRECIA", "AMORTIZA", "EXAUST", "PROVISÃO", "PERDAS",
        "(-)", "RETIFICADORA", "DEVEDORES DUVIDOSOS", "PREJUÍZO",
        "AJUSTE", "REDUÇÃO"
    ]
    
    achados: List[Dict[str, Any]] = []
    
    # Converter para Python dict para iteração
    registros = df_analiticas.to_dicts()
    
    for idx, row in enumerate(registros):
        natureza = row.get("natureza", "N/A")
        saldo_fin = row.get("ind_saldo_fin", "")
        valor_saldo = row.get("saldo_final", 0)
        descricao = (row.get("descricao") or "").upper()
        cod_conta = row.get("cod_conta", "")
        
        # Verificar se é conta retificadora
        eh_retificadora = any(termo in descricao for termo in termos_retificadoras)
        
        # Obter saldo esperado
        esperado = saldo_esperado.get(natureza)
        
        # Se não há expectativa definida, pular
        if esperado is None:
            continue
            
        # Verificar se há inversão
        if saldo_fin and saldo_fin != esperado:
            # Retificadoras são exceção conhecida
            if eh_retificadora:
                continue
            
            # Determinar severidade e mensagem
            if natureza == "ATIVO" and saldo_fin == "C":
                severidade = Severidade.CRITICO.value
                achado_msg = "Conta do ATIVO com saldo CREDOR"
                recomendacao = "Verificar se há erro de classificação ou lançamento incorreto. Pode indicar pagamento a maior ou estorno indevido."
                
            elif natureza == "PASSIVO" and saldo_fin == "D":
                severidade = Severidade.CRITICO.value
                achado_msg = "Conta do PASSIVO com saldo DEVEDOR"
                recomendacao = "Possível pagamento a maior, adiantamento não classificado ou erro de lançamento."
                
            elif natureza == "PATRIMÔNIO LÍQUIDO" and saldo_fin == "D":
                severidade = Severidade.ATENCAO.value
                achado_msg = "Conta do PL com saldo DEVEDOR"
                recomendacao = "Verificar se é Prejuízo Acumulado (normal) ou erro de classificação."
                
            else:
                severidade = Severidade.INFO.value
                achado_msg = "Saldo em natureza não usual"
                recomendacao = "Analisar razão contábil para verificar origem."
            
            achados.append({
                "id": str(idx + 1),
                "cod_conta": cod_conta,
                "descricao": row.get("descricao", "N/A"),
                "natureza": natureza,
                "saldo_esperado": "Devedor" if esperado == "D" else "Credor",
                "saldo_encontrado": "Devedor" if saldo_fin == "D" else "Credor",
                "valor": valor_saldo,
                "valor_formatado": formatar_moeda(valor_saldo),
                "severidade": severidade,
                "emoji": get_emoji_severidade(severidade),
                "cor": get_cor_severidade(severidade),
                "achado": achado_msg,
                "recomendacao": recomendacao,
            })
    
    # Estatísticas
    stats = {
        "total": len(achados),
        "criticos": len([a for a in achados if a["severidade"] == "CRÍTICO"]),
        "atencao": len([a for a in achados if a["severidade"] == "ATENÇÃO"]),
        "info": len([a for a in achados if a["severidade"] == "INFO"]),
    }
    
    return achados, stats


def formatar_moeda(valor: float) -> str:
    """Formata valor para moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_resumo_balancete(df_saldos: pl.DataFrame) -> Dict[str, Any]:
    """
    Gera resumo estatístico do balancete para o dashboard.
    
    Returns:
        Dict com totais por natureza e métricas gerais
    """
    
    if df_saldos.is_empty():
        return {
            "total_contas": 0,
            "contas_analiticas": 0,
            "por_natureza": {},
        }
    
    # Filtrar analíticas
    df_analiticas = df_saldos.filter(pl.col("tipo_conta") == "A")
    
    # Agrupar por natureza
    resumo_natureza = {}
    
    naturezas = ["ATIVO", "PASSIVO", "PATRIMÔNIO LÍQUIDO", "RESULTADO"]
    
    for nat in naturezas:
        df_nat = df_analiticas.filter(pl.col("natureza") == nat)
        
        if not df_nat.is_empty():
            # Somar valores considerando D como positivo e C como negativo para o total
            total = df_nat.select(pl.col("saldo_final").sum()).item()
            qtd = df_nat.height
            
            resumo_natureza[nat] = {
                "quantidade": qtd,
                "total": total,
                "total_formatado": formatar_moeda(abs(total)),
            }
    
    return {
        "total_contas": df_saldos.height,
        "contas_analiticas": df_analiticas.height,
        "por_natureza": resumo_natureza,
    }
