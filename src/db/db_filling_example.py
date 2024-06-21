import os
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.models import WordModel


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

words = [
    WordModel(
        id=uuid.uuid4(),
        word="accomplish",
        translated_word="достигать",
        context="She was able to accomplish her goals through hard work and determination.",
        translated_context="Она смогла достичь своих целей благодаря упорному труду и решительности.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="intricate",
        translated_word="сложный",
        context="The artist’s work is known for its intricate designs and detailed patterns.",
        translated_context="Работы художника известны своими сложными дизайнами и детализированными узорами.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="contemplate",
        translated_word="размышлять",
        context="He sat on the porch to contemplate the beautiful sunset.",
        translated_context="Он сел на крыльце, чтобы поразмышлять о прекрасном закате.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="perseverance",
        translated_word="упорство",
        context="Her perseverance in the face of adversity was truly inspirational.",
        translated_context="Ее упорство перед лицом трудностей было действительно вдохновляющим.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="substantial",
        translated_word="значительный",
        context="They received a substantial grant to fund their research.",
        translated_context="Они получили значительный грант для финансирования своих исследований.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="inevitable",
        translated_word="неизбежный",
        context="Growing older is an inevitable part of life.",
        translated_context="Старение - неизбежная часть жизни.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="elaborate",
        translated_word="разработать",
        context="Could you please elaborate on your plan for the new project?",
        translated_context="Не могли бы вы более подробно рассказать о вашем плане для нового проекта?",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="conscientious",
        translated_word="добросовестный",
        context="She is a conscientious worker who always completes her tasks on time.",
        translated_context="Она добросовестный работник, который всегда выполняет свои задачи вовремя.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="transform",
        translated_word="преобразовать",
        context="The new policy aims to transform the healthcare system.",
        translated_context="Новая политика направлена на преобразование системы здравоохранения.",
    ),
    WordModel(
        id=uuid.uuid4(),
        word="predominant",
        translated_word="преобладающий",
        context="The predominant language in the region is Spanish.",
        translated_context="Преобладающим языком в регионе является испанский.",
    ),
]

session.add_all(words)
session.commit()

for word in words:
    print(f"Inserted word with id: {word.id}")
