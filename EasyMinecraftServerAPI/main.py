# EasyMinecraftServerAPI <https://github.com/EasyMinecraftServer/EasyMinecraftServerAPI>
# Copyright (C) 2025 Nucceteere <ruzgar@nucceteere.xyz>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from scalar_doc import ScalarDoc
from data.software import softwares, setupmd
import data.models as models
import requests
import javaproperties
import json
import xml.etree.ElementTree as ET

app = FastAPI(
    title="EasyMinecraftServer API",
    version="0.0.5",
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


@app.get("/openapi", include_in_schema=False)
async def openapi():
    with open("EasyMinecraftServerAPI/data/openapi.json", "r") as file:
        openapi = file.read()
        openapi = json.loads(openapi)
    return openapi


@app.get("/", include_in_schema=False)
async def root():
    docs = ScalarDoc.from_spec(spec="/openapi", mode="url")
    docs.set_title("EasyMinecraftServer API")
    docs_html = docs.to_html()
    return HTMLResponse(docs_html)


@app.get(
    "/download",
    summary="Download server software",
    description="Redirects to the download link for the software specified",
    tags=["Download"],
    status_code=307,
    response_class=RedirectResponse,
    response_model_exclude=422,
    responses={501: {"description": "Invalid Type", "model": models.Message}},
)
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
    elif software == "leaves":
        if version == "latest":
            leavesmeta = requests.get("https://api.leavesmc.org/v2/projects/leaves/")
            data = json.loads(leavesmeta.content)
            version = data["versions"][len(data["versions"]) - 1]
        if build == "latest":
            leavesmeta = requests.get(
                f"https://api.leavesmc.org/v2/projects/leaves/versions/{version}/builds"
            )
            data = json.loads(leavesmeta.content)
            build = data["builds"][len(data["builds"]) - 1]["build"]
            filename = data["builds"][len(data["builds"]) - 1]["downloads"][
                "application"
            ]["name"]
        return RedirectResponse(
            url=f"https://api.leavesmc.org/v2/projects/leaves/versions/{version}/builds/{build}/downloads/${filename}",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "pufferfish":
        if version == "1.21.3":
            if build == "latest":
                redirect = (
                    "https://ci.pufferfish.host/job/Pufferfish-1.21/lastSuccessfulBuild/artifact/build/libs/pufferfish-paperclip-1.21.3-R0.1-SNAPSHOT-mojmap.jar",
                )
            else:
                redirect = (
                    f"https://ci.pufferfish.host/job/Pufferfish-1.21/{build}/artifact/build/libs/pufferfish-paperclip-1.21.3-R0.1-SNAPSHOT-mojmap.jar",
                )
        elif version == "1.20.4":
            if build == "latest":
                redirect = (
                    "https://ci.pufferfish.host/job/Pufferfish-1.20/lastSuccessfulBuild/artifact/build/libs/pufferfish-paperclip-1.20.4-R0.1-SNAPSHOT-reobf.jar",
                )
            else:
                redirect = (
                    f"https://ci.pufferfish.host/job/Pufferfish-1.20/{build}/artifact/build/libs/pufferfish-paperclip-1.20.4-R0.1-SNAPSHOT-reobf.jar",
                )
        elif version == "1.19.4":
            if build == "latest":
                redirect = "https://ci.pufferfish.host/job/Pufferfish-1.19/lastSuccessfulBuild/artifact/build/libs/pufferfish-paperclip-1.19.4-R0.1-SNAPSHOT-reobf.jar"
            else:
                redirect = f"https://ci.pufferfish.host/job/Pufferfish-1.19/{build}/artifact/build/libs/pufferfish-paperclip-1.19.4-R0.1-SNAPSHOT-reobf.jar"
        elif version == "1.18.2":
            if build == "latest":
                redirect = "https://ci.pufferfish.host/job/Pufferfish-1.18/lastSuccessfulBuild/artifact/build/libs/pufferfish-paperclip-1.18.2-R0.1-SNAPSHOT-reobf.jar"
            else:
                redirect = f"https://ci.pufferfish.host/job/Pufferfish-1.18/{build}/artifact/build/libs/pufferfish-paperclip-1.18.2-R0.1-SNAPSHOT-reobf.jar"
        elif version == "1.17.1":
            if build == "latest":
                redirect = "https://ci.pufferfish.host/job/Pufferfish-1.17/lastSuccessfulBuild/artifact/build/libs/Pufferfish-1.17.1-R0.1-SNAPSHOT.jar"
            else:
                redirect = f"https://ci.pufferfish.host/job/Pufferfish-1.17/{build}/artifact/build/libs/Pufferfish-1.17.1-R0.1-SNAPSHOT.jar"
        else:
            raise HTTPException(
                status_code=501, detail="Pufferfish does not support this version!"
            )
        return RedirectResponse(
            url=redirect,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "neoforge":
        neoversions = []
        xml = requests.get(
            "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
        ).content
        tree = ET.fromstring(xml)
        for i, version_xml in enumerate(tree.findall(".//version")):
            neoversions.append(version_xml.text)
        if version != "latest" and build != "latest":
            neoversion = f"{version[2:]}.{build}"
            if neoversion not in neoversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build != "latest":
            neoversion = f"{tree.find('.//latest').text[:4]}.{build}"
            if neoversion not in neoversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build == "latest":
            neoversion = tree.find(".//latest").text
        else:
            raise HTTPException(status_code=501, detail="Not Implemented!")
        return RedirectResponse(
            url=f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{neoversion}/neoforge-{neoversion}-installer.jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "lexforge":
        lexversions = []
        xml = requests.get(
            "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"
        ).content
        tree = ET.fromstring(xml)
        for i, version_xml in enumerate(tree.findall(".//version")):
            lexversions.append(version_xml.text)
        if version != "latest" and build != "latest":
            lexversion = f"{version}.{build}"
            if lexversion not in lexversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build != "latest":
            lexversion = f"{tree.find('.//latest').text[:4]}.{build}"
            if lexversion not in lexversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build == "latest":
            lexversion = tree.find(".//latest").text
        else:
            raise HTTPException(status_code=501, detail="Not Implemented!")
        return RedirectResponse(
            url=f"https://maven.minecraftforge.net/net/minecraftforge/forge/{lexversion}/forge-{lexversion}-installer.jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "spongevanilla":
        spongeversions = []
        xml = requests.get(
            "https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongevanilla/maven-metadata.xml"
        ).content
        tree = ET.fromstring(xml)
        for i, version_xml in enumerate(tree.findall(".//version")):
            spongeversions.append(version_xml.text)
        if version != "latest" and build != "latest":
            spongeversion = f"{version}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build != "latest":
            spongeversion = f"{tree.find('.//latest').text[:4]}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build == "latest":
            spongeversion = tree.find(".//latest").text
        else:
            raise HTTPException(status_code=501, detail="Not Implemented!")
        return RedirectResponse(
            url=f"https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongevanilla/{spongeversion}/spongevanilla-{spongeversion}-installer.jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "spongeforge":
        spongeversions = []
        xml = requests.get(
            "https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongeforge/maven-metadata.xml"
        ).content
        tree = ET.fromstring(xml)
        for i, version_xml in enumerate(tree.findall(".//version")):
            spongeversions.append(version_xml.text)
        if version != "latest" and build != "latest":
            spongeversion = f"{version}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build != "latest":
            spongeversion = f"{tree.find('.//latest').text[:4]}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build == "latest":
            spongeversion = tree.find(".//latest").text
        else:
            raise HTTPException(status_code=501, detail="Not Implemented!")
        return RedirectResponse(
            url=f"https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongeforge/{spongeversion}/spongeforge-{spongeversion}-installer.jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    elif software == "spongeneo":
        spongeversions = []
        xml = requests.get(
            "https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongeneo/maven-metadata.xml"
        ).content
        tree = ET.fromstring(xml)
        for i, version_xml in enumerate(tree.findall(".//version")):
            spongeversions.append(version_xml.text)
        if version != "latest" and build != "latest":
            spongeversion = f"{version}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build != "latest":
            spongeversion = f"{tree.find('.//latest').text[:4]}.{build}"
            if spongeversion not in spongeversions:
                raise HTTPException(
                    status_code=501, detail="This version does not exist!"
                )
        elif version == "latest" and build == "latest":
            spongeversion = tree.find(".//latest").text
        else:
            raise HTTPException(status_code=501, detail="Not Implemented!")
        return RedirectResponse(
            url=f"https://repo.spongepowered.org/repository/maven-releases/org/spongepowered/spongeneo/{spongeversion}/spongeneo-{spongeversion}-installer.jar",
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    else:
        raise HTTPException(status_code=501, detail="Not Implemented!")


@app.get(
    "/config/server.properties",
    summary="Return server.properties",
    description="Returns a server.properties with secure defaults",
    tags=["Config"],
    status_code=200,
    response_model_exclude=422,
    responses={
        200: {
            "description": "server.properties",
            "content": {
                "text/x-java-properties": {
                    "example": "hide-online-players=true\nwhite-list=true"
                }
            },
        }
    },
)
async def serverproperties():
    with open("EasyMinecraftServerAPI/data/server.properties", "r") as file:
        propertiesdata = file.read()
    properties = javaproperties.loads(propertiesdata)
    properties["hide-online-players"] = "true"
    properties["white-list"] = "true"
    properties = javaproperties.dumps(
        properties, comments="Minecraft server properties"
    )
    return Response(content=properties, media_type="text/x-java-properties")


@app.get(
    "/config/whitelist.json",
    summary="Return whitelist.json",
    description="Returns a whitelist.json file with the provided username",
    tags=["Config"],
    status_code=200,
    response_model_exclude=422,
    responses={
        200: {
            "description": "whitelist.json",
            "content": {
                "application/json": {
                    "example": '[\n  {"uuid":"9351f64d-8e92-451f-b764-7b5a3d5bec46",\n   "name":"Nucceteere"\n  }\n]'
                }
            },
        }
    },
)
async def whitelistjson(username: str = None):
    if username is None:
        raise HTTPException(
            status_code=422,
            detail="Please enter a username. Example: /config/whitelist.json?username=Notch",
        )
    playermeta = requests.get(f"https://playerdb.co/api/player/minecraft/{username}")
    if playermeta.status_code == 400:
        raise HTTPException(status_code=422, detail="User doesn't exist!")
    playermeta = json.loads(playermeta.content)
    uuid = playermeta["data"]["player"]["id"]
    whitelist = [{"uuid": uuid, "name": username}]
    return whitelist


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
Policy: https://github.com/EasyMinecraftServer/EasyMinecraftServerAPI/blob/master/SECURITY.md"""
    return Response(content=data, media_type="text/plain")
