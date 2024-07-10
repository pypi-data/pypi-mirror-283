import os
import torch
from groundingdino.util.inference import load_model, predict
import groundingdino.datasets.transforms as T
# from inference.models.yolo_world.yolo_world import YOLOWorld

from ovsegmentation.knowledge_mapping.processors.types import DETECTOR_TYPE

MODEL_DICT: dict = {
    DETECTOR_TYPE.GrouningDINO: {
        "SwinT": {
            "model": "groundingdino_swint_ogc.pth",
            "config": "groundingdino/config/GroundingDINO_SwinT_OGC.py",
        },
        "SwinB": {
            "model": "groundingdino_swinb_cogcoor.pth",
            "config": "groundingdino/config/GroundingDINO_SwinB_cfg.py",
        },
    },
    DETECTOR_TYPE.YOLOWorld: {
        "Small": "s",
        "Medium": "m",
        "Large": "l",
    },
}


class GroundingDINOModel:
    def __init__(
        self,
        model_name: str,
        model_version: str,
        device: str = "cuda",
        weights_path: str = "weights",
        **kwargs,
    ) -> None:
        """Initializes the GroundingDINO class
        Args:
            model_name (str): Name of the model
            model_version (str): Version of the model
            device (torch.device): device to run the model
        """
        self.model_name = model_name
        self.model_version = model_version
        self.device = device
        self.weights_path = weights_path
        self.model = self.create_detector_model(**kwargs)

    def _get_base_path(self):
        base_path = (
            os.path.dirname(os.path.abspath(__file__))
            + "/../third_party/"
            + "GroundingDINO/"
        )
        return base_path

    def create_detector_model(self, **kwargs):
        base_path = self._get_base_path()
        config_path = (
            base_path + MODEL_DICT[self.model_name][self.model_version]["config"]
        )
        model_path = os.path.join(
            self.weights_path,
            "GroundingDINO",
            MODEL_DICT[self.model_name][self.model_version]["model"],
        )
        model = load_model(config_path, model_path)
        return model

    def cxcxwh_norm_to_xyxy(self, box, image_width, image_height):
        center_x, center_y, width, height = box
        x1 = (center_x - (width / 2)) * image_width
        y1 = (center_y - (height / 2)) * image_height
        x2 = (center_x + (width / 2)) * image_width
        y2 = (center_y + (height / 2)) * image_height
        return [x1, y1, x2, y2]

    def detect_objects(self, image, prompt):
        """Get detections from image using GroundingDINO
        Args:
            image (PIL.Image.Image): input image
            prompt (str): text prompt
        Returns:
            boxes (torch.tensor): detection's boxes tensor
            logits (torch.tensor): detection confidence scores tensor
            phrases (List(str)): list of class labels
        """

        BOX_TRESHOLD = 0.25
        TEXT_TRESHOLD = 0.25
        transform = T.Compose(
            [
                T.ResizeDebug((640, 640)),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
        image_transformed, _ = transform(image, None)

        boxes, logits, phrases = predict(
            model=self.model,
            image=image_transformed,
            caption=prompt,
            box_threshold=BOX_TRESHOLD,
            text_threshold=TEXT_TRESHOLD,
        )
        # xyxy
        boxes = torch.tensor(
            [self.cxcxwh_norm_to_xyxy(box, image.width, image.height) for box in boxes]
        )
        return boxes, logits, phrases


class YOLOWorldModel:
    def __init__(
        self, model_name: str, model_version: str, device: str = "cuda", **kwargs
    ) -> None:
        """Initializes the YOLOWorld class
        Args:
            model_name (str): Name of the model
            model_version (str): Version of the model
            device (torch.device): device to run the model
        """
        self.model_name = model_name
        self.model_version = model_version
        self.device = device
        self.model = self.create_detector_model(**kwargs)

    def cxcxwh_to_xyxy(self, box):
        center_x, center_y, width, height = box
        x1 = center_x - (width / 2)
        y1 = center_y - (height / 2)
        x2 = center_x + (width / 2)
        y2 = center_y + (height / 2)
        return [x1, y1, x2, y2]

    def create_detector_model(self, **kwargs):
        model_id = f"yolo_world/{MODEL_DICT[self.model_name][self.model_version]}"
        model = YOLOWorld(model_id=model_id)
        return model

    def detect_objects(self, image, prompt):
        """Get detections from image using GroundingDINO
        Args:
            image (PIL.Image.Image): input image
            prompt (str): text prompt
        Returns:
            boxes (torch.tensor): detection's boxes tensor
            logits (torch.tensor): detection confidence scores tensor
            phrases (List(str)): list of class labels
        """
        CONFIDENCE = 0.04

        classes = [label.strip() for label in prompt.split(".")]
        self.model.set_classes(classes)
        detections = self.model.infer(image, confidence=CONFIDENCE).predictions
        # xyxy
        boxes = torch.tensor(
            [
                self.cxcxwh_to_xyxy([pred.x, pred.y, pred.width, pred.height])
                for pred in detections
            ]
        )
        logits = torch.tensor([pred.confidence for pred in detections])
        phrases = [pred.class_name for pred in detections]
        return boxes, logits, phrases
