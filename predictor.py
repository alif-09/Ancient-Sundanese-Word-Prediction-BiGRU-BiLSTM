import tensorflow as tf
import numpy as np
import pickle
import os
import re
from vocabulary import WordVocab #

class WordPredictor:
    def __init__(self, folder_path="models"):
        gru_path = os.path.join(folder_path, "best_model_gru.keras")
        lstm_path = os.path.join(folder_path, "best_model_lstm.keras")
        vocab_path = os.path.join(folder_path, "word_vocab.pkl")
        
        self.model_gru = tf.keras.models.load_model(gru_path)
        self.model_lstm = tf.keras.models.load_model(lstm_path)
        
        with open(vocab_path, 'rb') as f:
            self.vocab = pickle.load(f)
            
        self.window_size = 5
        self.max_len = 10 

    def normalize_for_mask(self, text):
        """Normalisasi tanpa merusak token [mask]"""
        text = text.lower().replace("\u00a0", " ")
        # Hanya menghapus simbol selain huruf dan kurung siku untuk [mask]
        text = re.sub(r'[^a-z\s\[\]]', '', text) 
        return re.sub(r"\s+", " ", text).strip()

    def predict_all_masks(self, text, model_type='gru'):
        """Mencari semua [mask] dan memberikan kandidat untuk setiap posisi"""
        model = self.model_gru if model_type == 'gru' else self.model_lstm
        words = self.normalize_for_mask(text).split()
        
        # Mencari semua indeks yang berisi [mask]
        mask_indices = [i for i, w in enumerate(words) if "[mask]" in w or "mask" == w]
        
        if not mask_indices:
            return None

        all_predictions = []
        for m_idx in mask_indices:
            # Ekstraksi konteks untuk posisi mask spesifik ini
            left = words[max(0, m_idx - self.window_size):m_idx]
            right = words[m_idx + 1:m_idx + 1 + self.window_size]
            context_query = left + right
            
            encoded = [self.vocab.stoi.get(w, self.vocab.stoi.get("[UNK]", 1)) for w in context_query]
            padded = tf.keras.preprocessing.sequence.pad_sequences(
                [encoded], maxlen=self.max_len, padding='post', value=0
            )
            
            preds = model.predict(padded, verbose=0)[0]
            top_10_idx = np.argsort(preds)[-10:][::-1]
            
            mask_results = []
            for idx in top_10_idx:
                mask_results.append({
                    "word": self.vocab.itos.get(idx, "[UNK]"),
                    "confidence": float(preds[idx])
                })
            all_predictions.append({"index": m_idx, "candidates": mask_results})
            
        return all_predictions