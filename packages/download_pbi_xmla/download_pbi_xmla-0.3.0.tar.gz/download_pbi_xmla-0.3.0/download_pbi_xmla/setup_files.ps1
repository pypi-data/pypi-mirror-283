# PowerShell script to copy and rename example files
Copy-Item -Path ".env_example" -Destination ".env"
Copy-Item -Path "example_config.json" -Destination "config.json"

Write-Output "Environment setup files have been created."
