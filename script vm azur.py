from fileinput import close
import subprocess
import json
from sys import stderr, stdin

try:

    #--------------------- Create Groupe ressource -------------------
    # az_login = "az login"
    create_app_command = "az group create --name B3_G2 --location eastus"

    # connect_az = subprocess.run(az_login, shell=True, stdout=None, stdin=None, stderr=None)
    create_app = subprocess.run(create_app_command, shell = True, capture_output=True)
    print(create_app)
    #---------------------- Create Vnet ---------------------------------
    create_vnet_command = "az network vnet create -g B3_G2 -n B3_G2_Vnet"
    create_vnet_r2_command = "az network vnet create -g B3_G2 -n B3_G2_r2_Vnet"
    create_vnet = subprocess.run(create_vnet_command, shell=True, capture_output=True, stdin=None)
    print(create_vnet)
    create_vnet_r2 = subprocess.run(create_vnet_r2_command, shell=True, capture_output=True, stdin=None)
    print(create_vnet_r2)
    #---------------------- Create subnet ----------------------------
    create_subnet_command = "az network vnet subnet create -g B3_G2 --vnet-name B3_G2_Vnet -n B3_G2_subnet \
        --address-prefixes 10.0.2.0/24"
    create_subnet_r2_command = "az network vnet subnet create -g B3_G2 --vnet-name B3_G2_r2_Vnet -n AzureBastionSubnet --address-prefixes 10.0.2.0/25"
    create_subnet = subprocess.run(create_subnet_command, shell=True, capture_output=True, stdin=None)
    print(create_subnet)
    create_subnet_r2 = subprocess.run(create_subnet_r2_command, shell=True, capture_output=True, stdin=None)
    print(create_subnet_r2)
 #-------------------------- Maria -------------------------------------------

    create_server_mariadb_cd = "az mariadb server create -l eastus -g B3_G2 -n B3G2mariadb -u B3_G2 -p Lavieestcourte123@ --sku-name GP_Gen5_2"
    create_server_mariadb = subprocess.run(create_server_mariadb_cd,shell=True, capture_output=True, stdin=None)
    print(create_server_mariadb)

    create_database_cd = "az mariadb db create -g B3_G2 -s B3G2mariadb -n B3_G2_db"
    create_database = subprocess.run(create_database_cd,shell=True, capture_output=True, stdin=None)
    print(create_database)

    
    
    #---------------------- Create VM -----------------------------------
    create_vm_command = "az vm create --name Vm_Gitea -g B3_G2 --image UbuntuLTS --location eastus --generate-ssh-keys --admin-username bapt --custom-data C:\\Users\\utilisateur\\Documents\\test\\gitea.yml --os-disk-size-gb 30 --data-disk-sizes-gb 30 --size Standard_D2as_v4 --vnet-name B3_G2_Vnet --subnet B3_G2_subnet"
    create_vm = subprocess.run(create_vm_command,shell=True, capture_output=True, stdin=None)
    print(create_vm)    
# --------------------------- Ouverture de port -------------------------------------
    port_80 = "az vm open-port -n VM_Gitea -g B3_G2 --port 80 --priority 700"
    port_443 = "az vm open-port -n VM_Gitea -g B3_G2 --port 443 --priority 800"
    port_3000 = "az vm open-port -n VM_Gitea -g B3_G2 --port 3000 --priority 900"
    open_port_80 = subprocess.run(port_80, shell=True, capture_output=True, stdin=None)
    open_port_443 = subprocess.run(port_443, shell=True, capture_output=True, stdin=None)
    open_port_3000 = subprocess.run(port_3000, shell=True, capture_output=True, stdin=None)


#----------------------- Bastion ---------------------------------------

    create_public_ip = "az network public-ip create --resource-group B3_G2 --name B3_G2_ip --sku Standard --location eastus --dns-name b3g2eastus"
    create_ip = subprocess.run(create_public_ip, shell=True,  capture_output=True, stdin=None)
    print(create_ip)
    create_bastion_azure = "az network bastion create --name B3_G2_bastion --public-ip-address B3_G2_ip --resource-group B3_G2 --vnet-name B3_G2_r2_Vnet --location eastus"
    create_bastion = subprocess.run(create_bastion_azure, shell=True,  capture_output=True, stdin=None) 
    print(create_bastion)


