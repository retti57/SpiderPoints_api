""" This module sets up an API POST endpoint """
import datetime
import os
from pathlib import Path
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from spiderpoints.spiderpoints import SpiderPoints

app = FastAPI()


class GridData(BaseModel):
    """ Data validator """
    initial_point: str
    occurrence: str
    distance: str


def clear_dir() -> None:
    """ Search for any older files KML and GPX in current directory and deletes them """
    for _, _, files in os.walk(os.getcwd()):
        for f in files:
            if f.endswith('.kml') or f.endswith('.gpx'):
                os.remove(f)


@app.post("/points/")
def create_gpx(data: GridData) -> FileResponse:
    """ Endpoint creates files using Spiderpoints package and sends them back as a FileResponse"""
    clear_dir()

    timestmp = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
    filename = f'punkty_{timestmp}'
    SpiderPoints(data.dict()['initial_point'],
                 data.dict()['occurrence'],
                 data.dict()['distance']
                 ).create_kml_gpx(filename=filename)
    return FileResponse(path=Path(f'{filename}.gpx'), filename=f'{filename}.gpx', media_type='application/octet-stream')


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
