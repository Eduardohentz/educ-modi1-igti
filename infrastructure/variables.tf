# Lista de variaveis utilizadas nos arquivos de terraform
variable "base_bucket_name" {
  default = "datalake-jorge-igti-tf"
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

variable "lambda_function_name" {
  default = "IGTIExecutaEMR"
}

variable "vpc_id" {
  default = "vpc-0fb41067e6532af27"
}

variable "key_pair_name" {
  default = "jorge-igti-teste"
}

variable "airflow_subnet_id" {
  default = "subnet-024b7a9fb8fd6c47d"
}