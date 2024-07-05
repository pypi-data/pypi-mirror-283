from datetime import datetime
import unittest
import shutil
import os
import json
from AetherDB.db import DB

class TestDB(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = './temp'
        os.makedirs(self.temp_dir, exist_ok=True)

        # Create a DB instance for testing
        self.db = DB(self.temp_dir)

    def tearDown(self):
        # Remove the temporary directory after testing
        shutil.rmtree(self.temp_dir)
        pass

    def test_init(self):
        # Check if the DB instance is initialized correctly
        self.assertEqual(self.db.path, self.temp_dir)
        self.assertEqual(self.db.name, 'temp')
        self.assertEqual(self.db.latest_cluster, -1)
        self.assertEqual(self.db.default_settings_file, None)
        self.assertEqual(self.db.settings, {
            "cluster_size": 1000,
            "cluster_cache_size": 100
        })

    def test_open_sub_db(self):
        # Create a sub database
        sub_db = self.db.create_sub_db('sub_db')

        # Open the sub database
        opened_sub_db = self.db.open_sub_db('sub_db')

        # Check if the opened sub database is an instance of DB
        self.assertIsInstance(opened_sub_db, DB)
        self.assertEqual(opened_sub_db.path, self.temp_dir + '/sub_db')

    def test_create_sub_db(self):
        # Create a sub database
        sub_db = self.db.create_sub_db('sub_db')

        # Check if the sub database is created correctly
        self.assertTrue(os.path.exists(self.temp_dir + '/sub_db'))
        self.assertTrue(os.path.exists(self.temp_dir + '/sub_db/settings.aethersettings'))

        # Check if the settings file is created correctly
        with open(self.temp_dir + '/sub_db/settings.aethersettings', 'r') as f:
            settings = json.load(f)
        self.assertEqual(settings, {
            "cluster_size": 1000,
            "cluster_cache_size": 100
        })

    def test_delete_sub_db(self):
        # Create a sub database
        try:
            sub_db = self.db.create_sub_db('sub_db')
        except Exception as e:
            print(e)

        # Delete the sub database
        self.db.delete_sub_db('sub_db')

        # Check if the sub database is deleted correctly
        self.assertFalse(os.path.exists(self.temp_dir + '/sub_db'))

    def test_write(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            },
            "2": {
                "key3": "value3",
                "key4": "value4"
            }
        }
        self.db.write(data)

        # Check if the data is written correctly
        with open(self.temp_dir + '/cluster_0.json', 'r') as f:
            written_data = json.load(f)
        self.assertEqual(written_data, data)

    def test_read(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            },
            "2": {
                "key3": "value3",
                "key4": "value4"
            }
        }
        self.db.write(data)

        # Read data from the database
        read_data = self.db.read("1")

        # Check if the data is read correctly
        self.assertEqual(read_data, {
            "key1": "value1",
            "key2": "value2"
        })

    def test_update(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        self.db.write(data)

        # Update data in the database
        updated_data = {
            "key2": "new_value2",
            "key3": "value3"
        }
        self.db.update("1", updated_data)

        # Check if the data is updated correctly
        with open(self.temp_dir + '/cluster_0.json', 'r') as f:
            updated_data = json.load(f)
        self.assertEqual(updated_data["1"], {
            "key1": "value1",
            "key2": "new_value2",
            "key3": "value3"
        })

    def test_delete(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        self.db.write(data)

        # Delete data from the database
        self.db.delete("1")

        # Check if the data is deleted correctly
        with open(self.temp_dir + '/cluster_0.json', 'r') as f:
            deleted_data = json.load(f)
        self.assertEqual(deleted_data, {})

    def test_backup(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        # self.db.write(data)

        # Backup the database
        self.db.backup("./tests/backup")

        # Check if the backup is created correctly
        format = "%Y_%m_%d_%H_%M_%S"
        backup = f'./tests/backup/temp_{datetime.now().strftime(format)}.zip'
        self.assertTrue(os.path.exists(backup))

    def test_query(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            },
            "2": {
                "key1": "value3",
                "key2": "value4"
            }
        }
        self.db.write(data)

        # Query the database
        result = self.db.query("selectWhere{key1=value1}.return")

        # Check if the query result is correct
        self.assertEqual(result, {
            "temp": {
                "1": {
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        })

    def test_query_select_by_id(self):
        # Write data to the database
        data = {
            "1": {
                "key1": "value1",
                "key2": "value2"
            },
            "2": {
                "key1": "value3",
                "key2": "value4"
            }
        }
        self.db.write(data)

        # Query the database
        result = self.db.query("selectById{2}.return")

        # Check if the query result is correct
        self.assertEqual(result, {
            "temp": {
                "2": {
                    "key1": "value3",
                    "key2": "value4"
                }
            }
        })

if __name__ == '__main__':
    unittest.main()
