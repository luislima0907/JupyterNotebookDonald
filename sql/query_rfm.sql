SET NOCOUNT ON;

-- Fecha de analisis para obtener la ultima cita registrada en el taller.
DECLARE @FechaReferencia DATE = (SELECT MAX(FechaCita) FROM dbo.Cita);

WITH FechaRef AS (
    SELECT MAX(FechaCita) AS FechaReferencia
    FROM dbo.Cita
),
Visitas AS (
    SELECT
        c.CodigoCliente,
        COUNT(DISTINCT c.NumeroCita) AS Frecuencia,
        MAX(c.FechaCita) AS UltimaVisita
    FROM dbo.Cita AS c
    WHERE c.CodigoCliente IS NOT NULL
      AND c.FechaCita IS NOT NULL
    GROUP BY c.CodigoCliente
),
Facturacion AS (
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
        FROM dbo.Cita AS c
        INNER JOIN dbo.OrdeDeTrabajo AS ot
            ON c.NumeroCita = ot.NumeroCita
        INNER JOIN dbo.DetalleManoDeObra AS dmo
            ON ot.NumeroOrden = dmo.NumeroOrden
        INNER JOIN dbo.DocumentoFiscal AS df
            ON dmo.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
           AND dmo.Serie = df.Serie
           AND dmo.Numero = df.Numero
        WHERE c.CodigoCliente IS NOT NULL
    ) AS d
    GROUP BY d.CodigoCliente
)
SELECT
    cli.CodigoCliente,
    COALESCE(sn.PrimerNombre, '') + ' ' + COALESCE(sn.PrimerApellido, '') AS NombreCliente,
    DATEDIFF(DAY, v.UltimaVisita, fr.FechaReferencia) AS Proximidad,
    v.Frecuencia AS Frecuencia,
    ISNULL(f.ValorMonetario, 0) AS ValorMonetario
FROM dbo.Cliente AS cli
INNER JOIN dbo.SocioNegocio AS sn
    ON cli.CodigoSocio = sn.CodigoSocio
INNER JOIN Visitas AS v
    ON cli.CodigoCliente = v.CodigoCliente
LEFT JOIN Facturacion AS f
    ON cli.CodigoCliente = f.CodigoCliente
CROSS JOIN FechaRef AS fr
ORDER BY ValorMonetario DESC, Frecuencia DESC, Proximidad ASC;
