#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (c) 2025 Ditra Estrategias Digitales S.A. de C.V.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# plugins/module_utils/fetch_utils.py

import requests
from requests.status_codes import codes
from typing import List, Dict, Optional, Any
from ansible.module_utils.exceptions import (
    APIRequestError,
    MissingPaginationDataError,
)


def search(
    url: str,
    token: str,
    search_params: Dict[str, Any],
    page_limit: Optional[int] = None,
) -> List[Any]:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    all_data = []

    def research(url: str, search_params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Llamar a la API
            response = requests.post(
                url, json={"search": search_params}, headers=headers
            )

            # Verificar el código de estado HTTP
            if response.status_code != codes.ok:
                raise APIRequestError(response.status_code, response.text)

            # Extraer la información del JSON
            data_fetch = response.json()
            current = data_fetch.get("current_page")
            last = data_fetch.get("last_page")
            page_data = data_fetch.get("data", [])

            # Validar valores de paginación
            if current is None or last is None:
                raise MissingPaginationDataError(
                    "'current_page' or 'last_page' is missing in the response"
                )

            return {"current_page": current, "last_page": last, "data": page_data}
        except ValueError:
            raise APIRequestError("Invalid JSON response", response.text)

    # Iterar el fetch sin límite de páginas si page_limit no está definido
    while True:
        # Llamar a la función de búsqueda
        res = research(url, search_params)
        current = res["current_page"]
        last = res["last_page"]
        all_data.extend(res["data"])

        # Verificar si se ha alcanzado el límite de páginas
        if current >= last or (page_limit is not None and current >= page_limit):
            break

        # Actualizar el parámetro de página para la siguiente iteración
        search_params["page"] = current + 1

    return all_data


def mutate(url: str, token: str, operations: list, batch_size: int) -> Dict[str, Any]:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    created_items = []  # Acumular IDs de elementos creados
    updated_items = []  # Acumular IDs de elementos actualizados

    for i in range(0, len(operations), batch_size):
        batch = operations[i : i + batch_size]
        res = requests.post(url, json={"mutate": batch}, headers=headers)

        # Verificar el código de estado HTTP de cada solicitud
        if res.status_code != codes.ok:
            raise APIRequestError(res.status_code, res.text)

        response_data = res.json()

        # Clasificar los elementos creados y actualizados
        created_items.extend(response_data.get("created", []))
        updated_items.extend(response_data.get("updated", []))

    return {"created": created_items, "updated": updated_items}


def delete(url: str, token: str, operations: list, batch_size: int) -> list[Any]:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    data = []

    for i in range(0, len(operations), batch_size):
        batch = operations[i : i + batch_size]
        res = requests.delete(url, json={"resources": batch}, headers=headers)

        # Verificar el código de estado HTTP de cada solicitud
        if res.status_code != codes.ok:
            raise APIRequestError(res.status_code, res.text)

        response_data = res.json()

        # Acumula las resp
        data.extend(response_data.get("data", []))

    return data
