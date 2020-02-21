resource "digitalocean_droplet" "tos" {
  image = "ubuntu-18-04-x64"
  name = "tos"
  region = "sfo2"
  size = ""
}