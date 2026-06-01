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


def homepage(request):
    return render(request,'updatehome.html')


def order_post(request):

    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']
    quantity = request.POST['quantity']

    print(name,email,phone,address,quantity,"fffffffffffffffffff")

    if quantity == "50g":
        amount = 1 * 100   # Razorpay uses paise

    elif quantity == "200g":
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




# def userpayment_post(request):

#     if request.method == "POST":

#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         address = request.POST.get('address')
#         quantity = request.POST.get('quantity')
#         payment_id = request.POST.get('payment_id')

#         if not email:
#             return HttpResponse("Email not found")

#         message = f"""
#         Dear {name},

#         Thank you for shopping with ECOMONKS.

#         Your payment has been received successfully and your order is now confirmed.

#         ━━━━━━━━━━━━━━━━━━
#         🧾 ORDER DETAILS
#         ━━━━━━━━━━━━━━━━━━

#         👤 Name       : {name}
#         📧 Email      : {email}
#         📞 Phone      : {phone}
#         📍 Address    : {address}
#         📦 Quantity   : {quantity}
#         💳 Payment ID : {payment_id}

#         ━━━━━━━━━━━━━━━━━━

#         We truly appreciate your support and trust in ECOMONKS.

#         You will receive further updates regarding your order soon.

#         Thank you,
#         Team ECOMONKS
#         """

#         print("FUNCTION CALLED")
#         print(name)
#         print(email)
#         print(phone)
#         print(address)
#         print(quantity)
#         print(payment_id)

#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.ehlo()

#         server.login(
#             # "leagaladvisorteam@gmail.com",
#             "founder@ecomonks.in",
#             "crmwddzdzoqatofz"
#             # "eugnxtyylwtqwlav"
#         )

#         subject = "ECOMONKS Order Confirmation"

#         msg = f"Subject: {subject}\n\n{message}"

#         server.sendmail(
#             "founder@ecomonks.in",
#             email,
#             msg
#         )

#         # Admin / Owner Mail
#         admin_message = f"""
#         🚨 NEW ORDER RECEIVED - ECOMONKS

#         ━━━━━━━━━━━━━━━━━━
#         🛒 CUSTOMER DETAILS
#         ━━━━━━━━━━━━━━━━━━

#         👤 Customer Name : {name}
#         📧 Email         : {email}
#         📞 Phone         : {phone}

#         📍 Delivery Address:
#         {address}

#         📦 Ordered Quantity : {quantity}

#         💳 Payment ID : {payment_id}

#         ━━━━━━━━━━━━━━━━━━
#         ✅ Payment Status : SUCCESSFUL
#         ━━━━━━━━━━━━━━━━━━
#         """

#         admin_msg = f"Subject: New ECOMONKS Order Received\n\n{admin_message}"

#         server.sendmail(
#             "founder@ecomonks.in",
#             "founder@ecomonks.in",
#             admin_msg
#         )

#         server.quit()

#         return HttpResponse("""
#             <script>
#                 alert('Payment Successful');
#                 window.location='/';
#             </script>
#         """)

#     return HttpResponse("Invalid Request")



# def emailenquiry(request):

#     if request.method == "POST":

#         email = request.POST.get('email')

#         subject = "ECOMONKS Subscription"

#         message = f"""
# Welcome to ECOMONKS

# Hello,

# Thank you for subscribing to ECOMONKS.

# We are excited to have you as part of our growing family ❤️

# ━━━━━━━━━━━━━━━━━━
# ✨ WHAT YOU WILL RECEIVE
# ━━━━━━━━━━━━━━━━━━

# 🛍️ Exclusive Product Updates

# 🎉 Special Offers & Discounts

# 📢 Latest Announcements

# 🌱 Natural & Traditional Product Information

# ━━━━━━━━━━━━━━━━━━

# Thank you for staying connected with us.

# We look forward to serving you with the best from ECOMONKS.

# Warm Regards,
# Team ECOMONKS
# """

#         try:
#             server = smtplib.SMTP('smtp.gmail.com', 587)
#             server.starttls()

#             # Gmail App Password
#             server.login(
#                  "founder@ecomonks.in",
#                  "crmwddzdzoqatofz"
#                 # "leagaladvisorteam@gmail.com",
#                 # "eugnxtyylwtqwlav"
#             )

#             msg = f"Subject: {subject}\n\n{message}"

#             # server.sendmail(
#             #     "yourgmail@gmail.com",
#             #     email,
#             #     msg
#             # )

#             # Subscriber confirmation mail
#             server.sendmail(
#                 "founder@ecomonks.in",
#                 email,
#                 msg
#             )

#             # Admin notification mail
#             admin_message = f"""
#             New Subscription Received

#             Subscriber Email:
#             {email}
#             """

#             admin_msg = f"Subject: New ECOMONKS Subscription\n\n{admin_message}"

#             server.sendmail(
#                 "founder@ecomonks.in",
#                 "founder@ecomonks.in",
#                 admin_msg
#             )

#             server.quit()

#             return HttpResponse(
#                 "<script>alert('Subscribed Successfully');window.location='/'</script>"
#             )

#         except Exception as e:
#             return HttpResponse(f"Error: {e}")

#     return HttpResponse("Invalid Request")




def userpayment_post(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')
        payment_id = request.POST.get('payment_id')

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
            Thank You For Your Order
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
            🚨 NEW ORDER RECEIVED
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