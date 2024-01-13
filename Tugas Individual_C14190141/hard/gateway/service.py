import json
from nameko.web.handlers import http
from werkzeug.wrappers import Response

import requests
import uuid

from nameko.rpc import RpcProxy

from gateway.dependencies.session import SessionProvider
from gateway.dependencies.dependencies import Database,DatabaseWrapper

class Service:
    name = "gatewayServices"
    
    userRpc = RpcProxy('userServices')

    session_provider = SessionProvider()
    
    #register
    @http('POST', '/register')
    def register(self, request):
        registData = request.json
        response = self.userRpc.add_user(registData['nrp'],registData['name'],registData['email'],registData['password'])
        
        return response
    
    #login
    @http('POST', '/login')
    def login(self, request):
        loginData = request.json
        
        data = self.userRpc.get_user(loginData['email'],loginData['password'])
        
        if data and len(data)>0 :
            data=data[0]
            session_id = self.session_provider.set_session(data)
            data['session_id']=session_id
            response = Response(str(data))
            response.set_cookie('SESSID', session_id)
            #print(session_id)
            return response
        else :
            response = Response("Login failed, username or password may be wrong!")
            return response
    
    @http('GET', '/checkUser')
    def check(self,request) :
        cookies = request.cookies
        if cookies:
            print("checkuser "+cookies["SESSID"])
            session_data = self.session_provider.get_session(str(cookies['SESSID']))   
            return str(session_data)
        else :
            return None
        
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        
        if cookies:
            session_data = self.session_provider.delete_session(cookies['SESSID'])
            
            response = Response('Logout succeed!')
            return response
        else:
            response = Response('Logout failed!')
            return response
    
    @http("POST", "/upload/<judul>/<abstract>")
    def save_file(self, request,judul,abstract):
        #print("request data")
        cookies = request.cookies
        session_data=None
        if cookies:
            print("checkuser "+cookies["SESSID"])
            session_data = self.session_provider.get_session(str(cookies['SESSID']))  
            
        if (session_data!=None):
            for file in request.files.items():
                _, file_storage = file
                lowercase_str = uuid.uuid4().hex  
                #print("File "+file_storage.filename)
                fnameakhir=lowercase_str+file_storage.filename
                fname="upload/"+fnameakhir
                self.userRpc.add_file(session_data['id'],fname,judul,abstract)
                
                file_storage.save(f"{fname}")
            return json.dumps({"Recieved": True})
        else :
            return "Upload failed!"
    
    
    @http('GET', "/download")
    def files(self,request):  # pragma: no cover
        url = "http://google.com/favicon.ico"
        r = requests.get(url, allow_redirects=True)
        #print(r.status)
        open("google.ico", "wb").write(r.content)
        return r
        #u"received: {}".format(request.get_data(as_text=True))
        
    @http('GET', "/search/<judul>/<abstract>")
    def search_file(self,request,judul,abstract):  # pragma: no cover
        cookies = request.cookies
        session_data = None
        
        if cookies:
            print("checkuser "+cookies["SESSID"])
            session_data = self.session_provider.get_session(str(cookies['SESSID']))  
        
        search = self.userRpc.search_file(judul,abstract)
        
        session_id = self.session_provider.set_session(search)
        search['session_id']=session_id
            
        response.set_cookie('SESSID', session_id)
        response = Response(str(search))
           
        return response
    
        
    
    