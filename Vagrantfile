# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "NotasIV"
  config.vm.box = "ubuntu/bionic64"
  config.vm.box_check_update = false
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "NotasIV"
    vb.memory = "1024"
    vb.cpus = 2
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "playbook.yml"
  end

end
