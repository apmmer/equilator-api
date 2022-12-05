from typing import Any, Dict, Optional
from pydantic import BaseModel, conint


class HTTPExceptionModel(BaseModel):
    """
    The basic model for exception response.
    """

    detail: str = 'Details of error.'


class Pagination(BaseModel):
    """
    Pagination default model
    """

    offset: conint(ge=0) = 0
    limit: Optional[conint(ge=1)] = None


class ImprovedBaseModel(BaseModel):
    """
    This class contains improvements for Pydantic's BaseModel
    """

    class Config:
        orm_mode = True

    @classmethod
    def get_field_names(cls, alias=False) -> list:
        return list(cls.schema(alias).get("properties").keys())

    @classmethod
    def _get_docs_schema(
        cls, docs: Dict[str, Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Returns schema of current class,
        which is needed for fastapi docs creation.
        Values for docs should be taken from
        docs (Dict[str, Dict[str, Any]])
        """

        # basic frame
        schema = {
            "type": docs.get("doc_scheme_type", "object"),
            "properties": {},
            "required": []
        }
        # attributes for docs
        attr_names = ['type', 'title', 'description', 'example']
        for field_name in cls.get_field_names():
            if field_name in docs:
                schema["properties"][field_name] = {}
                for attr_name in attr_names:
                    if docs[field_name].get(attr_name, None) is not None:
                        schema["properties"][field_name][attr_name] = (
                            docs[field_name][attr_name]
                        )
                # adding field as 'required'
                if docs[field_name].get("required", None):
                    schema["required"].append(field_name)

        return schema

    @classmethod
    def get_request_body_docs(
        cls,
        docs: Dict[str, Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Returns json-like (Dict) settings,
        used to customize fastapi auto documentation.
        Param <docs>:
            A Dict, containing fields and their description, examples etc.
            example:
                docs = {
                    'model_field_name_1': {
                        "type": "string",
                        "title": "Field 1",
                        "description": "bla bla",
                    },
                    'model_field_name_2': {
                        "type": "datetime",
                        "title": "Field 2",
                        "description": "bla bla",
                    }
                }
        """

        docs = {
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": cls._get_docs_schema(docs=docs)
                    }
                }
            }
        }
        return docs
