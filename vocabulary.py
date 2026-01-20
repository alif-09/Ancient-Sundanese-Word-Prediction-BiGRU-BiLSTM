import tensorflow as tf

class WordVocab:
    def __init__(self, docs=None):
        if docs:
            all_words = " ".join(docs).split()
            unique_words = sorted(list(set(all_words)))
            self.stoi = {w: i+3 for i, w in enumerate(unique_words)}
            self.stoi["[PAD]"] = 0
            self.stoi["[UNK]"] = 1
            self.stoi["[MASK]"] = 2
            self.itos = {i: w for w, i in self.stoi.items()}
            self.vocab_size = len(self.stoi)

    def encode(self, words, max_len):
        ids = [self.stoi.get(w, self.stoi["[UNK]"]) for w in words]
        return tf.keras.preprocessing.sequence.pad_sequences([ids], maxlen=max_len, padding='post', value=0)[0]