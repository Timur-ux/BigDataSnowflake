import asyncio
from typing import List
import pandas as pd
import os
import sys
import argparse

sys.path.append("/".join(__file__.split("/")[:-2]))
from db.api.rawData import addRawData
from db.models import RawData


async def fromCSV(directory: str):
    rows: List[RawData] = []
    kFile = -1
    for directory_, _, fileNames in os.walk(directory):
        for fileName in fileNames:
            kFile += 1
            df = pd.read_csv(str(os.path.join(directory_, fileName)))
            headers = df.columns
            kwDict = {}
            n = len(df)
            for i in range(n):
                values = df.iloc[i, :]
                for k, v in zip(headers, values):
                    kwDict[k] = str(v)
                    kwDict[k] = None if kwDict[k] == "" or kwDict[k] == "nan" else kwDict[k]
                kwDict["id"] = int(kwDict["id"]) +  (1000 * kFile)

                rows.append(RawData(**kwDict))

    print("Added rows:", len(rows))
    await addRawData(rows)

async def main():
    parser = argparse.ArgumentParser(description="Loader data from raw files(csv) to database")
    parser.add_argument("directory", type=str, help="Path to directory the data files will be taken from")
    args = parser.parse_args()
    
    await fromCSV(args.directory)

if __name__ == "__main__":
    asyncio.run(main())
