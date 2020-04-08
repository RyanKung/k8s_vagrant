IMAGE_NAME = "bento/ubuntu-16.04"
N = 2

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false
    # Turn off auto update, for using spec mirror
    config.vbguest.auto_update = false
    # ISSUE: https://stackoverflow.com/questions/54067192/vagrant-config-vm-provision-does-not-allow-me-to-copy-a-file-to-etc-nginx-conf
    # ISSUE: https://github.com/hashicorp/vagrant/issues/4032

    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end
    # cache docker images
    config.vm.synced_folder ".", "/vagrant"

    # vagrant network issue
    # https://github.com/hashicorp/vagrant/issues/1807
    # https://superuser.com/questions/850357/how-to-fix-extremely-slow-virtualbox-network-download-speed/850389#850389
    config.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      v.customize ["modifyvm", :id, "--nictype1", "virtio"]
    end

    config.vm.define "k8s-master" do |master|
        master.vm.box = IMAGE_NAME
        master.vm.network "private_network", ip: "192.168.50.10"
        master.vm.hostname = "k8s-master"
        master.vm.provision "shell" do |s|
          s.inline = <<-SHELL
                 cp -f /vagrant/sources_list /etc/apt/sources.list
                 apt-get update
                 apt-get -y upgrade
         SHELL
         s.privileged = true
       end

        master.vm.provision "ansible" do |ansible|
            ansible.playbook = "kubernetes-setup/master-playbook.yml"
            ansible.extra_vars = {
                node_ip: "192.168.50.10",
            }
        end

        master.vm.provision "shell" do |s|
          s.inline = <<-SHELL
                 kubeadm token create --print-join-command > /vagrant/join-command.sh
                 docker run -d -p 5000:5000 --restart=always --name registry registry:2
                 mkdir -p /etc/docker
                 cp -f /vagrant/docker-daemon.json /etc/docker/daemon.json
                 service docker restart
                 systemctl daemon-reload
          SHELL
          s.privileged = true
        end
    end

    (1..N).each do |i|
        config.vm.define "node-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            node.vm.hostname = "node-#{i}"
            node.vm.provision "shell" do |s|
             s.inline = <<-SHELL
                 cp -f /vagrant/sources_list /etc/apt/sources.list
                 apt-get update
                 apt-get -y upgrade
             SHELL
             s.privileged = true
           end

            node.vm.provision "ansible" do |ansible|
                ansible.playbook = "kubernetes-setup/node-playbook.yml"
                ansible.extra_vars = {
                    node_ip: "192.168.50.#{i + 10}",
                }
            end
            node.vm.provision "shell" do |s|
              s.inline = <<-SHELL
                 mkdir -p /etc/docker
                 cp -f /vagrant/docker-daemon.json /etc/docker/daemon.json
                 service docker restart
                 systemctl daemon-reload
              SHELL
              s.privileged = true
            end
        end
    end
end
