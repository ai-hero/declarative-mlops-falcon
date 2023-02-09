import sys
from transformers import pipeline, Pipeline
from time import perf_counter
import logging

# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


class ZeroShotTextClassifier:
    """A class for the classifier with only class methods for prediction"""

    # Class variable for the model pipeline
    classifier: Pipeline = None

    @classmethod
    def load(cls):
        # Only load one instance of the model
        if cls.classifier is None:
            # Load the model pipeline.
            # Note: Usually, this would also download the model.
            # But, we download the model into the container in the Dockerfile
            # so that it's built into the container and there's no download at
            # run time (otherwise, each time the container spins up
            # we'll download a 1GB model).
            # Loading still takes time, though. So, we do that here.
            # Note: You can use a GPU here if needed.
            t0 = perf_counter()
            cls.classifier = pipeline(
                "zero-shot-classification", model="valhalla/distilbart-mnli-12-1"
            )
            elapsed = 1000 * (perf_counter() - t0)
            log.info("Model warm-up time: %d ms.", elapsed)

    @classmethod
    def predict(cls, text: str, candidate_labels: list[str]) -> list[float]:
        """Return the prediction probabilities for each class in the same order"""
        assert text and candidate_labels  # sanity check

        # Make sure the model is loaded.
        cls.load()

        # Predict.
        t0 = perf_counter()
        # pylint: disable-next=not-callable
        huggingface_predictions = cls.classifier(text, candidate_labels)
        scores = {
            label: float(score)
            for (label, score) in zip(
                huggingface_predictions["labels"], huggingface_predictions["scores"]
            )
        }
        elapsed = 1000 * (perf_counter() - t0)
        log.info("Model prediction time: %d ms.", elapsed)

        # For the tutorial, let's return the list of prediction probabilities
        # in the same order as the candidate labels.
        return [scores[label] for label in candidate_labels]
