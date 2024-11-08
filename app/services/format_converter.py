import pandas as pd
from datetime import datetime
from typing import Union, TextIO
import csv
from config import Config

class FormatConverter:
    def __init__(self, config: Config):
        self.config = config

    def convert_lotto_format(self, input_file: Union[str, TextIO], output_file: str) -> None:
        """
        Converte il file storico del lotto nel formato richiesto da estrazioni-lotto.csv.

        Args:
            input_file: Path del file di input o file-like object contenente i dati storici
            output_file: Path dove salvare il file convertito

        Format input:  YYYY/MM/DD\tBA\t58\t22\t47\t49\t69
        Format output: DD/MM/YYYY;BA;58;22;47;49;69
        """
        try:
            # Legge il file di input
            df = pd.read_csv(
                input_file,
                delimiter=self.config.HISTORICAL_DELIMITER,
                header=None,
                names=['data', 'ruota', 'n1', 'n2', 'n3', 'n4', 'n5'],
                keep_default_na=False
            )

            # Converte il formato della data
            df['data'] = pd.to_datetime(df['data'], format='%Y/%m/%d')
            df['data'] = df['data'].dt.strftime(self.config.DATE_FORMAT)

            # Sostituisce RM con RO per mantenere la coerenza con il formato target
            df['ruota'] = df['ruota'].replace('RM', 'RO')

            # Salva nel nuovo formato
            df.to_csv(
                output_file,
                sep=self.config.CSV_DELIMITER,
                index=False,
                quoting=csv.QUOTE_NONE,
                escapechar=None
            )

        except pd.errors.ParserError as e:
            raise ValueError(f"Errore nel parsing del file di input: {str(e)}")
        except Exception as e:
            raise Exception(f"Errore durante la conversione del file: {str(e)}")