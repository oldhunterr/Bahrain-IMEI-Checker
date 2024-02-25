import json
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_contract', methods=['POST'])
def check_contract():
    imei = request.form['imei']

    # Check Contracts
    batelco_response = perform_batelco_request(imei)
    stc_response = perform_stc_request(imei)
    zain_response = perform_zain_request(imei)

    return jsonify({
        'batelco_response': batelco_response,
        'stc_response': stc_response,
        'zain_response': zain_response
    })

def perform_batelco_request(imei):
    url = "https://e-services.com.bh/BatelcoIMEI/BatelcoIMEI/GETIMEISatus"

    payload = json.dumps({
    "IMEI": imei,
    "CaptchaText": "03AFcWeA6RuOLkyOZTfVrj6kZoaE2ef6jY6inJv9UMc7MqSSGR16FaTcH5GV9Nwnm_euZV38OESmRoDTjs4bLqKvNmPaKVAMFpn5StweLOlAZTbVDkevsUogX7maV6WERbpcSx3a8W9CtcDzsgdl1BFQ7wGM7KvKqCuk7QfY9bwY3aeqOJSsrh4YOhFNc2tD120n0OY2XGhtRpViIqp0YE6dm2ZPHb_GXfyhyQhEIo8hG5OmInqJJBp9YS8FTQFoC6PAjZqGexf_PHbeN5rJWAZT8nEcH-HqYUvGT2W0_dQr36c9KCxelg-kezqJtQSKe7-92A7_uapWTb5iV38sxP5TBZ4ku5-20Ccm821MT8BsZVUcpgRqHKMGOSUA3Tc18GRocVyJHKO1wJsIbZD3Aym1aQaI6M4bLarWkux0yFHClNysRBr_d0MK4w2bd4Rl2hu9o3wuITg5ILOx8SdeW5pRjqVrXmdRJ_re8sqG8FCmc49ttsuoCdQuJ9Vlqu56bxjH_-sBPH6ccZLt_alHK7UYQeR7GKJiCAmK1wEBQyNhtzGrSuH4iN9RgqnVZtYz-AZXqaWf9JP__5"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text

def perform_stc_request(imei):
    url = "https://scp.stc.com.bh/site/check-imei?imei="+imei

    payload = {}
    headers = {
    'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def perform_zain_request(imei):
    url = "https://promo.bh.zain.com/imei-blacklisting/process.php"

    payload = {'formDataString': '{"IMEI":'+imei+'}'}
    files=[

    ]
    headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'cookiesession1=678B28759D4447DA4C23C6C82B2B5080'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.text

if __name__ == '__main__':
    app.run(debug=True)