
from typing import List

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Casa de Sucos",
    description=(
        "API para consultar informações nutricionais "
        "de frutas e cadastrar sucos."
    ),
    version="1.0.0",
)

URL_FRUITYVICE = "https://www.fruityvice.com/api/fruit"

# Armazenamento temporário dos sucos cadastrados.
sucos = []
proximo_id = 1


# Modelos de entrada


class SucoEntrada(BaseModel):
    nome: str = Field(min_length=1)
    frutas: List[str] = Field(min_length=1)
    tem_gosto_de: str = Field(min_length=1)


class AtualizacaoSuco(BaseModel):
    frutas: List[str] = Field(min_length=1)


# Consulta a Fruityvice


def consultar_fruta(nome: str) -> dict:
    try:
        resposta = requests.get(
            f"{URL_FRUITYVICE}/{nome.strip()}",
            timeout=10,
        )

        if resposta.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"A fruta '{nome}' não foi encontrada.",
            )

        resposta.raise_for_status()
        dados = resposta.json()

        if not isinstance(dados, dict) or "nutritions" not in dados:
            raise HTTPException(
                status_code=502,
                detail="A API de frutas retornou dados inválidos.",
            )

        nutricao = dados["nutritions"]

        return {
            "nome": dados["name"],
            "calorias": nutricao["calories"],
            "acucar": nutricao["sugar"],
        }

    except HTTPException:
        raise

    except (requests.RequestException, ValueError, KeyError, TypeError):
        raise HTTPException(
            status_code=502,
            detail=(
                "Não foi possível consultar os dados nutricionais "
                "da fruta. Tente novamente mais tarde."
            ),
        )


# Endpoint 1: consultar uma fruta


@app.get("/frutas/{nome}")
def obter_fruta(nome: str):
    return consultar_fruta(nome)


# Endpoint 2: cadastrar um suco


@app.post("/sucos", status_code=201)
def cadastrar_suco(suco: SucoEntrada):
    global proximo_id

    frutas_consultadas = [
        consultar_fruta(fruta) for fruta in suco.frutas
    ]

    total_calorias = sum(
        fruta["calorias"] for fruta in frutas_consultadas
    )

    total_acucar = round(
        sum(fruta["acucar"] for fruta in frutas_consultadas),
        2,
    )

    novo_suco = {
        "id": proximo_id,
        "nome": suco.nome.strip(),
        "frutas": [fruta["nome"] for fruta in frutas_consultadas],
        "tem_gosto_de": suco.tem_gosto_de.strip(),
        "total_calorias": total_calorias,
        "total_acucar": total_acucar,
    }

    sucos.append(novo_suco)
    proximo_id += 1

    return novo_suco


# Endpoint 3: listar todos os sucos


@app.get("/sucos")
def listar_sucos():
    return sucos


# Endpoint 4: atualizar as frutas de um suco (bônus)


@app.put("/sucos/{id}")
def atualizar_suco(id: int, atualizacao: AtualizacaoSuco):
    suco_encontrado = next(
        (suco for suco in sucos if suco["id"] == id),
        None,
    )

    if suco_encontrado is None:
        raise HTTPException(
            status_code=404,
            detail=f"Suco com ID {id} não encontrado.",
        )

    # Consultar todas as frutas antes de alterar o cadastro.
    frutas_consultadas = [
        consultar_fruta(fruta) for fruta in atualizacao.frutas
    ]

    total_calorias = sum(
        fruta["calorias"] for fruta in frutas_consultadas
    )

    total_acucar = round(
        sum(fruta["acucar"] for fruta in frutas_consultadas),
        2,
    )

    suco_encontrado["frutas"] = [
        fruta["nome"] for fruta in frutas_consultadas
    ]
    suco_encontrado["total_calorias"] = total_calorias
    suco_encontrado["total_acucar"] = total_acucar

    return suco_encontrado
