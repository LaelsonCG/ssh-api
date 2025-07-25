#!/bin/bash

nome=$1
pass=$2
u_temp=$3
limit=$4

useradd -M -s /bin/false $nome
(echo $pass;echo $pass) |passwd $nome > /dev/null 2>&1
echo "$pass" > /etc/SSHPlus/senha/$nome
echo "$nome $limit" >> /root/usuarios.db
echo "#!/bin/bash
killall -u $nome > /dev/null 2>&1
userdel -f $nome > /dev/null 2>&1
sed -i "/\b$nome\b/d" /root/usuarios.db
rm /etc/SSHPlus/senha/$nome > /dev/null 2>&1
rm /etc/SSHPlus/userteste/$nome.sh
exit 0" > /etc/SSHPlus/userteste/$nome.sh
chmod +x /etc/SSHPlus/userteste/$nome.sh
at -f /etc/SSHPlus/userteste/$nome.sh now + $u_temp hour > /dev/null 2>&1
echo "usuario criado"