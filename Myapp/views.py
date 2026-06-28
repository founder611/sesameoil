import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
import smtplib
from datetime import datetime
import requests
from supabase import create_client



def homepage(request):
    return render(request,'newhome.html')


def order_post(request):

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    quantity = request.POST['quantity']

    print(name,email,phone,address,quantity,"fffffffffffffffffff")

    if quantity == "100ml":
        amount = 1 * 100   # Razorpay uses paise

    elif quantity == "250ml":
        amount = 1 * 100

    else:
        amount = 0

    return render(request, 'pp.html', {

        'name': name,
        'email': email,
        'phone': phone,
        'address': address,
        'quantity': quantity,
        'amount': amount,
        'razorpay_api_key': 'rzp_live_Su35EVyNYFeKCF',
        'currency': 'INR'

    })


def raz_pay(request, amount):

    import razorpay

    razorpay_api_key = "rzp_live_Su35EVyNYFeKCF"
    razorpay_secret_key = "NQE3JfS6rdlmp8YtHrxF120H"

    razorpay_client = razorpay.Client(
        auth=(razorpay_api_key, razorpay_secret_key)
    )

    amount = float(amount)

    order_data = {
        'amount': amount,
        'currency': 'INR',
        'receipt': 'order_rcptid_11',
        'payment_capture': '1',
    }

    order = razorpay_client.order.create(data=order_data)

    return render(request, 'pp.html', {

        'razorpay_api_key': razorpay_api_key,
        'amount': order_data['amount'],
        'currency': order_data['currency'],
        'order_id': order['id']

    })



# ==========================================
# SAVE ORDER TO SUPABASE - FIXED VERSION
# ==========================================
def save_order_to_supabase(name, email, phone, address, quantity, amount, payment_id):
    """Save order to Supabase database"""
    try:
        # Your Supabase credentials - DIRECT values
        supabase_url = "https://uuzumstwtrgzmeqgkjrj.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV1enVtc3R3dHJnem1lcWdranJqIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MTUwODA1MSwiZXhwIjoyMDk3MDg0MDUxfQ.lZlydZ_sVQhcBteBBX1mucA_ZbmlkOS7yUVO8gYCV6U"
        
        # Create client
        supabase = create_client(supabase_url, supabase_key)
        
        # Get next order number by counting existing orders
        try:
            response = supabase.table('sesame_orders').select('id', count='exact').execute()
            order_no = response.count + 1 if response.count else 1
        except Exception as e:
            print(f"Could not get count: {e}")
            order_no = 1
        
        # Insert order
        order_data = {
            "order_no": order_no,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "customer_name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "quantity": quantity,
            "amount": amount,
            "payment_id": payment_id,
            "payment_status": "Success"

        }
        
        result = supabase.table('sesame_orders').insert(order_data).execute()
        print("SUPABASE RESULT:", result)

        print(f"✅ Order #{order_no} saved to Supabase")
        return True
        
    except Exception as e:
        print(f"❌ Supabase error: {str(e)}")
        return False



import requests

def send_whatsapp_message_template(name, phone, quantity, payment_id, amount, order_date=""):
    try:
        print("========== MBG WHATSAPP TEMPLATE ==========")

        phone = str(phone).replace(" ", "").replace("+", "").strip()
        if not phone.startswith("91"):
            phone = "91" + phone

        payload = {
            "templateName": "sesameoil_orderconfirmation",   # Your approved template name
            "senderId": phone,                   # No '+' unless documentation requires it
            "chatId": "1402050",
            "variables": {
                "header": [],
                "body": [
                    str(name),
                    str(quantity),
                    str(amount),
                    str(payment_id),
                    str(order_date)
                ]
            }
        }

        response = requests.post(
            "https://chatbot.digitalmbg.com/v1/whatsapp/send_templet",
            headers={
                "Content-Type": "application/json",
                "x-api-key": "39832662461ae94fa94b03487c7866f3"
            },
            json=payload,
            timeout=30
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        return response.status_code == 200

    except Exception as e:
        print(e)
        return False


import requests
def send_whatsapp_message(name, phone, quantity, payment_id, amount, order_date=""):

    phone = str(phone).replace("+", "").replace(" ", "")

    if not phone.startswith("91"):
        phone = "91" + phone

    payload = {
        "senderId": "+" + phone,
        "name": name,
        "actions": [

            {
                "action": "set_field_value",
                "field_name": "name",
                "value": name
            },

            {
                "action": "set_field_value",
                "field_name": "quantity",
                "value": str(quantity)
            },

            {
                "action": "set_field_value",
                "field_name": "amount",
                "value": str(amount)
            },

            {
                "action": "set_field_value",
                "field_name": "payment_id",
                "value": payment_id
            },

            {
                "action": "set_field_value",
                "field_name": "order_date",
                "value": order_date
            },

            {
                "action": "send_flow",
                "flow_id": "flow_1782640167786"
            }

        ]
    }

    response = requests.post(
        "https://chatbot.digitalmbg.com/v1/contacts",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": "39832662461ae94fa94b03487c7866f3"
        },
        json=payload
    )

    print(response.status_code)
    print(response.text)


