-------------------------------------------------------------------------
CREATE TABLE bitacora (
	id_cambio SERIAL PRIMARY KEY,
	id_historial_mod int,
	fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	usuario int,
	type_mod CHAR(1) NOT NULL,
	valor_pre JSONB,
    valor_nue JSONB,
	FOREIGN KEY (usuario) REFERENCES medico (id_medico)
);
------------------------------------------
CREATE OR REPLACE FUNCTION historial_trigger() RETURNS TRIGGER AS $$
DECLARE
    jsonb_dataNew JSONB;
	jsonb_dataOld JSONB;
BEGIN
    IF (TG_OP = 'INSERT') THEN-- ---------------------------------------------------------------INSERT
        jsonb_dataNew = row_to_json(NEW.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_nue)
        VALUES (CURRENT_TIMESTAMP, NEW.id_historial, 'I', jsonb_dataNew);
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN -- ------------------------------------------------------------UPDATE
        jsonb_dataNew = row_to_json(NEW.*);
		jsonb_dataOld = row_to_json(OLD.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_pre, valor_nue)
        VALUES (CURRENT_TIMESTAMP, OLD.id_historial, 'U', jsonb_dataOld, jsonb_dataNew);
        RETURN NEW;
    ELSIF (TG_OP = 'DELETE') THEN -- -------------------------------------------------------------DELETE
        jsonb_dataOld = row_to_json(OLD.*);
        INSERT INTO bitacora (fecha_modificacion, id_historial_mod, type_mod, valor_pre)
        VALUES (CURRENT_TIMESTAMP,OLD.id_historial, 'D', jsonb_dataOld);
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

------------------------------------------------
CREATE TRIGGER historial_changes
AFTER INSERT OR UPDATE OR DELETE
ON historial
FOR EACH ROW
EXECUTE PROCEDURE historial_trigger();
-----------------------------------------------------------
SELECT * FROM historial;
INSERT INTO historial VALUES (37,'2023-03-20','diabetes','Insulina','Va mal', 'Murio','No logro',2,2,3,5);
UPDATE historial SET comentario = 'Nuevo diagnostico' WHERE id_historial = 37;
DELETE FROM historial WHERE id_historial = 37;
SELECT * FROM bitacora;

---------------------------------------------------------------------------------------------------------------

-- Historial de paciente
SELECT p.nombre, p.masacorporal,p.altura,p.adicciones,p.telefono,p.direccion,
	h.herencia, e.nombre, h.tratamiento, h.evolucion, h.estado, h.comentario, m.nombre
FROM historial h
JOIN paciente p ON h.id_paciente = p.id_paciente
JOIN medico m ON h.id_medico = m.id_medico
JOIN enfermedad e ON h.id_enfermedad = e.id_enfermedad WHERE h.id_paciente = 1;


-- 15% de inventario
SELECT u.nombre, i.cantidad, (i.expiracion - current_date) AS dias_habiles FROM inventario i
JOIN utencilio_med u
ON u.id_utencilio = i.id_utencilio
WHERE i.cantidad<= (0.15*u.cant_optima) AND i.id_lugar = 1;














SELECT * FROM historial;
INSERT INTO historial VALUES (36,'2025-9-4','Ninguna','Ninguno','Murio','Muerto','Se nos fue',3,1,2,8)
-- Enfermedades mortales
SELECT e.nombre AS Enfermedad, count(h.id_enfermedad) AS Muertes FROM historial h
JOIN enfermedad e
ON e.id_enfermedad = h.id_enfermedad
WHERE h.estado LIKE 'Muerto%'
GROUP BY e.nombre
ORDER BY Muertes DESC;
--Top 10 de los médicos que más pacientes han atendido.
SELECT * FROM lugar;
SELECT m.nombre AS medico, count(h.id_medico) AS visita
FROM historial h
JOIN medico m ON h.id_medico = m.id_medico
GROUP BY medico
ORDER BY  visita DESC
LIMIT 10;
-- 5 Pacientes que mas veces han visitado el lugar
SELECT COUNT(h.id_paciente) AS cuenta, p.nombre, p.masacorporal, p.altura, p.adicciones, p.telefono, p.direccion
FROM historial h
JOIN paciente p
ON h.id_paciente = p.id_paciente
WHERE h.id_lugar = 1
GROUP BY p.id_paciente
ORDER BY cuenta desc
LIMIT 5;
-- Reporte mensual de utencilios de la unidad medica a punto de acabarse
SELECT u.nombre, i.cantidad FROM inventario i
JOIN utencilio_med u
ON i.id_utencilio = u.id_utencilio
WHERE i.cantidad<10 AND i.id_lugar = "Variable";
-- Todos los mas populares
SELECT lugar.nombre AS lugar, COUNT(*) AS cantidad_pacientes
FROM lugar
JOIN historial ON lugar.id_lugar = historial.id_lugar
GROUP BY lugar.id_lugar
ORDER BY cantidad_pacientes DESC
LIMIT 3;

--sacar top 3 de hospital
SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes
FROM lugar
JOIN historial ON lugar.id_lugar = historial.id_lugar
WHERE lugar.nombre LIKE '%Hospital%'
GROUP BY lugar.nombre
ORDER BY cantidad_pacientes DESC
LIMIT 3;
--sacar top 3 de clinica
SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes
FROM lugar
JOIN historial ON lugar.id_lugar = historial.id_lugar
WHERE lugar.nombre LIKE '%Clinica%'
GROUP BY lugar.nombre
ORDER BY cantidad_pacientes DESC
LIMIT 3;
--sacar top 3 de centro medico
SELECT lugar.nombre, COUNT(*) AS cantidad_pacientes
FROM lugar
JOIN historial ON lugar.id_lugar = historial.id_lugar
WHERE lugar.nombre LIKE '%Centro Medico%'
GROUP BY lugar.nombre
ORDER BY cantidad_pacientes DESC
LIMIT 3;


SELECT COUNT(h.id_paciente) AS cuenta, p.nombre, p.telefono, p.direccion FROM historial h JOIN paciente p ON h.id_paciente = p.id_paciente WHERE h.id_lugar = 1 GROUP BY p.id_paciente ORDER BY cuenta desc  LIMIT 5;