# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Nombre de la VM para vagrant y ansible
  config.vm.define "NotasIV"

  # Necesario para el plugin de Azure
  config.vm.box = "azure"

  # Especificamos el dummy box, el cual nos proporcionará una base para nuestra máquina.
  config.vm.box_url = 'https://github.com/msopentech/vagrant-azure/raw/master/dummy.box'

  # Clave privada del par usado para conectarse a la VM
  config.ssh.private_key_path = '~/.ssh/id_rsa'

  config.vm.provider :azure do |azure, override|
    # Credenciales guardadas en variables de entorno necesarias para poder
    # desplegar (la obtención de las mismas se explica en la documentación).
    azure.tenant_id = ENV['AZURE_TENANT_ID']
    azure.client_id = ENV['AZURE_CLIENT_ID']
    azure.client_secret = ENV['AZURE_CLIENT_SECRET']
    azure.subscription_id = ENV['AZURE_SUBSCRIPTION_ID']

		# Nombre de la máquina virtual en Azure
    azure.vm_name = "notasiv"
    # El tipo de máquina, este modelo tiene 1 CPU y 1GB de RAM, aparte de ser
    # de los mas baratos
    azure.vm_size = "Standard_B1s"
    # Abrimos el puerto donde escuchará nuestra app (que lo tenemos también
    # como variable de entorno).
    azure.tcp_endpoints = ENV['PORT']
		# Especificamos la imagen que vamos a montar en nuestra máquina, en este caso Ubuntu 18.04
		azure.vm_image_urn = 'Canonical:UbuntuServer:18.04-LTS:latest'
		# Grupo de recursos en Azure donde se creará la máquina
    azure.resource_group_name = 'Hito7'

  end

  # Usamos ansible como servicio de provisionamiento y le especificamos la ruta
  # del playbook
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end

end
