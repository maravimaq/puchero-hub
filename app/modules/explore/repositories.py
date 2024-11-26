from sqlalchemy import any_, and_, func, select
from app import db
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, title="", author="", date_from=None, date_to=None,
               publication_doi="", files_count="", format="", size_from=None, 
               size_to=None, publication_type="any",
               sorting="newest", tags=None, **kwargs):
        # Normalize and remove unwanted characters 

        filters = []
        if title:
            filters.append(DSMetaData.title.ilike(f"%{title}%"))
        if author:
            filters.append(Author.name.ilike(f"%{author}%"))
        if date_from:
            filters.append(DataSet.created_at >= date_from)
        if date_to:
            filters.append(DataSet.created_at <= date_to)
        if publication_doi:
            filters.append(FMMetaData.dataset_doi.ilike(f"%{publication_doi}%"))
        if files_count:
            subquery = (
                select(func.count(FMMetaData.id))
                .where(FMMetaData.id == DataSet.id)
                .scalar_subquery()
            )
            filters.append(subquery == int(files_count))
        if size_from:
            filters.append(DataSet.get_file_total_size() >= float(size_from)*1024)
        if size_to:
            filters.append(DataSet.get_file_total_size() <= float(size_to)*1024)
        if format:
            filters.append(DSMetaData.tags.ilike(f"%{format}%"))

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

        if tags is not None:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        return datasets.all()
