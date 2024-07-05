import os

import numpy as np
import torch
import torchvision
from typing import Any, Generator, List, Tuple, Dict

from ovsegmentation.knowledge_mapping.processors.types import SAM_TYPE

# mobilesam
# from ovsegmentation.knowledge_mapping.third_party.mobilesam import mobile_sam

from ovsegmentation.knowledge_mapping.processors.utils import (
    preprocess,
    get_preprocess_shape,
    apply_boxes,
    mask_postprocessing,
    area_from_rle,
    mask_to_rle_pytorch,
)


MODEL_DICT: dict = {
    SAM_TYPE.MobileSAM: {
        "v2": {
            "trt_encoder_engine": "l2_encoder.engine",
            "trt_decoder_engine": "mobilesamv2_decoder.engine",
            "trt_detector_engine": "ObjectAwareModel.engine",
        },
    }
}


class BaseModel:
    def __init__(self, model_name: str, model_version: str, mode: str, device, weights_path) -> None:
        self.model_name = model_name
        self.model_version = model_version
        self.mode = mode
        self.device = device
        self.weights_path = weights_path

    def create_sam_model(self):
        pass

    def generate(self, input):
        """Class-agnostic segmentation - SegEvery"""
        pass

    def predict(self, input):
        """Promptable segmentation - SegAny"""
        pass

def load_trt_mobilesamv2_model(weights_path) -> Tuple[Any, ...]:
    import tensorrt as trt
    from torch2trt import TRTModule
    from ovsegmentation.knowledge_mapping.third_party.mobilesam.MobileSAMv2.mobilesamv2_trt.promt_mobilesamv2 import (
        ObjectAwareModel as ObjectAwareModelTRT,
    )

    # detector
    detector_path = os.path.join(weights_path, "MobileSAMv2", MODEL_DICT[SAM_TYPE.MobileSAM]["v2"]["trt_detector_engine"])
    ObjAwareModel = ObjectAwareModelTRT(detector_path)
    ObjAwareModel.init()

    # encoder
    with trt.Logger() as logger, trt.Runtime(logger) as runtime:
        encoder_path = os.path.join(weights_path, "MobileSAMv2", MODEL_DICT[SAM_TYPE.MobileSAM]["v2"]["trt_encoder_engine"])
        with open(encoder_path, "rb") as f:
            engine_bytes = f.read()
        engine = runtime.deserialize_cuda_engine(engine_bytes)
    trt_encoder = TRTModule(
        engine, input_names=["input_image"], output_names=["image_embeddings"]
    )
    # decoder
    with trt.Logger() as logger, trt.Runtime(logger) as runtime:
        decoder_path = os.path.join(weights_path, "MobileSAMv2", MODEL_DICT[SAM_TYPE.MobileSAM]["v2"]["trt_decoder_engine"])
        with open(decoder_path, "rb") as f:
            engine_bytes = f.read()
        engine = runtime.deserialize_cuda_engine(engine_bytes)
    trt_decoder = TRTModule(
        engine,
        input_names=["image_embeddings", "point_coords", "point_labels"],
        output_names=["masks", "iou_predictions"],
    )
    return trt_encoder, trt_decoder, ObjAwareModel

def generate_masks_mobilesamv2_trt_model(
    input,
    model,
    ObjAwareModel,
    device,
):
    origin_image_size = input.shape[:2]
    img = preprocess(input, img_size=512, device=device)
    input_size = get_preprocess_shape(*origin_image_size, long_side_length=512)
    obj_results = ObjAwareModel(
        input,
        device=device,
        retina_masks=True,
        imgsz=640,
        conf=0.3,
        iou=0.7,
    )
    input_boxes = obj_results[0].boxes.xyxy
    boxes = input_boxes.cpu().numpy()
    boxes = apply_boxes(boxes, origin_image_size, input_size).astype(np.float32)
    boxes = torch.from_numpy(boxes).to(device)
    n = boxes.shape[0]
    batch_size = 16
    num_batches = n // batch_size + (1 if n % batch_size != 0 else 0)

    # print("---" * 20, model)
    image_embedding = model["encoder"](img)
    image_embedding = image_embedding[0].reshape(1, 256, 64, 64)

    result_mask = None
    iou_array = None
    for batch in range(num_batches):
        start_idx = batch * batch_size
        end_idx = min((batch + 1) * batch_size, boxes.shape[0])
        batch = boxes[start_idx:end_idx]

        box_label = np.array(
            [[2, 3] for _ in range(batch.shape[0])], dtype=np.float32
        ).reshape((-1, 2))
        point_coords = batch
        point_labels = box_label

        inputs = (
            image_embedding,
            point_coords,
            torch.from_numpy(point_labels).to(device),
        )
        low_res_masks, iou_pred = model["decoder"](*inputs)
        low_res_masks = low_res_masks.reshape(1, -1, 256, 256)
        iou_pred = iou_pred.cpu().numpy()

        masks = mask_postprocessing(low_res_masks, origin_image_size)[0]
        masks = masks > 0.0
        masks = masks.cpu().numpy()
        result_mask = (
            masks if result_mask is None else np.concatenate((result_mask, masks))
        )
        iou_array = (
            iou_pred if iou_array is None else np.concatenate((iou_array, iou_pred))
        )

    masks = np.asarray(result_mask).reshape(
        -1, origin_image_size[0], origin_image_size[1]
    )

    masks = torch.from_numpy(masks)
    bboxes = torchvision.ops.masks_to_boxes(masks)
    iou_array = np.squeeze(iou_array)
    res = []
    for bbox, mask, iou in zip(bboxes, masks, iou_array):
        ann = {
            "segmentation": mask.cpu().numpy(),
            "area": area_from_rle(mask_to_rle_pytorch(mask.unsqueeze(0))[0]),
            "bbox": bbox.to(int).cpu().tolist(),
            "predicted_iou": iou,
            "point_coords": [],
            "stability_score": 1.0,
            "crop_box": [],
        }
        res.append(ann)
    return res

