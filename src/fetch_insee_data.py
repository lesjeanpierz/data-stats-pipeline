import pandas as pd

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

