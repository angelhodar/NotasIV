Creación y aprovisionamiento
============================

En esta sección vamos a crear una máquina virtual, que aprovisionaremos con todo lo
necesario para poder ejecutar nuestra app.

Creación de la VM
-----------------

Para crear la VM vamos a usar **Vagrant**, que nos permitirá tener un archivo de
configuración para establecer la box que vamos a usar, el proveedor que ejecutará
la VM (en este caso he elegido **VirtualBox** por ser gratis y por su portabilidad),
además de otros ajustes. También podemos especificarle directamente el sistema de
aprovisionamiento que vamos a usar, que en mi caso ha sido **ansible**, asi podemos
tener todo lo necesario con el comando vagrant.

Para configurarlo todo, tan solo necesitamos crear un archivo con nombre ``Vagrantfile``,
que tiene el siguiente formato:

.. code:: ruby

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

Una vez tenemos este archivo, con la herramienta de construcción simplemente ejecutamos:

.. code:: bash

    $ make vm

Esto lo que hará será crearnos una máquina virtual con los ajustes que hayamos definido en el ``Vagrantfile``,
pero **no** aprovisionará la máquina. Para acceder a ella, podemos hacerlo con el siguiente comando:

.. code:: bash

    $ vagrant ssh

Esto funciona porque cuando vagrant crea nuestra máquina, también crea un usuario llamado ``vagrant``, generando un
par de llaves SSH e insertando la pública en la máquina virtual y la privada en la ruta ``.vagrant/machines/NotasIV/virtualbox/private_key``,
que es de donde la obtiene a la hora de hacer ssh. Esto lo vamos a modificar en el aprovisionamiento, creando un usuario dentro de
la máquina y asociandole la clave pública que nosotros queramos.

Aprovisionamiento
-----------------

Para aprovisionar la máquina se ha usado ansible, y para decirle qué queremos hacer he creado un archivo ``playbook.yml``
en el directorio ``provisioning``, que contiene lo siguiente:

.. code:: yaml

    ---
    # Como solo tenemos una máquina, usando all ansible solo se ejecutará en ella
    - hosts: all
    tasks:
        # Primero con apt vamos a varias dependencias, como pip, make y npm para usar pm2
        - name: Instalar dependencias
        become: true
        apt:
            name:
            - git
            - python3-pip
            - nodejs
            - npm
            - make
            state: present
            # Esto ejecuta sudo apt update antes de instalar las dependencias, necesario
            # para que encuentre el paquete python3-pip
            update_cache: true
        
        # Una vez tenemos npm ahora instalamos pm2 de forma global en el equipo para que
        # cualquier usuario que creemos tenga acceso.
        - name: Instalar pm2 globalmente
        become: true
        npm:
            name: pm2
            global: yes
        
        # Instalamos pipenv para tener las dependencias del proyecto aisladas del resto
        # de la VM
        - name: Instalar pipenv
        pip:
            name: pipenv

        # Me creo un usuario angel con una shell de bash. Por defecto le crea un home, no hace
        # falta especificarselo
        - name: Crear usuario angel
        become: true
        user:
            name: angel
            shell: /bin/bash
        
        # Como queremos configurar este usuario por ssh para acceder a él desde el anfitrion,
        # le mandamos la clave pública que queremos tener autorizada para ese usuario,
        # especificandole la tura en el anfitrion
        - name: Agregar clave publica para el usuario angel
        become: true
        authorized_key:
            user: angel
            state: present
            key: "{{ lookup('file', '/home/angel/.ssh/id_rsa.pub') }}"

Para ejecutar esto sobre la máquina, ejecutamos lo siguiente:

.. code:: bash

    $ make provision

