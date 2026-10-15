param(
    [Parameter(Mandatory)]
    [ValidatePattern('^ghcr\.io/mroshdy91/supplieratlas-demo@sha256:[a-f0-9]{64}$')]
    [string]$Image,
    [string]$Gcloud = "$env:LOCALAPPDATA\SupplierAtlas\tools\google-cloud-sdk\bin\gcloud.cmd"
)
$ErrorActionPreference = 'Stop'
$projectId = 'supplieratlas-demo-20261015'
$serviceName = 'supplieratlas-demo'
$region = 'us-central1'
$privateDir = Join-Path $env:USERPROFILE '.supplieratlas'
$runtimeFile = Join-Path $privateDir 'runtime.env.yaml'
New-Item -ItemType Directory -Path $privateDir -Force | Out-Null
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
& icacls $privateDir /inheritance:r /grant:r "${identity}:(OI)(CI)F" | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Could not restrict credential directory permissions' }
if (-not (Test-Path -LiteralPath $runtimeFile)) {
    $token = [Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
    $cursorKey = [Convert]::ToHexString([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
    $content = "SUPPLIER_ATLAS_TOKEN: '$token'`nSUPPLIER_ATLAS_CURSOR_KEY: '$cursorKey'`nSUPPLIER_ATLAS_ALLOWED_HOSTS: 'supplieratlas-demo-524685338738.us-central1.run.app'`n"
    [System.IO.File]::WriteAllText($runtimeFile, $content)
    Remove-Variable token,cursorKey,content
}
$runtimeContent = [System.IO.File]::ReadAllText($runtimeFile)
foreach ($setting in @{
    SUPPLIER_ATLAS_ACCESS_BACKEND = 'firestore'
    SUPPLIER_ATLAS_ACCESS_PROJECT = $projectId
}.GetEnumerator()) {
    $pattern = '(?m)^' + [regex]::Escape($setting.Key) + ':.*$'
    $line = $setting.Key + ": '" + $setting.Value + "'"
    if ([regex]::IsMatch($runtimeContent, $pattern)) {
        $runtimeContent = [regex]::Replace($runtimeContent, $pattern, $line)
    } else { $runtimeContent += "`n$line`n" }
}
[System.IO.File]::WriteAllText($runtimeFile, $runtimeContent)
Remove-Variable runtimeContent
& $Gcloud run deploy $serviceName --project=$projectId --region=$region --image=$Image `
    --service-account="supplieratlas-runtime@$projectId.iam.gserviceaccount.com" `
    --allow-unauthenticated --min=0 --max=1 --min-instances=0 --max-instances=1 --cpu=0.5 --memory=256Mi `
    --concurrency=1 --timeout=30 --execution-environment=gen1 --no-cpu-boost `
    --cpu-throttling --env-vars-file=$runtimeFile --quiet
if ($LASTEXITCODE -ne 0) { throw 'Cloud Run deployment failed' }
& $Gcloud run services describe $serviceName --project=$projectId --region=$region `
    --format='yaml(status.url,status.latestReadyRevisionName,status.conditions,spec.template.metadata.annotations,spec.template.spec.containers[0].resources)'
if ($LASTEXITCODE -ne 0) { throw 'Cloud Run verification failed' }
