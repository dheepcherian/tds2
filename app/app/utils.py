import zipfile
import pandas as pd
import pdfplumber
import geopandas as gpd
import requests
from bs4 import BeautifulSoup
import openai
import io


# 🎯 Extract answer from a CSV inside a ZIP
def extract_answer_from_csv(file):
    with zipfile.ZipFile(file) as z:
        csv_filename = [f for f in z.namelist() if f.endswith(".csv")][0]
        with z.open(csv_filename) as csv_file:
            df = pd.read_csv(csv_file)
            # Return the first value from the "answer" column
            return str(df["answer"].iloc[0])


# 📄 Extract text from a PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text if text else "No text found in the PDF."


# 🌍 Extract information from geospatial files (Shapefile, GeoJSON)
def extract_geospatial_data(file):
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext == "geojson":
        gdf = gpd.read_file(io.BytesIO(file.file.read()))
    elif file_ext == "shp":
        gdf = gpd.read_file(file.file)
    else:
        return "Unsupported geospatial format"

    # Example: Return the total area as the answer
    area_sum = gdf.geometry.area.sum()
    return f"Total area covered: {area_sum:.2f} sq units."


# 🌐 Scrape web content and extract relevant information
def scrape_web_data(question):
    url = question.split(" ")[-1]  # Extract URL from question
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Example: Find value in <span class="price">...</span>
        price_tag = soup.find("span", {"class": "price"})
        if price_tag:
            return f"The price is {price_tag.text}"
        else:
            return "Price field not found on the page."
    return "Unable to scrape the webpage."


# 🤖 Query LLM for theoretical/conceptual questions
def query_llm(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": question}],
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error querying LLM: {str(e)}"
