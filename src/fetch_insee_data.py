import requests
import pandas as pd

# === Téléchargement automatique du fichier depuis le site de l'INSEE ===
url = "https://www.insee.fr/fr/statistiques/fichier/8574712/t_2101.xlsx"
file_path = Path("src/t_2101.xlsx")

if not file_path.exists():
    print("Téléchargement du fichier depuis l'INSEE...")
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)
    print("Fichier téléchargé :", file_path)
else:
    print("Fichier déjà présent :", file_path)

# === Lecture propre du fichier ===
df = pd.read_excel("t_2101.xlsx", sheet_name="T_2101", header=5)

# Récupérer la ligne des années (ligne 3)
years_row = pd.read_excel("t_2101.xlsx", sheet_name="T_2101", header=None, skiprows=3, nrows=1)
years = years_row.iloc[0, 2:].dropna().astype(int).tolist()

# Remplacer les noms de colonnes par les années
new_columns = df.columns[:2].tolist() + years
df.columns = new_columns

# === Extraire la ligne B6G ===
b6g_row = df[df.iloc[:, 0] == "B6G"].iloc[0]
revenu = b6g_row[2:].astype(float)

print("Premières années :")
print(revenu.head(10))
print("\nDernières années :")
print(revenu.tail(10))
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
revenu.plot(marker='o')
plt.title("Revenu disponible brut des ménages (INSEE, 1959–2024)")
plt.xlabel("Année")
plt.ylabel("Milliards d'euros")
plt.grid(True)
plt.tight_layout()
plt.savefig("revenu_disponible_brut.png")
print("Graphique sauvegardé : revenu_disponible_brut.png")
# === Export Excel ===
revenu.to_excel("revenu_disponible_brut.xlsx", header=["Revenu disponible brut (Mds €)"])
print("Fichier Excel sauvegardé : revenu_disponible_brut.xlsx")

