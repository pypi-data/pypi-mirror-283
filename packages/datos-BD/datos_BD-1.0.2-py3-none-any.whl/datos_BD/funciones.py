

## Retornar servidores
def servidores():
    """ Función que retorna los Servidores Disponibles en la Librería

    Returns:
        [Tupla]: [Servidores disponibles para la Librería]
    """
    return ('isssteson01','serversql-oc')  


## Retornar las bases de datos disponibles para la Librería
def bases_d_datos(servidor):
    """AI is creating summary for bases_d_datos

    Args:
        servidor ([Tupla]): [description]

    Returns:
        [Tupla]: [Listado de Bases disponibles en la Librería según servidor seleccionado]
    """
    
    serv = servidores()
    
    if servidor == serv[0]:
        return ('ingresos','sipesdb','creditos')
    elif servidor == serv[1]:
        return ('ExpedientePensiones','ExpedientePrestaciones')
    else:
        return None



## Retornar los Datos para la Conexión dependiedo del Servidor
def DatosServidor(args):
    """Función para Retornar los parámetros para conexión a Base de Datos, según servidor

    Args:
        args ([Tupla]): [Servidor, Base de Datos]

    Returns:
        [Tupla]: [Servidor, Base de Datos, Usuario, Contraseña]
    """
    serv = servidores()
    
    if args[0] == serv[0]:
        cat = bases_d_datos(serv[0])
        if args[1] == cat[0]:
            return (serv[0],cat[0],'informatica','Erw47gLS')
        elif args[1] == cat[1]:
            return (serv[0],cat[1],'informatica','Erw47gLS')
        elif args[1] == cat[2]:
            return (serv[0],cat[2],'informatica','Erw47gLS')
        else:
            return None
    elif args[0] == serv[1]:
        cat = bases_d_datos(serv[1])
        if args[1] == cat[0]:
            return (serv[1],cat[0],'informatica','Erw47gLS')
        elif args[1] == cat[1]:
            return (serv[1],cat[1],'informatica','Erw47gLS')
        else:
            return None
    else:
        return None