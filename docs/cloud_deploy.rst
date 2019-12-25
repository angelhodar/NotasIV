Despliegue de la VM en Azure
============================

En esta sección vamos a utilizar un servicio en la nube (en este caso Azure) para alojar la VM
que crearemos con Vagrant y que aprovisionaremos usando ansible.

Configuración de Azure
----------------------

Antes de empezar, necesitamos configurar algunas cosas con el CLI de Azure para que la creación
de la VM se pueda llevar a cabo. En concreto, necesitamos:

* Un grupo de recursos
* Una serie de variables de entorno (como nuestra ID de suscripción a Azure).

Para crear un grupo de recursos, tan solo debemos ejecutar la siguiente orden:

.. code:: bash

    $ az group create -l westeurope -n Hito7

Con esto creamos un grupo de recursos llamado **Hito7** con la opción ``-n``, y también
le especificamos una región que queramos con ``-l``.

.. Note:: Según la región que se le especifique, tendremos acceso a una serie de máquinas u otras, que se pueden ver desde `este <https://docs.microsoft.com/es-es/azure/virtual-machines/windows/sizes-general>`_ enlace.

Ahora solo nos faltaria obtener las variables con los credenciales necesarios, que podemos hacerlo simplemente ejecutando el siguiente comando:

.. code:: bash

    $ az ad sp create-for-rbac

Que devolverá un JSON como el siguiente (se han cambiado los valores de las credenciales por **-**):
::

    {
        "appId": "-----------------",
        "displayName": "azure-cli-2019-12-23-09-47-36",
        "name": "http://azure-cli-2019-12-23-09-47-36",
        "password": "--------------",
        "tenant": "----------------"
    }

Con esto ya tenemos todo lo necesario para empezar a configurar nuestro **Vagrantfile** en la siguiente sección.

Configuración de Vagrant
------------------------

Una vez hemos obtenido en la sección anterior los credenciales necesarios, primero debemos instalar el plugin de azure para
vagrant, que se encuentra aqui y que se puede llevar a cabo con el siguiente comando:

.. code:: bash

    $ vagrant plugin install vagrant-azure

Ahora ya si podemos centrarnos en el **Vagrantfile**, que tiene la siguiente estructura:

.. code:: ruby

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

.. Note:: Para ver una lista de las imágenes de SO que tenemos disponibles en Azure, podemos hacerlo ejecutando ``az vm image list --output table``
   y ver la columna **Urn** del SO que queramos, cuyo valor es lo que deberemos especificarle al parámetro az.vm_image_urn en el Vagrantfile.

Una vez tenemos este archivo, con la herramienta de construcción simplemente ejecutamos:

.. code:: bash

    $ make vm

Esto lo que hará será crearnos una máquina virtual con los ajustes que hayamos definido en el ``Vagrantfile``,
pero **no** aprovisionará la máquina. En concreto, devolverá el siguiente output:
::

    Bringing machine 'NotasIV' up with 'azure' provider...
    ==> NotasIV: Launching an instance with the following settings...
    ==> NotasIV:  -- Management Endpoint: https://management.azure.com
    ==> NotasIV:  -- Subscription Id: ---------------------------
    ==> NotasIV:  -- Resource Group Name: Hito7
    ==> NotasIV:  -- Location: westeurope
    ==> NotasIV:  -- Admin Username: vagrant
    ==> NotasIV:  -- VM Name: notasiv
    ==> NotasIV:  -- VM Storage Account Type: Premium_LRS
    ==> NotasIV:  -- VM Size: Standard_B1s
    ==> NotasIV:  -- Image URN: Canonical:UbuntuServer:18.04-LTS:latest
    ==> NotasIV:  -- TCP Endpoints: 5000
    ==> NotasIV:  -- DNS Label Prefix: notasiv
    ==> NotasIV:  -- Create or Update of Resource Group: Hito7
    ==> NotasIV:  -- Starting deployment
    ==> NotasIV:  -- Finished deploying
    ==> NotasIV: Waiting for SSH to become available...
    ==> NotasIV: Machine is booted and ready for use!
    ==> NotasIV: Rsyncing folder: /home/angel/GitHub/NotasIV/ => /vagrant

Para acceder a ella, podemos hacerlo con el siguiente comando:

.. code:: bash

    $ vagrant ssh

Esto funciona porque cuando vagrant crea nuestra máquina, también crea un usuario llamado ``vagrant``, y utiliza la llave privada
que se encuentra en la ruta que le especificamos con ``config.ssh.private_key_path``.

Aprovisionamiento
-----------------

Como se ha dicho anteriormente, para aprovisionar la máquina se ha usado ansible, y para decirle qué debe aprovisionar sobre la máquina concretamente
he creado un archivo ``playbook.yml`` en el directorio ``provisioning``, que contiene lo siguiente:

