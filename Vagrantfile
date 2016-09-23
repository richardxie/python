# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
Vagrant.require_version ">= 1.6.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

	config.vm.define :virtualbox do |vb|
	  vm_name= "vb"
	  
	  vb.vm.host_name = "#{vm_name}.farm"
	  vb.vm.box = "ubuntu/trusty64"

	  vb.vm.network "forwarded_port", guest: 8082, host: 9902
	  vb.vm.network "forwarded_port", guest: 8083, host: 9903

	  vb.vm.network "private_network", ip: "77.77.77.56"

	  config.vm.provision "shell", path:"installer.sh"
	  config.vm.provider "virtualbox" do |v|
		v.customize ["modifyvm", :id, "--memory", "2048"]
		v.customize ["modifyvm", :id, "--cpus", "1"]
	  end
	  config.vm.provision "docker" do |d|
		d.build_image "/vagrant/python", 
			args: "-t richard/pyapp"
		d.run "richard/pyapp",
			cmd: "bash",
			args: "-i -t -v '/vagrant:/usr/src/vagrant' -p 80:8083"
	  end
	end

	config.vm.define :docker do |docker|
		config.vm.provider "docker" do |d|
			d.image = "python"
		end
	end
end