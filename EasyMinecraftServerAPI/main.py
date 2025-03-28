# EasyMinecraftServerAPI
# Copyright (C) 2025 Nucceteere <ruzgar@nucceteere.xyz>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import RedirectResponse
from data.software import softwares, setupmd
import json
import requests

app = FastAPI(
    title="EasyMinecraftServer API",
    version="0.0.1",
    contact={
        "name": "Nucceteere",
        "email": "ruzgar@nucceteere.xyz",
    },
    license_info={
        "name": "AGPL 3.0",
        "identifier": "AGPL-3.0-or-later",
        "url": "https://www.gnu.org/licenses/agpl-3.0.txt",
    },
    docs_url=None,
    redoc_url=None,
)


@app.get("/")
async def root():
    return RedirectResponse(
        url="https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/wiki",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@app.get("/download")  # Vanilla, latest version, latest build
@app.get("/download/{software}")  # Latest version, latest build
@app.get("/download/{software}/{version}")  # Latest build
@app.get(
    "/download/{software}/{version}/{build}"
)  # Specific build (No Effect on Vanilla)
def download(software: str = "vanilla", version: str = "latest", build: str = "latest"):
    if software not in softwares:
        raise HTTPException(
            status_code=406, detail=f"Software '{software}' is not supported!"
        )  # https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/406
    elif software in setupmd:
        return RedirectResponse(
            url=f"https://jar.setup.md/download/{software}/{version}/{build}",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "fabric":
        if version == "latest":
            fabricmeta = requests.get(
                "https://meta.fabricmc.net/v2/versions/game"
            ).content
            data = json.loads(fabricmeta)
            version = data[0]["version"]
        if build == "latest":
            fabricmeta = requests.get(
                "https://meta.fabricmc.net/v2/versions/loader"
            ).content
            data = json.loads(fabricmeta)
            build = data[0]["version"]
        return RedirectResponse(
            url=f"https://meta.fabricmc.net/v2/versions/loader/{version}/{build}/1.0.3/server/jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "quilt":
        return RedirectResponse(
            url="https://quiltmc.org/api/v1/download-latest-installer/java-universal",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
        # Version picking is handled by the CLI App
        # See https://quiltmc.org/en/install/server/ for more information
    else:
        raise HTTPException(status_code=503, detail="Not Implemented!")


@app.get("/security", operation_id="security", include_in_schema=False)
@app.get("/security.txt", operation_id="security.txt", include_in_schema=False)
@app.get(
    "/.well-known/security", operation_id="well-known-security", include_in_schema=False
)
@app.get(
    "/.well-known/security.txt",
    operation_id="well-known-security.txt",
    include_in_schema=False,
)
async def security():
    data = """Contact: mailto:ruzgar@nucceteere.xyz
Expires: 2027-12-31T23:59:00.000Z
Preferred-Languages: en, tr
Canonical: https://api.nucceteere.xyz/security
Canonical: https://api.nucceteere.xyz/security.txt
Canonical: https://api.nucceteere.xyz/.well-known/security
Canonical: https://api.nucceteere.xyz/.well-known/security.txt
Policy: https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/src/branch/master/SECURITY.md"""
    return Response(content=data, media_type="text/plain")