# #---------------------- Recupere ressource id---------------------------------
    ressource_groupe = {
        'vm': json.loads(create_vm.stdout.decode() or '{}'), 
        'bastion': json.loads(create_bastion.stdout.decode() or '{}')}
    print(ressource_groupe)
    with open(r"C:\Users\utilisateur\Documents\test\log\ressource.json", 'w', encoding='utf-8') as fichier:
        print("ressource.json open")
        json.dump(ressource_groupe, fichier, indent=4)
        print("dump ok")
    with open(r"C:\Users\utilisateur\Documents\test\log\ressource.json", 'r', encoding='utf-8') as fichier2:
        print("rentrer dans fichier 2")
        data = json.load(fichier2)
        print("fichier2 charger")
        ressource_id=data["vm"]["id"]
        ip = data["vm"]["publicIpAddress"]
        print(ressource_id)
        ressource_bastion=data["bastion"]["id"]
        print(ressource_bastion)


# #---------------------- Bastion--------------------------------------------------
    enable_tunneling_command = f"az resource update --ids {ressource_bastion} --set properties.enableTunneling=True"
    enable_tunneling = subprocess.run(enable_tunneling_command, shell=True, capture_output=True, stdin=None)
    print("--> tunnel :", enable_tunneling)
    # create_bastion_tunnel = f"az network bastion tunnel --name B3_G2_bastion --resource-group B3_G2 --target-resource-id {ressource_id} --resource-port 22 --port 50022"
    # create_bastion_tunel = subprocess.run(create_bastion_tunnel, shell=True, capture_output=True, stdin=None)
    # print(" --> bastion_tunnel: ",create_bastion_tunel)


#---------------firewal----------------------------------
    create_firewall_rule_cd =f"az mariadb server firewall-rule create -g B3_G2 -s B3G2mariadb -n firewallmariadb --start-ip-address {ip} --end-ip-address {ip}"
    create_firewall_rule = subprocess.run(create_firewall_rule_cd,shell=True, capture_output=True, stdin=None)
    print(create_firewall_rule)
   

#----------------------- Regroupement de tout les résultat ----------------
    res = { 
        'groupe ressource': json.loads(create_app.stdout.decode() or '{}'),
        'vnet': json.loads(create_vnet.stdout.decode() or '{}'),
        'vnet_R2': json.loads(create_vnet_r2.stdout.decode() or '{}'),
        'subnet': json.loads(create_subnet.stdout.decode() or '{}'),
        'subnet_R2': json.loads(create_subnet_r2.stdout.decode() or '{}'),
        'vm': json.loads(create_vm.stdout.decode() or '{}'),
        'port 80': json.loads(open_port_80.stdout.decode() or '{}'),
        'port 443': json.loads(open_port_443.stdout.decode() or '{}'),
        'port 3000': json.loads(open_port_3000.stdout.decode() or '{}'),
        'public-ip': json.loads(create_ip.stdout.decode()or '{}'),
        'bastion': json.loads(create_bastion.stdout.decode()or '{}'),
        'mariadb': json.loads(create_server_mariadb.stdout.decode() or '{}'),
        'database': json.loads(create_database.stdout.decode() or '{}'),
        'firewall': json.loads(create_firewall_rule.stdout.decode() or '{}')

    }
#----------------------- Création du fichier ------------------------
    with open(r"C:\Users\utilisateur\Documents\test\log\log.json", "w") as f: #création du fichier en mode écriture 
        json.dump(res, f, indent=4) # formatage en json de tout ce qui a étais récapituler


except ValueError as e:
    delete_ressourceGroupe_command = "az group delete -y --name B3_G2"
    delete_ressourceGroupe = subprocess.run(delete_ressourceGroupe_command, shell=True, stdout=None, stdin=None, stderr=None)
    print("erreur repéré")
    raise e