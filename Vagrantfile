Vagrant.configure("2") do |config|
   # config.vm.define "db" do |db|
      config.vm.box = "ubuntu/bionic64"
      config.vm.network "private_network", type:"dhcp"
      config.vm.provision "shell",path: "provision.sh"
    #end
end
    