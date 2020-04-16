/*

  when creating a complex infrastructure you will want/need to
  break up the config into multiple files with some kind of logical
  relation.  I'm only building a single server at the moment, but
  following "best practice" and examples I've found, I've created two
  files.  This file contains the variables used by the other file.

  the DigitalOcean terraform provider requires an API key in the variable called "token"
  Below creates a variable called 'do_token' and then assigs it to the tf required
  parameter 'token'.  Primary reason to establish the value this way is to extract it from
  the environment

*/

variable "do_token" {}
//variable "pubkey_file" {}
//variable "pub_key" {}
//variable "pvt_key" {}
//variable "do_ssh_fprint" {}


provider "digitalocean" {
  token = var.do_token
}

