from database import engine
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Perguntas, PerguntasBase
from typing import List

app = FastAPI()


@app.post("/perguntas", response_model=Perguntas)
def criar_perguntas(perguntas: PerguntasBase):
    with Session(engine) as session:
        db_perguntas = Perguntas.from_orm(perguntas)
        session.add(db_perguntas)
        session.commit()
        session.refresh(db_perguntas)
        return db_perguntas


@app.get("/perguntas", response_model=List[Perguntas])
def ler_perguntas(limit: int = 100):
    with Session(engine) as session:
        perguntas = session.exec(select(Perguntas).limit(limit)).all()
        return perguntas


@app.get("/perguntas/{categoria}", response_model=List[Perguntas])
def pergunta_por_categoria(categoria: str, limit: int = 100):
    try:
        with Session(engine) as session:
            perguntas = session.exec(select(Perguntas).where(Perguntas.categoria == categoria).limit(limit)).all()
            return perguntas
    except:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")


@app.delete("/perguntas/{id}")
def deletar_pergunta_por_id(id: int):
    with Session(engine) as session:
        pergunta = session.get(Perguntas, id)
        if not pergunta:
            raise HTTPException(status_code=404, detail="ID não encontrado")
        session.delete(pergunta)
        session.commit()
        return pergunta, "Pagado"


@app.patch("/perguntas/{id}", response_model=Perguntas)
def atualizar_pergunta_por_id(id: int, pergunta: PerguntasBase):
    with Session(engine) as session:
        db_perguntas = session.get(Perguntas, id)
        if not db_perguntas:
            raise HTTPException(status_code=404, detail="ID não encontrado")
        pergunta_df = pergunta.dict(exclude_unset=True)
        for key, value in pergunta_df.items():
            setattr(db_perguntas, key, value)
        session.add(db_perguntas)
        session.commit()
        session.refresh(db_perguntas)
        return db_perguntas
