
print("\
\n\
    AVISO DE LICENCIA\n\
\n\
Yo el creador de esta librería, he decidido hacer \n\
disponible esta, de manera abierta, para cualquiera. \n\
por supuesto que yo mismo, considero que yo, más adelante podre \n\
reemplazar este documento por uno que muestre los permisos \n\
más claramente.\n\
\n\
Espero también encontrar una licencia adecuada que también \n\
les permita a las empresas privadas la utilización de la libreria, \n\
que este documento se encuentra protegiendo, sin que \n\
estos estén obligados a ir en contra de su sustento \n\
(manteniendo que se encontrarían obligados a disponer todos \n\
sus productos de manera gratuita). A la vez, que me asegure, \n\
que los permisos o derechos no serán cooptados por alguna \n\
organización privada independiente.\n\
\n\
Téngase en cuenta la fecha de creación \n\
de este aviso de licencia y la del producto que esta protege: \n\
7 de junio de 2024 \n\
\n\
\n\
\n\
 DOCUMENTACION\n\
\n\
==============================================================\n\
Español... mi lengua natal \n\
\n\
\n\
Paquete de librería distribuida para python, Versión: 1.0.0 \n\
Nombre: PROSIGUE \n\
\n\
dependencias de librerías incorporadas:\n\
\n\
    multiprocessing \n\
    threading \n\
    time \n\
    os \n\
\n\
funcionalidades que puedo ver de PROSIGUE:\n\
\n\
    - Manejo de Sistema. \n\
    - Consulta a servidores externos. \n\
    - Le atribuye mayor importancia al tiempo de ejecución \n\
      de un proceso (sobre todo dentro de un sistema \n\
      desarrollado con múltiples prosigues). \n\
    - Tratamiento de los multi-hilos de la computación \n\
      cuántica para el desarrollo \n\
      de un núcleo o un único interprete con mucha más \n\
      potencia de trabajo (del famoso lenguaje booleano). \n\
    - como: métodos diseñados y utilizado \n\
      (en forma de varios estándares) para hacer \n\
      pruebas a los núcleos de la posibles futuras computadoras \n\
      cuánticas, antes de ser introducidas al mercado.\n\
\n\
PROSIGUE es una librería que...\n\
\n\
    He decidido desarrollarla con el propósito de nutrir \n\
    más al mundo de la programación. Es una librería \n\
    que, por supuesto busca ser sencilla de ser empleada. \n\
    Y realiza una operación tan practica que podría desearse \n\
    en cualquier sistema informático o de computo. \n\
\n\
    Por tanto, mantengo el deseo en este momento de \n\
    desarrollar su versión 2.0. en la que, puedan \n\
    manejarse en ciertas fases \n\
    (los distintos prosigues que se encuentre ejecutándose) \n\
    con una especie de reloj o clock que envíe pulsos \n\
    por todo el sistema. \n\
\n\
Forma de Ejecutar PROSIGUE:\n\
\n\
    utilice un formato similar al ejemplo siguiente: \n\
\n\
\n\
    from prosigue_v1.standard.principiofinal import Operador, Restituye \n\
    from prosigue_v1.command import Prosigue \n\
\n\
    def sample(): \n\
\n\
        dicci= dict([ \n\
            (1, 'camion'), (2, 'todo_terreno'), (3, 'deportivo') \n\
        ]) \n\
\n\
        prosigue_1= Prosigue(dicci) \n\
\n\
        #demolicion= prosigue_1.eliter() \n\
        moviendo= Operador() \n\
\n\
        prosigue_1.notisure(moviendo) \n\
        prosigue_1.tiempo(10) \n\
\n\
        config_01_back= prosigue_1.close(False) \n\
\n\
        '.................................' \n\
\n\
        if prosigue_1.answer == 1: \n\
\n\
            print(dicci) \n\
            print(config_01_back) \n\
            print() \n\
\n\
            for e, i in enumerate(config_01_back): # actualiza la list dicci \n\
\n\
                strem= config_01_back[i] \n\
                dicci[e + 1]= strem \n\
\n\
            print(dicci) \n\
            print(config_01_back) \n\
\n\
        else: \n\
            print('Se ha vencido el proceso') \n\
            a_restab= Restituye() \n\
            prosigue_1.imagen_reset(a_restab) \n\
\n\
        print() \n\
\n\
\n\
    if __name__ == '__main__': \n\
        sample() \n\
\n\
\n\
    Puedes modificar el tiempo de espera en: \n\
    prosigue_1.tiempo(10) \n\
\n\
    Ademas, debes saber que este scrip se encuentra \n\
    usando un ejemplo de los bloques a ejecutar \n\
    (Clasicos de la libreria PROSIGUE)... \n\
    Operar: para hacer la tarea secundaria, \n\
    en: moviendo= Operador() & \n\
    Restablece: para corregir o volver a hacer una posible solicitud, \n\
    en: a_restab= Restituye() \n\
\n\
    La segunda tarea tiene un time.sleep(8) \n\
    en su objeto del ejemplo 'moviendo= Operador()' \n\
    asi que si usted da una espera menor de (5 por ejemplo) \n\
    hara que la segunda tarea se demore mas de lo esperado \n\
    por el diseñador del software en este caso usted y \n\
    por tanto que se venza. ejemplo simple de todo esto:\n\
\n\
    en vez de:  prosigue_1.tiempo(10) \n\
    usa:        prosigue_1.tiempo(5) \n\
\n\
    Una tarea vencida por pasarse de tiempo podra \n\
    entrar a else (de utilizarse la instancia answer).\n\
\n\
    Sirvase reemplazar las dos clases 'clasicas' \n\
    de operacion para esta libreria, a saber (Operador(), Restituye()) \n\
    por dos clases personales, donde pueda depositar el codigo \n\
    que efectue la tarea que usted desee realizar.\n\
\n\
    Si utiliza su propia clase asegurece de quitarle el \n\
    carapter sharp (#) a la linea de eliter \n\
    en: #demolicion= prosigue_1.eliter() \n\
    y pasarle 'demolicion' como argumento al constructor \n\
    de su clase, en la siguiente linea. ademas, usted \n\
    debera cambiar: config_01_back= prosigue_1.close(False) \n\
    por:            config_01_back= prosigue_1.close(True) \n\
    para que funcione adecuadamente. \n\
    el_iter (demolicion) hará las veces de return en \n\
    su clase y se debera escribir: \n\
    su_nombre_argumento.put(nombre_variable_a_retornar) \n\
\n\
    Si su codigo no requiere de retornar un valor, \n\
    pruebe, desestimar el metodo.eliter y los cambios. \n\
    pero, procure pasar el argumento el_iter desde el \n\
    constructor (en su clase) al metodo 'empieza' \n\
    de su misma clase. \n\
    de manera que 'empieza' tenga dos (2) atributos de entrada.\n\
\n\
    Por ultimo la clase que contendra el codigo para la segunda \n\
    tarea debera tener un metodo llamado 'empieza' con un \n\
    atributo de entrada (que es el dato dado al instanciar \n\
    la clase PROSIGUE, osea dicci en nuestro ejemplo) \n\
    dentro de este metodo coloque el codigo. \n\
    Como puede ver, de entre nuestros objetos le podemos pasa uno (1) \n\
    al proceso que realiza la segunda tarea. \n\
    en: prosigue_1= Prosigue(dicci) \n\
    Ademas, Restituye tambien debera tener un atributo de \n\
    entrada que debera ser... en la version 1.0 de prosigue \n\
    de... (0) o False. \n\
    El modulo de entrada en este caso se llamara 'termina'.\n\
\n\
==============================================================\n\
translated with google \n\
\n\
Distributed library package for python, Version: 1.0.0 \n\
Name: PROSIGUE \n\
\n\
built-in library dependencies:\n\
\n\
    multiprocessing \n\
    threading \n\
    time \n\
    os \n\
\n\
features that I can see from PROSIGUE:\n\
\n\
    - System Management. \n\
    - Consultation with external servers. \n\
    - It attributes greater importance to the execution \n\
      time of a process (especially within a system developed \n\
      with multiple processes). \n\
    - Treatment of multi-threaded quantum computing for the \n\
      development of a core or a single interpreter with \n\
      much more working power (from the famous Boolean language). \n\
    - as: methods designed and used (in the form of various \n\
      standards) to test the cores of possible future \n\
      quantum computers, before being introduced to the market. \n\
\n\
PROSIGUE is a bookstore that... \n\
\n\
    I have decided to develop it with the purpose of further \n\
    nurturing the world of programming. It is a bookstore \n\
    that, of course, seeks to be easy to use. \n\
    And it performs an operation so practical that it could \n\
    be desired in any computer or computing system. \n\
\n\
    Therefore, I maintain the desire at this time to \n\
    develop its version 2.0. in which, they can be managed \n\
    in certain phases (the different processes that are \n\
    running) with a type of clock that sends pulses \n\
    throughout the system. \n\
\n\
    In addition to the clock implementation, I would \n\
    also like to make it possible to PROCEED pools. \n\
\n\
How to Execute PROSIGUE:\n\
\n\
    use a format similar to the example shown in the call.py module \n\
\n\
    namely: look at the example above \n\
\n\
    ... \n\
\n\
    You can modify the waiting time in: \n\
    prosigue_1.tiempo(10) \n\
\n\
    Also, you should know that this script is using \n\
    an example of the blocks to execute \n\
    (Classics from the PROSIGUE bookstore)... \n\
    Operate: to do the secondary task, \n\
    in: moviendo= Operador() & \n\
    Reset: to correct or resubmit a possible request, \n\
    in: a_restab= Restituye() \n\
\n\
    The second task has a time.sleep(8) \n\
    in your example object 'moviendo= Operador()' \n\
    so if you give a wait less than (5 for example) \n\
    will make the second task take longer than expected \n\
    by the software designer in this case you and \n\
    therefore it expires. simple example of all this:\n\
\n\
    instead of:     prosigue_1.tiempo(10) \n\
    use:            prosigue_1.tiempo(5) \n\
\n\
    A task overdue for overtime could \n\
    enter else (if the answer instance is used).\n\
\n\
    Please replace the two classic 'classes' \n\
    of operation for this library, namely (Operador(), Restituye()) \n\
    for two personal classes, where you can deposit the code \n\
    to perform the task you want to perform.\n\
\n\
    If you use your own class be sure to remove the \n\
    carapter sharp (#) to the eliter line \n\
    in: #demolicion= prosigue_1.eliter() \n\
    and pass 'demolicion' as an argument to the constructor \n\
    of its class, on the next line. Furthermore, you \n\
    should change:  config_01_back= prosigue_1.close(False) \n\
    by:             config_01_back= prosigue_1.close(True) \n\
    for it to work properly. \n\
    el_iter (demolicion) will act as return in \n\
    your class and you should write: \n\
    your_argument_name.put(variable_name_to_return) \n\
\n\
    If your code does not require returning a value, \n\
    try, dismiss the.eliter method and the changes. \n\
    but, try to pass the el_iter argument from \n\
    constructor (in your class) to the 'empieza' method \n\
    of the same class. \n\
    so 'empieza' has two (2) input attributes.\n\
\n\
    Finally, the class that will contain the code for the second \n\
    task should have a method called 'empieza' with a \n\
    input attribute (which is the data given when instantiating \n\
    the class PROSIGUE, that is, dicci in our example) \n\
    Inside this method place the code. \n\
    As you can see, from among our objects we can pass one (1) \n\
    to the process that performs the second task. \n\
    in: prosigue_1= Prosigue(dicci) \n\
    Additionally, Restituye must also have a \n\
    entry that should be... in version 1.0 of prosigue \n\
    of... (0) or False. \n\
    The input module in this case will be called 'termina'.\n\
    ")

