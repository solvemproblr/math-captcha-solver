import base64
import io

import numpy as np
from PIL import Image
from fastapi import FastAPI, HTTPException

import solver

app = FastAPI()

@app.post("/captcha_solver")
async def solve_captcha(image_data: dict):
    try:

        image_base64 = image_data.get("captcha_img")
        image_data = base64.b64decode(image_base64)
        image_pil = Image.open(io.BytesIO(image_data))
        image_np = np.array(image_pil)

        result = solver.solve_math_expression(image_np)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error processing image")