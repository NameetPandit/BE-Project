from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import shutil
import uvicorn
from ocr_module import detect_license_plate
import mysql.connector
from mysql.connector import Error

# ✅ FastAPI App
app = FastAPI()

# ✅ MySQL Database Connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="vehicle_access"
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# ✅ Upload Directory
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Home Route
@app.get("/")
def home():
    return {"message": "Vehicle Access Control API is Running!"}

# ✅ Lookup Owner Name in Database
# ✅ Lookup Owner Name in Database
def get_owner_name(plate_number):
    """Fetch the owner's name from the database based on plate number."""
    conn = connect_db()
    owner_name = "Unknown"

    if conn:
        try:
            cursor = conn.cursor()
            
            # ✅ Forcefully fetch all results to avoid "Unread result" error
            query = "SELECT owner_name FROM license_plates WHERE plate_number = %s"
            
            cursor.execute(query, (plate_number,))
            
            # ✅ Fetch all results before closing the cursor
            result = cursor.fetchall()  

            # ✅ Get the first result (if exists)
            if result:
                owner_name = result[0][0]

        except Error as e:
            print(f"Database Error: {e}")
        finally:
            cursor.close()  # ✅ Ensure cursor is closed properly
            conn.close()    # ✅ Close the connection after the query

    return owner_name

# ✅ Upload Image and OCR Route (API route first)
@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded image
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Perform OCR and get plate + owner name
    plate_number = detect_license_plate(file_path)
    # ✅ Fetch owner name separately in main.py
    owner_name = get_owner_name(plate_number)

    # Return the detected plate and owner name
    return {
        "plate_number": plate_number,
        "owner_name": owner_name if owner_name else "Unknown"
    }

# ✅ Mount the Static Folder **AFTER** the API routes
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# ✅ Run the FastAPI Server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, reload=True)
