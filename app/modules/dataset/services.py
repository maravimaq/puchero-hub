import logging
import os
import hashlib
import shutil
import tempfile
from typing import Optional
import uuid
from zipfile import ZipFile
from fpdf import FPDF
import json

from flask import request


from app.modules.auth.services import AuthenticationService
from app.modules.dataset.models import DSViewRecord, DataSet, DSMetaData
from app.modules.dataset.repositories import (
    AuthorRepository,
    DOIMappingRepository,
    DSDownloadRecordRepository,
    DSMetaDataRepository,
    DSViewRecordRepository,
    DataSetRepository
)
from app.modules.featuremodel.repositories import FMMetaDataRepository, FeatureModelRepository
from app.modules.hubfile.repositories import (
    HubfileDownloadRecordRepository,
    HubfileRepository,
    HubfileViewRecordRepository
)
from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)


def calculate_checksum_and_size(file_path):
    file_size = os.path.getsize(file_path)
    with open(file_path, "rb") as file:
        content = file.read()
        hash_md5 = hashlib.md5(content).hexdigest()
        return hash_md5, file_size


def convert_uvl_to_pdf(uvl_file_path: str, pdf_file_path: str):
    try:
        with open(uvl_file_path, 'r') as uvl_file:
            content = uvl_file.read()

        if not content:
            raise ValueError(f"El archivo {uvl_file_path} está vacío.")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, content)

        pdf.output(pdf_file_path)

    except Exception as e:
        print(f"Error al convertir {uvl_file_path} a PDF: {str(e)}")
        

def convert_uvl_to_json(uvl_file_path: str, json_file_path: str):
    try:
        with open(uvl_file_path, 'r') as uvl_file:
            content = uvl_file.read()
        
        if not content:
            raise ValueError(f"El archivo {uvl_file_path} está vacío.")
        
        json_content = {"data": content}

        with open(json_file_path, 'w') as json_file:
            json.dump(json_content, json_file, indent=4)
    
    except Exception as e:
        print(f"Error al convertir {uvl_file_path} a JSON: {str(e)}")


def convert_uvl_to_cnf(uvl_file_path: str, cnf_file_path: str):
    try:
        with open(uvl_file_path, 'r') as uvl_file:
            content = uvl_file.readlines()

        if not content:
            raise ValueError(f"El archivo {uvl_file_path} está vacío.")

        with open(cnf_file_path, 'w') as cnf_file:
            for line in content:
                cnf_file.write(line)

    except Exception as e:
        print(f"Error al convertir {uvl_file_path} a CNF: {str(e)}")


def convert_uvl_to_splx(uvl_file_path: str, splx_file_path: str):
    try:
        with open(uvl_file_path, 'r') as uvl_file:
            content = uvl_file.readlines()

        if not content:
            raise ValueError(f"El archivo {uvl_file_path} está vacío.")

        with open(splx_file_path, 'w') as splx_file:
            for line in content:
                splx_file.write(line)

    except Exception as e:
        print(f"Error al convertir {uvl_file_path} a SPLX: {str(e)}")


