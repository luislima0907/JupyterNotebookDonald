/*
   Consulta RFM - Taller Donald
   Consolida por cada cliente las tres dimensiones del modelo RFM:

     - Proximidad     (Recencia): dias transcurridos desde su ultima visita al
                       taller (tabla Cita).
     - Frecuencia     : cantidad de visitas distintas realizadas al taller
                       (tabla Cita).
     - ValorMonetario : total facturado al cliente segun los documentos
                       fiscales asociados a sus ordenes de trabajo.

   La fecha de referencia para la proximidad es la fecha de la cita mas reciente
   registrada en la base de datos (estandar para analisis RFM reproducible).
 */

SET NOCOUNT ON

-- Fecha de analisis para obtener la ultima cita registrada en el taller.
DECLARE @FechaReferencia DATE = (SELECT MAX(FechaCita) FROM dbo.Cita)

WITH Visitas AS (
    -- Frecuencia de visitas y fecha de la ultima visita por cliente.
    SELECT
        c.CodigoCliente,
        COUNT(DISTINCT c.NumeroCita) AS Frecuencia,
        MAX(c.FechaCita)             AS UltimaVisita
    FROM Cita AS c
    WHERE c.CodigoCliente IS NOT NULL
      AND c.FechaCita IS NOT NULL
    GROUP BY c.CodigoCliente
),
Facturacion AS (
    -- Valor monetario: se suma cada documento fiscal una sola vez por cliente
    -- (DISTINCT sobre la llave del documento) para evitar duplicar el total
    -- cuando una orden tiene varios detalles de mano de obra.
    SELECT
        d.CodigoCliente,
        SUM(d.ValorTotal) AS ValorMonetario
    FROM (
        SELECT DISTINCT
            c.CodigoCliente,
            df.CodigoTipoDocumentoFiscal,
            df.Serie,
            df.Numero,
            df.ValorTotal
        FROM Cita AS c
        INNER JOIN OrdeDeTrabajo AS ot
            ON c.NumeroCita = ot.NumeroCita
        INNER JOIN DetalleManoDeObra AS dmo
            ON ot.NumeroOrden = dmo.NumeroOrden
        INNER JOIN  DocumentoFiscal AS df
            ON dmo.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
           AND dmo.Serie  = df.Serie
           AND dmo.Numero = df.Numero
        WHERE c.CodigoCliente IS NOT NULL
    ) d
    GROUP BY d.CodigoCliente
)
SELECT
    cli.CodigoCliente,
    COALESCE(sn.PrimerNombre, '') + ' ' + COALESCE(sn.PrimerApellido, '') AS NombreCliente,
    DATEDIFF(DAY, v.UltimaVisita, @FechaReferencia)                       AS Proximidad,
    v.Frecuencia                                                          AS Frecuencia,
    ISNULL(f.ValorMonetario, 0)                                           AS ValorMonetario
FROM Cliente AS cli
INNER JOIN SocioNegocio AS sn
    ON cli.CodigoSocio = sn.CodigoSocio
INNER JOIN Visitas AS v
    ON cli.CodigoCliente = v.CodigoCliente
LEFT JOIN Facturacion AS f
    ON cli.CodigoCliente = f.CodigoCliente
ORDER BY ValorMonetario DESC, Frecuencia DESC, Proximidad ASC;
