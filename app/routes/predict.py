import falcon
from falcon.media.validators import jsonschema
from helpers.zero_shot_text_classification import ZeroShotTextClassifier


REQUEST_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "minLength": 1, "maxLength": 1000},
        "labels": {
            "type": "array",
            "items": {"type": "string", "minLength": 1, "maxLength": 10},
            "minItems": 1,
        },
    },
    "required": ["text", "labels"],
}


class Predict:
    @jsonschema.validate(REQUEST_SCHEMA)
    def on_post(self, req: falcon.Request, resp: falcon.Response) -> falcon.Response:
        """Handles prediction requests as POST"""
        request_obj = req.get_media()
        text = request_obj["text"]
        labels = request_obj["labels"]
        prediction = ZeroShotTextClassifier.predict(text=text, candidate_labels=labels)
        resp.status = falcon.HTTP_200  # pylint: disable=no-member
        resp.media = prediction
        return resp
