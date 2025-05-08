from flask import Flask, render_template, request, jsonify, send_file
from models.response_generator import ResponseGenerator
from models.nlp_processor import NLPProcessor
from config import Config
import os
from datetime import datetime
from models.conversation_history import ConversationHistory

app = Flask(__name__, 
    template_folder='web/templates',
    static_folder='web/static',
    static_url_path='/static'
)
app.config.from_object(Config)

# Initialisation des composants
response_generator = ResponseGenerator()
conversation_history = ConversationHistory()

@app.route('/')
def home():
    conversations = conversation_history.get_history()
    return render_template('index.html', conversations=conversations)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        response = response_generator.generate_response(user_message)
        
        # Sauvegarder la conversation dans l'historique
        conversation_history.add_conversation(user_message, response)
        
        return jsonify({'response': response})
    except Exception as e:
        print(f"Erreur lors du traitement de la requête: {str(e)}")
        return jsonify({'response': "Désolé, une erreur est survenue lors du traitement de votre demande. Veuillez réessayer."})

@app.route('/history')
def history():
    conversations = conversation_history.get_history()
    return render_template('history.html', conversations=conversations)

@app.route('/export_history/<format>')
def export_history(format):
    if format not in ['json', 'csv']:
        return jsonify({'error': 'Format non supporté'}), 400
    
    try:
        file_path = conversation_history.export_history(format)
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f'conversation_history.{format}'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        conversation_history.clear_history()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

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

@app.route('/health')
def health_check():
    """Endpoint pour vérifier l'état de l'application"""
    try:
        # Vérifier l'accès aux fichiers essentiels
        required_files = [
            'data/scraping-data.json',
            'data/training_data.json'
        ]
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Fichier manquant: {file}")

        # Vérifier l'accès à la base de données ou autres services si nécessaire
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 