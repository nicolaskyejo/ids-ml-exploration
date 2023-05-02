# vi: set ft=ruby :
# tested with vbox 6.1.38

ENV["LC_ALL"] = "en_US.UTF-8"

Vagrant.configure("2") do |config|

  config.vm.box = "kalilinux/rolling"
  config.vm.box_version = "2022.4.0"
  config.vm.box_url = "https://vagrantcloud.com/kalilinux/boxes/rolling"
  config.vm.box_check_update = false
  config.vm.synced_folder "./vagrant_shared_folder", "/vagrant", create: true

  config.vm.define "vulnerable-target" do |target|
    target.vm.hostname = "target"
    target.vm.network "private_network", ip: "192.168.60.60"
    target.vm.provider :virtualbox do |vb|
      vb.gui = false
      vb.name = "target"
      vb.memory = 1024
      vb.cpus = 1
    end
    target.vm.provision "bootstrap", type: "shell", path: "./make_dvwa_accessible_to_lan.sh", run: "once"
    target.vm.provision "start-dvwa", type: "shell", inline: "sudo dvwa-start", run: "always"
  end

  config.vm.define "blue-team", primary: true do |blue|
    blue.vm.hostname = "blue"
    blue.vm.network "private_network", ip: "192.168.60.120"
    blue.vm.provider :virtualbox do |vb|
      vb.gui = false
      vb.name = "defender"
      vb.memory = 2048
      vb.cpus = 2
      # allow network interface card to capture all traffic
      vb.customize ["modifyvm", :id, "--nicpromisc2", "allow-all"]
    end
    blue.vm.provision "shell", path: "./defender_setup.sh"
  end

  config.vm.define "red-team" do |red|
    red.vm.hostname = "red"
    red.vm.network "private_network", ip: "192.168.58.58"
    red.vm.provider :virtualbox do |vb|
      vb.gui = true
      vb.name = "attacker"
      vb.memory = 2048
      vb.cpus = 2
    end
    red.vm.provision "shell", inline: "echo '192.168.60.60 target.com target' | sudo tee -a /etc/hosts > /dev/null"
  end

end
