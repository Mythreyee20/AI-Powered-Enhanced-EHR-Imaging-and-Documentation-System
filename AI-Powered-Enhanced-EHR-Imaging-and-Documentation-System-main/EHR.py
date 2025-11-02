import os
import cv2
import pandas as pd
import plotext as plt  

# 1. IMAGE PREPROCESSING (Normal + Pneumonia)
folders = ["Normal", "Pneumonia"]
processed_folder = "Xray_processed"
os.makedirs(processed_folder, exist_ok=True)

size = (256, 256)
image_counts = {}

for folder in folders:
    count = 0
    for img_file in os.listdir(folder):
        if img_file.lower().endswith((".jpeg", ".jpg", ".png")):
            img_path = os.path.join(folder, img_file)
            img = cv2.imread(img_path)
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, size)
            save_path = os.path.join(processed_folder, f"{folder}_{img_file}")
            cv2.imwrite(save_path, resized)
            count += 1
    image_counts[folder] = count

print("✅ Images preprocessed! Saved in:", processed_folder)

# Terminal bar chart using plotext
plt.bar(list(image_counts.keys()), list(image_counts.values()))
plt.title("Image Class Distribution (Normal vs Pneumonia)")
plt.show()
print("✅ Visualization complete!")

# 2. TEXT PREPROCESSING (mtsamples.csv)
df_text = pd.read_csv("mtsamples.csv")
df_text.dropna(inplace=True)

text_col = df_text.columns[0]
df_text[text_col] = df_text[text_col].astype(str).str.lower()
df_text.to_csv("mtsamples_clean.csv", index=False)
print(f"✅ Text preprocessing done! Column used: {text_col}")

# 3. STRUCTURED DATA (healthcare_dataset & ICD10)
df_health = pd.read_csv("healthcare_dataset.csv")
df_icd = pd.read_csv("ICD10codes.csv")

print(f"✅ Healthcare dataset rows: {len(df_health)}")
print(f"✅ ICD10 dataset rows: {len(df_icd)}")

print("\n🎯 Completed Successfully – Data Cleaned, Labeled, and Visualized!")