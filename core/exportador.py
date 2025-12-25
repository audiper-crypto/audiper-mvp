"""
Exportador de Relatórios
Audiper - Sistema de Auditoria Digital

Gera arquivos Excel formatados com os resultados da auditoria.
"""

import polars as pl
from typing import List, Dict, Any, Optional
from io import BytesIO
from datetime import datetime


def exportar_achados_excel(
    achados: List[Dict[str, Any]],
    empresa_nome: str = "N/A",
    teste_nome: str = "Saldos Invertidos"
) -> BytesIO:
    """
    Exporta lista de achados para Excel formatado.
    
    Args:
        achados: Lista de dicionários com os achados
        empresa_nome: Nome da empresa auditada
        teste_nome: Nome do teste realizado
        
    Returns:
        BytesIO com o arquivo Excel
    """
    
    # Criar DataFrame para exportação
    if not achados:
        df_export = pl.DataFrame({
            "Mensagem": ["Nenhum achado encontrado neste teste."]
        })
    else:
        # Selecionar e renomear colunas para o relatório
        df_export = pl.DataFrame(achados).select([
            pl.col("cod_conta").alias("Código da Conta"),
            pl.col("descricao").alias("Descrição"),
            pl.col("natureza").alias("Natureza"),
            pl.col("saldo_esperado").alias("Saldo Esperado"),
            pl.col("saldo_encontrado").alias("Saldo Encontrado"),
            pl.col("valor").alias("Valor (R$)"),
            pl.col("severidade").alias("Severidade"),
            pl.col("achado").alias("Achado"),
            pl.col("recomendacao").alias("Recomendação"),
        ])
    
    # Exportar para Excel
    buffer = BytesIO()
    df_export.write_excel(
        buffer,
        worksheet="Achados",
        autofit=True,
    )
    buffer.seek(0)
    
    return buffer


def exportar_relatorio_completo(
    achados: List[Dict[str, Any]],
    df_saldos: pl.DataFrame,
    empresa_nome: str = "N/A",
    periodo: str = "N/A"
) -> BytesIO:
    """
    Exporta relatório completo com múltiplas abas:
    - Resumo
    - Achados
    - Balancete Completo
    
    Args:
        achados: Lista de achados encontrados
        df_saldos: DataFrame com todos os saldos
        empresa_nome: Nome da empresa
        periodo: Período de referência
        
    Returns:
        BytesIO com arquivo Excel
    """
    
    buffer = BytesIO()
    
    # Usar xlsxwriter via polars para múltiplas abas
    with pl.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        
        # Aba 1: Resumo
        resumo_data = {
            "Campo": [
                "Empresa",
                "Período",
                "Data da Auditoria",
                "Teste Realizado",
                "Total de Achados",
                "Críticos",
                "Atenção",
                "Informativos"
            ],
            "Valor": [
                empresa_nome,
                periodo,
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Saldos Invertidos",
                str(len(achados)),
                str(len([a for a in achados if a.get("severidade") == "CRÍTICO"])),
                str(len([a for a in achados if a.get("severidade") == "ATENÇÃO"])),
                str(len([a for a in achados if a.get("severidade") == "INFO"])),
            ]
        }
        df_resumo = pl.DataFrame(resumo_data)
        df_resumo.write_excel(
            writer,
            worksheet="Resumo",
            autofit=True,
        )
        
        # Aba 2: Achados
        if achados:
            df_achados = pl.DataFrame(achados).select([
                pl.col("cod_conta").alias("Conta"),
                pl.col("descricao").alias("Descrição"),
                pl.col("natureza").alias("Natureza"),
                pl.col("saldo_esperado").alias("Esperado"),
                pl.col("saldo_encontrado").alias("Encontrado"),
                pl.col("valor").alias("Valor"),
                pl.col("severidade").alias("Severidade"),
                pl.col("achado").alias("Achado"),
                pl.col("recomendacao").alias("Recomendação"),
            ])
        else:
            df_achados = pl.DataFrame({"Resultado": ["Nenhum achado encontrado"]})
        
        df_achados.write_excel(
            writer,
            worksheet="Achados",
            autofit=True,
        )
        
        # Aba 3: Balancete (se disponível)
        if not df_saldos.is_empty():
            df_balancete = df_saldos.select([
                pl.col("cod_conta").alias("Conta"),
                pl.col("descricao").alias("Descrição"),
                pl.col("natureza").alias("Natureza"),
                pl.col("saldo_inicial").alias("Saldo Inicial"),
                pl.col("valor_debito").alias("Débitos"),
                pl.col("valor_credito").alias("Créditos"),
                pl.col("saldo_final").alias("Saldo Final"),
                pl.col("ind_saldo_fin").alias("D/C"),
            ])
            
            df_balancete.write_excel(
                writer,
                worksheet="Balancete",
                autofit=True,
            )
    
    buffer.seek(0)
    return buffer
