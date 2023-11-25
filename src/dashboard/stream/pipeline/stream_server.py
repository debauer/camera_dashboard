from __future__ import annotations

from numpy import uint8, zeros



class StreamServer(SandNode, EnrichedSubscriber):
    def __init__(
        self,
        name: str,
        port: int,
        resolution: Dimensions,
        communication_config: CommunicationConfig,
        source: CollectAble[EnrichedSubscriber],
    ) -> None:
        SandNode.__init__(self, communication_config)
        server_adress = "0.0.0.0"
        self.log.d(
            f"start MJPEG Server for {name} on {server_adress}:{port}",
            "StreamServer",
        )
        self.server = FrameServer((server_adress, port), MjpegHandler)
        self.name = name
        source.subscribe(self)

        self.subscribe_topic(f"NeuralNetwork/{name}/data/boxes", self.push_neural_frame)
        self.subscribe_topic("NeuralNetwork/all/data/num_classes", self.set_num_classes)

        # noinspection PyTypeChecker
        self.server.frame = zeros(
            (
                resolution.height,
                resolution.width,
                3,
            ),
            dtype=uint8,
        )
        self.server.shutdown_event = self.shutdown_event
        self.create_thread(
            target=self.serve,
            name=f"mj_{name}",
            start=True,
        )

    def shutdown(self) -> None:
        self.log.i(
            f"Shutdown called for {self.__class__.__name__} / {self.name}",
            "shutdown",
        )
        self.server.shutdown()
        SandNode.shutdown(self)

    def push_neural_frame(self, _: Topic, boxes: SandBoxes) -> None:
        self.server.boxes = boxes

    def set_num_classes(self, _: Topic, num_classes: int) -> None:
        self.server.num_classes = num_classes

    def push_frame(self, frame: EnrichedFrame) -> None:
        self.server.frame = frame.frame

    def serve(self) -> None:
        self.log.d(f"{self.name}", "serve")
        self.server.serve_forever()
