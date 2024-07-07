import os
from pathlib import Path

from super_scad.private.PrivateMultiChildScadCommand import PrivateMultiChildScadCommand
from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.scad.Unit import Unit


class Scad:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, unit_length_final: Unit):
        """
        Object constructor.

        :param unit_length_final: The unit of length used in the generated OpenSCAD code.
        """

        self.__project_home: Path = Path(os.getcwd()).resolve()
        """
        The current project's home directory.
        """

        self.__context = Context(project_home=self.__project_home, unit_length_final=unit_length_final)

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
    def run_super_scad(self, scad_object: ScadObject, openscad_path: Path | str) -> None:
        """
        Runs SuperSCAD on a SuperSCAD object and stores the generated OpenSCAD code.

        :param scad_object: The SuperSCAD object to run.
        :param openscad_path: The path to the file were to store the generated OpenSCAD code.
        """
        self.__context.target_path = Path(openscad_path)
        self.__run_super_scad(scad_object)

        with open(openscad_path, 'wt') as handle:
            handle.write(self.__context.code_store.get_code())

    # ------------------------------------------------------------------------------------------------------------------
    def __run_super_scad(self, scad_object: ScadObject) -> None:
        """
        Runs SuperSCAD on the ScadObject.

        :param scad_object: The SuperSCAD object to run.
        """
        self.__context.code_store.clear()
        self.__context.code_store.add_line('// Unit of length: {}'.format(Context.get_unit_length_final()))
        self.__run_supe_scad_build_tree(scad_object)
        self.__context.code_store.add_line('')

    # ------------------------------------------------------------------------------------------------------------------
    def __run_supe_scad_build_tree(self, scad_object: ScadObject) -> None:
        """
        Helper method for __run_super_scad. Runs recursively on the ScadObject and its children until it finds a
        OpenSCAD command. This OpenSCAD command is used to generate the OpenSCAD code.
        """
        old_unit = Context.get_unit_length_current()
        scad_object = scad_object.build(self.__context)
        Context.set_unit_length_current(old_unit)

        if isinstance(scad_object, PrivateScadCommand):
            self.__context.code_store.add_line('{}{}'.format(scad_object.command,
                                                             scad_object.generate_args(self.__context)))

            if isinstance(scad_object, PrivateSingleChildScadCommand):
                self.__context.code_store.add_line('{')
                self.__run_supe_scad_build_tree(scad_object.child)
                self.__context.code_store.add_line('}')

            elif isinstance(scad_object, PrivateMultiChildScadCommand):
                self.__context.code_store.add_line('{')
                for child in scad_object.children:
                    self.__run_supe_scad_build_tree(child)
                self.__context.code_store.add_line('}')

            else:
                self.__context.code_store.append_to_last_line(';')

        else:
            self.__run_supe_scad_build_tree(scad_object)

# ----------------------------------------------------------------------------------------------------------------------
