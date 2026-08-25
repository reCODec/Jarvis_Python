import speech_recognition as sr
import webbrowser
import os
import pyautogui
import time
import requests
import threading
import tkinter as tk


# --- L'INTERFACE GRAPHIQUE ---
def mettre_a_jour_texte(texte):
    """Change le texte de la boîte de dialogue"""
    label_jarvis.config(text=texte)


def parler(texte):
    """Affiche le texte à l'écran au lieu de le lire à voix haute"""
    print(f"🤖 Jarvis : {texte}")
    # On met à jour la fenêtre graphique
    fenetre.after(0, mettre_a_jour_texte, texte)


# --- INITIALISATION DE L'ECOUTE ---
def ecouter():
    """Écoute le micro et retourne le texte en minuscules"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(" J'écoute...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            # On limite l'enregistrement à 7 secondes max par phrase
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
            texte = recognizer.recognize_google(audio, language="fr-FR").lower()
            print(f" Toi : {texte}")
            return texte

        except sr.WaitTimeoutError:
            return ""  # Si personne ne parle
        except sr.UnknownValueError:
            return ""  # S'il ne comprend pas
        except sr.RequestError:
            print(" Erreur de connexion Google")
            return ""


# --- BOUCLE PRINCIPALE EN ARRIÈRE-PLAN ---
def demarrer_jarvis():
    parler("Système en ligne. J'attends vos instructions.")

    while True:
        commande = ecouter()

        if not commande:
            continue

        # --- DISCUSSIONS BASIQUES ---
        if "bonjour" in commande:
            parler("Bonjour chef. J'espère que vous allez bien.")

        elif "merci" in commande:
            parler("C'est normal, je suis programmé pour ça.")

        # --- GESTION DU SYSTÈME ---
        elif "au revoir" in commande or "quitter" in commande or "arrête-toi" in commande or "meurs" in commande or "décède" in commande:
            parler("Très bien. Arrêt du système. À bientôt.")
            time.sleep(2)
            # Ferme la fenêtre graphique, ce qui coupe le programme
            fenetre.after(0, fenetre.destroy)
            break

        # --- CONTRÔLE SPOTIFY ET VALO ---
        elif "lance ma playlist spotify" in commande or "lance spotify" in commande or "ouvre spotify" in commande:
            parler("Bien sûr monsieur. Ouverture de Spotify.")
            webbrowser.open("https://open.spotify.com/playlist/37i9dQZF1F5p3rmiWPIYgZ?si=bb2c966ae7e24b81")
            time.sleep(4.5)
            pyautogui.press('playpause')

        elif "ferme ma playlist spotify" in commande or "ferme spotify" in commande or "quit spotify" in commande:
            parler("Fermeture de la musique.")
            os.system("taskkill /F /IM Spotify.exe")

        elif "lance valo" in commande or "lance valorant" in commande:
            parler("Je lance valorant.")
            chemin_valo = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Riot Games\VALORANT.lnk"
            try:
                os.startfile(chemin_valo)
            except Exception:
                parler("Chemin de Valorant introuvable.")

        elif "ferme valorant" in commande or "rage quit" in commande:
            parler("Fermeture du jeu.")
            os.system("taskkill /F /IM VALORANT-Win64-Shipping.exe")
            os.system("taskkill /F /IM RiotClientServices.exe")

        # --- CONTRÔLE NAVIGATEUR (YOUTUBE & ANIME) ---
        elif "lance youtube" in commande or "ouvre youtube" in commande:
            parler("Je lance youtube.")
            webbrowser.open("https://www.youtube.com/")

        elif "ferme youtube" in commande or "quitte youtube" in commande or "ferme l'onglet" in commande:
            parler("Je ferme l'onglet.")
            pyautogui.hotkey('ctrl', 'w')

        elif "lance animé sama" in commande or "ouvre animé sama" in commande or "ouvre animé" in commande or "lance animé" in commande:
            parler("Je lance animé sama.")
            webbrowser.open("https://anime-sama.to/")

        elif "ferme animé sama" in commande or "quitte animé sama" in commande:
            parler("Je ferme l'onglet.")
            pyautogui.hotkey('ctrl', 'w')

        # --- API RECHERCHE WIKIPEDIA AVANCÉE ---
        elif "recherche" in commande or "qui est" in commande or "c'est quoi" in commande or "explique-moi ce qu'est" in commande or "c'est qui" in commande or "ca veut dire quoi" in commande:
            sujet = commande.replace("recherche", "").replace("qui est", "").replace("c'est quoi", "").replace("jarvis",
                                                                                                               "").replace(
                "est-ce que tu peux me dire", "").replace("parle-moi de", "").strip()

            if not sujet:
                parler("Je n'ai pas compris ce que je dois chercher.")
                continue

            parler(f"Laisse-moi chercher {sujet}...")

            try:
                url = "https://fr.wikipedia.org/w/api.php"
                params = {
                    "action": "query",
                    "prop": "extracts",
                    "exsentences": 4,
                    "explaintext": 1,
                    "generator": "search",
                    "gsrsearch": sujet,
                    "gsrlimit": 1,
                    "format": "json"
                }

                headers = {"User-Agent": "JarvisProject/1.0"}
                reponse = requests.get(url, params=params, headers=headers)
                data = reponse.json()

                if "query" in data and "pages" in data["query"]:
                    pages = data["query"]["pages"]
                    premiere_page = list(pages.values())[0]
                    resume = premiere_page.get("extract", "")
                    titre = premiere_page.get("title", "")

                    if resume:
                        parler(f"Wiki ({titre}) : {resume}")
                    else:
                        parler(f"J'ai trouvé la page de {titre}, mais elle est vide.")
                else:
                    parler("Je n'ai absolument rien trouvé à ce sujet.")

            except Exception as e:
                parler("J'ai eu un problème de connexion.")
                print(f"Erreur API : {e}")


# ==========================================
# --- CRÉATION DE LA FENÊTRE PRINCIPALE ---
# ==========================================
fenetre = tk.Tk()
fenetre.title("Jarvis HUD")

# Configuration de la taille et de la position (500x120 pixels, placée en bas à droite)
fenetre.geometry("500x120+-10+-10")

# Force la fenêtre à rester au-dessus de tes jeux et navigateurs
fenetre.attributes("-topmost", True)

# Design de la fenêtre (fond noir, texte cyan style codeur)
fenetre.configure(bg="#0f0f0f")
label_jarvis = tk.Label(
    fenetre,
    text="Démarrage du système...",
    font=("Consolas", 11),
    fg="#00ffff",
    bg="#0f0f0f",
    wraplength=480,
    justify="left"
)
label_jarvis.pack(expand=True, fill="both", padx=10, pady=10)

# On lance le cerveau dans un thread parallèle pour que la fenêtre ne freeze pas
thread_cerveau = threading.Thread(target=demarrer_jarvis)
thread_cerveau.daemon = True
thread_cerveau.start()

# On fait tourner la fenêtre en boucle (indispensable pour l'affichage)
fenetre.mainloop()