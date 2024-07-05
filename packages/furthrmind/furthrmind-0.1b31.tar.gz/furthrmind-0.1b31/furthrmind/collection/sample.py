from inspect import isclass

from typing_extensions import Self, Dict, List, TYPE_CHECKING

from furthrmind.collection.baseclass import (BaseClassWithFieldData, BaseClassWithFiles,
                                             BaseClassWithGroup, BaseClass,
                                             BaseClassWithLinking)
from furthrmind.utils import instance_overload

if TYPE_CHECKING:
    from furthrmind.collection import *


class Sample(BaseClassWithFieldData,
             BaseClassWithFiles, BaseClassWithGroup,
             BaseClassWithLinking, BaseClass):
    id = ""
    name = ""
    neglect = False
    shortid = ""
    files: List["File"] = []
    fielddata: List["FieldData"] = []
    linked_experiments: List["Experiment"] = []
    linked_samples: List[Self] = []
    linked_researchitems: Dict[str, List["ResearchItem"]] = {}
    groups: List["Group"] = []
    datatables: List["DataTable"] = []

    _attr_definition = {
        "files": {"class": "File"},
        "fielddata": {"class": "FieldData"},
        "groups": {"class": "Group"},
        "linked_samples": {"class": "Sample"},
        "linked_experiments": {"class": "Experiment"},
        "linked_researchitems": {"class": "ResearchItem", "nested_dict": True},
        "datatables": {"class": "DataTable"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)
        # create instance methods for certain class_methods
        instance_methods = ["get"]
        instance_overload(self, instance_methods)

    def _get_url_instance(self, project_id=None):
        project_url = Sample.fm.get_project_url(project_id)
        url = f"{project_url}/samples/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/samples"
        return url

    @classmethod
    def get(cls, id: str = "", name: str = "", shortid: str = "", project_id: str = "") -> Self:
        """
        Method to get one sample by its id, short_id, or name.
        If called on an instance of the class, the id of the class is used

        Parameters
        ----------
        id : str
            The id or short_id of the requested sample.
        name : str
            The name of the requested sample.
        shortid : str
            The shortid of the requested sample.
        project_id : str, optional
            Optionally to get the sample from another project as the furthrmind sdk was initiated with

        Returns
        -------
        Self
            An instance of the sample class.

        Raises
        ------
        AssertionError
            If called as a class method and no id, shortid, or name is specified.

        """

        if isclass(cls):
            assert id or name or shortid, "Either id, shortid, or name must be specified"

        return cls._get(id, shortid, name, project_id=project_id)

    @classmethod
    def get_many(cls, ids: List[str] = (), shortids: List[str] = (), names: List[str] = (),
                 project_id: str = None) -> List[Self]:
        """
        Method to get many samples by its ids, short_ids, or names.

        Parameters
        ----------
        ids : List[str]
            List of sample ids to filter samples by.
        shortids : List[str]
            List of short ids to filter samples by.
        names : List[str]
            List of names to filter samples by.
        project_id : str, optional
            Optionally to get samples from another project as the furthrmind sdk was initiated with

        Returns
        -------
        List[Self]
            List of instances of the sample class.

        Raises
        ------
        AssertionError
            If neither ids, shortids, nor names are specified.

        """

        assert ids or names or shortids, "Either ids, shortids, or names must be specified"
        return cls._get_many(ids, shortids, names, project_id=project_id)

    @classmethod
    def get_all(cls, project_id: str = "") -> List[Self]:
        """
        Method to get all samples belonging to one project

        Parameters
        ----------
        project_id : str, optional
            Optionally to get samples from another project as the furthrmind sdk was initiated with

        Returns
        -------
        List[Self]
            List of instances of the `Sample` class representing the fetched samples.
        """

        return cls._get_all(project_id)

    @classmethod
    @BaseClass._create_instances_decorator(_fetched=False)
    def create(cls, name, group_name=None, group_id=None, project_id=None) -> Self:
        """
        Method to create a new sample

        :param name: the name of the item to be created
        :param group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
        :param group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return instance of the sample class

        """

        return Sample._create(name, group_name, group_id, project_id)

    @classmethod
    @BaseClass._create_instances_decorator(_fetched=False)
    def create_many(cls, data_list: List[Dict], project_id=None) -> Self:
        """
        Method to create multiple samples

        :param data_list: dict with the following keys:
            - name: the name of the item to be created
            - group_name: The name of the group where the new item will belong to. group name can be only considered
            for groups that are not subgroups. Either group_name or group_id must be specified
            - group_id: the id of the group where the new item will belong to. Either group_name or group_id must be specified
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return list with instance of the sample class

        """

        return Sample._create_many(data_list, project_id)

    def add_datatable(self, name: str, columns: List[Dict] = None, project_id=None) -> "DataTable":
        """
        Method to create a new datatable within this sample

        :param name: name of the datatable
        :param columns: a list of columns that should be added to the datatable. List with dicts with the following keys:
            - name: name of the column
            - type: Type of the column, Either "Text" or "Numeric". Data must fit to type, for Text all data
            will be converted to string and for Numeric all data is converted to float (if possible)
            - data: List of column values, must fit to column_type
            - unit: dict with id or name, or name as string, or id as string
        :param project_id: Optionally to create an item in another project as the furthrmind sdk was initiated with
        :return: instance of column datatable class

        """

        from furthrmind.collection import DataTable
        datatable = DataTable.create(name, sample_id=self.id, columns=columns, project_id=project_id)

        new_datatable = list(self.datatables)
        new_datatable.append(datatable)
        self.datatables = new_datatable

        return datatable