def pack_datasets() -> str:
    if not os.path.exists("uploads"):
        return None

    temp_directory = tempfile.mkdtemp()
    archive_name = "datasets_collection.zip"
    full_archive_path = os.path.join(temp_directory, archive_name)

    datasets_found = False

    with ZipFile(full_archive_path, "w") as zip_file:
        user_folders = [folder for folder in os.listdir("uploads") if folder.startswith("user_")]

        if not user_folders:
            return None

        for user_folder in user_folders:
            user_folder_path = os.path.join("uploads", user_folder)

            if os.path.isdir(user_folder_path):
                dataset_folders = [folder for folder in os.listdir(user_folder_path)
                                   if folder.startswith("dataset_")]

                if not dataset_folders:
                    continue

                for dataset_folder in dataset_folders:
                    dataset_folder_path = os.path.join(user_folder_path, dataset_folder)

                    if os.path.isdir(dataset_folder_path):
                        for root, dirs, files in os.walk(dataset_folder_path):
                            for file_name in files:
                                if file_name.endswith('.uvl'):
                                    datasets_found = True
                                    file_path = os.path.join(root, file_name)
                                    relative_path = os.path.relpath(file_path, dataset_folder_path)

                                    uvl_folder_path = os.path.join(dataset_folder, "uvl")
                                    zip_file.write(file_path, arcname=os.path.join(uvl_folder_path, relative_path))

                                    pdf_file_path = file_path.replace('.uvl', '.pdf')
                                    convert_uvl_to_pdf(file_path, pdf_file_path)
                                    if os.path.exists(pdf_file_path):
                                        pdf_folder_path = os.path.join(dataset_folder, "pdf")
                                        zip_file.write(pdf_file_path, arcname=os.path.join(
                                            pdf_folder_path, relative_path.replace('.uvl', '.pdf')))
                                        os.remove(pdf_file_path)

                                    json_file_path = file_path.replace('.uvl', '.json')
                                    convert_uvl_to_json(file_path, json_file_path)
                                    if os.path.exists(json_file_path):
                                        json_folder_path = os.path.join(dataset_folder, "json")
                                        zip_file.write(json_file_path, arcname=os.path.join(
                                            json_folder_path, relative_path.replace('.uvl', '.json')))
                                        os.remove(json_file_path)

                                    cnf_file_path = file_path.replace('.uvl', '.cnf')
                                    convert_uvl_to_cnf(file_path, cnf_file_path)
                                    if os.path.exists(cnf_file_path):
                                        cnf_folder_path = os.path.join(dataset_folder, "cnf")
                                        zip_file.write(cnf_file_path, arcname=os.path.join(
                                            cnf_folder_path, relative_path.replace('.uvl', '.cnf')))
                                        os.remove(cnf_file_path)

                                    splx_file_path = file_path.replace('.uvl', '.splx')
                                    convert_uvl_to_splx(file_path, splx_file_path)
                                    if os.path.exists(splx_file_path):
                                        splx_folder_path = os.path.join(dataset_folder, "splx")
                                        zip_file.write(splx_file_path, arcname=os.path.join(
                                            splx_folder_path, relative_path.replace('.uvl', '.splx')))
                                        os.remove(splx_file_path)

    if not datasets_found:
        return None

    return full_archive_path


