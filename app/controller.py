from .model import predict_fish
from .regulations import load_regulations, format_regulations

class Controller:
    def __init__(self, config):
        self.config = config
        self.regulations = load_regulations()
        self.search_history = []

    def predict(self, image_path):
        top_classes, probabilities = predict_fish(
            image_path,
            self.config['PREDICTION_KEY'],
            self.config['PREDICTION_ENDPOINT'],
            self.config['PROJECT_ID'],
            self.config['PUBLISHED_NAME']
        )
        if top_classes:
            self.search_history.append((top_classes[0], probabilities[0], image_path))
        return top_classes, probabilities

    def get_regulations_text(self, species):
        return format_regulations(species, self.regulations)