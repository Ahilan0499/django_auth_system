import jwt,datetime

def create_access_token(id):
    payload={
         
        'id':id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat':datetime.datetime.utcnow()

           }
    token1=jwt.encode(payload , 'access_secret' , algorithm='HS256')
    return token1    


def create_refresh_taken(id):
    payload={
         
        'id':id,
        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat':datetime.datetime.utcnow()

           }
    token2=jwt.encode(payload , 'refresh_secret' , algorithm='HS256')
    return token2
   
          

                
              
