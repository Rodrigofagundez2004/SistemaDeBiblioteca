CREATE DATABASE IF NOT EXISTS sistemadebiblioteca;
USE SistemaDeBiblioteca;

-- =============================================
-- TABLAS MAESTRAS (sin dependencias)
-- =============================================

-- Tabla: facultad
CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla: participante
CREATE TABLE participante (
    ci VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: edificio
CREATE TABLE edificio (
    nombre_edificio VARCHAR(50) PRIMARY KEY,
    direccion VARCHAR(200) NOT NULL,
    departamento VARCHAR(50) NOT NULL
);

-- =============================================
-- TABLAS CON DEPENDENCIAS
-- =============================================

-- Tabla: programa_academico
CREATE TABLE programa_academico (
    nombre_programa VARCHAR(100) PRIMARY KEY,
    id_facultad INT NOT NULL,
    tipo ENUM('grado', 'posgrado') NOT NULL,
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

-- Tabla: sala
CREATE TABLE sala (
    nombre_sala VARCHAR(50) PRIMARY KEY,
    edificio VARCHAR(50) NOT NULL,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    tipo_sala ENUM('libre', 'posgrado', 'docente') NOT NULL,
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

-- Tabla: turno
CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- Tabla: participante_programa_academico
CREATE TABLE participante_programa_academico (
    id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
    ci_participante VARCHAR(20) NOT NULL,
    nombre_programa VARCHAR(100) NOT NULL,
    rol ENUM('alumno', 'docente') NOT NULL,
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

-- Tabla: reserva
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(50) NOT NULL,
    edificio VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    id_turno INT NOT NULL,
    estado ENUM('activa', 'cancelada', 'sin asistencia', 'finalizada') NOT NULL DEFAULT 'activa',
    FOREIGN KEY (nombre_sala) REFERENCES sala(nombre_sala),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

-- Tabla: reserva_participante
CREATE TABLE reserva_participante (
    ci_participante VARCHAR(20) NOT NULL,
    id_reserva INT NOT NULL,
    fecha_solicitud_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    asistencia BOOLEAN DEFAULT NULL,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- Tabla: sancion_participante
CREATE TABLE sancion_participante (
    ci_participante VARCHAR(20) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    PRIMARY KEY (ci_participante, fecha_inicio),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

-- Tabla: login
CREATE TABLE login (
    correo VARCHAR(100) PRIMARY KEY,
    contraseña VARCHAR(255) NOT NULL,
    FOREIGN KEY (correo) REFERENCES participante(email)
);