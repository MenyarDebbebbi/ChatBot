from flask import Flask, render_template, request, jsonify
from models.text_processor import TextProcessor
from models.classifier import ChatbotClassifier
from utils.search_engine import SearchEngine
from utils.feedback import FeedbackManager
from config import Config
import os

app = Flask(__name__, 
    template_folder='web/templates',
    static_folder='web/static'
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

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    # Prétraitement du texte
    processed_text = text_processor.preprocess(user_message)
    
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

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback_data = request.json
    feedback_manager.save_feedback(feedback_data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True) 