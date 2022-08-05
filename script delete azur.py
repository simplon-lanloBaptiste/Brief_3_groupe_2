from sqlite3 import connect
import subprocess
import json
from sys import stderr, stdin

#------------------ Delete ressource groupe -------------------

delete_ressourceGroupe_command = "az group delete -y --name B3_G2"

a = "az vm delete -g test_5 -n test_5vm -y"
# connect_command = "az login"
delete_vnet_command = "az network vnet delete -g B3_G2 -n B3_G2_Vnet"
delete_subnet_command = "az network vnet subnet delete -g B3_G2 -n B3_G2_subnet"
delete_vnet_r2_command = "az network vnet delete -g B3_G2 -n B3_G2_r2_Vnet"
delete_subnet_r2_command = "az network vnet subnet delete -g B3_G2 -n B3_G2_r2_subnet"

# connect_az = subprocess.run(connect_command,shell=True, stdout=None, stdin=None, stderr=None)
delete_ressourceGroupe = subprocess.run(delete_ressourceGroupe_command, shell=True, stdout=None, stdin=None, stderr=None)

# az network bastion tunnel --name MyBastionHost --resource-group MyResourceGroup --target-resource-id vmResourceId --resource-port 22 --port 50022