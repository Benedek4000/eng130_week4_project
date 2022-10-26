Vagrant.configure("2") do |config|
   # config.vm.define "db" do |db|
      config.vm.box = "ubuntu/bionic64"
      config.vm.network "private_network", ip:"192.168.10.150"
      config.vm.network "forwarded_port", guest: 80, host: 8080 
         auto_correct: true
      config.vm.provision "shell",path: "provision.sh"
    #end
end
    