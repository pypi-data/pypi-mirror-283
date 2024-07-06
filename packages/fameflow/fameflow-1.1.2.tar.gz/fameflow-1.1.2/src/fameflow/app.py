import requests

class api : 
    def ListServices(self):
        response = requests.get('https://fameflows.site/api/services/page?v=3&full=false')
        return response.json()
    
    def ServiceInfo(self,id):
        response = requests.get(f'https://fameflows.site/api/services/{id}')
        return response.json()
    
    def NewOrder(self,id,link,quantity,Keye):
        response = requests.get(f'https://fameflows.site/api/v2?action=add&service={id}&link={link}&quantity={quantity}&key={Keye}')
        return response.json()
    
    def OrderStatus(self,orders,Keye):
        response = requests.get(f'https://fameflows.site/api/v2?action=status&orders={orders}&key={Keye}')
        return response.json()
        
    def Balance(self,Keye):
        response = requests.get(f'https://fameflows.site/api/v2?action=balance&key={Keye}')
        return response.json()
    