from pydantic import BaseModel
from fastapi_utils.cbv import cbv
from fastapi import Depends, Request
from fastapi_utils.inferring_router import InferringRouter

from gencipher.model import GeneticDecipher


class RequestBody(BaseModel):
    cipher_text: str
    max_iter: int = 20
    n_population: int = 100
    mutation_type: str = "scramble"
    crossover_type: str = "full"
    mutation_rate: float = 0.01
    crossover_rate: float = 0.6


class ResponseBody(BaseModel):
    plain_text: str
    history: dict[str, list]


async def get_model(request: Request):
    return request.app.state.model


router = InferringRouter()


@cbv(router)
class GencipherController:
    model: GeneticDecipher = Depends(get_model)

    @router.post("/decipher")
    def decipher(self, body: RequestBody):
        plain_text = self.model.decipher(**body.dict())

        return ResponseBody(plain_text=plain_text,
                            history=self.model.history)
