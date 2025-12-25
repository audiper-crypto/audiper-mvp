"""
Gerador de Dados de Demonstração
Audiper - Sistema de Auditoria Digital

Gera dados fictícios para demonstração do sistema quando
não há arquivo SPED real disponível.
"""

import polars as pl
from typing import Tuple
from core.leitor_sped import DadosEmpresa


def gerar_dados_demonstracao() -> Tuple[DadosEmpresa, pl.DataFrame, pl.DataFrame]:
    """
    Gera dados fictícios com anomalias propositais para demonstrar o sistema.
    
    Returns:
        Tupla com (DadosEmpresa, DataFrame Plano, DataFrame Saldos)
    """
    
    # Dados da empresa fictícia
    empresa = DadosEmpresa(
        nome="MEGA TELEINFORMÁTICA LTDA",
        cnpj="12.345.678/0001-90",
        uf="PI",
        data_inicio="01/01/2024",
        data_fim="31/12/2024"
    )
    
    # Plano de Contas completo
    plano_contas_data = [
        # ATIVO
        {"cod_conta": "1", "descricao": "ATIVO", "cod_natureza": "01", "tipo_conta": "S", "nivel": "1", "natureza": "ATIVO", "conta_superior": ""},
        {"cod_conta": "1.1", "descricao": "ATIVO CIRCULANTE", "cod_natureza": "01", "tipo_conta": "S", "nivel": "2", "natureza": "ATIVO", "conta_superior": "1"},
        {"cod_conta": "1.1.01", "descricao": "DISPONIBILIDADES", "cod_natureza": "01", "tipo_conta": "S", "nivel": "3", "natureza": "ATIVO", "conta_superior": "1.1"},
        {"cod_conta": "1.1.01.001", "descricao": "Caixa Geral", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.01"},
        {"cod_conta": "1.1.01.002", "descricao": "Banco Bradesco C/C 1234-5", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.01"},
        {"cod_conta": "1.1.01.003", "descricao": "Banco Itaú C/C 9876-0", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.01"},
        {"cod_conta": "1.1.02", "descricao": "CLIENTES", "cod_natureza": "01", "tipo_conta": "S", "nivel": "3", "natureza": "ATIVO", "conta_superior": "1.1"},
        {"cod_conta": "1.1.02.001", "descricao": "Duplicatas a Receber", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.02"},
        {"cod_conta": "1.1.02.002", "descricao": "(-) Provisão p/ Devedores Duvidosos", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.02"},
        {"cod_conta": "1.1.03", "descricao": "ESTOQUES", "cod_natureza": "01", "tipo_conta": "S", "nivel": "3", "natureza": "ATIVO", "conta_superior": "1.1"},
        {"cod_conta": "1.1.03.001", "descricao": "Mercadorias para Revenda", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.1.03"},
        {"cod_conta": "1.2", "descricao": "ATIVO NÃO CIRCULANTE", "cod_natureza": "01", "tipo_conta": "S", "nivel": "2", "natureza": "ATIVO", "conta_superior": "1"},
        {"cod_conta": "1.2.01", "descricao": "IMOBILIZADO", "cod_natureza": "01", "tipo_conta": "S", "nivel": "3", "natureza": "ATIVO", "conta_superior": "1.2"},
        {"cod_conta": "1.2.01.001", "descricao": "Veículos", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.2.01"},
        {"cod_conta": "1.2.01.002", "descricao": "(-) Depreciação Acumulada Veículos", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.2.01"},
        {"cod_conta": "1.2.01.003", "descricao": "Móveis e Utensílios", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.2.01"},
        {"cod_conta": "1.2.01.004", "descricao": "Equipamentos de Informática", "cod_natureza": "01", "tipo_conta": "A", "nivel": "4", "natureza": "ATIVO", "conta_superior": "1.2.01"},
        
        # PASSIVO
        {"cod_conta": "2", "descricao": "PASSIVO", "cod_natureza": "02", "tipo_conta": "S", "nivel": "1", "natureza": "PASSIVO", "conta_superior": ""},
        {"cod_conta": "2.1", "descricao": "PASSIVO CIRCULANTE", "cod_natureza": "02", "tipo_conta": "S", "nivel": "2", "natureza": "PASSIVO", "conta_superior": "2"},
        {"cod_conta": "2.1.01", "descricao": "FORNECEDORES", "cod_natureza": "02", "tipo_conta": "S", "nivel": "3", "natureza": "PASSIVO", "conta_superior": "2.1"},
        {"cod_conta": "2.1.01.001", "descricao": "Fornecedores Nacionais", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.01"},
        {"cod_conta": "2.1.02", "descricao": "OBRIGAÇÕES TRABALHISTAS", "cod_natureza": "02", "tipo_conta": "S", "nivel": "3", "natureza": "PASSIVO", "conta_superior": "2.1"},
        {"cod_conta": "2.1.02.001", "descricao": "Salários a Pagar", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.02"},
        {"cod_conta": "2.1.02.002", "descricao": "FGTS a Recolher", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.02"},
        {"cod_conta": "2.1.02.003", "descricao": "INSS a Recolher", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.02"},
        {"cod_conta": "2.1.03", "descricao": "OBRIGAÇÕES FISCAIS", "cod_natureza": "02", "tipo_conta": "S", "nivel": "3", "natureza": "PASSIVO", "conta_superior": "2.1"},
        {"cod_conta": "2.1.03.001", "descricao": "ICMS a Recolher", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.03"},
        {"cod_conta": "2.1.03.002", "descricao": "PIS a Recolher", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.03"},
        {"cod_conta": "2.1.03.003", "descricao": "COFINS a Recolher", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.1.03"},
        {"cod_conta": "2.2", "descricao": "PASSIVO NÃO CIRCULANTE", "cod_natureza": "02", "tipo_conta": "S", "nivel": "2", "natureza": "PASSIVO", "conta_superior": "2"},
        {"cod_conta": "2.2.01", "descricao": "EMPRÉSTIMOS E FINANCIAMENTOS", "cod_natureza": "02", "tipo_conta": "S", "nivel": "3", "natureza": "PASSIVO", "conta_superior": "2.2"},
        {"cod_conta": "2.2.01.001", "descricao": "Financiamento Veículo - Bradesco", "cod_natureza": "02", "tipo_conta": "A", "nivel": "4", "natureza": "PASSIVO", "conta_superior": "2.2.01"},
        
        # PATRIMÔNIO LÍQUIDO
        {"cod_conta": "3", "descricao": "PATRIMÔNIO LÍQUIDO", "cod_natureza": "03", "tipo_conta": "S", "nivel": "1", "natureza": "PATRIMÔNIO LÍQUIDO", "conta_superior": ""},
        {"cod_conta": "3.1", "descricao": "CAPITAL SOCIAL", "cod_natureza": "03", "tipo_conta": "S", "nivel": "2", "natureza": "PATRIMÔNIO LÍQUIDO", "conta_superior": "3"},
        {"cod_conta": "3.1.01", "descricao": "Capital Social Integralizado", "cod_natureza": "03", "tipo_conta": "A", "nivel": "3", "natureza": "PATRIMÔNIO LÍQUIDO", "conta_superior": "3.1"},
        {"cod_conta": "3.2", "descricao": "RESERVAS E LUCROS", "cod_natureza": "03", "tipo_conta": "S", "nivel": "2", "natureza": "PATRIMÔNIO LÍQUIDO", "conta_superior": "3"},
        {"cod_conta": "3.2.01", "descricao": "Lucros Acumulados", "cod_natureza": "03", "tipo_conta": "A", "nivel": "3", "natureza": "PATRIMÔNIO LÍQUIDO", "conta_superior": "3.2"},
        
        # RESULTADO
        {"cod_conta": "4", "descricao": "RECEITAS", "cod_natureza": "04", "tipo_conta": "S", "nivel": "1", "natureza": "RESULTADO", "conta_superior": ""},
        {"cod_conta": "4.1", "descricao": "RECEITA OPERACIONAL", "cod_natureza": "04", "tipo_conta": "S", "nivel": "2", "natureza": "RESULTADO", "conta_superior": "4"},
        {"cod_conta": "4.1.01", "descricao": "Receita de Venda de Mercadorias", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "4.1"},
        {"cod_conta": "4.1.02", "descricao": "Receita de Prestação de Serviços", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "4.1"},
        {"cod_conta": "5", "descricao": "CUSTOS E DESPESAS", "cod_natureza": "04", "tipo_conta": "S", "nivel": "1", "natureza": "RESULTADO", "conta_superior": ""},
        {"cod_conta": "5.1", "descricao": "CUSTOS", "cod_natureza": "04", "tipo_conta": "S", "nivel": "2", "natureza": "RESULTADO", "conta_superior": "5"},
        {"cod_conta": "5.1.01", "descricao": "CMV - Custo das Mercadorias Vendidas", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "5.1"},
        {"cod_conta": "5.2", "descricao": "DESPESAS OPERACIONAIS", "cod_natureza": "04", "tipo_conta": "S", "nivel": "2", "natureza": "RESULTADO", "conta_superior": "5"},
        {"cod_conta": "5.2.01", "descricao": "Despesas com Pessoal", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "5.2"},
        {"cod_conta": "5.2.02", "descricao": "Despesas Administrativas", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "5.2"},
        {"cod_conta": "5.2.03", "descricao": "Despesas com Depreciação", "cod_natureza": "04", "tipo_conta": "A", "nivel": "3", "natureza": "RESULTADO", "conta_superior": "5.2"},
    ]
    
    # Saldos com ANOMALIAS PROPOSITAIS para demonstrar o sistema
    saldos_data = [
        # ===== CONTAS NORMAIS =====
        {"cod_conta": "1.1.01.001", "saldo_final": 15000.00, "ind_saldo_fin": "D", "valor_debito": 50000.00, "valor_credito": 35000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.1.01.002", "saldo_final": 85000.00, "ind_saldo_fin": "D", "valor_debito": 200000.00, "valor_credito": 115000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.1.01.003", "saldo_final": 42000.00, "ind_saldo_fin": "D", "valor_debito": 150000.00, "valor_credito": 108000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.1.02.001", "saldo_final": 120000.00, "ind_saldo_fin": "D", "valor_debito": 300000.00, "valor_credito": 180000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.1.02.002", "saldo_final": 6000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 6000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},  # PDD - Retificadora (OK ser credor)
        {"cod_conta": "1.1.03.001", "saldo_final": 75000.00, "ind_saldo_fin": "D", "valor_debito": 180000.00, "valor_credito": 105000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.2.01.001", "saldo_final": 95000.00, "ind_saldo_fin": "D", "valor_debito": 95000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "1.2.01.002", "saldo_final": 19000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 19000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},  # Depreciação (OK ser credor)
        {"cod_conta": "1.2.01.003", "saldo_final": 25000.00, "ind_saldo_fin": "D", "valor_debito": 25000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        
        # ⚠️ ANOMALIA 1: Equipamentos de Informática com saldo CREDOR
        # Isso pode indicar venda sem baixa correta ou erro de lançamento
        {"cod_conta": "1.2.01.004", "saldo_final": 8500.00, "ind_saldo_fin": "C", "valor_debito": 15000.00, "valor_credito": 23500.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        
        # Passivo NORMAL
        {"cod_conta": "2.1.01.001", "saldo_final": 45000.00, "ind_saldo_fin": "C", "valor_debito": 30000.00, "valor_credito": 75000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "2.1.02.001", "saldo_final": 12000.00, "ind_saldo_fin": "C", "valor_debito": 144000.00, "valor_credito": 156000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        # ⚠️ ANOMALIA 2: FGTS com saldo DEVEDOR
        # Pode indicar recolhimento a maior ou erro no lançamento da provisão
        {"cod_conta": "2.1.02.002", "saldo_final": 3500.00, "ind_saldo_fin": "D", "valor_debito": 15000.00, "valor_credito": 11500.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        {"cod_conta": "2.1.02.003", "saldo_final": 8000.00, "ind_saldo_fin": "C", "valor_debito": 96000.00, "valor_credito": 104000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        # ⚠️ ANOMALIA 3: ICMS com saldo DEVEDOR
        # Pode ser crédito acumulado legítimo OU erro de classificação
        {"cod_conta": "2.1.03.001", "saldo_final": 12000.00, "ind_saldo_fin": "D", "valor_debito": 85000.00, "valor_credito": 73000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        {"cod_conta": "2.1.03.002", "saldo_final": 3200.00, "ind_saldo_fin": "C", "valor_debito": 38400.00, "valor_credito": 41600.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "2.1.03.003", "saldo_final": 14800.00, "ind_saldo_fin": "C", "valor_debito": 177600.00, "valor_credito": 192400.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "2.2.01.001", "saldo_final": 65000.00, "ind_saldo_fin": "C", "valor_debito": 24000.00, "valor_credito": 89000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        # PL
        {"cod_conta": "3.1.01", "saldo_final": 100000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 100000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "3.2.01", "saldo_final": 85000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 85000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        
        # Resultado
        {"cod_conta": "4.1.01", "saldo_final": 480000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 480000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "4.1.02", "saldo_final": 120000.00, "ind_saldo_fin": "C", "valor_debito": 0.00, "valor_credito": 120000.00, "saldo_inicial": 0.0, "ind_saldo_ini": "C", "centro_custo": ""},
        {"cod_conta": "5.1.01", "saldo_final": 288000.00, "ind_saldo_fin": "D", "valor_debito": 288000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "5.2.01", "saldo_final": 144000.00, "ind_saldo_fin": "D", "valor_debito": 144000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "5.2.02", "saldo_final": 72000.00, "ind_saldo_fin": "D", "valor_debito": 72000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
        {"cod_conta": "5.2.03", "saldo_final": 19000.00, "ind_saldo_fin": "D", "valor_debito": 19000.00, "valor_credito": 0.00, "saldo_inicial": 0.0, "ind_saldo_ini": "D", "centro_custo": ""},
    ]
    
    # Criar DataFrames
    df_plano = pl.DataFrame(plano_contas_data)
    df_saldos = pl.DataFrame(saldos_data)
    
    # Enriquecer saldos com dados do plano
    df_saldos = df_saldos.join(
        df_plano.select(["cod_conta", "descricao", "natureza", "tipo_conta"]),
        on="cod_conta",
        how="left"
    )
    
    return empresa, df_plano, df_saldos
