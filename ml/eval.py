import pandas as pd
from sentence_transformers import SentenceTransformer
from sentence_transformers.evaluation import InformationRetrievalEvaluator
import random

# Загрузка предобученной модели 'multilingual-e5-large-hack' для трансформации предложений
model = SentenceTransformer('dankalin/multilingual-e5-large-hack')

# Загрузка данных из Excel-файла с реальными кейсами
df = pd.read_excel('data/02_Реальные_кейсы.xlsx')

# Создание корпуса: словарь, где ключ — это индекс строки, а значение — текст ответа из базы знаний (БЗ)
corpus = dict(zip(df.index.astype(str), df['Ответ из БЗ']))

# Создание запросов: словарь, где ключ — это индекс строки, а значение — текст вопроса из БЗ
queries = dict(zip(df.index.astype(str), df['Вопрос из БЗ']))

# Создание словаря релевантных документов
# В этом случае мы предполагаем, что каждый вопрос соответствует только одному ответу
relevant_docs = {str(idx): set([str(idx)]) for idx in df.index}

# Инициализация объекта для оценки качества модели на основе метрик Information Retrieval
ir_evaluator = InformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
    name="Your-Dataset-Evaluation",
)

# Проведение оценки модели с использованием предоставленных данных
results = ir_evaluator(model)

# Вывод результатов оценки
print(results)