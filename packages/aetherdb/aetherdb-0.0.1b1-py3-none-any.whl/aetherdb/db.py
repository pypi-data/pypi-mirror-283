import os
import json
import re
import zipfile
import time
from datetime import datetime



class DB:
    """Class representing a database in AetherDB.

    In AetherDB, a Database is a directory.
    Database contains clustered data 
    in form of json files and optionally sub databases.
    Sub datadase are simply another database.

    Attributes:
        path: Path to the database directory.
        name: Name of the database.
        latest_cluster: Index of the latest cluster.
        default_settings_file: Path to the default settings file. If
        not provided, the default settings will be used.
        settings: Settings for the database.
        parent_db: Parent database object. If provided,
        the current database will be a sub database of the parent database.
        If not provided, the current database will be a root database.
    """
    def __init__(self, path: str, default_settings_file: str = None,
                 parent_db: 'DB' = None) -> None:
        """Constructor for DB class.

        Args:
            path: Path to the database directory.
            default_settings_file: Path to the default settings file. If 
            the database settingsfile does not exist, 
            the default settings file will be used.
            parent_db: Parent database object. If provided,
            the current database will be a sub database of the parent database.
        """
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.name = os.path.basename(path)
        self.parent_db = parent_db
        max_cluster = -1
        for file in os.listdir(self.path):
            if file.startswith('cluster_'):
                num = int(file.split('_')[1].split('.')[0])
                if num > max_cluster:
                    max_cluster = num
        self.latest_cluster = max_cluster
        self.default_settings_file = default_settings_file
        if os.path.exists(self.path + '/settings.aethersettings'):
            with open(self.path + '/settings.aethersettings',
                      'r', encoding="utf8") as f:
                self.settings = json.load(f)
        elif default_settings_file:
            with open(default_settings_file, 'r', encoding="utf8") as f:
                self.settings = json.load(f)
            with open(self.path + '/settings.aethersettings',
                      'w', encoding="utf8") as f:
                json.dump(self.settings, f)
        else:
            self.settings = {
                "cluster_size": 1000,
                "cluster_cache_size": 100
            }
            with open(self.path + '/settings.aethersettings',
                      'w', encoding="utf8") as f:
                json.dump(self.settings, f)

    def open_sub_db(self, name: str) -> 'DB':
        """Open a sub database in the current database.

        Args:
            name: Name of the sub database.

        Returns:
            DB: Sub database object.

        Raises:
            FileNotFoundError: If the sub database does not exist.
        """
        if not os.path.exists(self.path + '/' + name):
            self.create_sub_db(name)
        return DB(self.path + '/' + name, self.default_settings_file,
                  self.parent_db)

    def create_sub_db(self, name: str) -> 'DB':
        """Create a sub database in the current database.

        Args:
            name: Name of the sub database.

        Returns:
            DB: Sub database object.

        Raises:
            FileExistsError: If the sub database already exists.
        """
        if os.path.exists(self.path + '/' + name):
            raise FileExistsError(f"Database {name} already exists")
        os.makedirs(self.path + '/' + name)
        with open(self.path + '/' + name + '/settings.aethersettings',
                  'w', encoding="utf8") as f:
            json.dump(self.settings, f)
        return DB(self.path + '/' + name, self.default_settings_file)

    def delete_sub_db(self, name: str) -> None:
        """Delete a sub database in the current database.

        Database containig anithing other than clusters and settings file
        cannot be deleted.

        Args:
            name: Name of the sub database.

        Raises:
            FileNotFoundError: If the sub database does not exist.
            PermissionError: If the sub database contains files other than clusters
            and settings file.
        """
        if not os.path.exists(self.path + '/' + name):
            raise FileNotFoundError(f"Database {name} not found")
        to_remove = []
        for file in os.listdir(self.path + '/' + name):
            if re.match(r'cluster_\d+.json', file):
                to_remove.append(file)
            elif file == 'settings.aethersettings':
                to_remove.append(file)
            else:
                raise PermissionError(
                    f"Database {name} contains files other than clusters")
        for file in to_remove:
            os.remove(self.path + '/' + name + '/' + file)
        os.rmdir(self.path + '/' + name)

    def write(self, data: dict) -> None:
        """Write data to the database.

        Args:
            data: Data to write. Format:
            {
                "id_in_db": {
                    "key": "value",
                    ...
                },
            }
        """
        if self.latest_cluster == -1:
            self.latest_cluster = 0
            with open(self.path + '/cluster_0.json',
                      'w', encoding="utf8") as f:
                json.dump(data, f)
        else:
            if os.path.getsize(
                self.get_cluster_path(self.latest_cluster)) > 0:
                with open(self.get_cluster_path(self.latest_cluster),
                        'r', encoding="utf8") as f:
                    cluster = json.load(f)
            else:
                cluster = {}
            if len(cluster) >= self.settings["cluster_size"]:
                self.latest_cluster += 1
                with open(self.get_cluster_path(self.latest_cluster),
                          'w', encoding="utf8") as f:
                    json.dump(data, f)
            else:
                cluster_size = len(cluster)
                for key in data:
                    if key in cluster:
                        raise KeyError(f"Data with ID {key} already exists")
                    cluster[key] = data[key]
                    cluster_size += 1
                    if cluster_size >= self.settings["cluster_size"]:
                        self.latest_cluster += 1
                        with open(self.get_cluster_path(self.latest_cluster),
                                  'w', encoding="utf8") as f:
                            json.dump(cluster, f)
                        break
                with open(self.get_cluster_path(self.latest_cluster),
                          'w', encoding="utf8") as f:
                    json.dump(cluster, f)

    def read(self, id_in_db: str) -> dict:
        """Read data from the database.

        Args:
            id_in_db: ID of the data to read.

        Returns:
            dict: Data read from the database.

        Raises:
            FileNotFoundError: If the data with the given ID does not exist.
        """
        for i in range(self.latest_cluster, -1, -1):
            if os.path.exists(self.get_cluster_path(i)):
                with open(self.get_cluster_path(i),
                          'r', encoding="utf8") as f:
                    cluster = json.load(f)
                if id_in_db in cluster:
                    return cluster[id_in_db]
        raise FileNotFoundError(f"Data with ID {id_in_db} not found")

    def update(self, id_in_db: str, data: dict) -> None:
        """Update data in the database.

        Args:
            id_in_db: ID of the data to update.
            data: Data to update. Format:
            {
                "key": "value",
                ...
            }

        Raises:
            FileNotFoundError: If the data with the given ID does not exist.
        """
        for i in range(self.latest_cluster, -1, -1):
            if os.path.exists(self.get_cluster_path(i)):
                with open(self.get_cluster_path(i),
                          'r', encoding="utf8") as f:
                    cluster = json.load(f)
                if id_in_db in cluster:
                    for key in data:
                        cluster[id_in_db][key] = data[key]
                    with open(self.get_cluster_path(i),
                              'w', encoding="utf8") as f:
                        json.dump(cluster, f)
                    return
        raise FileNotFoundError(f"Data with ID {id_in_db} not found")

    def delete(self, id_in_db: str) -> None:
        """Delete data from the database.

        Args:
            id_in_db: ID of the data to delete.

        Raises:
            FileNotFoundError: If the data with the given ID does not exist.
        """
        for i in range(self.latest_cluster, -1, -1):
            if os.path.exists(self.get_cluster_path(i)):
                with open(self.get_cluster_path(i),
                          'r', encoding="utf8") as f:
                    cluster = json.load(f)
                if id_in_db in cluster:
                    del cluster[id_in_db]
                    with open(self.get_cluster_path(i),
                              'w', encoding="utf8") as f:
                        json.dump(cluster, f)
                    return
        raise FileNotFoundError(f"Data with ID {id_in_db} not found")
    
    def backup(self, path: str = None) -> None:
        """Backup the database.

        Args:
            path: Path to the backup directory.
        """
        if path == None:
            path = f"{self.path}/backup"
        if not os.path.exists(path):
            os.makedirs(path)
        format = "%Y_%m_%d_%H_%M_%S"
        path += f'/{self.name}_{datetime.now().strftime(format)}.zip'
        with zipfile.ZipFile(path, 'w') as zipf:
            for root, _, files in os.walk(self.path):
                for file in files:
                    zipf.write(os.path.join(root, file), 
                                os.path.relpath(os.path.join(root, file), 
                                                self.path))
                    


    def query(self, query: str) -> dict:
        """Query the database.

        Args:
            query: Query to execute.

        Returns:
            dict: Result of the query.
        """
        result = { self.name: {}}
        query = re.split(r'}\.', query)
        for i in range(len(query) - 1):
            query[i] += "}"
        for query_part in query:
            if query_part.startswith("selectByIdRegex"):
                regex = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                for i in range(self.latest_cluster, -1, -1):
                    if os.path.exists(self.get_cluster_path(i)):
                        with open(self.get_cluster_path(i),
                                  'r', encoding="utf8") as f:
                            cluster = json.load(f)
                        for key, value in cluster.items():
                            if re.match(regex, key):
                                result[self.name][key] = value
            elif query_part.startswith("selectWhereRegex"):
                select = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                for i in range(self.latest_cluster, -1, -1):
                    if os.path.exists(self.get_cluster_path(i)):
                        with open(self.get_cluster_path(i),
                                  'r', encoding="utf8") as f:
                            cluster = json.load(f)
                        for key, value in cluster.items():
                            for rule in select.split(","):
                                rule = rule.split("=")
                                if rule[0] not in value:
                                    continue
                                if re.match(rule[1], value[rule[0]]):
                                    result[self.name][key] = value
            elif query_part.startswith("selectById"):
                id_in_bd = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                for i in range(self.latest_cluster, -1, -1):
                    print(self.get_cluster_path(i))
                    if os.path.exists(self.get_cluster_path(i)):
                        with open(self.get_cluster_path(i),
                                  'r', encoding="utf8") as f:
                            cluster = json.load(f)
                        if id_in_bd in cluster:
                            result[self.name][id_in_bd] = cluster[id_in_bd]
                            break
            elif query_part.startswith("withDB"):
                name = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                if name not in result:
                    result[name] = {}
                sub_result = self.open_sub_db(name).query('.'.join(
                        query[query.index(query_part) + 1:]))
                if name in sub_result:
                    for key, value in sub_result[name].items():
                        result[name][key] = value
                return result
            elif query_part.startswith("createDB"):
                name = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                self.create_sub_db(name)
            elif query_part.startswith("selectWhere"):
                select = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                for i in range(self.latest_cluster, -1, -1):
                    if os.path.exists(self.get_cluster_path(i)):
                        with open(self.get_cluster_path(i),
                                  'r', encoding="utf8") as f:
                            cluster = json.load(f)
                        for key, value in cluster.items():
                            for rule in select.split(","):
                                rule = rule.split("=")
                                if rule[0] not in value:
                                    continue
                                if value[rule[0]] == rule[1]:
                                    result[self.name][key] = value
            elif query_part.startswith("deleteSelection"):
                for key, value in result[self.name].copy().items():
                    if value != "deleted":
                        self.delete(key)
                        result[self.name][key] = "deleted"
            elif query_part.startswith("delete"):
                id_in_bd = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                self.delete(id_in_bd)
            elif query_part.startswith("update"):
                request = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                id_in_bd = request.split(",", 1)[0]
                data = request.split(",", 1)[1]
                self.update(id_in_bd, data)
            elif query_part.startswith("insert"):
                data = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                data = json.loads(data)
                self.write(data)
            elif query_part.startswith("withParentDB"):
                if self.parent_db:
                    if self.parent_db.name not in result:
                        result[self.parent_db.name] = {}
                    sub_result = self.parent_db.query(
                            '.'.join(query[query.index(query_part) + 1:]))
                    if self.parent_db.name in sub_result:
                        for key, value in sub_result[
                                self.parent_db.name].items():
                            result[self.parent_db.name][key] = value
            elif query_part.startswith("filter"):
                filter = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                for rule in filter.split(","):
                    rule = rule.split("=")
                    for key, value in result[self.name].copy().items():
                        if value[rule[0]] != rule[1]:
                            del result[self.name][key]
            elif query_part.startswith("backup"):
                path = re.search(r'(?:{)(.*)(?:})', query_part).group(1)
                if path == "":
                    self.backup()
                else:
                    self.backup(path)
            elif query_part.startswith("return"):
                return result
        return {}

    def get_cluster_path(self, cluster: int) -> str:
        """Get the path to a cluster.

        Args:
            cluster: Index of the cluster.

        Returns:
            str: Path to the cluster. Cluster is not guaranteed to exist.
        """
        return self.path + '/cluster_' + str(cluster) + '.json'