.. code:: yaml

    ---
    # Como Vagrant nos crea un inventario, aqui podemos poner directamente el nombre que le dimos a la VM.
    - hosts: NotasIV
    environment:
        PORT: 5000
    tasks:
        # Primero con apt vamos a varias dependencias, como pip, make y npm para usar pm2
        - name: Instalar dependencias
          become: true
          apt:
            name:
            - git
            - python3-pip
            - python3-setuptools
            - python-pip
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

        # Me creo un usuario angel con una shell de bash. Por defecto le crea un home, no hace
        # falta especificarselo
        - name: Crear usuario angel
          become: true
          user:
            name: angel
            shell: /bin/bash
        
        # Como queremos configurar este usuario por ssh para acceder a él desde el anfitrion,
        # le mandamos la clave pública que queremos tener autorizada para ese usuario,
        # especificandole la ruta en el anfitrion
        - name: Agregar clave publica para el usuario angel
          become: true
          authorized_key:
            user: angel
            state: present
            key: "{{ lookup('file', '/home/angel/.ssh/id_rsa.pub') }}"
        
        # Obtenemos el codigo de nuestro repo de GitHub
        - name: Clonar repo de GitHub
          git:
            repo: https://github.com/angelhodar/NotasIV.git
            dest: ~/NotasIV
        
        # Instalamos las dependencias del proyecto
        - name: Instala librerias necesarias
          pip:
            requirements: ~/NotasIV/requirements.txt
            executable: pip3

        # Usamos la herramienta de construccion para ejecutar la app
        - name: Ejecuta la app
          make:
            chdir: ~/NotasIV
            target: start
            file: ~/NotasIV/Makefile


.. Note:: Un detalle importante es que, como explico en el propio playbook al principio, Vagrant nos crea un inventario para ansible
   en ``.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory`` con las maquinas que hayamos definido en el ``Vagrantfile``.
   Como se definió una máquina de nombre NotasIV, podemos ponerla directamente en la clave hosts. Si tuvieramos mas máquinas podriamos
   agruparlas en un grupo y especificar ese grupo, o simplemente usar el keyword **all** o **default** para ejecutar las tasks del playbook
   sobre todas las maquinas definidas en el Vagrantfile. Si estuvieramos usando el comando **ansible-playbook** en lugar de vagrant,
   el inventario por defecto estaría en ``/etc/ansible/hosts``.


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

    TASK [Crear usuario angel] *****************************************************
    changed: [NotasIV]

    TASK [Agregar clave publica para el usuario angel] *****************************
    changed: [NotasIV]

    TASK [Clonar repo de GitHub] *********************************************************
    changed: [NotasIV]

    TASK [Instala librerias necesarias] *********************************************************
    changed: [NotasIV]

    TASK [Ejecuta la app] *********************************************************
    changed: [NotasIV]

    PLAY RECAP *********************************************************************
    NotasIV  : ok=6  changed=7  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0 

Las tareas marcadas con **changed** viene a decir que esa tarea se ha realizado y ha cambiado el estado de la máquina. Si por el contrario pusiera **ok**,
significaría que esa tarea ya ha sido ejecutada y tenemos el sistema con el estado requerido para esa tarea, por lo que no es necesario ejecutarla.

Veamos a grandes rasgos qué hace nuestro playbook:

1. Usando el modulo **apt** de ansible, instala y actualiza las dependencias necesarias para crear el entorno necesario
   para ejecutar la app.
2. Usando el módulo **npm** instalamos pm2, necesario para tener control sobre la ejecución de nuestra app
3. Creamos un usuario llamado *angel* con el módulo **user**, asignándole un shell de bash en lugar de sh que es el que viene por defecto.
4. Al usuario le asignamos la llave pública del par que vamos a usar para conectarnos a la máquina con ese usuario.
5. Clonamos el repo de GitHub.
6. Instalamos las librerias de python necesarias para nuestro proyecto con pip.
7. Arrancamos el servicio con nuestra herramienta de construcción.

Para conectarnos con ssh a la máquina usando el usuario *angel* que hemos creado en el aprovisionamiento, debemos hacerlo con el comando **ssh**
en lugar de **vagrant ssh**, usando el puerto 22 para acceder y la IP pública que nos asigna Azure a nuestra máquina, que en este caso es **52.236.139.44**

.. code:: bash 

    $ ssh angel@52.236.139.44 -p 22

.. Note:: Suponemos que tenemos la llave privada asociada a ese usuario en ``~/.ssh`` en nuestra máquina, de lo contrario deberiamos de especificarselo
   al comando ssh con la opción **-i**.



