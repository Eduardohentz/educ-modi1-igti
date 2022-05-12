import logging
import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, min, max, lit

# Configuracao de logs de aplicacao
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger('datalake_enem_small_upsert')
logger.setLevel(logging.DEBUG)

# Definicao da Spark Session
spark = (SparkSession.builder.appName("DeltaExercise")
    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .getOrCreate()
)


logger.info("Importing delta.tables...")
from delta.tables import *


logger.info("Produzindo novos dados...")
enemnovo = (
    spark.read.format("delta")
    .load("s3://datalake-jorge-igti-tf-producao-431738431676/staging-zone/enem")
)

# Define algumas inscricoes (chaves) que serao alteradas
inscricoes = [200001595656,
            200001421546,
            200001133210,
            200001199383,
            200001237802,
            200001782198,
            200001421548,
            200001595657,
            200001592264,
            200001592266,
            200001592265,
            200001475147,
            200001867756,
            200001133211,
            200001237803,
            200001493186,
            200001421547,
            200001493187,
            200001210202,
            200001421549,
            200001595658,
            200002037437,
            200001421550,
            200001595659,
            200001421551,
            200001237804,
            200001867757,
            200001184600,
            200001692704,
            200001867758,
            200002037438,
            200001595660,
            200001237805,
            200001705260,
            200001421552,
            200001867759,
            200001595661,
            200001042834,
            200001237806,
            200001595662,
            200001421553,
            200001475148,
            200001421554,
            200001493188,
            200002037439,
            200001421555,
            200001480442,
            200001493189,
            200001705261,
            200001421556]


logger.info("Reduz a 50 casos e faz updates internos no municipio da escola")
enemnovo = enemnovo.where(enemnovo.NU_INSCRICAO.isin(inscricoes))
enemnovo = enemnovo.withColumn("NO_MUNICIPIO_ESC", lit("NOVA CIDADE")).withColumn("CO_MUNICIPIO_ESC", lit(10000000))


logger.info("Pega os dados do Enem velhos na tabela Delta...")
enemvelho = DeltaTable.forPath(spark, "s3://datalake-jorge-igti-tf-producao-431738431676/staging-zone/enem")


logger.info("Realiza o UPSERT...")
(
    enemvelho.alias("old")
    .merge(enemnovo.alias("new"), "old.NU_INSCRICAO = new.NU_INSCRICAO")
    .whenMatchedUpdateAll()
    .whenNotMatchedInsertAll()
    .execute()
)

logger.info("Atualizacao completa! \n\n")

logger.info("Gera manifesto symlink...")
enemvelho.generate("symlink_format_manifest")

logger.info("Manifesto gerado.")