import logging
import unittest
from typing import Optional

import torch
from parameterized import parameterized

from birder.core.net.base import net_factory
from birder.core.net.detection import base

logging.disable(logging.CRITICAL)


class TestNetDetection(unittest.TestCase):
    @parameterized.expand(  # type: ignore[misc]
        [
            ("faster_rcnn", None, ("resnet_v2", 50)),
            ("retinanet", None, ("mobilenet_v3", 1)),
            ("ssd", None, ("efficientnet_v2", 0)),
        ]
    )
    def test_net_detection(self, network_name: str, net_param: Optional[float], encoder: tuple[str, float]) -> None:
        backbone = net_factory(encoder[0], 3, 10, encoder[1])
        n = base.detection_net_factory(network_name, 10, backbone, net_param=net_param)
        size = n.default_size
        backbone.adjust_size(size)

        n.eval()
        out = n(torch.rand((1, 3, size, size)))
        (detections, losses) = out
        self.assertEqual(len(losses), 0)
        for detection in detections:
            for key in ["boxes", "labels", "scores"]:
                self.assertFalse(torch.isnan(detection[key]).any())

        n.train()
        out = n(
            torch.rand((1, 3, size, size)),
            targets=[
                {
                    "boxes": torch.tensor([[10.1, 10.1, 30.2, 40.2]]),
                    "labels": torch.tensor([1]),
                }
            ],
        )
        (detections, losses) = out
        self.assertGreater(len(losses), 0)
        for loss in losses.values():
            self.assertFalse(torch.isnan(loss).any())

        for detection in detections:
            for key in ["boxes", "labels", "scores"]:
                self.assertFalse(torch.isnan(detection[key]).any())

        torch.jit.script(n)
