from sqlmodel import Field, SQLModel
from typing import List, Optional


class PerguntasBase(SQLModel):
    categoria: str
    pergunta: str
    opcao1: str
    opcao2: str
    opcao3: str
    opcao4: str
    resposta: int


class Perguntas(PerguntasBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
