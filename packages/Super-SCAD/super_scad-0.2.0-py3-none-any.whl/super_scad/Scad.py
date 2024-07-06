import os
from pathlib import Path
from typing import Dict, List

from super_scad.Context import Context
from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.ScadObject import ScadObject
from super_scad.Unit import Unit


class Scad:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, unit: Unit):
        """
        Object constructor.
        """
        self.__project_home: Path = Path(os.getcwd()).resolve()
        """
        The current project's home directory.
        """

        self.__context = Context(project_home=self.__project_home, unit=unit)

        # ------------------------------------------------------------------------------------------------------------------

    @property
    def project_home(self) -> Path:
        """
        Returns the current project's home directory.
        """
        return self.__project_home

    # ------------------------------------------------------------------------------------------------------------------
    @project_home.setter
    def project_home(self, project_home: Path) -> None:
        """
        Sets the current project's home directory.

        :param Path project_home: The current project's home directory.
        """
        self.__project_home = project_home

    # ------------------------------------------------------------------------------------------------------------------
    def run_super_scad(self, scad_object: ScadObject, output_scad: Path | str) -> None:
        """

        :param scad_object:
        :param output_scad:
        """
        self.__context.target_path = Path(output_scad)
        self.__run_super_scad(scad_object)

        with open(output_scad, 'wt') as handle:
            handle.write(self.__context.code_store.get_code())

    # ------------------------------------------------------------------------------------------------------------------
    def __run_super_scad(self, scad_object: ScadObject) -> None:
        """
        Runs SuperSCAD on the ScadObject and recursively on it child objects, if any.

        :param scad_object:
        """
        builders = []
        self.__run_happy_scad_build(scad_object, builders)

        self.__context.code_store.clear()
        self.__context.code_store.add_line('// Unit of length: {}'.format(self.__context.unit))
        self.__run_super_scad_code(builders)
        self.__context.code_store.add_line('')

    # ------------------------------------------------------------------------------------------------------------------
    def __run_happy_scad_build(self, scad_object: ScadObject, parent: List[Dict]):
        old_unit = self.__context.unit
        tmp = {}

        builder = scad_object.build(self.__context)
        if builder != scad_object:
            tmp['parent'] = scad_object
            tmp['children'] = []
            self.__run_happy_scad_build(builder, tmp['children'])
        else:
            tmp['parent'] = builder
            children = builder.children()
            if children is None:
                tmp['children'] = None
            elif isinstance(children, ScadObject):
                tmp['children'] = []
                self.__run_happy_scad_build(children, tmp['children'])
            elif isinstance(children, list):
                tmp['children'] = []
                for child in children:
                    self.__run_happy_scad_build(child, tmp['children'])
            else:
                raise ValueError('Expecting None, ScadObject or List[ScadObject], got {}'.format(type(children)))

        parent.append(tmp)
        self.__context.unit = old_unit

        # ------------------------------------------------------------------------------------------------------------------

    def __run_super_scad_code(self, builders) -> None:
        if isinstance(builders, list):
            for builder in builders:
                self.__run_super_scad_code(builder)
        elif isinstance(builders['parent'], PrivateScadCommand):
            self.__context.code_store.add_line('{}{}'.format(builders['parent'].command,
                                                             builders['parent'].generate_args(self.__context)))
            if builders['children'] is None:
                self.__context.code_store.append_to_last_line(';')
            else:
                self.__context.code_store.add_line('{')
                self.__run_super_scad_code(builders['children'])
                self.__context.code_store.add_line('}')
        else:
            self.__run_super_scad_code(builders['children'])

# ----------------------------------------------------------------------------------------------------------------------
