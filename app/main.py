from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from typing import Optional
import io
import zipfile
import pandas as pd
import geopandas as gpd
import pdfplumber
import requests
from bs4 import BeautifulSoup
import openai
import json

app = FastAPI()

import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY



# 📚 Utility Functions
from app.utils import (
    extract_answer_from_csv,
    extract_text_from_pdf,
    extract_geospatial_data,
    scrape_web_data,
    query_llm,
)


@app.post("/api/")
async def get_answer(
    question: str = Form(...), file: Optional[UploadFile] = File(None)
):
    try:
        # 🔎 Handle file if provided
        if file:
            file_ext = file.filename.split(".")[-1].lower()

            if file_ext == "zip":
                answer = extract_answer_from_csv(io.BytesIO(await file.read()))
            elif file_ext == "pdf":
                answer = extract_text_from_pdf(io.BytesIO(await file.read()))
            elif file_ext in ["shp", "geojson", "kml"]:
                answer = extract_geospatial_data(file)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported file format: {file_ext}")
        # 🌐 Handle web scraping questions
        elif "http" in question:
            answer = scrape_web_data(question)
        # 🤖 Default to LLM for text questions
        else:
            answer = query_llm(question)

        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}
