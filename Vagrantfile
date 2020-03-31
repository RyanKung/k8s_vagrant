IMAGE_NAME = "bento/ubuntu-16.04"
N = 2

Vagrant.configure("2") do |config|
    config.ssh.insert_key = false
    # Turn off auto update, for using spec mirror
    config.vbguest.auto_update = false
    # ISSUE: https://stackoverflow.com/questions/54067192/vagrant-config-vm-provision-does-not-allow-me-to-copy-a-file-to-etc-nginx-conf
    # ISSUE: https://github.com/hashicorp/vagrant/issues/4032

    config.vm.provision  "file", source: "./sources_list", destination: "/tmp/sources.list"
    config.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
    end

    config.vm.define "k8s-master" do |master|
        master.vm.box = IMAGE_NAME
        master.vm.network "private_network", ip: "192.168.50.10"
        master.vm.hostname = "k8s-master"
        master.vm.provision "shell" do |s|
          s.inline = <<-SHELL
                 cp /tmp/sources.list /etc/apt/sources.list
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
    end

    (1..N).each do |i|
        config.vm.define "node-#{i}" do |node|
            node.vm.box = IMAGE_NAME
            node.vm.network "private_network", ip: "192.168.50.#{i + 10}"
            node.vm.hostname = "node-#{i}"
            node.vm.provision "shell" do |s|
             s.inline = <<-SHELL
                 cp /tmp/sources.list /etc/apt/sources.list
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
        end
    end
end
