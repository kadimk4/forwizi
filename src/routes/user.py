

from fastapi import APIRouter, Depends, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


from core.user_session import current_user
from src.auth.models import User

smtp_host = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP(smtp_host, smtp_port)
server.starttls()
message = MIMEMultipart()
server.login('khaydarshin2007@gmail.com', 'hqebptzjhecgqhhs')
message['From'] = 'khaydarshin2007@gmail.com'
message['Subject'] = 'Информация вашего профиля'

user = APIRouter(
    prefix='/user',
    tags=['USER']
)


@user.get('/inf')
async def get_inf(user: User = Depends(current_user)):
    try:
        phone = user.phone[0:2] + '########' + user.phone[-2::]
        cards = []
        for i in user.cards:
            i = str(i)
            card = i[0] + '##############' + i[-1]
            cards.append(card)
        result = {'first_name': user.first_name, 'last_name': user.last_name,'email': user.email, 'phone': phone,'cards':cards, 'address': user.address, 'verified': user.is_verified}
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'loggin {e}')


@user.get('inf/email')
def get_int_on_email(user: User = Depends(current_user)):
   try:
       message['To'] = user.email
       body = f"first_name - {user.first_name};\n last_name - {user.last_name};\n email - {user.email};\n phone - {user.phone};\n cards - {user.cards};\n address - {user.address};\n verified - {user.is_verified}"
       message.attach(MIMEText(body, 'plain'))
       server.send_message(message)
       return {
           'status': 'successful',
       }
   except Exception as e:
       raise HTTPException(status_code=400, detail=f'loggin')

