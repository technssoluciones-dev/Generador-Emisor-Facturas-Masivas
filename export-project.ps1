# ============================================================
#  export-project.ps1
#  Exporta todos los archivos de un proyecto a un .txt
#  Uso: .\export-project.ps1
#  Opcional: .\export-project.ps1 -Ruta "C:\MiProyecto" -Salida "output.txt"
# ============================================================

param (
    [string]$Ruta   = (Get-Location).Path,
    [string]$Salida = "proyecto_completo.txt"
)

# Carpetas a ignorar
$carpetasExcluidas = @(
    ".git", "node_modules", "bin", "obj", ".vs",
    "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".idea", ".mypy_cache"
)

# Extensiones prioritarias (aparecen primero en el output)
$prioAlta = @(".py", ".json", ".sql")

# Extensiones a incluir (vacío = todas)
$extensionesIncluidas = @()  # Dejar vacío para incluir TODO

# Extensiones a excluir siempre
$extensionesExcluidas = @(
    ".exe", ".dll", ".pdb", ".bin", ".obj",
    ".png", ".jpg", ".jpeg", ".gif", ".ico",
    ".zip", ".rar", ".7z", ".tar", ".gz",
    ".pdf", ".docx", ".xlsx", ".pptx",
    ".pyc", ".pyo", ".db", ".sqlite3"
)

# ============================================================

Write-Host ""
Write-Host "  TECHNS - Exportador de Proyectos" -ForegroundColor Cyan
Write-Host "  Ruta: $Ruta" -ForegroundColor Gray
Write-Host "  Salida: $Salida" -ForegroundColor Gray
Write-Host ""

# Preguntar si se desea excluir carpetas adicionales
$respuesta = Read-Host "  Desea omitir alguna carpeta adicional? (s/n)"
if ($respuesta -eq "s" -or $respuesta -eq "S") {
    $input = Read-Host "  Ingrese el nombre de la carpeta a omitir"
    if ($input -ne "") {
        $carpetasExcluidas += $input
        Write-Host "  Carpeta '$input' agregada a la lista de exclusion." -ForegroundColor Yellow
    }
}
Write-Host ""

$scriptActual = $MyInvocation.MyCommand.Path

$todosLosArchivos = Get-ChildItem -Path $Ruta -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $filePath = $_.FullName
    if ($filePath -eq $scriptActual) { return $false }   # ← excluye el propio script
    $enCarpetaExcluida = $false
    foreach ($carpeta in $carpetasExcluidas) {
        if ($filePath -like "*\$carpeta\*" -or $filePath -like "*/$carpeta/*") {
            $enCarpetaExcluida = $true
            break
        }
    }
    if ($enCarpetaExcluida) { return $false }

    # Excluir extensiones no deseadas
    if ($extensionesExcluidas -contains $_.Extension.ToLower()) { return $false }

    # Si hay filtro de extensiones, aplicar
    if ($extensionesIncluidas.Count -gt 0) {
        return ($extensionesIncluidas -contains $_.Extension.ToLower())
    }

    return $true
}

# Ordenar: primero los de alta prioridad, luego el resto
$archivosOrdenados = $todosLosArchivos | Sort-Object {
    if ($prioAlta -contains $_.Extension.ToLower()) { 0 } else { 1 }
}, FullName

$totalArchivos  = $archivosOrdenados.Count
$totalLineas    = 0
$output         = ""

# Encabezado del archivo
$output += "# EXPORTACION DE PROYECTO`n"
$output += "# Generado: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$output += "# Ruta origen: $Ruta`n"
$output += "# Total archivos: $totalArchivos`n"
$output += "`n"

# Indice de archivos
$output += "================================================================`n"
$output += "INDICE DE ARCHIVOS`n"
$output += "================================================================`n"
foreach ($archivo in $archivosOrdenados) {
    $rel = $archivo.FullName.Replace($Ruta, "").TrimStart("\", "/")
    $output += "  $rel`n"
}
$output += "`n`n"

# Contenido de cada archivo
$contador = 0
foreach ($archivo in $archivosOrdenados) {
    $contador++
    $rel = $archivo.FullName.Replace($Ruta, "").TrimStart("\", "/")

    Write-Host "  [$contador/$totalArchivos] $rel" -ForegroundColor DarkGray

    $contenido = Get-Content $archivo.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue

    if ($null -eq $contenido) {
        $contenido = "[No se pudo leer el archivo o esta vacio]"
    }

    $lineas = ($contenido -split "`n").Count
    $totalLineas += $lineas

    $output += "================================================================`n"
    $output += "FILE: $rel`n"
    $output += "TIPO: $($archivo.Extension.ToUpper())  |  LINEAS: $lineas  |  TAMAÑO: $([math]::Round($archivo.Length/1KB, 2)) KB`n"
    $output += "================================================================`n"
    $output += $contenido
    $output += "`n`n"
}

# Pie de pagina
$output += "================================================================`n"
$output += "FIN DE EXPORTACION`n"
$output += "Archivos: $totalArchivos  |  Lineas totales: $totalLineas`n"
$output += "================================================================`n"

# Guardar
$output | Set-Content -Path $Salida -Encoding UTF8

Write-Host ""
Write-Host "  Listo!" -ForegroundColor Green
Write-Host "  Archivos exportados : $totalArchivos" -ForegroundColor White
Write-Host "  Lineas totales      : $totalLineas" -ForegroundColor White
Write-Host "  Archivo generado    : $Salida" -ForegroundColor Cyan
Write-Host ""
