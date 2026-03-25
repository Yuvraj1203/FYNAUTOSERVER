from beanie import Document

class PipelinePayload(Document):
    tenantName: str
    forAndroid: bool
    forIos: bool

    class Settings:
        name="pipeline_payload"