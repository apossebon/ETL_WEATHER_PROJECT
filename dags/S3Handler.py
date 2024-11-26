import boto3
from botocore.exceptions import NoCredentialsError
import io
import csv


class S3Handler:
    def __init__(self, bucket_name, region_name=None):
        """
        Inicializa o cliente S3 e configura o bucket.
        :param bucket_name: Nome do bucket S3.
        :param region_name: Região AWS (opcional).
        """
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', region_name=region_name)

    def upload_file(self, file_path, object_name):
        """
        Faz upload de um arquivo para o S3.
        :param file_path: Caminho do arquivo local.
        :param object_name: Nome do arquivo no bucket S3.
        """
        try:
            self.s3.upload_file(file_path, self.bucket_name, object_name)
            print(f"Arquivo {file_path} enviado como {object_name} para o bucket {self.bucket_name}.")
        except FileNotFoundError:
            print(f"O arquivo {file_path} não foi encontrado.")
        except NoCredentialsError:
            print("Credenciais AWS não configuradas.")
        except Exception as e:
            print(f"Erro ao fazer upload: {e}")

    def download_file(self, object_name, file_path):
        """
        Faz download de um arquivo do S3.
        :param object_name: Nome do arquivo no bucket S3.
        :param file_path: Caminho local para salvar o arquivo.
        """
        try:
            self.s3.download_file(self.bucket_name, object_name, file_path)
            print(f"Arquivo {object_name} baixado para {file_path}.")
        except FileNotFoundError:
            print(f"O caminho {file_path} é inválido.")
        except NoCredentialsError:
            print("Credenciais AWS não configuradas.")
        except Exception as e:
            print(f"Erro ao fazer download: {e}")

    def read_file_content(self, object_name):
        """
        Lê o conteúdo de um arquivo no S3.
        :param object_name: Nome do arquivo no bucket S3.
        :return: Conteúdo do arquivo como string.
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
            content = response['Body'].read().decode('utf-8')
            return content
        except NoCredentialsError:
            print("Credenciais AWS não configuradas.")
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            return None

    def write_string_to_s3(self, content, object_name):
        """
        Escreve uma string diretamente em um arquivo no S3.
        :param content: Conteúdo a ser escrito.
        :param object_name: Nome do arquivo no bucket S3.
        """
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=object_name, Body=content)
            print(f"Conteúdo escrito em {object_name} no bucket {self.bucket_name}.")
        except NoCredentialsError:
            print("Credenciais AWS não configuradas.")
        except Exception as e:
            print(f"Erro ao escrever no S3: {e}")

    def append_to_file(self, object_name, new_content):
        """
        Adiciona conteúdo ao final de um arquivo no S3.
        :param object_name: Nome do arquivo no bucket S3.
        :param new_content: Novo conteúdo a ser adicionado.
        """
        try:
            # Obter o conteúdo existente
            existing_content = self.read_file_content(object_name) or ""
            
            # Adicionar o novo conteúdo
            updated_content = existing_content + new_content
            
            # Atualizar o arquivo no S3
            self.write_string_to_s3(updated_content, object_name)
            print(f"Conteúdo adicionado ao arquivo {object_name}.")
        except Exception as e:
            print(f"Erro ao adicionar conteúdo ao arquivo: {e}")
            
    def append_csv_to_s3(self, object_name, row_data):
        """
        Adiciona uma nova linha ao arquivo CSV no S3 sem baixar todo o arquivo.
        :param object_name: Nome do arquivo no bucket S3.
        :param row_data: Dados a serem adicionados (uma lista representando a linha do CSV).
        """
        try:
            # Baixar as primeiras partes (se o arquivo existir)
            try:
                # Lendo o arquivo original
                response = self.s3.get_object(Bucket=self.bucket_name, Key=object_name)
                existing_data = response['Body'].read().decode('utf-8')
            except self.s3.exceptions.NoSuchKey:
                # Arquivo não existe; criar um novo
                print(f"Arquivo {object_name} não existe. Criando novo.")
                existing_data = ""

            # Adicionar a nova linha
            buffer = io.StringIO()
            if existing_data:
                buffer.write(existing_data)
            writer = csv.writer(buffer)
            writer.writerow(row_data)

            # Fazer upload novamente
            self.s3.put_object(Bucket=self.bucket_name, Key=object_name, Body=buffer.getvalue())
            print(f"Nova linha adicionada ao arquivo {object_name} no bucket {self.bucket_name}.")
        except Exception as e:
            print(f"Erro ao adicionar linha ao CSV no S3: {e}")
