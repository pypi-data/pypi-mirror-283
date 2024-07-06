from __future__ import annotations

import importlib
import json
import os
import platform
import re
import sys
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID

from jsonpath_ng.ext import parse
from pydantic import BaseModel, Field, create_model
from pydantic.main import ModelMetaclass, PrivateAttr

import osw.model.entity as model
from osw.model.static import OswBaseModel
from osw.utils.templates import (
    compile_handlebars_template,
    eval_compiled_handlebars_template,
)
from osw.utils.util import parallelize
from osw.utils.wiki import (
    get_namespace,
    get_title,
    namespace_from_full_title,
    title_from_full_title,
)
from osw.wiki_tools import SearchParam
from osw.wtsite import WtPage, WtSite


class OswClassMetaclass(ModelMetaclass):
    def __new__(cls, name, bases, dic, osl_template, osl_footer_template):
        base_footer_cls = type(
            dic["__qualname__"] + "Footer",
            (BaseModel,),
            {
                "__annotations__": {"osl_template": str},
                "osl_template": Field(
                    default=osl_footer_template,
                    title=dic["__qualname__"] + "FooterTemplate",
                ),
            },
        )
        if "__annotations__" not in dic:
            dic["__annotations__"] = {}
        dic["__annotations__"]["osl_template"] = str
        dic["osl_template"] = Field(
            default=osl_template, title=dic["__qualname__"] + "Template"
        )
        dic["__annotations__"]["osl_footer"] = base_footer_cls
        dic["osl_footer"] = Field(
            default={"osl_template": osl_footer_template},
            title=dic["__qualname__"] + "Footer",
        )
        new_cls = super().__new__(cls, name, bases, dic)
        return new_cls


