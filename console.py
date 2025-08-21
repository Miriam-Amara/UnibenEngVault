#!/usr/bin/env python3

"""
This module contains the entry point of the
command interpreter for UnibenEngVault console.
"""

from cmd import Cmd
from typing import Any, cast
import ast
import logging

from models import storage
from models.basemodel import BaseModel
from models.admin import Admin, Permission, AdminPermission
from models.course import Course, CourseAssignment
from models.department import Department
from models.faculty import Faculty
from models.feedback import Feedback
from models.file import File
from models.help import Help
from models.level import Level
from models.notification import Notification
from models.report import Report
from models.tutoriallink import TutorialLink
from models.user import User


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
    filename="console.log",
    force=True,
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)


class UnibenEngVaultCommand(Cmd):
    """
    Defines the command interpreter for UnibenEngVault
    """
    prompt = "(UnibenEngVault) "
    classes: dict[str, Any] = {
        "BaseModel": BaseModel,
        "Admin": Admin,
        "Permission": Permission,
        "AdminPermission": AdminPermission,
        "Course": Course,
        "CourseAssignment": CourseAssignment,
        "Department": Department,
        "Faculty": Faculty,
        "Feedback": Feedback,
        "File": File,
        "Help": Help,
        "Level": Level,
        "Notification": Notification,
        "Report": Report,
        "TutorialLink": TutorialLink,
        "User": User
    }

    def preloop(self) -> None:
        """
        Executes the welcome message before the start of the program.
        """
        print("""\n\tWelcome to UnibenEngVault command line.
              Enter these commands:
                    all
                    count
                    create
                    destroy
                    show
                    update\n""")

    def postloop(self) -> None:
        """
        Executed once before the end of the program.
        """
        print("\n\n\tBye!\n")

    def emptyline(self) -> bool:
        """
        Overrides default emptyline method.
        Ensures nothing is printed when an emptyline is entered.
        """
        return False

    def default(self, line: str) -> None:
        return super().default(line)

    def do_EOF(self, arg: str) -> bool:
        """
        Exits the program.
        """
        return True
    
    def do_quit(self, arg: str) -> bool:
        """
        Exits the program
        """
        return True
    
    def do_all(self, args: str) -> None:
        """
        Returns all objects of a given class or objects of all classes
        in storage.

        Usage:
            - (UnibenEngVault) all BaseModel
            - (UnibenEngVault) all
        """
        if not args:
            all_objects = storage.all()
            for obj in all_objects.values():
                print(obj)
            return
        
        parts = args.split()
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **") 
            return

        cls_objects = storage.all(cls_name)
        for obj in cls_objects.values():
            print(obj)

    def do_count(self, args: str) -> None:
        """
        Returns the total number of objects of a given class or
        total number of objects of all classes in storage.

        Usage:
            - (UnibenEngVault) count BaseModel
            - (UnibenEngVault) count
        """
        if not args:
            all_objects_count = storage.count()
            print(all_objects_count)
            return
        
        parts = args.split()
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **") 
            return

        cls_objects_count = storage.count(cls_name)
        print(cls_objects_count)
        
    
    def do_create(self, args: str) -> None:
        """
        Creates an object of a class in UnibenEngVault and
        save it to storage.

        Usage:
            - (UnibenEngVault) create BaseModel
            - (UnibenEngVault) create User email="unibenengvault@gmail.com"
                    department="industrial engineering" level="100"
        """
        if not args:
            print("** class name missing **")
            return
        
        parts = args.split()
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(parts) == 1:
            obj = self.classes[cls_name]()
            obj.save()
            print(obj.id)
            return
        
        params = parts[1:]
        kwargs = {}
        for param in params:
            try:
                attr, value = param.split("=")
                value = ast.literal_eval(value)
            except Exception:
                continue
            if isinstance(value, str):
                value = value.replace("_", " ")
            kwargs[attr] = value
        
        if kwargs:
            obj = self.classes[cls_name](**kwargs)
            obj.save()
            print(obj.id)
            return

    def do_destroy(self, args: str) -> None:
        """
        Deletes an object from UnibenEngVault storage.

        Usage:
            - (UnibenEngVault) destroy BaseModel 1234-1234-1234
        """
        if not args:
            print("** class name missing **")
            return
        
        parts = args.split()
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return
        
        if len(parts) < 2:
            print("** instance id missing **")
            return
        
        obj_id = parts[1]
        all_objects = storage.all()
        cls_id = f"{cls_name}.{obj_id}"
        if cls_id not in all_objects:
            print("** no instance found **")
            return
        obj = all_objects[cls_id]
        obj.delete()
        obj.save()

    def do_show(self, args: str) -> None:
        """
        Displays the string representation of an object
        based on class and id.

        Usage:
            - (UnibenEngVault) show BaseModel 1234-1234-1234            
        """
        if not args:
            print("** class name missing **")
            return
        
        parts = args.split()
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return
        
        if len(parts) < 2:
            print("** instance id missing **")
            return
        
        obj_id = parts[1]
        all_objects = storage.all()
        cls_id = f"{cls_name}.{obj_id}"
        if cls_id not in all_objects:
            print("** no instance found **")
            return
        obj = all_objects[cls_id]
        print(obj)

    def do_update(self, args:str) -> None:
        """
        Updates the attributes of an object and saves to UnibenEngVault storage.

        Usage:
        - (UnibenEngVault) update User 1234-1234-1234 department "electrical engineering"
        - (UnibenEngVault) update User 1235-1235-1235 {"name": "Eng", "level": 100}
        """
        if not args:
            print("** class name missing **")
            return
        
        parts = args.partition(" ")
        cls_name = parts[0].strip()
        if cls_name not in self.classes:
            print("** class doesn't exist **")
            return
        
        obj_id, _, params = parts[2]. partition(" ")
        if not obj_id:
            print("** instance id missing **")
            return
        if not params:
            print("** attribute name missing **")
            return
        
        all_objects = storage.all()
        cls_id = f"{cls_name}.{obj_id}"
        if cls_id not in all_objects:
            print("** no instance found **")
            return
        try:
            parsed_data = ast.literal_eval(params)
        except Exception:
            parsed_data = None
        
        obj = all_objects[cls_id]
        if isinstance(parsed_data, dict):
            attr_dict = cast(dict[str, Any], parsed_data)
            for attr, value in attr_dict.items():
                setattr(obj, attr, value)
            obj.save()
            logging.debug(f"{obj}")
            logging.debug(f"{obj.to_dict()}")
            return
        
        attr_parts = params.split()
        if len(attr_parts) < 2:
            print("** value missing **")
            return
        attr = attr_parts[0]
        value = attr_parts[1]
        try:
            logging.debug(value)
            value = ast.literal_eval(value)
            logging.debug(value)
            setattr(obj, attr, value)
        except Exception as e:
            logging.debug(f"{e}")
            return
        obj.save()
        logging.debug(f"{obj}")
        logging.debug(f"{obj.to_dict()}")
        print(f"{cls_name} updated")

        

if __name__ == "__main__":
    UnibenEngVaultCommand().cmdloop()