class DataSetService(BaseService):
    def __init__(self):
        super().__init__(DataSetRepository())
        self.feature_model_repository = FeatureModelRepository()
        self.author_repository = AuthorRepository()
        self.dsmetadata_repository = DSMetaDataRepository()
        self.fmmetadata_repository = FMMetaDataRepository()
        self.dsdownloadrecord_repository = DSDownloadRecordRepository()
        self.hubfiledownloadrecord_repository = HubfileDownloadRecordRepository()
        self.hubfilerepository = HubfileRepository()
        self.dsviewrecord_repostory = DSViewRecordRepository()
        self.hubfileviewrecord_repository = HubfileViewRecordRepository()

    def move_feature_models(self, dataset: DataSet):
        current_user = AuthenticationService().get_authenticated_user()
        source_dir = current_user.temp_folder()

        working_dir = os.getenv("WORKING_DIR", "")
        dest_dir = os.path.join(working_dir, "uploads", f"user_{current_user.id}", f"dataset_{dataset.id}")

        os.makedirs(dest_dir, exist_ok=True)

        for feature_model in dataset.feature_models:
            uvl_filename = feature_model.fm_meta_data.uvl_filename
            shutil.move(os.path.join(source_dir, uvl_filename), dest_dir)

    def get_synchronized(self, current_user_id: int) -> DataSet:
        return self.repository.get_synchronized(current_user_id)

    def get_unsynchronized(self, current_user_id: int) -> DataSet:
        return self.repository.get_unsynchronized(current_user_id)

    def get_unsynchronized_dataset(self, current_user_id: int, dataset_id: int) -> DataSet:
        return self.repository.get_unsynchronized_dataset(current_user_id, dataset_id)

    def latest_synchronized(self):
        return self.repository.latest_synchronized()

    def count_synchronized_datasets(self):
        return self.repository.count_synchronized_datasets()

    def count_feature_models(self):
        return self.feature_model_service.count_feature_models()

    def count_authors(self) -> int:
        return self.author_repository.count()

    def count_dsmetadata(self) -> int:
        return self.dsmetadata_repository.count()

    def total_dataset_downloads(self) -> int:
        return self.dsdownloadrecord_repository.total_dataset_downloads()

    def total_dataset_views(self) -> int:
        return self.dsviewrecord_repostory.total_dataset_views()

    def create_from_form(self, form, current_user) -> DataSet:
        main_author = {
            "name": f"{current_user.profile.surname}, {current_user.profile.name}",
            "affiliation": current_user.profile.affiliation,
            "orcid": current_user.profile.orcid,
        }
        try:
            logger.info(f"Creating dsmetadata...: {form.get_dsmetadata()}")
            dsmetadata = self.dsmetadata_repository.create(**form.get_dsmetadata())
            for author_data in [main_author] + form.get_authors():
                author = self.author_repository.create(commit=False, ds_meta_data_id=dsmetadata.id, **author_data)
                dsmetadata.authors.append(author)

            dataset = self.create(commit=False, user_id=current_user.id, ds_meta_data_id=dsmetadata.id)

            for feature_model in form.feature_models:
                uvl_filename = feature_model.uvl_filename.data
                fmmetadata = self.fmmetadata_repository.create(commit=False, **feature_model.get_fmmetadata())
                for author_data in feature_model.get_authors():
                    author = self.author_repository.create(commit=False, fm_meta_data_id=fmmetadata.id, **author_data)
                    fmmetadata.authors.append(author)

                fm = self.feature_model_repository.create(
                    commit=False, data_set_id=dataset.id, fm_meta_data_id=fmmetadata.id
                )

                # associated files in feature model
                file_path = os.path.join(current_user.temp_folder(), uvl_filename)
                checksum, size = calculate_checksum_and_size(file_path)

                file = self.hubfilerepository.create(
                    commit=False, name=uvl_filename, checksum=checksum, size=size, feature_model_id=fm.id
                )
                fm.files.append(file)
            self.repository.session.commit()
        except Exception as exc:
            logger.info(f"Exception creating dataset from form...: {exc}")
            self.repository.session.rollback()
            raise exc
        return dataset

    def update_dsmetadata(self, id, **kwargs):
        return self.dsmetadata_repository.update(id, **kwargs)

    def get_uvlhub_doi(self, dataset: DataSet) -> str:
        domain = os.getenv('DOMAIN', 'localhost')
        return f'http://{domain}/doi/{dataset.ds_meta_data.dataset_doi}'

    def pack_datasets(self) -> str:
        temp_directory = tempfile.mkdtemp()
        archive_name = "datasets_collection.zip"
        full_archive_path = os.path.join(temp_directory, archive_name)

        with ZipFile(full_archive_path, "w") as zip_file:
            user_folders = [folder for folder in os.listdir("uploads") if folder.startswith("user_")]

            for user_folder in user_folders:
                user_folder_path = os.path.join("uploads", user_folder)

                if os.path.isdir(user_folder_path):
                    dataset_folders = [folder for folder in os.listdir(user_folder_path)
                                       if folder.startswith("dataset_")]

                    for dataset_folder in dataset_folders:
                        dataset_folder_path = os.path.join(user_folder_path, dataset_folder)

                        if os.path.isdir(dataset_folder_path):
                            for root, dirs, files in os.walk(dataset_folder_path):
                                for file_name in files:
                                    file_path = os.path.join(root, file_name)

                                    if file_name.endswith('.uvl'):
                                        relative_path = os.path.relpath(file_path, dataset_folder_path)

                                        uvl_folder_path = os.path.join(dataset_folder, "uvl")
                                        zip_file.write(file_path, arcname=os.path.join(uvl_folder_path, relative_path))

                                        pdf_file_path = file_path.replace('.uvl', '.pdf')
                                        convert_uvl_to_pdf(file_path, pdf_file_path)
                                    
                                        if os.path.exists(pdf_file_path):
                                            pdf_folder_path = os.path.join(dataset_folder, "pdf")
                                            zip_file.write(pdf_file_path, arcname=os.path.join(
                                                pdf_folder_path, relative_path.replace('.uvl', '.pdf')))
                                            os.remove(pdf_file_path)

                                        json_file_path = file_path.replace('.uvl', '.json')
                                        convert_uvl_to_json(file_path, json_file_path)
                                    
                                        if os.path.exists(json_file_path):
                                            json_folder_path = os.path.join(dataset_folder, "json")
                                            zip_file.write(json_file_path, arcname=os.path.join(
                                                json_folder_path, relative_path.replace('.uvl', '.json')))
                                            os.remove(json_file_path)

                                        cnf_file_path = file_path.replace('.uvl', '.cnf')
                                        convert_uvl_to_cnf(file_path, cnf_file_path)
                                    
                                        if os.path.exists(cnf_file_path):
                                            cnf_folder_path = os.path.join(dataset_folder, "cnf")
                                            zip_file.write(cnf_file_path, arcname=os.path.join
                                                           (cnf_folder_path, relative_path.replace('.uvl', '.cnf')))
                                        os.remove(cnf_file_path)

                                        splx_file_path = file_path.replace('.uvl', '.splx')
                                        convert_uvl_to_splx(file_path, splx_file_path)
                                    
                                        if os.path.exists(splx_file_path):
                                            splx_folder_path = os.path.join(dataset_folder, "splx")
                                            zip_file.write(splx_file_path, arcname=os.path.join(
                                                splx_folder_path, relative_path.replace('.uvl', '.splx')))
                                            os.remove(splx_file_path)

        return full_archive_path
    

