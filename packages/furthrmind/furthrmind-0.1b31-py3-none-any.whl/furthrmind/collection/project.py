from furthrmind.collection.baseclass import BaseClass
from typing_extensions import List, Dict, Self, TYPE_CHECKING
from inspect import isclass
if TYPE_CHECKING:
    from furthrmind.collection import *

class Project(BaseClass):
    id = ""
    name = ""
    info = ""
    shortid = ""
    samples: List["Sample"] = []
    experiments: List["Experiment"] = []
    groups: List["Group"] = []
    units: List["Unit"] = []
    researchitems: Dict[str, List["ResearchItem"]] = {}
    permissions = []
    fields: List["Field"] = []

    _attr_definition = {
        "samples": {"class": "Sample"},
        "experiments": {"class": "Experiment"},
        "groups": {"class": "Group"},
        "units": {"class": "Unit"},
        "researchitems": {"class": "ResearchItem", "nested_dict": True},
        "fields": {"class": "Field"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self):
        project_url = self.fm.get_project_url(self.id)
        return project_url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(id)
        return project_url

    @classmethod
    def _get_all_url(cls, project_id=None):
        return f"{cls.fm.base_url}/projects"

    @classmethod
    def _post_url(cls):
        return f"{cls.fm.base_url}/projects"
    
    @classmethod
    def get(cls, id: str = "", name: str = "") -> Self:
        """
        This method is used to get one project by its id or name.
        If called on an instance of the class, the id of the class is used.
        Either id or name must be specified.

        Parameters
        ----------
        id : str, optional
            id or short_id of the requested project.
            Default value is an empty string.
        name : str, optional
            name of the requested project.
            Default value is an empty string.

        Returns
        -------
        Self
            Instance of the project class.

        """

        if isclass(cls):
            assert id or name, "Either id or name must be specified"

        return cls._get(id=id, name=name)


    @classmethod
    def get_many(cls, ids: List[str] = (), names: List[str] = ()) -> List[Self]:
        """
        Method to get many projects

        Parameters
        ----------
        ids : List[str]
            List of ids.

        names : List[str]
            List of names.

        Returns
        -------
        List[Self]
            List of instances of the class.

        Raises
        ------
        AssertionError
            If neither ids nor names are specified.
        """
        pass

        assert ids or names, "Either ids or names must be specified"
        return cls._get_many(ids, names)

    @classmethod
    def get_all(cls) -> List[Self]:
        """
        Method to get all projects

        Returns
        -------
        List[Self]
            List of instances of the class.

        """

        return super()._get_all()

    @classmethod
    @BaseClass._create_instances_decorator(_fetched=False)
    def create(cls, name: str) -> Self:
        """
        Method to create a new project

        Parameters
        ----------
        name : str
            Name of the new project

        Returns
        -------
        Self
            Instance of the project class

        Raises
        ------
        ValueError
            If name is empty or None

        """

        if not name:
            raise ValueError("Name is required")
        data = {"name": name}
        id = cls._post(data)
        data["id"] = id
        return data




