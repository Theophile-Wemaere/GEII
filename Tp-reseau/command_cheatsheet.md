# Commande utiles

## netstat
>netstat est un outils commun à windows et et linux, permettant d'afficher l'état des connexions
>
>>les commandes suivantes sont pour linux:

| **Command** | **Description** |
|---|----|
| `netstat -tnp` | affiche les connexions établis avec un serveur distant |
| `netstat -tln` | affiche les connexions en attentes (ports ouverts) |
| `netstat -tanp` | affiche toute les connexions (en attente et établis |


## nmap 
>nmap est un outils permettant de scanner des machines pour trouver les "ports ouverts" (connexion en attente)

| **Command** | **Description** |
|---|----|
| `nmap 10.10.10.15` | simple scan sur les 1000 ports les plus utilisés |
| `nmap 10.10.10.15 -p 25` | ne scanne qu'un seul port, ici le 25 (SMTP) |
| `nmap 10.10.10.15 -p-` | scanne tous les ports |
| `nmap 10.10.10.15 -p3000-4000` | scanne tous les ports entre 3000 et 4000 |

## telnet
> telnet est un client (service) permettant de se connecter à un serveur distant
>
>>attention, les données transferées avec telnet ne sont pas cryptées, et donc récupérables

| **Command** | **Description** |
|---|----|
| `telnet 10.10.10.11 8443` | se connecte au port 8443 sur la machine à l'adresse 10.10.10.11 |

## nslookup et dig
>ces 2 commandes permettent d'obtenir des informations sur une adresse IP ou un nom de domaine

| **Command** | **Description** |
|---|----|
| `nslookup google.com` | renvois l'adresse IP du serveur du nom de google.com |
| `dig google.com` | même chose, mais avec plus d'informations (comme le temps de réponse) |
| `dig google.com +short` | ne renvois que l'adresse IP du serveur |
| `dig -x 216.58.198.206` | renvois le nom de domaine du serveur à l'adresse 216.58... |
| `dig 10.10.10.15 google.com` | même action, mais en utilisant le serveur DNS à l'adresse 10.10.10.15 |
| `dig ... \| grep ms` | n'affiche que les lignes contenant le mot 'ms' |
>`|grep quelquechose` peut être utilisé pour trouver n'importe quel mot. ex: `dig ... | grep server`
>> la commande `dig -x ...` peut être remplacé par un navigateur, pour trouver le nom de domaine associé<br/>à une adresse IP

## ping
> commande permettant de tester la connectivité entre votre machine et une autre machine

| **Command** | **Description** |
|---|----|
| `ping 10.10.10.11` | test de connectivité avec la machine à l'adresse 10.10.10.11 |
| `ping google.com` | test de connectivité avec la machine au nom de domaine google.com |
| `ping 10.10.10.11 -s 2000` | test de connectivité avec des trames de 2000octets |
| `ping 10.10.10.11 -s 2000 -M do` | test de connectivité, en ajoutant la détection du MTU |
> `-M do` permet de détecter si trames envoyés sont supérieur au MTU (Maximum Transfert Unit)

## table des entrées ARP
> affiche la table des entrées ARP (adresse IP dont les ont connait l'adresse MAC reliée)

| **Command** | **Description** |
|---|----|
| `arp` | affiche la table des entrées arp |
| `arp -n` | affiche la table, sans résoudre les noms d'hotes (uniquement des adresses IP) |
|`arp -d 10.10.10.15` | efface l'entrée de l'adresse 10.10.10.15 de la table |

## smb
> (Server Message Block), protocole de transfert de fichier windows, accessible aussi depuis linux.
>
>>La commande suivante est pour windows:

| **Command** | **Description** |
|---|----|
| `net use -x:\\10.10.10.15\Share` | monte le dossier Share (de la machine à l'adresse 10.10...)<br/>sur le volume de nom 'x' (comme C:\ est votre disque dur) |

>>La commande suivante est pour linux:

| **Command** | **Description** |
|---|----|
| `smbclient //10.10.10.15/Share -U user` | monte le dossier Share (de la machine à l'adresse 10.10...)<br/>Il faut le nom et le mdp d'un utilisateur sur la machine<br/> faisant le partage |

## divers

| **Command** | **Description** |
|---|----|
| `ipconfig` | affiche les informations des cartes réseaux, y compris l'adresse IP (windows)|
| `ifconfig` | affiche les informations des cartes réseaux, y compris l'adresse IP (linux) |
| `ipconfig/ifconfig -a` | affiche toutes les informations, y compris l'adresse IP et l'adresse MAC |
| `unecommande --help` | affiche les différentes options de cette commande |
| `man unecommande` | ouvre un manuel d'aide sur la commande (appuyer sur q pour quitter le manuel) |
| `wget http://site.com/document.pdf` | permet de télécharger un document depuis le terminal |

/!\ Attention, sur linux, les chemins vers des documents se font de la manières suivantes:
<br/>`/home/geii/Documents/tp.pdf`
<br/>Alors que sur windows
, elles se font de la manière suivante:<br/>
`C:\Users\geii\Documents\tp.pdf`
<br/>
Lors d'une configuration en IP fixe sur windows, on peut utiliser la commande suivante:<br/>
`netsh -c interface dump > C:\config.txt`<br/>
pour créer un fichier de configuration de la configuration réseau actuelle, afin de pouvoir la réutiliser plus rapidement si besoin.
