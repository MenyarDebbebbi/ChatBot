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
classifier = ChatbotClassifier()
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
    
    # Validation de la question
    is_valid, processed_text = text_processor.validate_question(user_message)
    if not is_valid:
        return jsonify({'response': "Je n'ai pas compris votre question. Pouvez-vous la reformuler ?"})
    
    try:
        # Classification et génération de réponse
        response, confidence = classifier.get_response(processed_text)
        
        # Si la confiance est faible, utiliser le moteur de recherche
        if confidence < Config.MIN_CONFIDENCE_SCORE:
            search_results = search_engine.search(processed_text)
            if search_results:
                response = {
                    'text': response,
                    'links': search_results
                }
        
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
        response, confidence = classifier.get_response(q)
        results.append({
            'question': q,
            'response': response,
            'confidence': confidence
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 