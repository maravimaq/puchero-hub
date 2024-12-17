from sqlalchemy import and_, func
from sqlalchemy.sql import select
from app import db
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FeatureModel
# FMMetaData
from app.modules.hubfile.models import Hubfile
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, title="", author="", date_from=None, date_to=None,
               publication_doi="", files_count="", description="", size_from=None,
               size_to=None, publication_type="any",
               sorting="newest", tags=None, **kwargs):
        filters = []
        if title:
            filters.append(DSMetaData.title.ilike(f"%{title}%"))
        if author:
            filters.append(Author.name.ilike(f"%{author}%"))
        if publication_doi:
            filters.append(DSMetaData.dataset_doi.ilike(f"%{publication_doi}%"))
        if date_from:
            filters.append(DataSet.created_at >= date_from)
        if date_to:
            filters.append(DataSet.created_at <= date_to)
        if description:
            filters.append(DSMetaData.description.ilike(f"%{description}%"))
        if tags:
            filters.append(DSMetaData.tags.ilike(f"%{tags}%"))

        # Subconsulta para files_count
        if files_count != "" and files_count is not None and files_count != "0":
            subquery_files_count = (
                select(func.count(FeatureModel.id))
                .where(FeatureModel.data_set_id == DataSet.id)
                .scalar_subquery()
            )
            filters.append(subquery_files_count == int(files_count))

        # Subconsulta para size_from y size_to
        if size_from != "" and size_from is not None and size_from != "0":
            subquery_size_from = (
                select(func.sum(Hubfile.size))
                .join(FeatureModel, FeatureModel.id == Hubfile.feature_model_id)
                .where(FeatureModel.data_set_id == DataSet.id)
                .scalar_subquery()
            )
            filters.append(subquery_size_from / 1024 >= float(size_from))

        if size_to != "" and size_to is not None and size_to != "0":
            subquery_size_to = (
                select(func.sum(Hubfile.size))
                .join(FeatureModel, FeatureModel.id == Hubfile.feature_model_id)
                .where(FeatureModel.data_set_id == DataSet.id)
                .scalar_subquery()
            )
            filters.append(subquery_size_to / 1024 <= float(size_to))

        datasets = (
            db.session.query(DataSet)
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .filter(and_(*filters))
        )

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

#        if tags is not None:
#            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()
