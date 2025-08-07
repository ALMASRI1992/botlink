
# linkedin_auto_apply.py
#def run_apply():
# linkedin_auto_apply.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def create_driver():
    options = Options()
    # use the built-in headless flag
    options.headless = True
    # specify a window size so pages render correctly
    options.add_argument("--window-size=1920x1080")

    # do *not* pass any other arguments—no disable-gpu, no no-sandbox, no experimental flags
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

def run_apply(first_name, last_name, specialty,
              experience, LINKEDIN_EMAIL, LINKEDIN_PASSWORD,
              url_search):
    """
    Exécute ta logique Selenium : connexion LinkedIn, scroll, Easy Apply, etc.
    Retourne un tuple (success: bool, message: str).
    """
    try:
        # ==== COPIE-COLLE ICI TON CODE ENTIER, sauf la partie "driver.quit()" à la fin ====
        # Par exemple :

        #https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4258713313
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import Select
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        import random



        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import Select
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        import random








        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By

        def select_binary_labels(modal, driver):
            try:
                labels = modal.find_elements(By.XPATH, ".//label[@data-test-text-selectable-option__label]")
                found = False
                for label in labels:
                    text = label.text.strip().lower()
                    if text in ["Yes", "Oui", "Si"]:
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].click();", label)
                        print(f"  '{text}' sélectionné via le label cliquable")
                        found = True
                        break
                if not found:
                    print("  Aucun label binaire détecté (Yes/Oui/Si)")
            except Exception as e:
                print("  Erreur lors du clic sur les labels binaires :", e)


        def try_select_binary_labels(modal, driver):
            try:
                labels = modal.find_elements(By.XPATH, ".//label[@data-test-text-selectable-option__label]")
                for label in labels:
                    text = label.text.strip().lower()
                    if text in ["yes", "oui", "si"]:
                        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", label)
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].click();", label)
                        print(f"  Label binaire sélectionné : {text}")
                        return True
                print("  Aucun label binaire (Yes/Oui/Si) trouvé à cette étape.")
                return False
            except Exception as e:
                print("  Erreur lors du clic sur le label binaire :", e)
                return False


        
        def is_first_step_window(modal):
            try:
                #   Vérifie si le titre contient des indices d'informations personnelles
                header = modal.find_element(By.XPATH, ".//h3 | .//h2").text.strip().lower()
                if any(word in header for word in ["contact", "informations", "coordonnées"]):
                    return True
            except:
                pass

            try:
                #   Vérifie si c’est la première étape (0%)
                progress = modal.find_element(By.XPATH, ".//span[contains(text(),'%')]").text.strip()
                if progress.startswith("0%"):
                    return True
            except:
                pass

            try:
                #   Recherche des labels indiquant des infos personnelles
                labels = modal.find_elements(By.XPATH, ".//label")
                for label in labels:
                    text = label.text.strip().lower()
                    if any(word in text for word in ["first name", "last name", "prénom", "nom", "email", "e-mail", "phone", "téléphone", "mobile"]):
                        return True
            except:
                pass

            return False












        import threading

        def timeout_close_dialog(driver, timeout=20):
            def close_after_timeout():
                try:
                    time.sleep(timeout)

                    # 1er clic : bouton X (ferme l'offre)
                    x_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss')]")
                    driver.execute_script("arguments[0].click();", x_button)
                    print("  Premier clic sur le bouton 'X'")

                    time.sleep(1.5)  # délai avant la boîte de confirmation

                    # 2e clic : bouton X ou Discard dans la boîte de confirmation
                    discard_button = driver.find_element(By.XPATH, "//button[contains(., 'Discard') or contains(@aria-label, 'Dismiss')]")
                    driver.execute_script("arguments[0].click();", discard_button)
                    print("  Deuxième clic pour confirmer la fermeture")
                except Exception as e:
                    print("  Fermeture automatique échouée :", e)

            threading.Thread(target=close_after_timeout).start()



        









        # --- Configuration ---
        EMAIL_KEYWORD = "mahmoud"
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')

        service = Service(ChromeDriverManager().install())
        #driver = webdriver.Chrome(service=service, options=options)
        driver = create_driver()

        wait = WebDriverWait(driver, 10)

        #LINKEDIN_EMAIL = "mahmoud_university@hotmail.com"
        #LINKEDIN_PASSWORD = "Masri71854415"

        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        print("  Connexion LinkedIn réussie")

        # attends que la redirection se termine puis passe à la page de recherche
        time.sleep(5)
        #url_search="https://www.linkedin.com/jobs/collections/easy-apply/?currentJobId=4270150134&discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII"
        driver.get(url_search)

        print("  Navigation vers la recherche d'emploi...")



        # ⚠️ Force un clic initial sur le premier job (nécessaire pour déclencher le lazy loading)
        try:
            first_job = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".job-card-container")))
            driver.execute_script("arguments[0].scrollIntoView(true);", first_job)
            time.sleep(1)
            first_job.click()
            print("  Clic initial sur une offre déclenché.")
            time.sleep(3)
        except Exception as e:
            print("    Erreur lors du clic initial :", e)




        # 📦 Adaptation spéciale : Passer à page 2 puis revenir à page 1
        try:
            next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Page 2')]")))
            driver.execute_script("arguments[0].click();", next_btn)
            print("   Page 2 ouverte pour déclencher le lazy loading...")
            time.sleep(4)
            
            prev_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Page 1')]")))
            driver.execute_script("arguments[0].click();", prev_btn)
            print("  Retour à la page 1 pour forcer le chargement complet")
            time.sleep(4)
        except Exception as e:
            print("  Navigation page 2 -> page 1 échouée :", e)

        # Scroll utilisateur classique
        print("  Défilement via Keys.PAGE_DOWN pour chargement offres...")
        stable_rounds = 0
        previous_count = 0

        for i in range(30):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(2.5)
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
            current_count = len(job_cards)
            print(f"  Scroll {i+1}: {current_count} offres visibles")

            if current_count == previous_count:
                stable_rounds += 1
            else:
                stable_rounds = 0
            previous_count = current_count

            if stable_rounds >= 3:
                print("  Scroll terminé : plus de nouvelles offres détectées.")
                break

        print(f"  Total offres chargées après forçage : {previous_count}")

        try:
            seen_job_ids = set()
            try:
                job_list_panel = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container"))
                )
            except Exception as e:
                print("  Impossible de trouver la liste des offres (.scaffold-layout__list-container). Vérifie que tu es bien connecté et que la page est chargée.")


        

            print(f"   Fin du scroll initial. Total offres chargées : {previous_count}")
            finished = False
            while not finished:

                previous_count = 0
                stable_rounds = 0
                while stable_rounds < 3:  # attendre 3 cycles où le nombre d’offres ne change plus
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                    time.sleep(random.uniform(1.5, 2.2))
                    job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
                    if len(job_cards) == previous_count:
                        stable_rounds += 1
                    else:
                        stable_rounds = 0
                    previous_count = len(job_cards)




                job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
                new_jobs = [job for job in job_cards if job.get_attribute("data-job-id") not in seen_job_ids]
                # 🔄 Scroll + attendre que toutes les offres soient bien chargées
        






                if not new_jobs:
                    # 🔄 Scroll vers le bas pour chercher plus d’offres sur la même page
                    previous_count = len(job_cards)
                    for _ in range(3):  # scroll 3 fois max
                        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
                        time.sleep(random.uniform(1.5, 2.5))
                        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")
                        current_count = len(job_cards)
                        if current_count > previous_count:
                            print(f"  {current_count - previous_count} nouvelles offres chargées.")
                            break
                        previous_count = current_count
                    else:
                        # 🛑 Rien de nouveau, on peut passer à la page suivante
                        print("  Toutes les offres visibles ont été traitées.")
                        finished = True
                        break

                for job in new_jobs:
                    job_id = job.get_attribute("data-job-id")
                    seen_job_ids.add(job_id)
                    #seen_job_ids.add(job_id)

                    try:
                        print(f"  Offre ID {job_id} cliquée")
                        driver.execute_script("arguments[0].scrollIntoView(true);", job)
                        time.sleep(1)
                        job.click()
                        #timeout_close_dialog(driver, timeout=15)
                        time.sleep(2.5)
                        
                        try:
                            easy_apply_button = wait.until(
                                EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]"))
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", easy_apply_button)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", easy_apply_button)
                            print("  Easy Apply cliqué !")
                        except:
                            print("  Easy Apply non cliqué")
                            continue

                        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='dialog']")))
                        time.sleep(1)
                        modal = driver.find_element(By.XPATH, "//div[@role='dialog']")

                        select_binary_labels(modal, driver)






                        for _ in range(5):
                            modal.send_keys(Keys.PAGE_DOWN)
                            time.sleep(0.4)

                        print("Scroll effectué dans la fenêtre Easy Apply")
                        


                        # ✅ Scroll de stabilisation pour laisser les champs apparaître (utile sur certains formulaires longs)
                        for _ in range(5):
                            modal.send_keys(Keys.PAGE_DOWN)
                            time.sleep(random.uniform(0.8, 1.2))

                        
                        
                        first_step = True
                        max_steps = 5
                        step_counter = 0
                        while step_counter < max_steps:
                    # while True:
                            try_select_binary_labels(modal, driver)
                            print("je suis la yes, oui, si")
                            dropdowns = modal.find_elements(By.XPATH, ".//select")
                            for dropdown in dropdowns:
                                try:
                                    driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
                                    time.sleep(0.2)
                                    select = Select(dropdown)
                                    if first_step:
                                        found = False
                                        for i, option in enumerate(select.options):
                                            if EMAIL_KEYWORD in option.text.lower():
                                                select.select_by_index(i)
                                                print("  Adresse e-mail sélectionnée :", option.text)
                                                found = True
                                                break
                                        if not found and len(select.options) > 1:
                                            select.select_by_index(1)
                                    else:
                                        if len(select.options) > 1:
                                            select.select_by_index(1)
                                except Exception as e:
                                    print("  Erreur dropdown :", e)

                        # inputs = modal.find_elements(By.XPATH, ".//input[@type='text']")
                        #    is_first_window = is_first_step_window(modal)
                        #    is_first_window = is_first_step_window(modal)
                        #    is_first_window = is_first_step_window(modal)
                        #    is_first_window = is_first_step_window(modal)

                        #    is_first_window = is_first_step_window(modal)

                        
                            is_first_window = is_first_step_window(modal)

                            #iis_first_window = is_first_step_window(modal)

                            inputs = modal.find_elements(By.XPATH, ".//input[@type='text']")
                            for idx, input_field in enumerate(inputs):
                                try:
                                    input_id = (input_field.get_attribute("id") or "").lower()
                                    input_name = (input_field.get_attribute("name") or "").lower()
                                    input_aria = (input_field.get_attribute("aria-label") or "").lower()
                                    label_text = ""

                                    # 🔍 Cherche le label si disponible
                                    try:
                                        label_el = driver.find_element(By.XPATH, f"//label[@for='{input_id}']")
                                        label_text = label_el.text.strip().lower()
                                    except:
                                        pass

                                    full_descriptor = " ".join([input_id, input_name, input_aria, label_text])

                                    if is_first_window:
                                        if any(x in full_descriptor for x in [
                                            "first name", "last name", "prénom", "nom",
                                            "email", "e-mail", "phone", "mobile", "téléphone", "number"
                                        ]):
                                            print(f"  Champ personnel ignoré (étape 1) : {full_descriptor}")
                                            continue
                                        # 🔐 Fallback: ne jamais modifier les 3 premiers champs s’ils ont des contenus sensibles
                                        if idx < 2:
                                            print(f"  Champ sensible ignoré (index < 2) : {full_descriptor}")
                                            continue

                                    # ✅ Remplissage automatique
                                    input_field.click()
                                    input_field.send_keys(Keys.CONTROL, "a")
                                    input_field.send_keys(Keys.BACKSPACE)
                                    value = str(random.randint(experience/2, experience))
                                    input_field.send_keys(value)
                                    print(f"  Champ rempli : {full_descriptor} → {value}")
                                    time.sleep(0.3)

                                except Exception as e:
                                    print("  Erreur remplissage champ texte :", e)





                            radio_groups = modal.find_elements(By.XPATH, ".//fieldset[contains(@class, 'artdeco-question-form-fieldset')]")
                            for group in radio_groups:
                                try:
                                    radios = group.find_elements(By.XPATH, ".//input[@type='radio']")
                                    if radios:
                                        driver.execute_script("arguments[0].click();", radios[0])
                                        print("  Premier bouton radio sélectionné (souvent Yes)")
                                        time.sleep(0.3)
                                except:
                                    print("  Aucun bouton radio cliquable détecté dans ce groupe")

                            try:
                                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Next']]")))
                                driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                                time.sleep(0.5)
                                next_btn.click()
                                print("  Bouton Next cliqué")
                                time.sleep(1.2)
                                modal.send_keys(Keys.PAGE_DOWN)
                                time.sleep(0.8)
                                try_select_binary_labels(modal, driver)
                                first_step = False
                            except:
                                print("  Aucun bouton Next trouvé, passage à Review ou Submit")
                                break
                            step_counter += 1

                        try:
                            review_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Review']]")))
                            driver.execute_script("arguments[0].scrollIntoView(true);", review_btn)
                            review_btn.click()
                            print("  Bouton Review cliqué")
                            time.sleep(1.5)
                        except:
                            print("  Bouton Review non trouvé")

                        try:
                            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Submit application']]")))
                            driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
                            time.sleep(0.5)
                            submit_btn.click()
                            print("  Candidature soumise !")
                            time.sleep(1.5)

                            try:
                                done_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Done']]")))
                                driver.execute_script("arguments[0].scrollIntoView(true);", done_btn)
                                time.sleep(0.5)
                                done_btn.click()
                                print("  Bouton Done cliqué")
                            except:
                                print("  Bouton Done non trouvé")
                        except Exception as e:
                            print("  Erreur lors du Submit :", e)

                            
                            # 🔄 Fermer la modale si erreur Review ou Submit
                            try:
                                print("  Une erreur est survenue, tentative de fermeture via le bouton 'X'")
                                close_button = wait.until(EC.element_to_be_clickable(
                                    (By.XPATH, "//button[contains(@aria-label, 'Dismiss') or contains(@aria-label, 'Fermer') or contains(@aria-label, 'Close')]")
                                ))
                                close_button.click()
                                print("  Fenêtre fermée par bouton Dismiss")
                                time.sleep(2)

                                # ✅ Deuxième tentative de fermeture s’il y a une fenêtre "Discard or Save"
                            #try:
                                    # 🛑 Tentative de fermeture via le bouton Discard si la modale "Save this application?" est ouverte
                                try:
                                    discard_btn = WebDriverWait(driver, 5).until(
                                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Discard']]"))
                                    )
                                    driver.execute_script("arguments[0].click();", discard_btn)
                                    print("  Clic forcé sur 'Discard' effectué")
                                    time.sleep(1.5)
                                except Exception as e:
                                    print("  Échec du clic sur 'Discard' :", e)


                            except Exception as e:
                                print("  Impossible de fermer la fenêtre via le bouton 'X' :", e)


        

                        try:
                            dismiss_btn = driver.find_element(By.XPATH, "//button[contains(@aria-label,'Dismiss')]")
                            dismiss_btn.click()
                            wait.until_not(
                                EC.presence_of_element_located((By.CLASS_NAME, "artdeco-modal-overlay--is-top-layer"))
                            )
                        except:
                            pass

                        time.sleep(2)

                    except Exception as e:
                        print(f"  Erreur offre ID {job_id} : {e}")

                                        # 🔄 Tentative de libérer l’écran en fermant modale ou discard
                        try:
                            print("  Blocage détecté : tentative de fermeture des fenêtres actives")

                            # 1️⃣ Fermer la modale principale (Easy Apply) via le bouton X
                            close_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Dismiss') or contains(@aria-label, 'Fermer') or contains(@aria-label, 'Close')]")
                            close_button.click()
                            print("  Fenêtre Easy Apply fermée via 'X'")
                            time.sleep(1.5)

                            # 2️⃣ Fermer la modale secondaire (Discard / Ignorer)
                            try:
                                discard_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Discard') or contains(text(),'Ignorer')]")
                                discard_btn.click()
                                print("  Fenêtre 'Discard or Save' fermée")
                                time.sleep(1.5)
                            except:
                                print("  Pas de fenêtre 'Discard or Save' détectée")

                        except Exception as cleanup_error:
                            print("  Échec de fermeture automatique des modales :", cleanup_error)

                        # 🚀 Passer à l’offre suivante
                        continue
                    

                scroll_attempts = 0
                previous_count = len(driver.find_elements(By.CSS_SELECTOR, ".job-card-container"))

                while scroll_attempts < 5:
                    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                    time.sleep(2)

                




                    current_count = len(driver.find_elements(By.CSS_SELECTOR, ".job-card-container"))
                    if current_count > previous_count:
                        print(f"  {current_count - previous_count} nouvelles offres chargées.")
                        break
                    scroll_attempts += 1
                    print("  Scroll supplémentaire...")

                try:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, "button.jobs-search-pagination__button--next")
                    for next_button in next_buttons:
                        if next_button.is_displayed() and next_button.is_enabled():
                            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                            time.sleep(1)
                            next_button.click()
                            print("  Bouton 'Suivant' cliqué via .jobs-search-pagination__button--next")
                            time.sleep(3)
                            break
                    else:
                        print("  Aucun bouton 'Suivant' activé visible.")
                except Exception as e:
                    print("  Aucun bouton 'Suivant' trouvé (fallback) :", e)

        except Exception as e:
            print(f"  Erreur globale : {e}")

      #  print("\n  Fini.")
      #  driver.quit()
    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        return False, str(e)







        

        