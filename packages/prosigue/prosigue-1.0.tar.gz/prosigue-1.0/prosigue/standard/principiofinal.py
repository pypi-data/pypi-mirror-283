
""" Proceso que se realiza al entrar a un comando prosigue """


"===================================================="

import time

"===================================================="

class Restituye:
    
    def termina(self, caso):
        
        if caso == False:
            
            print()
            print("Usted estaria restableciendo los datos")
            print("sirvase emplear una clase personal")
            print("en reemplazo de Restituye.")
            

class Operador:
    
    def empieza(self, configura, iter):
        
        configura[1]= "mi_carro"  # o, se puede mod una instancia
        iter.put(configura)

        time.sleep(8)