def predict_masks_mobilesamv2_trt_model(input, bboxes, model, device):
    origin_image_size = input.shape[:2]
    img = preprocess(input, img_size=512, device=device)
    input_size = get_preprocess_shape(*origin_image_size, long_side_length=512)

    boxes = bboxes.cpu().numpy()
    boxes = apply_boxes(boxes, origin_image_size, input_size).astype(np.float32)
    boxes = torch.from_numpy(boxes).to(device)
    n = boxes.shape[0]
    batch_size = 16
    num_batches = n // batch_size + (1 if n % batch_size != 0 else 0)

    image_embedding = model["encoder"](img)
    image_embedding = image_embedding[0].reshape(1, 256, 64, 64)

    result_mask = None
    iou_array = None
    for batch in range(num_batches):
        start_idx = batch * batch_size
        end_idx = min((batch + 1) * batch_size, boxes.shape[0])
        batch = boxes[start_idx:end_idx]

        box_label = np.array(
            [[2, 3] for _ in range(batch.shape[0])], dtype=np.float32
        ).reshape((-1, 2))
        point_coords = batch
        point_labels = box_label

        inputs = (
            image_embedding,
            point_coords,
            torch.from_numpy(point_labels).to(device),
        )
        low_res_masks, iou_pred = model["decoder"](*inputs)
        low_res_masks = low_res_masks.reshape(1, -1, 256, 256)
        iou_pred = iou_pred.cpu().numpy()

        masks = mask_postprocessing(low_res_masks, origin_image_size)[0]
        masks = masks > 0.0
        masks = masks.cpu().numpy()
        result_mask = (
            masks if result_mask is None else np.concatenate((result_mask, masks))
        )
        iou_array = (
            iou_pred if iou_array is None else np.concatenate((iou_array, iou_pred))
        )

    masks = np.asarray(result_mask).reshape(
        -1, origin_image_size[0], origin_image_size[1]
    )

    masks = torch.from_numpy(masks)
    iou_array = (
        np.squeeze(iou_array)
        if iou_array.shape != (1, 1)
        else np.squeeze(iou_array, axis=1)
    )
    res = []
    for bbox, mask, iou in zip(bboxes, masks, iou_array):
        ann = {
            "segmentation": mask.cpu().numpy(),
            "area": area_from_rle(mask_to_rle_pytorch(mask.unsqueeze(0))[0]),
            "bbox": bbox.detach().cpu().numpy(),
            "predicted_iou": iou,
            "point_coords": [],
            "stability_score": 1.0,
            "crop_box": [],
        }
        res.append(ann)
    return res


class MobileSamModel(BaseModel):
    def __init__(
        self,
        model_name,
        model_version,
        mode,
        device,
        weights_path,
        v2_inference_type: str = "trt",
        **kwargs,
    ) -> None:
        super().__init__(model_name, model_version, mode, device, weights_path)
        # NOTE: supported v2_inference_type: ["sam", "trt"]
        self.v2_inference_type = v2_inference_type
        (
            self.model,
            self.mask_generator,
            self.predictor,
            self.ObjAwareModel,
            self.PromptGuidedDecoder,
        ) = self.create_sam_model()

    def create_sam_model(self):
        ObjAwareModel, PromptGuidedDecoder = None, None

        if self.model_version == "v2":
            print(
                "[DEBUG] [create_sam_model]",
                "***" * 20,
                self.model_name,
                self.model_version,
                self.v2_inference_type,
            )

            weights_paths = self.weights_path

            if self.v2_inference_type == "trt":
                trt_encoder, trt_decoder, ObjAwareModel = load_trt_mobilesamv2_model(
                    weights_paths
                )
                model = {"encoder": trt_encoder, "decoder": trt_decoder}

            if self.v2_inference_type == "trt":
                generator = None
                predictor = None
            else:
                raise ValueError

        return (
            model,
            generator,
            predictor,
            ObjAwareModel,
            PromptGuidedDecoder,
        )

    @staticmethod
    def batch_iterator(batch_size: int, *args) -> Generator[List[Any], None, None]:
        assert len(args) > 0 and all(
            len(a) == len(args[0]) for a in args
        ), "Batched iteration must have inputs of all the same size."
        n_batches = len(args[0]) // batch_size + int(len(args[0]) % batch_size != 0)
        for b in range(n_batches):
            yield [arg[b * batch_size : (b + 1) * batch_size] for arg in args]

    def generate(self, input):
        if self.model_version == "v1":
            return self.mask_generator.generate(input)

        if self.model_version == "v2":
            if self.v2_inference_type == "trt":
                res = generate_masks_mobilesamv2_trt_model(
                    input, self.model, self.ObjAwareModel, self.device
                )
            else:
                # "sam"
                res = self.mask_generator.generate(input)
        return res

    def predict(self, input, bboxes):
        if self.model_version == "v2":
            if self.v2_inference_type == "trt":
                res = predict_masks_mobilesamv2_trt_model(
                    input, bboxes, self.model, self.device
                )
            else:
                # "sam"
                res = predict_masks_mobilesam_model(self.predictor, bboxes, self.device)
        else:
            raise NotImplementedError
        return res
