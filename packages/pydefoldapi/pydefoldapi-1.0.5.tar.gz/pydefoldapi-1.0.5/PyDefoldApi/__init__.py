import PyDefold
import json , os , sys , inspect , importlib , pkgutil  , collections
from google.protobuf.descriptor import FieldDescriptor



class ApiBaseClass : 
    def __init__(self,**kwargs) : 
        self.keys = {k.name for k in self.fields}
        for k in self.fields : 
            if k.required : 
                setattr(self,k.name,k.default_value)
        {self.__dict__.update({k : v } ) for k , v  in kwargs.items() if k in self.keys}


    def to_dict(self) : 
        res = dict()
        res.update({ k.name : getattr(self,k.name ).to_dict() if hasattr(getattr(self,k.name ),'to_dict') else getattr(self,k.name )   for k in  self.fields if k.required })
        res.update({ k.name : getattr(self,k.name ).to_dict() if hasattr(getattr(self,k.name ),'to_dict') else getattr(self,k.name )  for k in  self.fields if (not k.required ) and ( getattr(self,k.name,None) is not None ) })
        return res  

    def __repr__(self) : 
        return f"{self.__class__.__name__}{json.dumps(self.to_dict() , indent = 4 )}"




class ApiBaseClassGenerator :
 
    def __init__(self , class_type ) : 
        self.types = { getattr(FieldDescriptor,k) : k.replace("TYPE_","").lower() for k in dir(FieldDescriptor) if k.startswith("TYPE_")}
        self.msg = class_type 


    def Parse(self) : 
        fields = [self.LoadField(field) for field in self.msg.DESCRIPTOR.fields ]
        exported = dict(fields = fields , protobuf = self.msg)
        exported_api_class = type(f"DF{self.msg.__name__}",(ApiBaseClass,),exported)
        return exported_api_class



    def LoadField(self,key) : 
        Field = collections.namedtuple('Field' , ['name' , 'type' , 'required' , 'default_value' , 'has_default_value'] )
        _name , _required , _default_value , _type , _has_default_value = key.name , key.has_presence , key.default_value , self.types[key.type] , key.has_default_value
        return Field(name = _name , required = _required , default_value = _default_value , type = _type , has_default_value = _has_default_value ) 






class Utils : 
    @classmethod
    def getPyDefoldPkgs(cls) : 
        return ['PyDefold'] + [module_info.name  for module_info in pkgutil.iter_modules(PyDefold.__path__)] 

    @classmethod
    def getPyDefoldMessages(cls) : 
        modules = cls.getPyDefoldPkgs()
        result = list()
        for module_name in modules : 
            pkg_name = 'PyDefold' if module_name == 'PyDefold' else f'PyDefold.{module_name}'
            pkg = importlib.import_module(pkg_name)
            for key in dir(pkg) : 
                if type(pkg.__getattribute__(key)).__name__ == 'MessageMeta' : 
                    message_type = pkg.__getattribute__(key) 
                    itm = dict(msg = message_type , pkg = pkg_name)
                    result.append(itm)
        return result

    @classmethod
    def getPyDefoldApiClasses(cls) : 
        exported_module_classes = list()
        messages = Utils.getPyDefoldMessages()
        for msg_dict in messages  : 
            msg = msg_dict.get('msg')
            gencls = ApiBaseClassGenerator(msg).Parse()
            cls_name = f"DF{msg.__name__}"
            globals()[cls_name] = gencls
            exported_module_classes.append(cls_name)



__all__ = Utils.getPyDefoldApiClasses()        



