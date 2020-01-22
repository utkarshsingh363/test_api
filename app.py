from flask import Flask, request,make_response,jsonify, render_template, session, redirect,url_for
import requests
import twilio
from twilio.rest import Client
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)

app.config['SECRET_KEY']='uJFZnfTy2Tb_ahxTk0BQBg'

@app.route('/')
def run_api():
    return "Hello!!"

@app.route('/otp_validation',methods=['GET','POST'])
def otp_validation():

    # if request.method=='POST':
    #     req= request.form

    if session.get('otp',None) is not None:
        otp=session.get('otp')
        data = session.get('data')


        g = input("Enter OTP-----------")
        print(g)
        # print("otp is " + str(otp) + " & otp1 is " + str(g))
        if int(otp) == int(g):
            print("inside")
            data =session.get('data')
            return data
        return "False"

    return "Incorrect",200

@app.route('/get_txnid',methods=['GET','POST'])
def get_txnid():
    # req = request.get_json()
    req = {
        'txnid':'016341301200260648'
    }

    response = {
        "message": "JSON received!",
        "txnid": req.get("txnid")
    }

    txnid = response['txnid']

    print(txnid)
    res = make_response(jsonify(response), 200)

    result = requests.get('https://securetest.sabpaisa.in/SabPaisaReport/REST/Transaction/searchByTxnId/'+txnid)
    r = result.json()

    response_req={
        "transxnID": r['payeeMob'],
        "paymentMode": r["paymentMode"],
        "payeeFirstName": r["payeeFirstName"],
        "payeeMob": r["payeeMob"],
        "payeeEmail": r["payeeEmail"],
        "status": r["status"],
        "clientName": r["clientName"],
        "payeeAmount":r["payeeAmount"],
        "paidAmount": r["paidAmount"],
        "transDate": r["transDate"],
        "transCompleteDate": r["transCompleteDate"],
        "resMsg": r["resMsg"]
    }
    mob=r['payeeMob']
    em=r["payeeEmail"]


    otp=random.randint(1000,9999)


    # trial number---> +14697891144

    account_sid = 'AC7ca3e7630b7a8290a0a1a7bd625d0276'
    auth_token = '91530c548972da2213286939abb56222'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="You verification code is"+str(otp),
        from_='+14697891144',
        to='+917004793599'
    )

    print(message.sid)

    session['data']=response_req
    session['otp']=otp




    # def sendmail(from_email,password,to_email,subject,message):
    #     msg = MIMEMultipart()
    #     msg['From'] = from_email
    #     msg['To'] = to_email
    #     msg['Subject'] = subject
    #
    #     msg.attach(MIMEText(message,'plain'))
    #     try:
    #         server=smtplib.SMTP_SSL('smtp.gmail.com', 587)
    #         server.ehlo()
    #         server.starttls()
    #         server.echo()
    #         server.login(from_email,password)
    #         server.sendmail(from_email,to_email,msg.as_string())
    #         server.close()
    #         return True
    #     except Exception as e:
    #         print('Something went wrong:' + str(e))
    #         return False
    #
    # mail_msg="You verification code is"+str(otp)
    # sendmail('utkarshsingh0894@gmail.com','Zlatan@1234','utkarshsingh3631@gmail.com','OTP Validation',mail_msg)
    #

    # return str(otp)

    return redirect('/otp_validation')



    # return render_template('/get_txnid.html')



if __name__=='__main__':
    app.run(debug=True)