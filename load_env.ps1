Get-Content .env | foreach{

   if([string]::IsNullOrEmpty($_)){
      return
   }

   $name, $value = $_.split('=', 2)

   if(!$name.Contains('#')){
      New-Item -Path env:\$name -Value $value 
   }

 }
