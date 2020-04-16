/*

  when creating a complex infrastructure you'll want/need to
  break the config into multiple files with some kind of logical
  relation.  I'm only building a single server at the moment, but
  following "best practice" (?) and examples I've found, I've created two
  files.  This file does the work, but relies variables defined in the
  other file



  to create the vms, issue these tf cli commands

    # the token is the API token, from the DO website (possibly available
    # via api.  Obviously it expects this to be in the envornment
    # plan runs through the configs and generates a plan file
    # I'm still not sure of the details, but it appears that
    # this is a way to deal with bootstraping problems - i.e.
    # there is some info tf needs, but doesn't have until it processes
    # the files, that info, or at least hints that such info will be needed
    # are probably put into the plan file, probably also helps tf figure
    # out how to order things when not explicitly defined

    terraform plan -out=tfplan -var "do_token=${TOS_DO_TOKEN}"  # do_token is the var name inside the tf file

    terraform apply tfplan

    terraform destroy -var "do_token=${TOS_DO_TOKEN}"

*/

// This is a tf data object, i.e. it has to already exist somewhere
// in this case it does - on DO, so don't need the fingerprint up front
data "digitalocean_ssh_key" "do" {
  name = "do"
}

resource "digitalocean_droplet" "tos2" {
  image = "ubuntu-18-04-x64"
  name = "tos2"
  region = "sfo2"
  size = "s-1vcpu-1gb"
//  ssh_keys = [var.do_ssh_fprint]  // this way the first try
  ssh_keys = [data.digitalocean_ssh_key.do.fingerprint]  // references the key above
  user_data = file("cinit.yaml")

// below to provision the server after it's created
// gonna try cloud init first

//  connection {
//    user = "root"
//    type = "ssh"
//    private_key = file(var.pvt_key)
//    timeout = "2m"
//    host = self.ipv4_address
//  }
//
//  provisioner "remote-exec" {
//    inline = [
//      "export PATH=$PATH:/user/bin",
//      "sudo apt -y update && sudo apt -y install nginx"
//    ]
//  }
}

output "instance_addr" { value = digitalocean_droplet.tos2.ipv4_address}