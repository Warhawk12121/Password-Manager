from pydantic import BaseModel
from typing import List, Optional, Union
import os
from json import dump, load


class Credentials(BaseModel):
    username: str
    password: str


class JSONHandler:
    """Handles the updation and modification of the JSONified credentials database.
    """

    def __init__(self, path: Union[os.PathLike, str]) -> None:
        """JSONHandler class constructor.

        Args:
            path (Union[os.PathLike, str]): A path to the location of the database.
                If the file does not exist, it will be created.
        """
        if os.path.isfile(path) is True:
            pass
        else:
            with open(path, "w") as _:
                dump(dict(), _, indent=4)

        self.path = path
        self.database: dict = self.refreshDB()

    def refreshDB(self) -> dict:
        """Converts the credential JSON file to a dictionary.

        Returns:
            dict: The converted dictionary.
        """
        with open(self.path, "r") as db:
            temp = load(db)
        return temp

    def saveJSON(self) -> None:
        """Rewrites the credential JSON database.
        """
        with open(self.path, "w", encoding="utf8") as db:
            dump(self.database, db, indent=4)

    def getCredentials(self,
                       site: str,
                       uname: str = None) -> Union[Credentials, List[Credentials], None]:
        """Fetches the credentials specified by the arguments from the database instance.

        Args:
            site (str): The site for which the credentials are stored.
            uname (str, optional): The username contained inside a specific credential.
                Defaults to None.

        Returns:
            Union[Credentials, List[Credentials], None]: A single credential if the uname was specified.
                A list of credentials if only the site was specified.
                None in all other cases.
        """
        credsList = self.database.get(site, None)
        if uname is not None and credsList is not None:
            temp = None
            for cred in credsList:
                cred = Credentials.parse_obj(cred)
                if cred.username == uname:
                    temp = cred
                    break
            return temp

        if credsList is not None:
            credsList = list(map(Credentials.parse_obj, credsList))
        return credsList

    def newCredentials(self, site: str, creds: Credentials) -> None:
        """Adds a new credential to the database.
        Note that calling this function automatically updates the JSON.
        If the specified username already exists, its corresponding password is updated.

        Args:
            site (str): The site the credential corresponds with.
            creds (Credentials): The credentials to be stored.
        """
        updated = False
        if site in self.database:
            for i in range(len(self.database[site])):
                cred = Credentials.parse_obj(self.database[site][i])
                if cred.username == creds.username:
                    cred.password = creds.password
                    self.database[site][i] = cred.dict()
                    updated = True
                    break
            if not updated:
                self.database[site].append(creds.dict())
        else:
            self.database[site] = [creds.dict()]

        self.saveJSON()
