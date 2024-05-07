from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost",
    "http://localhost:8080",
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

@app.post("/convert")
async def convert_image(image: UploadFile = File(...)):
    try:
        # Open the uploaded image
        image_bytes = await image.read()
        #creates a PIL Image object by opening the image data stored in the image_bytes variable.
        # It uses io.BytesIO to wrap the image data as a file-like object.
        input_image = Image.open(io.BytesIO(image_bytes))

        # Convert image to JPEG format
        #This line creates an empty BytesIO object, which will be used to store the converted image data.
        output_image = io.BytesIO()
        #This line converts the input image to the RGB color mode 
        #(if it's not already in RGB) and saves it as a JPEG image to the output_image BytesIO object.
        input_image.convert("RGB").save(output_image, "JPEG")
        output_image.seek(0)

        # Convert the output image to byte array
        byte_array = output_image.getvalue()

        # Return the byte array as response
        return Response(content=byte_array, media_type="image/jpeg")
    except Exception as e:
        return {"error": str(e)}
