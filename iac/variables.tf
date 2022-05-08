# Lista de variaveis utilizadas nos arquivos de terraform

variable "base_bucket_name" {
  default = "datalake-igti-tf"
}

variable "environment" {
  default = "producao"
}

variable "account_number" {
  default = "431738431676"
}

variable "aws_region" {
  default = "us-east-1"
}
