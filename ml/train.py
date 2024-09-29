import pandas as pd
from datasets import Dataset
from sklearn.model_selection import train_test_split
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from datasets import load_dataset
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sentence_transformers.evaluation import TripletEvaluator
from huggingface_hub import login

# Загрузка данных из CSV файла
df = pd.read_csv('data/training_data.csv')

# Переименование столбцов для соответствия требованиям модели
# 'Вопрос из БЗ' переименовывается в 'anchor' (якорь), позитивные и негативные ответы остаются неизменными
df = df.rename(columns={"Вопрос из БЗ": "anchor", "positive": "positive", "negative": "negative"})[['anchor','positive','negative']]

# Разделение данных на тренировочный и валидационный наборы (80% тренировочные данные, 20% — валидационные)
train_df, eval_df = train_test_split(df, test_size=0.2, random_state=42)

# Сохранение тренировочных и валидационных данных в формате JSON для дальнейшего использования
train_df.to_json('data/train_df.json', orient='records', lines=True, index=False)
eval_df.to_json('data/eval_df.json', orient='records', lines=True, index=False)

# Загрузка тренировочного и валидационного наборов данных с использованием библиотеки datasets
train_dataset = load_dataset('json',data_files='data/train_df.json')['train']
eval_dataset = load_dataset('json',data_files='data/eval_df.json')['train']

# Вывод первого примера из тренировочного набора для проверки
print(train_dataset[0])

# Загрузка предварительно обученной модели SentenceTransformer
model = SentenceTransformer("/home/dkalin/train_encoder/models/multilingual-e5-large_triplet")

# Определение функции потерь MultipleNegativesRankingLoss для обучения
loss = MultipleNegativesRankingLoss(model)

# 6. Настройки обучения
args = SentenceTransformerTrainingArguments(
    output_dir="intfloat/multilingual-e5-large_triplet",
    num_train_epochs=2,# Количество эпох обучения
    per_device_train_batch_size=4,# Размер батча для обучения
    per_device_eval_batch_size=4, # Размер батча для валидации
    learning_rate=2e-5, # Скорость обучения
    warmup_ratio=0.1, # Процент шагов обучения, используемый для разогрева
    bf16=True,# Использование 16-битной точности
    gradient_accumulation_steps=32,
    gradient_checkpointing=False, 
    eval_strategy="steps", # Стратегия валидации во время обучения (валидация каждые N шагов)
    eval_steps=50, # Количество шагов между каждой валидацией
    save_strategy="steps",
    save_steps=300, # Количество шагов между сохранениями
    save_total_limit=2, # Максимальное количество сохранений модели 
    logging_steps=1,
    run_name="e5_triplet",
)

# Настройка триплетного оценивателя (TripletEvaluator) для валидации модели
dev_evaluator = TripletEvaluator(
    anchors=eval_dataset["anchor"],
    positives=eval_dataset["positive"],
    negatives=eval_dataset["negative"],
    name="e5_triplet_eval",
)

# Оценка модели на валидационном наборе перед началом обучения
dev_evaluator(model)

# Инициализация тренера для обучения модели с заданными параметрами
trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=dev_evaluator,
)

# Запуск обучения модели
trainer.train()

# Сохранение обученной модели в локальный каталог
model.save_pretrained("models/multilingual-e5-large_triplet")

# Загрузка модели на HuggingFace Hub для общего использования
model.push_to_hub("dankalin/multilingual-e5-large-hack")