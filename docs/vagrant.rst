Creación y aprovisionamiento
============================

En esta sección vamos a crear una máquina virtual, que aprovisionaremos con todo lo
necesario para poder ejecutar nuestra app.

Creación de la VM
-----------------

Para crear la VM vamos a usar **Vagrant**, que nos permitirá tener un archivo de
configuración para establecer la box que vamos a usar y el proveedor que ejecutará
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

.. Note:: Como SO base he seleccionado la última versión estable de Ubuntu, la 18.04 LTS, ya que no es muy pesada
   (307MB) y tiene las últimas actualizaciones de la distribución.

Una vez tenemos este archivo, con la herramienta de construcción simplemente ejecutamos:

.. code:: bash

    $ make vm

Esto lo que hará será crearnos una máquina virtual con los ajustes que hayamos definido en el ``Vagrantfile``,
pero **no** aprovisionará la máquina. En concreto, devolverá el siguiente output:
::

        Bringing machine 'NotasIV' up with 'virtualbox' provider...
    ==> NotasIV: Importing base box 'ubuntu/bionic64'...
    ==> NotasIV: Matching MAC address for NAT networking...
    ==> NotasIV: Setting the name of the VM: NotasIV
    ==> NotasIV: Clearing any previously set network interfaces...
    ==> NotasIV: Preparing network interfaces based on configuration...
        NotasIV: Adapter 1: nat
    ==> NotasIV: Forwarding ports...
        NotasIV: 5000 (guest) => 5000 (host) (adapter 1)
        NotasIV: 22 (guest) => 2222 (host) (adapter 1)
    ==> NotasIV: Running 'pre-boot' VM customizations...
    ==> NotasIV: Booting VM...
    ==> NotasIV: Waiting for machine to boot. This may take a few minutes...
        NotasIV: SSH address: 127.0.0.1:2222
        NotasIV: SSH username: vagrant
        NotasIV: SSH auth method: private key
        NotasIV: Warning: Remote connection disconnect. Retrying...
        NotasIV: 
        NotasIV: Vagrant insecure key detected. Vagrant will automatically replace
        NotasIV: this with a newly generated keypair for better security.
        NotasIV: 
        NotasIV: Inserting generated public key within guest...
        NotasIV: Removing insecure key from the guest if it's present...
        NotasIV: Key inserted! Disconnecting and reconnecting using new SSH key...
    ==> NotasIV: Machine booted and ready!
    ==> NotasIV: Checking for guest additions in VM...
        NotasIV: Guest Additions Version: 5.2.34
        NotasIV: VirtualBox Version: 6.0
    ==> NotasIV: Mounting shared folders...
        NotasIV: /vagrant => /home/angel/GitHub/NotasIV

Para acceder a ella, podemos hacerlo con el siguiente comando:

.. code:: bash

    $ vagrant ssh

Esto funciona porque cuando vagrant crea nuestra máquina, también crea un usuario llamado ``vagrant``, generando un
par de llaves SSH e insertando la pública en la máquina virtual y la privada en la ruta ``.vagrant/machines/NotasIV/virtualbox/private_key``,
que es de donde la obtiene a la hora de hacer ssh. De hecho el proceso de creación del par de llaves y la inserción de la pública se muestra
en parte de la salida de cuando levantamos la máquina:
::

    NotasIV: Vagrant insecure key detected. Vagrant will automatically replace
    NotasIV: this with a newly generated keypair for better security.
    NotasIV: 
    NotasIV: Inserting generated public key within guest...
    NotasIV: Removing insecure key from the guest if it's present...
    NotasIV: Key inserted! Disconnecting and reconnecting using new SSH key...

Esto lo vamos a modificar en el aprovisionamiento, creando un usuario dentro de la máquina y asociandole el
par de llaves que nosotros queramos.

Aprovisionamiento
-----------------

Como se ha dicho anteriormente, para aprovisionar la máquina se ha usado ansible, y para decirle qué debe aprovisionar sobre la máquina concretamente
he creado un archivo ``playbook.yml`` en el directorio ``provisioning``, que contiene lo siguiente:

.. code:: yaml

    ---
    # Como Vagrant nos crea un inventario, aqui podemos poner directamente el nombre que le dimos a la VM.
    - hosts: NotasIV
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


.. Note:: Un detalle importante es que, como explico en el propio playbook al principio, Vagrant nos crea un inventario para ansible
   en ``.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory`` con las maquinas que hayamos definido en el ``Vagrantfile``.
   Como se definió una máquina de nombre NotasIV, podemos ponerla directamente en la clave hosts. Si tuvieramos mas máquinas podriamos
   agruparlas en un grupo y especificar ese grupo, o simplemente usar el keyword **all** para ejecutar las tasks del playbook sobre todas las maquinas definidas
   en el Vagrantfile. Si estuvieramos usando el comando **ansible-playbook** en lugar de vagrant, el inventario por defecto estaría en ``/etc/ansible/hosts``.


Una vez tenemos todo listo para aprovisionar la máquina, ejecutamos lo siguiente:

.. code:: bash

    $ make provision

Lo cual generará un output como el siguiente al ejecutarlo por primera vez:
::

    NotasIV: Running ansible-playbook...

    PLAY [NotasIV] *****************************************************************

    TASK [Gathering Facts] *********************************************************
    ok: [NotasIV]

    TASK [Instalar dependencias] ***************************************************
    changed: [NotasIV]

    TASK [Instalar pm2 globalmente] ************************************************
    changed: [NotasIV]

    TASK [Instalar pipenv] *********************************************************
    changed: [NotasIV]

    TASK [Crear usuario angel] *****************************************************
    changed: [NotasIV]

    TASK [Agregar clave publica para el usuario angel] *****************************
    changed: [NotasIV]

    PLAY RECAP *********************************************************************
    NotasIV  : ok=6  changed=5  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0 

Las tareas marcadas con **changed** viene a decir que esa tarea se ha realizao y ha cambiado el estado de la máquina. Si por el contrario pusiera **ok**,
significaría que esa tarea ya ha sido ejecutada y tenemos el sistema con el estado requerido para esa tarea, por lo que no es necesario ejecutarla.

Veamos a grandes rasgos qué hace nuestro playbook:

1. Usando el modulo **apt** de ansible, instala y actualiza las dependencias necesarias para crear el entorno necesario
   para ejecutar la app.
2. Usando los modulos **npm** y **pip**, instalamos pm2 y pipenv, necesarias para tener control sobre la ejecución de nuestra app
   y las librerías necesarias.
3. Creamos un usuario llamado *angel* con el módulo **user**, asignándole un shell de bash en lugar de sh que es el que viene por defecto.
4. Al usuario le asignamos la llave pública del par que vamos a usar para conectarnos a la máquina con ese usuario.

Para conectarnos con ssh a la máquina usando el usuario *angel* que hemos creado en el aprovisionamiento, debemos hacerlo con el comando **ssh**
en lugar de **vagrant ssh**. Como vagrant asocia el puerto 2222 a ssh en la máquina y además tiene asociado *127.0.0.1* como IP de acceso, tan
solo debemos ejecutar: 

.. code:: bash 

    $ ssh angel@localhost -p 2222

.. Note:: Suponemos que tenemos la llave privada asociada a ese usuario en ``~/.ssh`` en nuestro anfitrión, de lo contrario deberiamos de especificarselo
   al comando ssh con la opción **-i**.

