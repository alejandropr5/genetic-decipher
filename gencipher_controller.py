from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from fastapi import Depends, Request
from fastapi_utils.inferring_router import InferringRouter

from gencipher.model import GeneticDecipher


class Body(BaseModel):
    cipher_text: str


router = InferringRouter()


async def get_model(request: Request):
    return request.app.state.model


@cbv(router)
class GencipherController:
    model: GeneticDecipher = Depends(get_model)

    @router.get("/hi")
    def hi(self):
        return "Hi from GencipherController"

    @router.post("/decipher")
    def decipher(self, body: Body):
        cipher_text = body.cipher_text
        predictions = self.model.decipher(cipher_text)
        return {"predictions": predictions}
