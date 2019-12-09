# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Definimos el nombre de nuestra VM para Vagrant
  config.vm.define "NotasIV"
  # He elegido Ubuntu 18.04 LTS ya que es la última version
  # estable y con mayor tiempo de soporte actualmente de Ubuntu
  config.vm.box = "ubuntu/bionic64"
  # Con esto evitamos que busque actualizaciones de la box automaticamente
  # Mejor actualizar manualmente que en un posible descuido
  config.vm.box_check_update = false
  # Asociamos el acceso a la VM a través de 127.0.0.1, asociando el puerto 5000
  # del anfitrion al puerto 5000 de la VM.
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Localmente he usado virtualbox
  config.vm.provider "virtualbox" do |vb|
    # Configuramos el nombre que queremos que tenga la VM dentro de virtualbox
    # para que no nos ponga nombres raros vagrant
    vb.name = "NotasIV"
    # Aparte le definimos 1GB de RAM y 2 nucleos de CPU
    vb.memory = "1024"
    vb.cpus = 2
  end

  # Simplemente configuramos ansible y la ruta de nuestro playbook
  # para el aprovisionamiento
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/playbook.yml"
  end

end
