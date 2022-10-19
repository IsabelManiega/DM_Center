from pydantic import BaseModel

class Empleado(BaseModel):
    numero_empleado: int
    #Nombre y appelidos
    nombre: str
    edad: int
    
    #Director
    cargo: str

    #Ventas
    departamento: str

    #Mensual
    salario: float