class AuthorService(BaseService):
    def __init__(self):
        super().__init__(AuthorRepository())


class DSDownloadRecordService(BaseService):
    def __init__(self):
        super().__init__(DSDownloadRecordRepository())


class DSMetaDataService(BaseService):
    def __init__(self):
        super().__init__(DSMetaDataRepository())

    def update(self, id, **kwargs):
        return self.repository.update(id, **kwargs)

    def filter_by_doi(self, doi: str) -> Optional[DSMetaData]:
        return self.repository.filter_by_doi(doi)


class DSViewRecordService(BaseService):
    def __init__(self):
        super().__init__(DSViewRecordRepository())

    def the_record_exists(self, dataset: DataSet, user_cookie: str):
        return self.repository.the_record_exists(dataset, user_cookie)

    def create_new_record(self, dataset: DataSet,  user_cookie: str) -> DSViewRecord:
        return self.repository.create_new_record(dataset, user_cookie)

    def create_cookie(self, dataset: DataSet) -> str:

        user_cookie = request.cookies.get("view_cookie")
        if not user_cookie:
            user_cookie = str(uuid.uuid4())

        existing_record = self.the_record_exists(dataset=dataset, user_cookie=user_cookie)

        if not existing_record:
            self.create_new_record(dataset=dataset, user_cookie=user_cookie)

        return user_cookie


class DOIMappingService(BaseService):
    def __init__(self):
        super().__init__(DOIMappingRepository())

    def get_new_doi(self, old_doi: str) -> str:
        doi_mapping = self.repository.get_new_doi(old_doi)
        if doi_mapping:
            return doi_mapping.dataset_doi_new
        else:
            return None


class SizeService():

    def __init__(self):
        pass

    def get_human_readable_size(self, size: int) -> str:
        if size < 1024:
            return f'{size} bytes'
        elif size < 1024 ** 2:
            return f'{round(size / 1024, 2)} KB'
        elif size < 1024 ** 3:
            return f'{round(size / (1024 ** 2), 2)} MB'
        else:
            return f'{round(size / (1024 ** 3), 2)} GB'
