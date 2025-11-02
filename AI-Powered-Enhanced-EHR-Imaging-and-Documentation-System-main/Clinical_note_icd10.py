import pandas as pd
import os
from transformers import pipeline

# Load datasets
df_health = pd.read_csv("healthcare_dataset.csv")
df_icd = pd.read_csv("ICD10codes.csv")

# Folder containing all processed images (from Module 1)
processed_folder = "Xray_processed"
image_files = [f for f in os.listdir(processed_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]

# Hugging Face text generation model
generator = pipeline("text2text-generation", model="google/flan-t5-base")

# ICD column setup
df_icd.columns = df_icd.columns.str.strip()
disease_col = [c for c in df_icd.columns if "Disease" in c or "Cholera" in c][0]
code_col = df_icd.columns[0]

records = []

for i, image_name in enumerate(image_files):
    # Pick corresponding patient (loop through dataset if fewer images)
    patient = df_health.iloc[i % len(df_health)]
    
    age = patient.get("Age", "N/A")
    gender = patient.get("Gender", "N/A")
    symptom = patient.get("Symptom", "N/A")
    diagnosis = patient.get("Diagnosis", "N/A")
    lab_result = patient.get("Lab_Result", "N/A")
    
    # ICD-10 code match
    match = df_icd[df_icd[disease_col].str.lower().str.contains(str(diagnosis).lower()[:5], na=False)]
    icd_code = match[code_col].iloc[0] if not match.empty else "N/A"
    
    # Hugging Face prompt
    prompt = f"""
    Generate a concise clinical summary:
    Age: {age}, Gender: {gender}, Symptom: {symptom}, Lab Result: {lab_result},
    Diagnosis: {diagnosis}, ICD-10 Code: {icd_code}.
    """
    summary = generator(prompt, max_length=120, do_sample=True)[0]['generated_text']
    
    records.append({
        "Image_File": image_name,
        "Diagnosis": diagnosis,
        "ICD10_Code": icd_code,
        "Generated_Summary": summary
    })

# Save all summaries
final_df = pd.DataFrame(records)
final_df.to_csv("Final_Clinical_Notes_All.csv", index=False)

print(f"✅ Clinical summaries generated for {len(records)} images!")
print(final_df.head())
