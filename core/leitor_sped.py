"""
Leitor de SPED ECD com Polars
Audiper - Sistema de Auditoria Digital

Extrai registros:
- 0000: Dados da empresa
- I050: Plano de Contas
- I155: Saldos Periódicos (Balancete)
"""

import polars as pl
import io
from dataclasses import dataclass
from typing import Tuple, Optional, List, Dict, Any


@dataclass
class DadosEmpresa:
    """Dados extraídos do registro 0000"""
    nome: str
    cnpj: str
    uf: str
    data_inicio: str
    data_fim: str
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "nome": self.nome,
            "cnpj": self.cnpj,
            "uf": self.uf,
            "data_inicio": self.data_inicio,
            "data_fim": self.data_fim
        }


def limpar_campo(valor: str) -> str:
    """Remove espaços extras"""
    return valor.strip() if valor else ""


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ: 12345678000190 -> 12.345.678/0001-90"""
    cnpj = cnpj.replace(".", "").replace("/", "").replace("-", "")
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj


def formatar_data(data: str) -> str:
    """Formata data: 01012024 -> 01/01/2024"""
    if len(data) == 8:
        return f"{data[:2]}/{data[2:4]}/{data[4:]}"
    return data


def processar_sped_ecd(conteudo: str) -> Tuple[Optional[DadosEmpresa], pl.DataFrame, pl.DataFrame, str]:
    """
    Processa arquivo SPED ECD e retorna dados estruturados.
    
    Args:
        conteudo: String com conteúdo do arquivo SPED
        
    Returns:
        Tupla com (DadosEmpresa, DataFrame Plano, DataFrame Saldos, mensagem_status)
    """
    
    linhas = conteudo.split("\n")
    
    # Estruturas para coleta
    dados_empresa = None
    registros_i050: List[Dict[str, Any]] = []
    registros_i155: List[Dict[str, Any]] = []
    
    for linha in linhas:
        if not linha.startswith("|"):
            continue
            
        campos = linha.strip().split("|")
        if len(campos) < 3:
            continue
            
        registro = campos[1]
        
        # Registro 0000 - Abertura (dados da empresa)
        if registro == "0000" and len(campos) >= 9:
            dados_empresa = DadosEmpresa(
                nome=limpar_campo(campos[6]) if len(campos) > 6 else "N/A",
                cnpj=formatar_cnpj(limpar_campo(campos[7])) if len(campos) > 7 else "N/A",
                uf=limpar_campo(campos[8]) if len(campos) > 8 else "N/A",
                data_inicio=formatar_data(limpar_campo(campos[3])) if len(campos) > 3 else "N/A",
                data_fim=formatar_data(limpar_campo(campos[4])) if len(campos) > 4 else "N/A",
            )
        
        # Registro I050 - Plano de Contas
        # Layout: |I050|DT_ALT|COD_NAT|IND_CTA|NIVEL|COD_CTA|COD_CTA_SUP|CTA|
        elif registro == "I050" and len(campos) >= 9:
            cod_nat = limpar_campo(campos[3])
            registros_i050.append({
                "cod_conta": limpar_campo(campos[6]),
                "descricao": limpar_campo(campos[8]),
                "cod_natureza": cod_nat,
                "natureza": mapear_natureza(cod_nat),
                "tipo_conta": limpar_campo(campos[4]),  # S=Sintética, A=Analítica
                "nivel": limpar_campo(campos[5]),
                "conta_superior": limpar_campo(campos[7]),
            })
        
        # Registro I155 - Saldos Periódicos
        # Layout: |I155|COD_CTA|COD_CCUS|VL_SLD_INI|IND_DC_INI|VL_DEB|VL_CRED|VL_SLD_FIN|IND_DC_FIN|
        elif registro == "I155" and len(campos) >= 10:
            try:
                registros_i155.append({
                    "cod_conta": limpar_campo(campos[2]),
                    "centro_custo": limpar_campo(campos[3]),
                    "saldo_inicial": converter_valor(campos[4]),
                    "ind_saldo_ini": limpar_campo(campos[5]),
                    "valor_debito": converter_valor(campos[6]),
                    "valor_credito": converter_valor(campos[7]),
                    "saldo_final": converter_valor(campos[8]),
                    "ind_saldo_fin": limpar_campo(campos[9]),
                })
            except (ValueError, IndexError):
                continue  # Ignora linhas mal formatadas
    
    # Criar DataFrames Polars
    df_plano = pl.DataFrame(registros_i050) if registros_i050 else pl.DataFrame()
    df_saldos = pl.DataFrame(registros_i155) if registros_i155 else pl.DataFrame()
    
    # Validações
    if df_plano.is_empty():
        return dados_empresa, df_plano, df_saldos, "⚠️ Nenhum Plano de Contas (I050) encontrado"
    
    if df_saldos.is_empty():
        return dados_empresa, df_plano, df_saldos, "⚠️ Nenhum Saldo (I155) encontrado"
    
    # Enriquecer saldos com dados do plano
    df_saldos = df_saldos.join(
        df_plano.select(["cod_conta", "descricao", "natureza", "tipo_conta"]),
        on="cod_conta",
        how="left"
    )
    
    return dados_empresa, df_plano, df_saldos, "✅ Arquivo processado com sucesso"


def mapear_natureza(codigo: str) -> str:
    """Mapeia código de natureza para descrição"""
    mapa = {
        "01": "ATIVO",
        "02": "PASSIVO",
        "03": "PATRIMÔNIO LÍQUIDO",
        "04": "RESULTADO",
        "05": "COMPENSAÇÃO",
        "09": "OUTRAS",
    }
    return mapa.get(codigo, "N/A")


def converter_valor(valor_str: str) -> float:
    """Converte string de valor SPED para float: 1.234,56 -> 1234.56"""
    if not valor_str or not valor_str.strip():
        return 0.0
    
    valor = valor_str.strip()
    # Remove pontos de milhar e troca vírgula por ponto
    valor = valor.replace(".", "").replace(",", ".")
    
    try:
        return float(valor)
    except ValueError:
        return 0.0


def carregar_arquivo_upload(arquivo_upload) -> str:
    """Carrega arquivo do upload do Streamlit"""
    return arquivo_upload.getvalue().decode("latin-1")
