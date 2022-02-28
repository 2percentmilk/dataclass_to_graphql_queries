from datetime import datetime
from dataclasses import dataclass
from enums import (
    CalculatedIndex,
    ColorApplied,
    GpsCarrierPhaseStatus,
    SensorType,
)


@dataclass
class Id:
    sentera_id: str


@dataclass
class Pagination:
    page: int
    page_size: int


@dataclass
class User:
    address_1: str
    address_2: str
    city: str
    country_code: str
    email: str
    enterprise_license_agreement: bool
    first_name: str
    last_name: str
    license_type: str  # UserLicense
    organization_maps: dict
    roles: str  # [UserRole]
    sentera_id: Id
    state: str
    status: str  # UserStatus
    zip_code: str


@dataclass
class Image:
    altitude: float
    calculated_index: CalculatedIndex
    camera_make: str
    camera_model: str
    captured_at: datetime
    color_applied: ColorApplied
    content_hash: str
    created_at: datetime
    created_by: User
    download_filename: str
    filename: str
    gps_carrier_phase_status: GpsCarrierPhaseStatus
    gps_horizontal_accuracy: float
    gps_vertical_accuracy: float
    latitude: float
    longitude: float
    orientation: str
    path: str
    pitch: float
    roll: float
    sensor_type: SensorType
    sentera_id: Id
    size: int
    updated_at: datetime
    updated_by: User
    url: str
    yaw: float


@dataclass
class File:
    created_at: datetime
    created_at: User
    download_filename: str
    file_type: str
    filename: str
    path: str
    s3_uri: str
    sentera_id: Id
    size: str
    updated_at: datetime
    updated_by: User
    url: str


@dataclass
class FilesQueryResult:
    total_count: int
    results: [File]
    page: int
    page_size: int


@dataclass
class FeatureSet:
    type: str
    sentera_id: Id
    name: str
    error: str
    files: FilesQueryResult
    status: str
    created_at: datetime


@dataclass
class Mosaic:
    sentera_id: Id
    mosaic_type: str
    quality: str
    s3_uri: str
    name: str
    image_status: bool
    is_from_sentera_sensor: bool
    message: str
    files: FilesQueryResult
    captured_at: datetime
    acres: float


@dataclass
class ImagesQueryResult:
    total_count: int
    results: [Image]
    page: int
    page_size: int


@dataclass
class FeatureSetsQueryResult:
    total_count: int
    results: [FeatureSet]
    page: int
    page_size: int


@dataclass
class MosaicsQueryResult:
    total_count: int
    results: [Mosaic]
    page: int
    page_size: int


@dataclass
class Survey:
    sentera_id: Id
    start_time: datetime
    end_time: datetime
    images: ImagesQueryResult
    mosaics: MosaicsQueryResult
    feature_sets: FeatureSetsQueryResult
    files: FilesQueryResult