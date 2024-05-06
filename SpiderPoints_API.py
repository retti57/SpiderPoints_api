import datetime
import time
from pathlib import Path
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from spiderpoints.spiderpoints import SpiderPoints

app = FastAPI()


class GridData(BaseModel):
    initial_point: str
    occurrence: str
    distance: str


@app.post("/kml/points/")
def create_kml(data: GridData):
    timestmp = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
    filename = f'punkty_{timestmp}'

    SpiderPoints(data.dict()['initial_point'],
                 data.dict()['occurrence'],
                 data.dict()['distance']
                 ).create_kml_gpx(filename=filename)
    return FileResponse(Path(f'{filename}.kml'), filename=f'{filename}.kml', media_type='application/octet-stream')


@app.post("/gpx/points/")
def create_gpx(data: GridData):
    timestmp = datetime.datetime.now().strftime('%d%m%Y_%H%M%S')
    filename = f'punkty_{timestmp}'
    SpiderPoints(data.dict()['initial_point'],
                 data.dict()['occurrence'],
                 data.dict()['distance']
                 ).create_kml_gpx(filename=filename)
    return FileResponse(Path(f'{filename}.gpx'), filename=f'{filename}.gpx', media_type='application/octet-stream')


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
