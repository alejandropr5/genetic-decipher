from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from fastapi import Depends, Request
from fastapi_utils.inferring_router import InferringRouter

from gencipher.model import GeneticDecipher


class Body(BaseModel):
    cipher_text: str
    max_iter: int = 20
    n_population: int = 100


class ResponseBody(BaseModel):
    plain_text: str
    history: dict[str, list]


async def get_model(request: Request):
    return request.app.state.model


router = InferringRouter()


@cbv(router)
class GencipherController:
    model: GeneticDecipher = Depends(get_model)

    @router.get("/hi")
    def hi(self):
        return "Hi from GencipherController"

    @router.post("/decipher")
    def decipher(self, body: Body):
        plain_text = self.model.decipher(cipher_text=body.cipher_text,
                                         max_iter=body.max_iter,
                                         n_population=body.n_population)

        return ResponseBody(plain_text=plain_text,
                            history=self.model.history)
