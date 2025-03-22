from flask import Flask, render_template, request, jsonify
from models.text_processor import TextProcessor
from models.classifier import ChatbotClassifier
from utils.search_engine import SearchEngine
from utils.feedback import FeedbackManager
from config import Config
import os

app = Flask(__name__, 
    template_folder='web/templates',
    static_folder='web/static',
    static_url_path='/static'
)
app.config.from_object(Config)

# Initialisation des composants
text_processor = TextProcessor()
classifier = ChatbotClassifier(text_processor=text_processor)
search_engine = SearchEngine()
feedback_manager = FeedbackManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({
            'response': "Je n'ai pas reçu de message. Pouvez-vous réessayer ?"
        })
    
    try:
        # Obtenir la réponse du classificateur
        result = classifier.get_response(user_message)
        
        # Si la confiance est faible, utiliser le moteur de recherche
        if result['confidence'] < Config.MIN_CONFIDENCE_SCORE:
            search_results = search_engine.search(user_message)
            if search_results:
                response = {
                    'text': result['response'],
                    'links': search_results
                }
            else:
                response = result['response']
        else:
            response = result['response']
        
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({
            'response': "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer."
        })

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    feedback_manager.save_feedback(feedback_data)
    return jsonify({'status': 'success'})

@app.route('/test_model')
def test_model():
    test_questions = [
        "Bonjour",
        "Comment s'inscrire à l'ISET ?",
        "Où se trouve l'ISET Sfax ?",
        "Quels sont les programmes disponibles ?"
    ]
    results = []
    for q in test_questions:
        result = classifier.get_response(q)
        results.append({
            'question': q,
            'response': result['response'],
            'confidence': result['confidence']
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 