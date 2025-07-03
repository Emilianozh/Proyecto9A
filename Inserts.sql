Drop database inventario;

select * from Usuarios;

-- usuario administrador
insert into Usuarios (tipo_usuario, nombre, apellido, nombre_usuario, direccion, teléfono, correo, contraseña)
values (True, "Emi", "Zuñiga", "admin", "Morelos", "77711111111", "20223tn117@utez.edu.mx", "emi12345") ;

-- usuario normal 
insert into Usuarios (tipo_usuario, nombre, apellido, nombre_usuario, direccion, teléfono, correo, contraseña)
values (False, "Carlos", "Zuñigaa", "cliente", "Morelos", "7772222222", "20223tn000@utez.edu.mx", "carlos12345");

select * from articulo;