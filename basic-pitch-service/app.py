import os
import io
import json
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import librosa
from basic_pitch.inference import predict
from basic_pitch import SAMPLE_RATE
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'basic-pitch'}), 200

@app.route('/api/pitch', methods=['POST'])
def extract_pitch():
    """
    Extract pitch from audio file
    
    Expected request:
    - multipart/form-data with 'audio' file
    
    Returns:
    - JSON with pitch contour, confidence, and metadata
    """
    try:
        # Check if audio file is in request
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(audio_file.filename):
            return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Check file size
        audio_file.seek(0, os.SEEK_END)
        file_size = audio_file.tell()
        audio_file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({'error': f'File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB'}), 400
        
        # Read audio file
        audio_data, sr = librosa.load(io.BytesIO(audio_file.read()), sr=SAMPLE_RATE)
        
        # Extract pitch using Basic Pitch
        model_output, midi_data, note_events = predict(audio_data)
        
        # Prepare response
        response_data = {
            'success': True,
            'metadata': {
                'sample_rate': int(SAMPLE_RATE),
                'duration_seconds': float(len(audio_data) / SAMPLE_RATE),
                'filename': audio_file.filename
            },
            'pitch_contour': {
                'times': model_output[0].tolist(),
                'frequencies': model_output[1].tolist(),
                'confidence': model_output[2].tolist()
            },
            'midi_data': midi_data.tolist() if midi_data is not None else None,
            'note_events': [
                {
                    'start_time': float(event.start_time),
                    'end_time': float(event.end_time),
                    'pitch_midi': int(event.pitch_midi),
                    'velocity': int(event.velocity)
                }
                for event in note_events
            ] if note_events else []
        }
        
        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/pitch/batch', methods=['POST'])
def extract_pitch_batch():
    """
    Extract pitch from multiple audio files
    
    Expected request:
    - multipart/form-data with multiple 'audio' files
    
    Returns:
    - JSON array with pitch data for each file
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio files provided'}), 400
        
        audio_files = request.files.getlist('audio')
        results = []
        
        for audio_file in audio_files:
            if audio_file.filename == '':
                continue
            
            if not allowed_file(audio_file.filename):
                results.append({
                    'filename': audio_file.filename,
                    'error': f'File type not allowed'
                })
                continue
            
            try:
                audio_data, sr = librosa.load(io.BytesIO(audio_file.read()), sr=SAMPLE_RATE)
                model_output, midi_data, note_events = predict(audio_data)
                
                results.append({
                    'filename': audio_file.filename,
                    'success': True,
                    'metadata': {
                        'sample_rate': int(SAMPLE_RATE),
                        'duration_seconds': float(len(audio_data) / SAMPLE_RATE)
                    },
                    'pitch_contour': {
                        'times': model_output[0].tolist(),
                        'frequencies': model_output[1].tolist(),
                        'confidence': model_output[2].tolist()
                    },
                    'note_events': len(note_events) if note_events else 0
                })
            except Exception as e:
                results.append({
                    'filename': audio_file.filename,
                    'error': str(e)
                })
        
        return jsonify({'results': results}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info', methods=['GET'])
def service_info():
    """Get service information"""
    return jsonify({
        'service': 'Basic Pitch Service',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check',
            '/api/pitch': 'Extract pitch from single audio file',
            '/api/pitch/batch': 'Extract pitch from multiple audio files',
            '/api/info': 'Service information'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

