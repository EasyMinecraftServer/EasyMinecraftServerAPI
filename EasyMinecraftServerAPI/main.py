# EasyMinecraftServerAPI
# Copyright (C) 2025 Nucceteere <ruzgar@nucceteere.xyz>
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.


from fastapi import FastAPI, Response

description = "EasyMinecraftServer API implemented in Python <br> Maintained by [Nucceteere](https://git.funtimes909.xyz/Nucceteere) <br> [Docs](https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/wiki)"

app = FastAPI(
    title="EasyMinecraftServer API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Nucceteere",
        "email": "ruzgar@nucceteere.xyz",
    },
    license_info={
        "name": "AGPLv3",
        "url": "https://www.gnu.org/licenses/agpl-3.0.txt",
    },
    docs_url=None,
    redoc_url=None,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


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
def security():
    data = """Contact: mailto:ruzgar@nucceteere.xyz
Expires: 2027-12-31T23:59:00.000Z
Preferred-Languages: en, tr
Canonical: https://api.nucceteere.xyz/security
Canonical: https://api.nucceteere.xyz/security.txt
Canonical: https://api.nucceteere.xyz/.well-known/security
Canonical: https://api.nucceteere.xyz/.well-known/security.txt
Policy: https://git.funtimes909.xyz/Nucceteere/EasyMinecraftServerAPI/src/branch/master/SECURITY.md"""
    return Response(content=data, media_type="text/plain")
