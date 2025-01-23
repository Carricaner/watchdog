from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter
from app.core.usecase.object.usecases import ObjectUseCase


@pytest.fixture
def mock_use_case_adapter(mocker):
    return mocker.Mock(spec=ObjectUseCaseAdapter)


@pytest.fixture
def mock_use_case(mock_use_case_adapter):
    return ObjectUseCase(mock_use_case_adapter)


@pytest.fixture
def mock_user(mocker):
    user = mocker.Mock(spec=User)
    user.id = 'CHIIKAWA-2025'
    user.username = 'kurimanjuu'
    user.email = 'kurimanjuu@chiikawa.com'
    user.disabled = False
    user.password = 'ya'
    return user


@pytest.mark.usefixtures("setup_module", "setup_func")
class TestInitializeWatchDogStorage:

    @pytest.mark.asyncio
    async def test_initialize_watchdog_storage_if_lifecycle_policy_exists(self, mock_use_case_adapter,
                                                                          mock_use_case):
        # Arrange
        mock_use_case_adapter.lifecycle_policy_exits = AsyncMock(return_value=True)
        mock_use_case_adapter.update_lifecycle_policy = AsyncMock()

        # Act
        await mock_use_case.initialize_watchdog_storage()

        # Assert
        mock_use_case_adapter.lifecycle_policy_exits.assert_called_once()
        mock_use_case_adapter.update_lifecycle_policy.assert_not_called()

    @pytest.mark.asyncio
    async def test_initialize_watchdog_storage_if_lifecycle_policy_not_exist(self, mock_use_case_adapter,
                                                                             mock_use_case):
        # Arrange
        mock_use_case_adapter.lifecycle_policy_exits = AsyncMock(return_value=False)
        mock_use_case_adapter.update_lifecycle_policy = AsyncMock()

        # Act
        await mock_use_case.initialize_watchdog_storage()

        # Assert
        mock_use_case_adapter.lifecycle_policy_exits.assert_called_once()
        mock_use_case_adapter.update_lifecycle_policy.assert_called_once()


class TestCreateAFile:

    @pytest.mark.asyncio
    async def test_create_a_file(self, mock_use_case_adapter, mock_user, mock_use_case):
        # Arrange
        mock_use_case_adapter.create_a_file = AsyncMock()
        file = Mock(sepc=UploadFile)

        # Act
        await mock_use_case.create_a_file(mock_user, file)

        # Assert
        mock_use_case_adapter.create_a_file.assert_called_once()


class TestGetAllUserFiles:

    @pytest.mark.asyncio
    async def test_get_all_user_files(self, mock_use_case_adapter, mock_user, mock_use_case):
        # Arrange
        expected_files = ['file1.txt', 'file2.txt']
        mock_use_case_adapter.get_all_user_files.return_value = expected_files

        # Act
        result = await mock_use_case.get_all_user_files(mock_user)

        # Assert
        mock_use_case_adapter.get_all_user_files.assert_called_once_with(mock_user)
        assert result == expected_files


class TestCreatePresignedUrl:

    @pytest.mark.asyncio
    async def test_create_presigned_url_with_empty_file_name(self, mock_use_case, mock_user):
        # Arrange
        file = ''

        # Assert
        with pytest.raises(ValueError):
            # Act
            await mock_use_case.create_presigned_url(mock_user, file)

    @pytest.mark.asyncio
    async def test_create_presigned_url_with_nonexistent_file(self, mock_use_case, mock_use_case_adapter):
        # Arrange
        user = Mock(spec=User)
        file_name = 'nonexistent_file.txt'
        mock_use_case_adapter.file_exists.return_value = False

        # Assert
        with pytest.raises(Exception):
            # Act
            await mock_use_case.create_presigned_url(user, file_name)

    @pytest.mark.asyncio
    async def test_create_presigned_url_success(self, mock_use_case, mock_use_case_adapter):
        # Arrange
        user = Mock(spec=User)
        file_name = 'existing_file.txt'
        expiration_in_seconds = 3600
        presigned_url = 'http://example.com/presigned-url'
        mock_use_case_adapter.file_exists.return_value = True
        mock_use_case_adapter.create_presigned_url.return_value = presigned_url

        # Act
        result = await mock_use_case.create_presigned_url(user, file_name, expiration_in_seconds)

        # Assert
        mock_use_case_adapter.file_exists.assert_called_once_with(user, file_name)
        mock_use_case_adapter.create_presigned_url.assert_called_once_with(user, file_name, expiration_in_seconds)
        assert result == presigned_url
