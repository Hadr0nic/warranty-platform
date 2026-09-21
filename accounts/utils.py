import http.client
import json

def send_sms_via_smsir(mobile, template_id, parameters, api_key):
    """
    Send SMS via sms.ir

    mobile: recipient phone number as string
    template_id: integer, your template ID on sms.ir
    parameters: list of dicts, e.g. [{"name": "PARAM1", "value": "1234"}]
    api_key: your sms.ir API key
    """
    conn = http.client.HTTPSConnection("api.sms.ir")
    payload = json.dumps({
        "mobile": mobile,
        "templateId": template_id,
        "parameters": parameters
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': api_key
    }
    conn.request("POST", "/v1/send/verify", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")