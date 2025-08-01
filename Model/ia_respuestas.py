def ia_responder(user_msg):
    user_msg = user_msg.lower()
    if 'hola' in user_msg or 'buenas' in user_msg:
        return "¡Hola! ¿En qué puedo ayudarte hoy?"
    elif 'precio' in user_msg:
        return "Puedes ver los precios de los artículos en la tarjeta de cada producto."
    elif 'carrito' in user_msg:
        return "Para agregar productos al carrito, haz clic en el botón correspondiente en cada artículo."
    elif 'historial' in user_msg:
        return "Puedes consultar tu historial de compras en la sección 'Historial' del menú."
    elif 'ayuda' in user_msg or 'soporte' in user_msg:
        return "Si necesitas ayuda adicional, contáctanos a soporte@tusitio.com."
    elif 'devolver' in user_msg or 'devolución' in user_msg:
        return "Para solicitar una devolución, por favor contacta a soporte@tusitio.com con tu número de pedido."
    elif 'pago' in user_msg or 'metodo de pago' in user_msg:
        return "Aceptamos pagos con tarjeta, PayPal y transferencias bancarias."
    elif 'envío' in user_msg or 'entrega' in user_msg:
        return "El envío tarda de 2 a 5 días hábiles. Puedes ver el estado en tu historial de compras."
    elif 'factura' in user_msg:
        return "Puedes solicitar tu factura enviando un correo a facturacion@tusitio.com."
    elif 'contacto' in user_msg or 'correo' in user_msg:
        return "Nuestro correo de contacto es soporte@tusitio.com."
    elif 'gracias' in user_msg or 'thank' in user_msg:
        return "¡De nada! Si tienes otra pregunta, aquí estoy."
    else:
        return "Lo siento, no entendí tu pregunta. ¿Puedes reformularla o ser más específico?"
