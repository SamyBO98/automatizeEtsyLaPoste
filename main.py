from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://www.laposte.fr/colissimo-en-ligne/parcours/caracteristiques"
#Mettre ça dans un placeholder
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()


    print("Ouverture de la page...")
    page.goto(URL)

    # Accepter les cookies
    try:
        page.locator("#popin_tc_privacy_button_3").click()
        print("Cookies acceptés !")
    except Exception as e:
        print(f"Pas de bannière cookies : {e}")
    
    
    page.locator("a[alt='Se connecter']").click()
    print("Clic sur Se connecter !")
    page.locator("span.button__label", has_text="Se connecter").first.click()
    print("Clic sur Se connecter dans la modale !")
    page.locator("input#username").fill(EMAIL)
    page.locator("input[name='password']").fill(PASSWORD)
    page.locator("button#submit-button").click()
    print("Connexion envoyée !")
    page.wait_for_load_state("networkidle")

    #Changement de pays
    page.locator(".lp-dropdown__combobox").nth(1).click()
    page.locator(".lp-dropdown__listbox input.input__field").first.fill("France")
    page.locator("li[role='option']", has_text="France").first.click()


    # Remplir le poids
    print("Remplissage du poids...")
    poids_input = page.locator("input#weightInput")
    poids_input.click()
    poids_input.fill("1")

    #Changement de pays
    #page.locator(".lp-dropdown__combobox").nth(1).click()
    #page.locator(".lp-dropdown__listbox input.input__field").first.fill("Allemagne")
    #page.locator("li[role='option']", has_text="Allemagne").first.click()

    page.locator(".summary-step__validate__button--fullwidth").click()
    print("Étape suivante cliquée !")
    page.wait_for_load_state("networkidle")

    page.locator("input#notif").click(force=True)
    print("Notification cochée !")

    #page.locator("input#card-input-id-D_BP").click(force=True)
    #print("Point de contact La Poste sélectionné !")

    page.locator("input#card-input-id-D_BAL").click(force=True)
    print("Point de contact La Poste sélectionné !")

    page.locator(".summary-step__validate__button--fullwidth").click()
    print("Étape suivante cliquée !")
    page.wait_for_load_state("networkidle")


    input("Appuie sur Entrée pour fermer...")