SELECT
    cli.CodigoCliente,
    COALESCE(sn.PrimerNombre, '') + ' ' + COALESCE(sn.PrimerApellido, '') AS NombreCliente,
    SUM(df.ValorTotal) AS Monetary
FROM dbo.Cliente cli
INNER JOIN dbo.SocioNegocio sn
    ON cli.CodigoSocio = sn.CodigoSocio
INNER JOIN dbo.Cita c
    ON cli.CodigoCliente = c.CodigoCliente
INNER JOIN dbo.OrdeDeTrabajo ot
    ON c.NumeroCita = ot.NumeroCita
INNER JOIN dbo.DetalleManoDeObra dmo
    ON ot.NumeroOrden = dmo.NumeroOrden
INNER JOIN dbo.DocumentoFiscal df
    ON dmo.CodigoTipoDocumentoFiscal = df.CodigoTipoDocumentoFiscal
   AND dmo.Serie = df.Serie
   AND dmo.Numero = df.Numero
WHERE df.FechaEmision BETWEEN '2016-06-02' AND '2026-06-02'
GROUP BY
    cli.CodigoCliente,
    COALESCE(sn.PrimerNombre, '') + ' ' + COALESCE(sn.PrimerApellido, '')
ORDER BY Monetary DESC;
