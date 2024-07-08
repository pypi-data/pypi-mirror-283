from twilio.rest import Client

account_sid = 'ACd984f45e2006d275aeb6c0d0cd799bf6'
auth_token = '6068bd5920a7c3aaa3a533e7c80340d7'
def send_msg(mesg):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=f'Open redirect: {mesg}',
            to='whatsapp:+917695985534'
        )
        print(f"Message sent successfully: {message.sid} {mesg}")
    except Exception as e:
        print(f"Failed to send message: {e}")
