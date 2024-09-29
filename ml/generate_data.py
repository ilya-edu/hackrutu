import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Загрузка обновленного датасета из CSV файла
data = pd.read_csv('data/updated_dataset.csv')

# Вычисление TF-IDF матрицы для удаления дубликатов
# Это необходимо для последующего выявления дубликатов на основе схожести текстов
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['Ответ из БЗ'])

# Вычисление косинусной схожести между всеми парами ответов
cosine_sim = cosine_similarity(tfidf_matrix)

# Порог для определения дубликатов
threshold = 0.85

# Создание матрицы дубликатов на основе порогового значения косинусной схожести
duplicates = np.triu(cosine_sim, k=1) > threshold

# Удаление дубликатов
unique_rows = ~duplicates.any(axis=1)
data_cleaned = data[unique_rows].reset_index(drop=True)

print('Кол-во строк после очистки: ' + str(len(data_cleaned)))

# Настройка модели для генерации эмбеддингов (векторных представлений) на основе предобученной модели HuggingFace
model_name = "intfloat/multilingual-e5-large"
model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': False}

# Инициализация модели эмбеддингов
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# Преобразование ответов в объекты Document для дальнейшего создания векторного хранилища
documents = [Document(page_content=text, metadata={"source": i}) for i, text in enumerate(data_cleaned['Ответ из БЗ'])]

# Создание векторного хранилища с использованием FAISS для быстрого поиска по схожести
vectorstore = FAISS.from_documents(documents, embeddings)


# Функция для поиска 10 наиболее релевантных ответов на заданный вопрос
# Возвращает ответы, которые не совпадают с правильным ответом (негативные примеры)
def get_top_10_answers(question, true_ans):
    docs = vectorstore.similarity_search(question, k=10)
    
    answer = []
    for i, doc in enumerate(docs, 1):
        # Исключаем правильный ответ из списка негативных
        if doc.page_content != true_ans:
            answer.append(doc.page_content)
    return answer

# Создание датафрейма для данных, которые будут использоваться для обучения
df_for_training = pd.DataFrame(columns=['Вопрос из БЗ', 'positive', 'negative', 'Классификатор 1 уровня', 'Классификатор 2 уровня'])

# Проход по каждому вопросу и ответу в очищенных данных
for index, row in data_cleaned.iterrows():
    question = row['Вопрос из БЗ']
    true_answer = row['Ответ из БЗ']
    classifier_1 = row['Классификатор 1 уровня']
    classifier_2 = row['Классификатор 2 уровня']
    
    # Получаем 10 наиболее релевантных негативных примеров
    negatives = get_top_10_answers(question, true_answer)
    
    # Для каждого негативного примера добавляем строку в датафрейм
    for neg_answer in negatives:
        df_for_training = pd.concat([df_for_training, pd.DataFrame([{
            'Вопрос из БЗ': question,
            'positive': true_answer,
            'negative': neg_answer,
            'Классификатор 1 уровня': classifier_1,
            'Классификатор 2 уровня': classifier_2
        }])], ignore_index=True)

# Сохранение сформированных данных для обучения в CSV файл
df_for_training.to_csv('training_data.csv', index=False)

# Вывод первых 30 строк полученных данных для проверки
print(df_for_training.head(30))