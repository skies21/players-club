from django.shortcuts import render
from transformers import BertTokenizer, BertForSequenceClassification
import torch

from users.models import Comment

tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
model = BertForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()
    return predicted_class

def analyze_comments(request):
    comments = Comment.objects.all()
    comment_texts = [comment.text for comment in comments]

    sentiments = [predict_sentiment(text) for text in comment_texts]

    positive_count = sentiments.count(4)
    total_comments = len(sentiments)
    if total_comments:
        loyalty = 'Высокая' if positive_count / total_comments > 0.5 else 'Низкая'
    else:
        loyalty = 'Высокая'

    last_sentiment = sentiments[-1] if sentiments else 0

    sentiment_labels = ['Крайне негативная', 'Негативная', 'Нейтральная', 'Позитивная', 'Крайне позитивная']
    sentiment_text = sentiment_labels[last_sentiment]

    context = {
        'sentiment': sentiment_text,  # Последний прогноз для тональности
        'loyalty': loyalty,           # Лояльность на основе позитивных комментариев
    }

    return render(request, 'users/comments_analyze.html', context)
