from flask import Flask, render_template, request, jsonify
from models.response_generator import ResponseGenerator
from models.nlp_processor import NLPProcessor
from config import Config
import os

app = Flask(__name__, 
    template_folder='web/templates',
    static_folder='web/static',
    static_url_path='/static'
)
app.config.from_object(Config)

# Initialisation des composants
response_generator = ResponseGenerator()

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
            'response': {
                'text': "Je n'ai pas reçu de message. Pouvez-vous réessayer ?"
            }
        })
    
    try:
        # Générer la réponse
        response = response_generator.generate_response(user_message)
        
        # Si la réponse est une chaîne simple, la convertir en dictionnaire
        if isinstance(response, str):
            response = {'text': response}
            
        return jsonify({'response': response})
        
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return jsonify({
            'response': {
                'text': "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer."
            }
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