from inspect import isclass
from furthrmind.collection.baseclass import BaseClass
from typing_extensions import List, Self


class Category(BaseClass):
    id = ""
    name = ""
    description = ""
    project = ""

    _attr_definition = {
        "project": {"class": "Project"}
    }

    def __init__(self, id=None, data=None):
        super().__init__(id, data)

    def _get_url_instance(self, project_id=None):
        project_url = Category.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory/{self.id}"
        return url

    @classmethod
    def _get_url_class(cls, id, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory/{id}"
        return url

    @classmethod
    def _get_all_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory"
        return url

    @classmethod
    def _post_url(cls, project_id=None):
        project_url = cls.fm.get_project_url(project_id)
        url = f"{project_url}/researchcategory"
        return url

    @classmethod
    def get(cls, id: str = "", project_id: str = "") -> Self:
        """
        Parameters
        ----------
        id : str
            The id of the requested category. Only needed if used on as a class method
        project_id : str
            The project_id parameter is optional and can be used to retrieve categories
            from another project as the furthrmind sdk was initiated with.

        Returns
        -------
        Self
            An instance of the category class.

        Raises
        ------
        AssertionError
            If used as a class method and id is not specified.

        Example Usage
        -------------
        # Get a category by id
        category = Category.get(id='category_id')

        # Get a category by id using class method
        category = Category.get('category_id')

        # Get a category using the id of the instance
        category = category.get()
        """

        if isclass(cls):
            assert id, "id must be specified"
        return super().get(id=id, project_id=project_id)


    # noinspection PyMethodOverriding
    @classmethod
    def get_many(cls, ids: List[str] = (), names: List[str] = (), project_id: str = "") -> List[Self]:
        """
        Parameters
        ----------
        ids : List[str]
            List with ids.
        names : List[str]
            List with names.
        project_id : str, optional
            Optionally, to get experiments from another project as the furthrmind sdk was initiated with. Defaults to None.

        Returns
        -------
        List[Self]
            List with instances of the category class.

        Raises
        ------
        AssertionError
            If ids or names are not specified.
        """

        assert ids or names, "ids or names must be specified"
        return cls._get_many(ids, names, project_id=project_id)

    @classmethod
    def get_all(cls, project_id: str = "") -> List[Self]:
        """
        Parameters
        ----------
        project_id : str (optional)
            Optionally to get categories from another project as the furthrmind sdk was initiated with, defaults to None

        Returns
        -------
        List[Self]
            List with instances of category class
        """

        return cls._get_all(project_id=project_id)
    
    @staticmethod
    def create(name: str, project_id: str = "") -> Self:
        """
        Method to create a new category

        Parameters
        ----------
        name : str
            Name of the new category

        project_id : str, optional
            Identifier of another project where the category should be created,
            defaults to an empty string

        Returns
        -------
        Self
            The newly created category object
        """

        pass




