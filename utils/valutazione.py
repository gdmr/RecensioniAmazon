from transformers import pipeline

def get_valutazione(text):
    classifier = pipeline("sentiment-analysis", model="LiYuan/amazon-review-sentiment-analysis")
    prediction = classifier(text)
    result = prediction[0]
    star = result['label']
    star_number = star.split(' ')[0]
    return star_number