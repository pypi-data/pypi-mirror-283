import pandas as pd
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import emoji
from googletrans import Translator


class SentimentAnalyzer:
    # Nome do arquivo CSV na pasta 'dados'
    CSV_FILENAME = 'dataset_complete_with_emotions.csv'

    def __init__(self):
        # Obtém o caminho completo para o arquivo CSV
        csv_path = os.path.join(os.path.dirname(__file__), 'Dados', self.CSV_FILENAME)
        self.df = pd.read_csv(csv_path)
        self.analyzer = SentimentIntensityAnalyzer()
        self.translator = Translator()

    def replace_emoji_with_emotion(self, texto):
        emoji_emocao_dict = dict(zip(self.df['Design'], self.df['emotion']))
        for emoji_char, emocao in emoji_emocao_dict.items():
            texto = texto.replace(emoji_char, emocao)
        return texto

    def sentiment_analyze(self, texto):
        scores = self.analyzer.polarity_scores(texto)
        sentimento = scores['compound']
        return sentimento

    def extract_emojis(self, texto):
        return [char for char in texto if char in emoji.EMOJI_DATA]

    def translate_text(self, texto, idioma_destino):
        translated = self.translator.translate(texto, dest=idioma_destino).text
        return translated

    def translate_info(self, campos, idioma_destino):
        campos_traduzidos = {}
        for chave, valor in campos.items():
            valor_str = str(valor)
            campos_traduzidos[chave] = self.translate_text(valor_str, idioma_destino)
        return campos_traduzidos

    def text_analyze(self, texto):
        # Detecta o idioma do texto de entrada
        idioma_entrada = self.translator.detect(texto).lang

        # Extrai os emojis do texto original
        emojis_usados = self.extract_emojis(texto)

        # Substitui emojis pela emoção correspondente
        texto_modificado = self.replace_emoji_with_emotion(texto)

        # Realiza análise de sentimentos no texto modificado
        sentimento = self.sentiment_analyze(texto_modificado)

        # Traduz o texto modificado
        texto_traduzido = self.translate_text(texto_modificado, idioma_entrada)

        # Obtém informações detalhadas sobre os emojis usados
        emoji_info = {}
        for emoji_char in emojis_usados:
            row = self.df[self.df['Design'] == emoji_char].iloc[0]
            info = {
                'Emoção': row['emotion'],
                'Descrição': row['Description'],
                'Unicode': row['Unicode'],
                'Score': row['Score'],
                'Sentimento': row['Sentiment']
            }
            # Traduz os campos para o idioma de entrada
            emoji_info[emoji_char] = self.translate_info(info, idioma_entrada)

        resultados_traduzidos = {
            "Texto com emojis substituídos pelas emoções correspondentes": texto_traduzido,
            "Sentimento do texto": sentimento,
            "Informações dos emojis usados": emoji_info
        }

        return resultados_traduzidos

# Exemplo de uso da classe SentimentAnalyzer
if __name__ == "__main__":
    sa = SentimentAnalyzer()
    texto_input = input("Digite seu texto: ")
    resultados = sa.text_analyze(texto_input)

    # Exibe os resultados
    print("Texto com emojis substituídos pelas emoções correspondentes:", resultados["Texto com emojis substituídos pelas emoções correspondentes"])
    print("Sentimento do texto:", resultados["Sentimento do texto"])
    print("Informações dos emojis usados:")
    for emoji_char, info in resultados["Informações dos emojis usados"].items():
        print(f"{emoji_char}: {info}")
