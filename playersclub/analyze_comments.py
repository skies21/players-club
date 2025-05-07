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
    comments = Comment.objects.order_by('-created_at')[:5]
    comment_texts = [comment.text for comment in comments]

    if not comment_texts:
        context = {
            'sentiment': 'Нет комментариев',
            'loyalty': 'Нет данных',
            'avg_score': '-',
            'total_comments': 0
        }
        return render(request, 'users/comments_analyze.html', context)

    sentiments = [predict_sentiment(text) for text in comment_texts]

    avg_score = sum(sentiments) / len(sentiments)

    if avg_score >= 4.5:
        sentiment = 'Крайне позитивная'
    elif avg_score >= 3.5:
        sentiment = 'Позитивная'
    elif avg_score >= 2.5:
        sentiment = 'Нейтральная'
    elif avg_score >= 1.5:
        sentiment = 'Негативная'
    else:
        sentiment = 'Крайне негативная'

    positive_count = sum(1 for score in sentiments if score >= 4)
    loyalty = 'Высокая' if positive_count > len(sentiments) / 2 else 'Низкая'

    context = {
        'sentiment': sentiment,
        'loyalty': loyalty,
        'avg_score': round(avg_score, 2),
        'total_comments': len(sentiments)
    }

    return render(request, 'users/comments_analyze.html', context)
