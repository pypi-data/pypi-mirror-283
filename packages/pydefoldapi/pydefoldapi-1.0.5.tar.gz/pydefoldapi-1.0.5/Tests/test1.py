import PyDefoldApi 

def test_import() : 
    
    x = PyDefoldApi.DFPoint3(x=0.0, y=0.0, z=0.0)
    
    return x.to_dict() == dict(x=0.0, y=0.0, z=0.0) 
    