class OSW(BaseModel):
    """Bundles core functionalities of OpenSemanticWorld (OSW)"""

    uuid: str = "2ea5b605-c91f-4e5a-9559-3dff79fdd4a5"
    _protected_keywords = (
        "_osl_template",
        "_osl_footer",
    )  # private properties included in model export

    class Config:
        arbitrary_types_allowed = True  # neccessary to allow e.g. np.array as type

    site: WtSite

    @staticmethod
    def get_osw_id(uuid: uuid) -> str:
        """Generates a OSW-ID based on the given uuid by prefixing "OSW" and removing
        all '-' from the uuid-string

        Parameters
        ----------
        uuid
            uuid object, e. g. UUID("2ea5b605-c91f-4e5a-9559-3dff79fdd4a5")

        Returns
        -------
            OSW-ID string, e. g. OSW2ea5b605c91f4e5a95593dff79fdd4a5
        """
        return "OSW" + str(uuid).replace("-", "")

    @staticmethod
    def get_uuid(osw_id) -> uuid:
        """Returns the uuid for a given OSW-ID

        Parameters
        ----------
        osw_id
            OSW-ID string, e. g. OSW2ea5b605c91f4e5a95593dff79fdd4a5

        Returns
        -------
            uuid object, e. g. UUID("2ea5b605-c91f-4e5a-9559-3dff79fdd4a5")
        """
        return UUID(osw_id.replace("OSW", ""))

    class SchemaRegistration(BaseModel):
        """
        dataclass param of register_schema()

        Attributes
        ----------
        model_cls:
            the model class
        schema_name:
            the name of the schema
        schema_bases:
            list of base schemas (referenced by allOf)
        """

        class Config:
            arbitrary_types_allowed = True  # allow any class as type

        model_cls: ModelMetaclass
        schema_uuid: str  # Optional[str] = model_cls.__uuid__
        schema_name: str  # Optional[str] = model_cls.__name__
        schema_bases: List[str] = ["Category:Item"]

    def register_schema(self, schema_registration: SchemaRegistration):
        """Registers a new or updated schema in OSW by creating the corresponding
        category page.

        Parameters
        ----------
        schema_registration
            see SchemaRegistration
        """
        entity = schema_registration.model_cls

        jsondata = {}
        jsondata["uuid"] = schema_registration.schema_uuid
        jsondata["label"] = {"text": schema_registration.schema_name, "lang": "en"}
        jsondata["subclass_of"] = schema_registration.schema_bases

        if issubclass(entity, BaseModel):
            entity_title = "Category:" + OSW.get_osw_id(schema_registration.schema_uuid)

            page = WtPage(wtSite=self.site, title=entity_title)
            if page.exists:
                page = self.site.get_page(
                    WtSite.GetPageParam(titles=[entity_title])
                ).pages[0]

            page.set_slot_content("jsondata", jsondata)

            # entity = ModelMetaclass(entity.__name__, (BaseModel,), dict(entity.__dict__)) #strips base classes but fiels are already importet
            schema = json.loads(
                entity.schema_json(indent=4).replace("$ref", "dollarref")
            )

            jsonpath_expr = parse("$..allOf")
            # replace local definitions (#/definitions/...) with embedded definitions to prevent resolve errors in json-editor
            for match in jsonpath_expr.find(schema):
                result_array = []
                for subschema in match.value:
                    # pprint(subschema)
                    value = subschema["dollarref"]
                    if value.startswith("#"):
                        definition_jsonpath_expr = parse(
                            value.replace("#", "$").replace("/", ".")
                        )
                        for def_match in definition_jsonpath_expr.find(schema):
                            # pprint(def_match.value)
                            result_array.append(def_match.value)
                    else:
                        result_array.append(subschema)
                match.full_path.update_or_create(schema, result_array)
            if "definitions" in schema:
                del schema["definitions"]

            if "allOf" not in schema:
                schema["allOf"] = []
            for base in schema_registration.schema_bases:
                schema["allOf"].append(
                    {"$ref": f"/wiki/{base}?action=raw&slot=jsonschema"}
                )

            page.set_slot_content("jsonschema", schema)
        else:
            print("Error: Unsupported entity type")
            return

        page.edit()
        print("Entity stored at " + page.get_url())

    class SchemaUnregistration(BaseModel):
        """
        dataclass param of register_schema()

        Attributes
        ----------
        model_cls:
            the model class
        schema_name:
            the name of the schema
        schema_bases:
            list of base schemas (referenced by allOf)
        """

        class Config:
            arbitrary_types_allowed = True  # allow any class as type

        model_cls: Optional[ModelMetaclass]
        model_uuid: Optional[str]
        comment: Optional[str]

    def unregister_schema(self, schema_unregistration: SchemaUnregistration):
        """deletes the corresponding category page

        Parameters
        ----------
        schema_unregistration
            see SchemaUnregistration
        """
        uuid = ""
        if schema_unregistration.model_uuid:
            uuid = schema_unregistration.model_uuid
        elif (
            not uuid
            and schema_unregistration.model_cls
            and issubclass(schema_unregistration.model_cls, BaseModel)
        ):
            uuid = schema_unregistration.model_cls.__uuid__
        else:
            print("Error: Neither model nor model id provided")

        entity_title = "Category:" + OSW.get_osw_id(uuid)
        page = self.site.get_page(WtSite.GetPageParam(titles=[entity_title])).pages[0]
        page.delete(schema_unregistration.comment)

    class FetchSchemaMode(Enum):
        """Modes of the FetchSchemaParam class

        Attributes
        ----------
        append:
            append to the current model
        replace:
            replace the current model
        """

        append = "append"  # append to the current model
        replace = "replace"  # replace the current model

    class FetchSchemaParam(BaseModel):
        """Param for fetch_schema()

        Attributes
        ----------
        schema_title:
            one or multiple titles (wiki page name) of schemas (default: Category:Item)
        mode:
            append or replace (default) current schema, see FetchSchemaMode
        """

        schema_title: Optional[Union[List[str], str]] = "Category:Item"
        mode: Optional[str] = (
            "replace"  # type 'FetchSchemaMode' requires: 'from __future__ import annotations'
        )

    def fetch_schema(self, fetchSchemaParam: FetchSchemaParam = None) -> None:
        """Loads the given schemas from the OSW instance and autogenerates python
        datasclasses within osw.model.entity from it

        Parameters
        ----------
        fetchSchemaParam
            See FetchSchemaParam, by default None
        """
        if not isinstance(fetchSchemaParam.schema_title, list):
            fetchSchemaParam.schema_title = [fetchSchemaParam.schema_title]
        first = True
        for schema_title in fetchSchemaParam.schema_title:
            mode = fetchSchemaParam.mode
            if not first:  # 'replace' makes only sense for the first schema
                mode = "append"
            self._fetch_schema(
                OSW._FetchSchemaParam(schema_title=schema_title, mode=mode)
            )
            first = False

    class _FetchSchemaParam(BaseModel):
        """Internal param for _fetch_schema()

        Attributes
        ----------
        schema_title:
            the title (wiki page name) of the schema (default: Category:Item)
        root:
            marks the root iteration for a recursive fetch (internal param,
            default: True)
        mode:
            append or replace (default) current schema, see FetchSchemaMode
        """

        schema_title: Optional[str] = "Category:Item"
        root: Optional[bool] = True
        mode: Optional[str] = (
            "replace"  # type 'FetchSchemaMode' requires: 'from __future__ import annotations'
        )

    def _fetch_schema(self, fetchSchemaParam: _FetchSchemaParam = None) -> None:
        """Loads the given schema from the OSW instance and autogenerates python
        datasclasses within osw.model.entity from it

        Parameters
        ----------
        fetchSchemaParam
            See FetchSchemaParam, by default None
        """
        site_cache_state = self.site.get_cache_enabled()
        self.site.enable_cache()
        if fetchSchemaParam is None:
            fetchSchemaParam = OSW._FetchSchemaParam()
        schema_title = fetchSchemaParam.schema_title
        root = fetchSchemaParam.root
        schema_name = schema_title.split(":")[-1]
        page = self.site.get_page(WtSite.GetPageParam(titles=[schema_title])).pages[0]
        if not page.exists:
            print(f"Error: Page {schema_title} does not exist")
            return
        if schema_title.startswith("Category:"):
            schema_str = ""
            if page.get_slot_content("jsonschema"):
                schema_str = json.dumps(page.get_slot_content("jsonschema"))
        else:
            schema_str = page.get_content()
        if (schema_str is None) or (schema_str == ""):
            print(f"Error: Schema {schema_title} does not exist")
            return
        schema = json.loads(
            schema_str.replace("$ref", "dollarref")
        )  # '$' is a special char for root object in jsonpath
        print(f"Fetch {schema_title}")

        jsonpath_expr = parse("$..dollarref")
        for match in jsonpath_expr.find(schema):
            # value = "https://" + self.site._site.host + match.value
            if match.value.startswith("#"):
                continue  # skip self references
            ref_schema_title = match.value.replace("/wiki/", "").split("?")[0]
            ref_schema_name = ref_schema_title.split(":")[-1] + ".json"
            value = ""
            for i in range(0, schema_name.count("/")):
                value += "../"  # created relative path to top-level schema dir
            value += ref_schema_name  # create a reference to a local file
            # keep document-relative jsonpointer if present
            if "#/" in match.value:
                value += "#/" + match.value.split("#/")[-1]
            match.full_path.update_or_create(schema, value)
            # print(f"replace {match.value} with {value}")
            if (
                ref_schema_title != schema_title
            ):  # prevent recursion in case of self references
                self._fetch_schema(
                    OSW._FetchSchemaParam(schema_title=ref_schema_title, root=False)
                )  # resolve references recursive

        model_dir_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "model"
        )  # src/model
        schema_path = os.path.join(model_dir_path, schema_name + ".json")
        os.makedirs(os.path.dirname(schema_path), exist_ok=True)
        with open(schema_path, "w", encoding="utf-8") as f:
            schema_str = json.dumps(schema, ensure_ascii=False, indent=4).replace(
                "dollarref", "$ref"
            )
            # print(schema_str)
            f.write(schema_str)

        # result_model_path = schema_path.replace(".json", ".py")
        result_model_path = os.path.join(model_dir_path, "entity.py")
        temp_model_path = os.path.join(model_dir_path, "temp.py")
        if root:
            exec_name = "datamodel-codegen"
            # default: assume datamodel-codegen is in PATH
            exec_path = exec_name
            if platform.system() == "Windows":
                exec_name += ".exe"
                exec_path = os.path.join(
                    os.path.dirname(os.path.abspath(sys.executable)), exec_name
                )
                if not os.path.isfile(exec_path):
                    exec_path = os.path.join(
                        os.path.dirname(os.path.abspath(sys.executable)),
                        "Scripts",
                        exec_name,
                    )
                if not os.path.isfile(exec_path):
                    print("Error: datamodel-codegen not found")
                    return
            os.system(
                f"{exec_path}  \
                --input {schema_path} \
                --input-file-type jsonschema \
                --output {temp_model_path} \
                --base-class osw.model.static.OswBaseModel \
                --use-default \
                --enum-field-as-literal all \
                --use-title-as-name \
                --use-schema-description \
                --use-field-description \
                --encoding utf-8 \
                --use-double-quotes \
                --collapse-root-models \
                --reuse-model \
            "
            )
            # see https://koxudaxi.github.io/datamodel-code-generator/
            # --base-class OswBaseModel: use a custom base class
            # --custom-template-dir src/model/template_data/
            # --extra-template-data src/model/template_data/extra.json
            # --use-default: Use default value even if a field is required
            # --enum-field-as-literal all: prevent 'value is not a valid enumeration member' errors after schema reloading
            # --use-schema-description: Use schema description to populate class docstring
            # --use-field-description: Use schema description to populate field docstring
            # --use-title-as-name: use titles as class names of models, e. g. for the footer templates
            # --collapse-root-models: Models generated with a root-type field will be merged
            # into the models using that root-type model, e. g. for Entity.statements
            # --reuse-model: Re-use models on the field when a module has the model with the same content

            content = ""
            with open(temp_model_path, "r", encoding="utf-8") as f:
                content = f.read()
            os.remove(temp_model_path)

            content = re.sub(
                r"(UUID = Field\(...)",
                r"UUID = Field(default_factory=uuid4",
                content,
            )  # enable default value for uuid

            if fetchSchemaParam.mode == "replace":
                header = (
                    "from uuid import uuid4\n"
                    "from typing import Type, TypeVar\n"
                    "from osw.model.static import OswBaseModel, Ontology\n"
                    # "from osw.model.static import *\n"
                    "\n"
                )

                content = re.sub(
                    r"(class\s*\S*\s*\(\s*OswBaseModel\s*\)\s*:.*\n)",
                    header + r"\n\n\n\1",
                    content,
                    1,
                )  # add header before first class declaration

                with open(result_model_path, "w", encoding="utf-8") as f:
                    f.write(content)

            if fetchSchemaParam.mode == "append":
                org_content = ""
                with open(result_model_path, "r", encoding="utf-8") as f:
                    org_content = f.read()

                pattern = re.compile(
                    r"class\s*([\S]*)\s*\(\s*\S*\s*\)\s*:.*\n"
                )  # match class definition [\s\S]*(?:[^\S\n]*\n){2,}
                for cls in re.findall(pattern, org_content):
                    print(cls)
                    content = re.sub(
                        r"(class\s*"
                        + cls
                        + r"\s*\(\s*\S*\s*\)\s*:.*\n[\s\S]*?(?:[^\S\n]*\n){3,})",
                        "",
                        content,
                        count=1,
                    )  # replace duplicated classes

                content = re.sub(
                    r"(from __future__ import annotations)", "", content, 1
                )  # remove import statement
                # print(content)
                with open(result_model_path, "a", encoding="utf-8") as f:
                    f.write(content)

            importlib.reload(model)  # reload the updated module
            if not site_cache_state:
                self.site.disable_cache()  # restore original state

    class LoadEntityParam(BaseModel):
        """Param for load_entity()"""

        titles: Union[str, List[str]]
        """The pages titles to load - one or multiple titles (wiki page name) of
        entities"""
        autofetch_schema: Optional[bool] = True
        """If true, load the corresponding schemas /
        categories ad-hoc if not already present"""
        disable_cache: bool = False
        """If true, disable the cache for the loading process"""

        def __init__(self, **data):
            super().__init__(**data)
            if not isinstance(self.titles, list):
                self.titles = [self.titles]

    class LoadEntityResult(BaseModel):
        """Result of load_entity()"""

        entities: Union[model.Entity, List[model.Entity]]
        """The dataclass instance(s)"""

    def load_entity(
        self, entity_title: Union[str, List[str], LoadEntityParam]
    ) -> Union[model.Entity, List[model.Entity], LoadEntityResult]:
        """Loads the entity with the given wiki page name from the OSW instance.
        Creates an instance of the class specified by the "type" attribute, default
        model.Entity. An instance of model.Entity can be cast to any subclass with
        .cast(model.<class>) .

        Parameters
        ----------
        entity_title
            the wiki page name

        Returns
        -------
            the dataclass instance if only a single title is given
            a list of dataclass instances if a list of titles is given
            a LoadEntityResult instance if a LoadEntityParam is given
        """
        if isinstance(entity_title, str):
            param = OSW.LoadEntityParam(titles=[entity_title])
        elif isinstance(entity_title, list):
            param = OSW.LoadEntityParam(titles=entity_title)
        else:
            param = entity_title

        # store original cache state
        cache_state = self.site.get_cache_enabled()
        if param.disable_cache:
            self.site.disable_cache()
        if not cache_state and param.disable_cache:
            # enable cache to speed up loading
            self.site.enable_cache()

        entities = []
        pages = self.site.get_page(WtSite.GetPageParam(titles=param.titles)).pages
        for page in pages:
            entity = None
            schemas = []
            schemas_fetched = True
            jsondata = page.get_slot_content("jsondata")
            if jsondata:
                for category in jsondata["type"]:
                    schema = (
                        self.site.get_page(WtSite.GetPageParam(titles=[category]))
                        .pages[0]
                        .get_slot_content("jsonschema")
                    )
                    schemas.append(schema)
                    # generate model if not already exists
                    cls = schema["title"]
                    if not hasattr(model, cls):
                        if param.autofetch_schema:
                            self.fetch_schema(
                                OSW.FetchSchemaParam(
                                    schema_title=category, mode="append"
                                )
                            )
                    if not hasattr(model, cls):
                        schemas_fetched = False
                        print(
                            f"Error: Model {cls} not found. Schema {category} needs to be fetched first."
                        )
            if not schemas_fetched:
                continue

            if len(schemas) == 0:
                print("Error: no schema defined")

            elif len(schemas) == 1:
                cls = schemas[0]["title"]
                entity: model.Entity = eval(f"model.{cls}(**jsondata)")

            else:
                bases = []
                for schema in schemas:
                    bases.append(eval("model." + schema["title"]))
                cls = create_model("Test", __base__=tuple(bases))
                entity = cls(**jsondata)

            if entity is not None:
                # make sure we do not override existing meta data
                if not hasattr(entity, "meta") or entity.meta is None:
                    entity.meta = model.Meta()
                if (
                    not hasattr(entity.meta, "wiki_page")
                    or entity.meta.wiki_page is None
                ):
                    entity.meta.wiki_page = model.WikiPage()
                entity.meta.wiki_page.namespace = namespace_from_full_title(page.title)
                entity.meta.wiki_page.title = title_from_full_title(page.title)

            entities.append(entity)
        # restore original cache state
        if cache_state:
            self.site.enable_cache()
        else:
            self.site.disable_cache()

        if isinstance(entity_title, str):  # single title
            if len(entities) >= 1:
                return entities[0]
            else:
                return None
        if isinstance(entity_title, list):  # list of titles
            return entities
        if isinstance(entity_title, OSW.LoadEntityParam):  # LoadEntityParam
            return OSW.LoadEntityResult(entities=entities)

    class StoreEntityParam(OswBaseModel):
        entities: Union[OswBaseModel, List[OswBaseModel]]
        namespace: Optional[str]
        parallel: Optional[bool] = None
        meta_category_title: Optional[str] = "Category:Category"
        debug: Optional[bool] = False

        def __init__(self, **data):
            super().__init__(**data)
            if not isinstance(self.entities, list):
                self.entities = [self.entities]
            if len(self.entities) > 5 and self.parallel is None:
                self.parallel = True
            if self.parallel is None:
                self.parallel = False

    def store_entity(
        self, param: Union[StoreEntityParam, OswBaseModel, List[OswBaseModel]]
    ) -> None:
        """stores the given dataclass instance as OSW page by calling BaseModel.json()

        Parameters
        ----------
        param:
            StoreEntityParam, the dataclass instance or a list of instances
        """
        if isinstance(param, model.Entity):
            param = OSW.StoreEntityParam(entities=[param])
        if isinstance(param, list):
            param = OSW.StoreEntityParam(entities=param)
        if not isinstance(param.entities, list):
            param.entities = [param.entities]

        max_index = len(param.entities)

        meta_category = self.site.get_page(
            WtSite.GetPageParam(titles=[param.meta_category_title])
        ).pages[0]
        # ToDo: we have to do this iteratively to support meta categories inheritance
        meta_category_template = meta_category.get_slot_content("schema_template")
        if meta_category_template:
            meta_category_template = compile_handlebars_template(meta_category_template)

        def store_entity_(
            entity: model.Entity, namespace_: str = None, index: int = None
        ) -> None:
            title_ = get_title(entity)
            if namespace_ is None:
                namespace_ = get_namespace(entity)
            if namespace_ is None or title_ is None:
                print("Error: Unsupported entity type")
                return
            entity_title = namespace_ + ":" + title_
            page = self.site.get_page(WtSite.GetPageParam(titles=[entity_title])).pages[
                0
            ]

            jsondata = json.loads(
                entity.json(exclude_none=True)
            )  # use pydantic serialization, skip none values
            page.set_slot_content("jsondata", jsondata)
            page.set_slot_content(
                "header", "{{#invoke:Entity|header}}"
            )  # required for json parsing and header rendering
            page.set_slot_content(
                "footer", "{{#invoke:Entity|footer}}"
            )  # required for footer rendering
            if namespace_ == "Category":
                if meta_category_template:
                    try:
                        schema_str = eval_compiled_handlebars_template(
                            meta_category_template,
                            jsondata,
                            {"_page_title": entity_title},
                        )
                        schema = json.loads(schema_str)
                        page.set_slot_content("jsonschema", schema)
                    except Exception as e:
                        print(
                            f"Schema generation from template failed for {entity}: {e}"
                        )
            page.edit()
            if index is None:
                print(f"Entity stored at '{page.get_url()}'.")
            else:
                print(f"({index + 1}/{max_index}) Entity stored at '{page.get_url()}'.")

        if param.parallel:
            _ = parallelize(
                store_entity_,
                param.entities,
                flush_at_end=param.debug,
                namespace_=param.namespace,
            )
        else:
            _ = [
                store_entity_(e, param.namespace, i)
                for i, e in enumerate(param.entities)
            ]

    class DeleteEntityParam(OswBaseModel):
        entities: Union[OswBaseModel, List[OswBaseModel]]
        comment: Optional[str] = None
        parallel: Optional[bool] = None
        debug: Optional[bool] = False

        def __init__(self, **data):
            super().__init__(**data)
            if not isinstance(self.entities, list):
                self.entities = [self.entities]
            if len(self.entities) > 5 and self.parallel is None:
                self.parallel = True
            if self.parallel is None:
                self.parallel = False

    def delete_entity(
        self, entity: Union[OswBaseModel, DeleteEntityParam], comment: str = None
    ):
        """Deletes the given entity/entities from the OSW instance."""
        if not isinstance(entity, OSW.DeleteEntityParam):
            entity = OSW.DeleteEntityParam(entities=entity)
        if comment is not None:
            entity.comment = comment

        def delete_entity_(entity, comment_: str = None):
            """Deletes the given entity from the OSW instance.

            Parameters
            ----------
            entity:
                The dataclass instance to delete
            comment_:
                Command for the change log, by default None
            """
            title_ = None
            namespace_ = None
            if hasattr(entity, "meta") and entity.meta and entity.meta.wiki_page:
                if entity.meta.wiki_page.title:
                    title_ = entity.meta.wiki_page.title
                if entity.meta.wiki_page.namespace:
                    namespace_ = entity.meta.wiki_page.namespace
            if namespace_ is None:
                namespace_ = get_namespace(entity)
            if title_ is None:
                title_ = OSW.get_osw_id(entity.uuid)
            if namespace_ is None or title_ is None:
                print("Error: Unsupported entity type")
                return
            entity_title = namespace_ + ":" + title_
            page = self.site.get_page(WtSite.GetPageParam(titles=[entity_title])).pages[
                0
            ]

            if page.exists:
                page.delete(comment_)
                print("Entity deleted: " + page.get_url())
            else:
                print(f"Entity '{entity_title}' does not exist!")

        if entity.parallel:
            _ = parallelize(
                delete_entity_,
                entity.entities,
                flush_at_end=entity.debug,
                comment_=entity.comment,
            )
        else:
            _ = [delete_entity_(e, entity.comment) for e in entity.entities]

    class QueryInstancesParam(OswBaseModel):
        categories: Union[Union[str, OswBaseModel], List[Union[str, OswBaseModel]]]
        parallel: Optional[bool] = None
        debug: Optional[bool] = False
        limit: Optional[int] = 1000
        _category_string_parts: List[Dict[str, str]] = PrivateAttr()
        _titles: List[str] = PrivateAttr()

        @staticmethod
        def get_full_page_name_parts(
            category_: Union[str, OswBaseModel]
        ) -> Dict[str, str]:
            error_msg = (
                f"Category must be a string or a dataclass instance with "
                f"a 'type' attribute. This error occurred on '{str(category_)}'"
            )
            if isinstance(category_, str):
                string_to_split = category_
            elif isinstance(category_, OswBaseModel):
                type_ = getattr(category_, "type", None)
                if type_ is None:
                    raise TypeError(error_msg)
                string_to_split = type_[0]
            else:
                raise TypeError(error_msg)
            if "Category:" not in string_to_split:
                raise TypeError(error_msg)
            return {
                "namespace": string_to_split.split(":")[0],
                "title": string_to_split.split(":")[-1],
            }

        def __init__(self, **data):
            super().__init__(**data)
            if not isinstance(self.categories, list):
                self.categories = [self.categories]
            if len(self.categories) > 5 and self.parallel is None:
                self.parallel = True
            if self.parallel is None:
                self.parallel = False
            self._category_string_parts = [
                OSW.QueryInstancesParam.get_full_page_name_parts(cat)
                for cat in self.categories
            ]
            self._titles = [parts["title"] for parts in self._category_string_parts]

    def query_instances(
        self, category: Union[str, OswBaseModel, OSW.QueryInstancesParam]
    ) -> List[str]:
        if not isinstance(category, OSW.QueryInstancesParam):
            category = OSW.QueryInstancesParam(categories=category)
        page_titles = category._titles
        search_param = SearchParam(
            query=[f"[[HasType::Category:{page_title}]]" for page_title in page_titles],
            **category.dict(
                exclude={"categories", "_category_string_parts", "_titles"}
            ),
        )
        full_page_titles = self.site.semantic_search(search_param)
        return full_page_titles