# def send_whatsapp_message(name, phone, quantity):
#     try:

#         print("========== WHATSAPP FUNCTION STARTED ==========")

#         # Clean phone number
#         phone = str(phone).replace(" ", "").replace("+", "").strip()

#         # Add country code if missing
#         if not phone.startswith("91"):
#             phone = f"91{phone}"

#         print("FINAL PHONE:", phone)

#         # WATI API URL
        
#         url = f"https://live-mt-server.wati.io/1043453/api/v1/sendTemplateMessage?whatsappNumber={phone}"


#         # Payload
#         payload = {
#             "template_name": "order_confirmation",
#             "broadcast_name": "order_confirmation",
#             "parameters": [
#                 {
#                     "name": "1",
#                     "value": str(name)
#                 },
#                 {
#                     "name": "2",
#                     "value": str(quantity)
#                 }
#             ]
#         }

#         print("PAYLOAD:", payload)

#         # Headers
#         headers = {
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InByZW1zZWtoYXJAeWF0aGlzaGEuY29tIiwibmFtZWlkIjoicHJlbXNla2hhckB5YXRoaXNoYS5jb20iLCJlbWFpbCI6InByZW1zZWtoYXJAeWF0aGlzaGEuY29tIiwiYXV0aF90aW1lIjoiMDYvMDYvMjAyNiAxNzoxOToxNCIsInRlbmFudF9pZCI6IjEwNDM0NTMiLCJkYl9uYW1lIjoibXQtcHJvZC1UZW5hbnRzIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.i7aQp3cYOtk2wraWyMjHLP7L0T8znm-xf7SthfOPvZ4",
#             "Content-Type": "application/json"
#         }

#         # Send request
#         response = requests.post(
#             url,
#             json=payload,
#             headers=headers,
#             timeout=30
#         )

#         print("========== WATI RESPONSE ==========")
#         print("STATUS CODE:", response.status_code)
#         print("RESPONSE:", response.text)
#         print("===================================")

#         return response.status_code == 200

#     except Exception as e:

#         print("WhatsApp Error:", str(e))
#         return False





