import datetime
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


@app.get("/kml/points/")
def create_kml(data: GridData):
    timestmp = datetime.datetime.now().strftime('%d%m%YYYY_%H%M%S')
    filename = f'punkty_{timestmp}.kml'
    SpiderPoints(*data).create_kml_gpx(filename=filename)
    return FileResponse(Path(filename), filename=filename, media_type='application/octet-stream')


@app.get("/gpx/points/")
def create_gpx(data: GridData):
    timestmp = datetime.datetime.now().strftime('%d%m%YYYY_%H%M%S')
    filename = f'punkty_{timestmp}.gpx'
    SpiderPoints(*data).create_kml_gpx(filename=filename)
    return FileResponse(Path(filename), filename=filename, media_type='application/octet-stream')


if __name__ == '__main__':
    uvicorn.run(app, port=5000)
