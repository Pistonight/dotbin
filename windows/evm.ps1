$vm = $args[0]
$user = $args[1]
if ($user -eq $null) {
    $user = $env:VMUSER
}
ssh -i ~\.ssh\$vm $user@$vm
