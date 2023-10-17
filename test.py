from routers.gencipher_controller import RequestBody
from gencipher.model import GeneticDecipher


def main():
    gencipher = GeneticDecipher()
    body = RequestBody(cipher_text="Hello World", max_iter=21)

    result = gencipher.decipher(**body.dict())

    print(result)
    print(len(gencipher.history["key"]))


if __name__ == "__main__":
    main()