def userpayment_post(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        payment_id = request.POST.get('payment_id')


        try:
            amount = float(amount) / 100   # Paisa → Rupees
        except:
            amount = 0

        if not email:
            return HttpResponse("Email not found")

        try:

            # ==========================================
            # CUSTOMER HTML EMAIL
            # ==========================================

            customer_html = f"""
            <html>

            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#0b7d45; text-align:center;">
            🌿 ECOMONKS
            </h1>

            <h2 style="color:#222;">
            Thank You For Your Ordering sesame oil from ECOMONKS!
            </h2>

            <p style="font-size:16px; color:#555;">
            Dear <b>{name}</b>,
            </p>

            <p style="font-size:16px; color:#555;">
            Your payment has been received successfully and your order is confirmed.
            </p>

            <div style="
            background:#f7fff9;
            border:1px solid #d4f5dd;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <h3 style="color:#0b7d45;">
            🧾 Order Details
            </h3>

            <p><b>👤 Name:</b> {name}</p>

            <p><b>📧 Email:</b> {email}</p>

            <p><b>📞 Phone:</b> {phone}</p>

            <p><b>📍 Address:</b> {address}</p>

            <p><b>📦 Quantity:</b> {quantity}</p>

            <p><b>💳 Payment ID:</b> {payment_id}</p>

            </div>

            <p style="
            margin-top:25px;
            font-size:16px;
            color:#444;
            ">
            We truly appreciate your support and trust in ECOMONKS.
            </p>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            Thank you for shopping with us ❤️

            </div>

            </div>

            </body>

            </html>
            """

            # ==========================================
            # SMTP SERVER
            # ==========================================

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.ehlo()

            server.login(
                "founder@ecomonks.in",
                "crmwddzdzoqatofz"
            )

            # ==========================================
            # CUSTOMER EMAIL
            # ==========================================

            customer_msg = MIMEMultipart()

            customer_msg['From'] = "founder@ecomonks.in"

            customer_msg['To'] = email

            customer_msg['Subject'] = "ECOMONKS Order Confirmation"

            customer_msg.attach(
                MIMEText(customer_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                email,
                customer_msg.as_string()
            )

            # ==========================================
            # ADMIN EMAIL
            # ==========================================

            admin_html = f"""
            <html>

            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#d62828; text-align:center;">
            🚨 NEW ORDER RECEIVED sessame oil from ECOMONKS!
            </h1>

            <div style="
            background:#fff5f5;
            border:1px solid #ffd6d6;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <p><b>👤 Customer Name:</b> {name}</p>

            <p><b>📧 Email:</b> {email}</p>

            <p><b>📞 Phone:</b> {phone}</p>

            <p><b>📍 Address:</b> {address}</p>

            <p><b>📦 Quantity:</b> {quantity}</p>

            <p><b>💳 Payment ID:</b> {payment_id}</p>

            </div>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            ✅ PAYMENT SUCCESSFUL

            </div>

            </div>

            </body>

            </html>
            """

            admin_msg = MIMEMultipart()

            admin_msg['From'] = "founder@ecomonks.in"

            admin_msg['To'] = "founder@ecomonks.in"

            admin_msg['Subject'] = "New ECOMONKS Order Received"

            admin_msg.attach(
                MIMEText(admin_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                "founder@ecomonks.in",
                admin_msg.as_string()
            )

            server.quit()

            # 2. Send supabase for saving (non-critical)


            try:
                save_order_to_supabase(name, email, phone, address, quantity, amount, payment_id)
            except Exception as e:
                print(f"❌ Supabase save error: {str(e)}")
        
            # 3. Send WhatsApp (non-critical)
            try:
                send_whatsapp_message(name, phone, quantity, payment_id, amount, order_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            except Exception as e:
                print(f"❌ WhatsApp error: {str(e)}")

            

            return HttpResponse("""
            <script>
            alert('Payment Successful & Email Sent');
            window.location='/';
            </script>
            """)

        except Exception as e:

            return HttpResponse(f"ERROR: {e}")
        
        

    return HttpResponse("Invalid Request")



# ==========================================
# SUBSCRIPTION EMAIL FUNCTION
# ==========================================

def emailenquiry(request):

    if request.method == "POST":

        email = request.POST.get('email')

        try:

            subscription_html = f"""
            <html>

            <body style="font-family: Arial; background:#f4f4f4; padding:30px;">

            <div style="
            max-width:600px;
            margin:auto;
            background:white;
            border-radius:15px;
            padding:30px;
            box-shadow:0 0 10px rgba(0,0,0,0.1);
            ">

            <h1 style="color:#0b7d45; text-align:center;">
            🌿 Welcome to ECOMONKS
            </h1>

            <p style="font-size:16px; color:#555;">
            Thank you for subscribing to ECOMONKS.
            </p>

            <p style="font-size:16px; color:#555;">
            We are excited to have you as part of our growing family ❤️
            </p>

            <div style="
            background:#f7fff9;
            border:1px solid #d4f5dd;
            padding:20px;
            border-radius:10px;
            margin-top:20px;
            ">

            <h3 style="color:#0b7d45;">
            ✨ What You Will Receive
            </h3>

            <p>🛍️ Exclusive Product Updates</p>

            <p>🎉 Special Offers & Discounts</p>

            <p>📢 Latest Announcements</p>

            <p>🌱 Natural & Traditional Product Information</p>

            </div>

            <div style="
            margin-top:30px;
            background:#0b7d45;
            color:white;
            padding:15px;
            border-radius:10px;
            text-align:center;
            ">

            Thank You For Staying Connected With Us ❤️

            </div>

            </div>

            </body>

            </html>
            """

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.ehlo()

            server.login(
                "founder@ecomonks.in",
                "crmwddzdzoqatofz"
            )

            # Subscriber Email
            subscriber_msg = MIMEMultipart()

            subscriber_msg['From'] = "founder@ecomonks.in"

            subscriber_msg['To'] = email

            subscriber_msg['Subject'] = "ECOMONKS Subscription"

            subscriber_msg.attach(
                MIMEText(subscription_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                email,
                subscriber_msg.as_string()
            )

            # Admin Email
            admin_html = f"""
            <html>

            <body style="font-family: Arial;">

            <h2>📩 New Subscription Received</h2>

            <p><b>Subscriber Email:</b> {email}</p>

            </body>

            </html>
            """

            admin_msg = MIMEMultipart()

            admin_msg['From'] = "founder@ecomonks.in"

            admin_msg['To'] = "founder@ecomonks.in"

            admin_msg['Subject'] = "New ECOMONKS Subscription"

            admin_msg.attach(
                MIMEText(admin_html, 'html', 'utf-8')
            )

            server.sendmail(
                "founder@ecomonks.in",
                "founder@ecomonks.in",
                admin_msg.as_string()
            )

            server.quit()

            return HttpResponse("""
            <script>
            alert('Subscribed Successfully');
            window.location='/';
            </script>
            """)

        except Exception as e:

            return HttpResponse(f"ERROR: {e}")

    return HttpResponse("Invalid Request")