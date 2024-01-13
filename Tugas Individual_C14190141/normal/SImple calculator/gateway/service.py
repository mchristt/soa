from nameko.web.handlers import http
from werkzeug.wrappers import Response
import uuid

from gateway.dependencies.session import SessionProvider

class Service:
    name = "gateway_service"

    session_provider = SessionProvider()
    
    @http('GET', '/login')
    def login(self, request):
        user_data = {
            'id': 1,
            'username': 'User'
        }
        
        session_id = self.session_provider.set_session(user_data)
        response = Response(str(user_data))
        response.set_cookie('SESSID', session_id)
        return response

    @http('GET', '/prime/<number>')
    def prima(self, request,number):
        print("number "+str(number))
        
        ctr=2
        isi=-1
        ctrPrima=0
        number=int(number)
        
        while (isi==-1):
            if (self.is_prime(ctr)) :
                print(str(ctrPrima)+":"+str(number)+":"+str(ctr))
                if (ctrPrima==number) :
                    isi=ctr
                ctrPrima=ctrPrima+1
            ctr=ctr+1
            
        response = Response("Prime "+str(isi))
        return response
    
    def is_prime(self,n):
        for i in range(2,n):
            if (n%i) == 0:
                return False
        return True

    @http('GET', '/check')
    def check(self, request):
        cookies = request.cookies
        return Response(cookies['SESSID'])

    @http('GET', '/primepalindrome/<number>')
    def primepalindrome(self, request,number):
        print("number "+str(number))
        
        ctr=2
        isi=-1
        ctrPrima=0
        number=int(number)
        
        while (isi==-1):
            if (self.temp(ctr)) :
                if (ctrPrima==number) :
                    isi=ctr
                ctrPrima=ctrPrima+1
            ctr=ctr+1
            
        response = Response("PrimePalindrome index - "+ str(ctrPrima) + " is " + str(isi))
        return response
    
    def is_PrimePalindrome(self,num):
        reverse= int(str(num)[::-1])
        
        if num==reverse:
            if num>1:
                for i in range(2,num):
                    if num%i==0:
                        return False
        else:
            return True
        
    def temp(self,number):
        isprime = True
        for i in range(2,number):
            if (number % i) == 0:
                 isprime= False
                 #return False
        
        if(str(number) != str(number)[::-1]):
            isprime=False
        
        return isprime