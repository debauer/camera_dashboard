from dataclasses import dataclass


@dataclass
class DeviceConfig:
    name: str
    serve_port: int
    stream_resolution: str
    stream: str = ""
    fps: int = 25
    static_image: str = ""
