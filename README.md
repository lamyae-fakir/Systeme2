# Systeme2 Le code est executable que sur LINUX et non pas Windows .
Projet de programmation système 2023-2024
Le jeu comporte deux exécutables:

server.py : l'exécutable lancé par le modérateur de jeu. Cet exécutable lance le serveur de chat dans le terminal (reste attaché au terminal). Le modérateur, via cet exécutable:

peut suivre toutes les discussions
connait tous les secrets
decide quand lancer la partie
peut suspendre temporairement ou bannir définitivement un joueur au cours de partie (c'est un modérateur)
vérifie que le programmeur a bien fait son travail (débogage)


client.py : l'exécutable lancé par un joueur. Cet exécutable se détache du terminal (double fork) et crée deux nouveaux terminaux, l'un affichant les messages, l'autre permettant de saisir des commandes et des messages. Les commandes commencent par un !, les messages privés commencent par @toto (pour envoyer à toto), ou @toto @titi @tata pour envoyer un message privé à plusieurs destinataires. Lorsque le joueur meurt, toutes les fenêtres et les processus créés pour lui doivent être tués.


Communications
Le modérateur de jeu et chaque joueur peuvent être sur des machines différentes. Les communications entre chaque application client et le serveur se font via des sockets en mode connecté TCP.

Le serveur est lancé par le modérateur sur sa machine par une commande de la forme

python3 chat_killer_server.py 42042
où 42042 désigne le numéro de port choisi par le modérateur pour la socket d'écoute.

Le client est lancé par le joueur sur sa machine par une commande de la forme

python3 chat_killer_client.py 134.59.2.162 42042
où 134.59.2.162 est l'adresse IPv4 de la machine du modérateur (vous pourrez utiliser la même machine pour tout le monde est utiliser l'adresse 127.0.0.1).

Au lancement, le client demande à l'utilisateur de choisir un pseudo (qui ne pourra pas être changé pendant toute la partie).

Le format des données échangées entre le client et le serveur est laissé libre. Si vous travaillez à plusieurs il faudra vous mettre d'accord sur le format de ces données. Dans le cas de gros messages (fichiers volumineux) il faudra découper les données en plusieurs paquets de taille limitée (par exemple 16 Ko max) et créer de nouveaux processus et des connections UDP pour ne pas bloquer l'application (que ce soit côté client ou côté serveur). Un test d'intégrité du fichier se fera en utilisant une fonction de hachage.

Suggestion pour le format des données: échangez des chaînes de caractères (en dehors des fichiers à transférer), et restez le plus proche possible des chaînes de caractères saisies par les utilisateurs. Ce sera plus facile pour débugger. Si vous voulez que le processus serveur et le processus superviseur s'échanges des messages "en interne" (ne correspondant pas à des saisies des utilisateurs), gardez des chaînes de caractères avec des commandes "internes" de votre invention, que vous pouvez préfixer avec deux ! pour bien le préciser, par exemple: !!request_cookie, !!not_found, !!my_cookie_is 129029320, !!choose_a_pseudo,!!my_pseudo_is Calamity Jane, !!ca_va?, !!ca_va!, etc.


Liste des commandes utilisateurs disponibles
Rappelons que le modérateur, ou un joueur, peut saisir un message public, un message privé, ou une commande. Les messages privés commence par @, les commandes par !. Tous les autres messages sont publics. Certaines commandes visent un joueur en particulier. Elles commencent alors par @ (voir plus bas).

Exemple saisie de message privé

@Jojo Je te dit un secret...
Exemple saisie de message privé au modérateur

@Admin Je te dit un secret...
Exemple de message public

Hello tout le monde!
On liste ci-dessous les commandes que le serveur ou un superviseur doit être capable d'exécuter.

Commandes disponibles uniquement pour le modérateur
!start : lance la partie. Plus aucun nouveau joueur ne peut se connecter.
@PSEUDO !ban : tue le joueur désigné par le pseudo, comme s'il avait été tué par son mot mortel.
@PSEUDO !suspend : gèle le terminal de saisie (il reçoit un signal SIGSTOP) de l'utilisateur concerné. C'est le serveur qui donne l'ordre au superviseur visé d'envoyer le signal au terminal de saisie (rappelons que le serveur n'est pas forcément sur la même machine que le client, il ne peut pas envoyer le signal SIGSTOP au terminal directement).
@PSEUDO !forgive : restaure le terminal de saisie (il reçoit le signal SIGCONT) de l'utilisateur concerné.
Commandes disponibles pour tout joueur (y compris le modérateur)
@PSEUDO !send_file PATH : envoie le fichier local PATH au joueur dont le pseudo est indiqué. Le pseudo peut être @Admin pour envoyer au serveur. Un cache permet d'améliorer les performances (voir plus bas).
!broadcast_file PATH: similaire à send_file, mais le fichier est envoyé à tous les autres joueurs
!list : liste les pseudos, en indiquant leur état actuel (vivant, mort, crashed)
Commandes disponibles pour tout joueur (sauf le modérateur)
!reconnect: tente de reprendre contact avec le serveur (après un crash du serveur)



BAREME 

Un serveur monoclient qui accepte une connection avec telnet : 2/20
Un client qui lance deux terminaux avec les bonnes commandes et les bonnes redirections, et qu'on peut tester sans connection avec un serveur (le superviseur ne se détache pas de son terminal, il lit et écrit dans le terminal au lieu de communiquer avec le serveur): 6/20
Un serveur monoclient + un client qui échangent des messages en alternance (le serveur envoie, puis le client, puis le serveur, etc): 8/20
Un serveur monoclient + un client qui échangent des messages sans alternance (utilisation de select): 10/20
Un serveur multi-client sans pseudo ni messages privés: 12/20
Gestion des pseudos, messages privés, commande !list basique (seulement les pseudos, pas leur état): 15/20
Commandes !start (ferme la porte aux nouvelles demandes de connection), !ban, !suspend, !forgive, !list : 18/20
Tolérance aux diverses pannes de client (détection par échec d'envoi de message, pas de heartbeat demandé), technique du cookie : 20/20
