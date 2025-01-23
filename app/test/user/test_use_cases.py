from unittest.mock import AsyncMock, Mock

import pytest

from app.core.config.security.services import JWTService, BcryptService
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.entities import SigninUseCaseInput
from app.core.usecase.user.usecases import AuthUseCase


@pytest.fixture
def mock_jwt_service(mocker):
    return mocker.Mock(sepc=JWTService)


@pytest.fixture
def mock_hash_service(mocker):
    return mocker.Mock(spec=BcryptService)


@pytest.fixture
def mock_user_use_case_adapter(mocker):
    return mocker.Mock(spec=UserUseCaseAdapter)


@pytest.fixture
def mock_auth_use_case(mock_jwt_service, mock_user_use_case_adapter, mock_hash_service):
    return AuthUseCase(mock_jwt_service, mock_user_use_case_adapter, mock_hash_service)


class TestSingIn:

    @pytest.mark.asyncio
    async def test_sign_in_when_email_already_exists(self, mock_auth_use_case, mock_user_use_case_adapter):
        # Assign
        sign_in_input = SigninUseCaseInput(username="Twen", email="test@example.com", password="password123")
        mock_user_use_case_adapter.get_user_by_email.return_value = AsyncMock(return_value=Mock())

        # Act
        with pytest.raises(Exception):
            await mock_auth_use_case.sing_in(sign_in_input)

        # Assert
        mock_user_use_case_adapter.get_user_by_email.assert_called_once_with(sign_in_input.email)

    @pytest.mark.asyncio
    async def test_sign_in_creates_new_user(self, mock_auth_use_case, mock_user_use_case_adapter):
        # Assign
        sign_in_input = SigninUseCaseInput(username="Twen", email="test2@example.com", password="password123")
        mock_user_use_case_adapter.get_user_by_email.return_value = None
        mock_user_use_case_adapter.create_user.return_value = True

        # Act
        result = await mock_auth_use_case.sing_in(sign_in_input)

        assert result is True
        mock_user_use_case_adapter.get_user_by_email.assert_called_once_with(sign_in_input.email)
        mock_user_use_case_adapter.create_user.assert_called_once_with(sign_in_input)


class TestLogin:
    @pytest.mark.asyncio
    async def test_log_in_when_user_does_not_exist(self, mock_auth_use_case, mock_user_use_case_adapter):
        # Assign
        email = "test@example.com"
        password = "password123"
        mock_user_use_case_adapter.get_user_by_email.return_value = AsyncMock(return_value=None)

        # Act
        result = await mock_auth_use_case.log_in(email, password)

        # Assert
        assert result.success is False

    @pytest.mark.asyncio
    async def test_log_in_when_user_is_disabled(self, mock_auth_use_case, mock_user_use_case_adapter):
        # Assign
        email = "test@example.com"
        password = "password123"
        user = Mock()
        user.disabled = True
        mock_user_use_case_adapter.get_user_by_email.return_value = user

        # Act
        result = await mock_auth_use_case.log_in(email, password)

        # Assert
        assert result.success is False  # Expect failure when user is disabled

    @pytest.mark.asyncio
    async def test_log_in_with_invalid_password(self, mock_auth_use_case, mock_user_use_case_adapter,
                                                mock_hash_service):
        # Assign
        email = "test@example.com"
        password = "wrong_password"
        user = Mock()
        user.disabled = False
        user.password = "hashed_password"
        mock_user_use_case_adapter.get_user_by_email.return_value = AsyncMock(return_value=user)
        mock_hash_service.verify.return_value = False

        # Act
        result = await mock_auth_use_case.log_in(email, password)

        # Assert
        assert result.success is False

    @pytest.mark.asyncio
    async def test_log_in_success(self, mock_auth_use_case, mock_user_use_case_adapter, mock_hash_service,
                                  mock_jwt_service):
        # Assign
        email = "test@example.com"
        password = "correct_password"
        user = Mock()
        user.disabled = False
        user.password = "hashed_password"
        user.id = 1
        user.username = "testuser"
        mock_user_use_case_adapter.get_user_by_email.return_value = user
        mock_hash_service.verify.return_value = True
        token = "mocked_jwt_token"

        mock_jwt_service.encode.return_value = token

        # Act
        result = await mock_auth_use_case.log_in(email, password)

        # Assert
        assert result.success is True
        assert result.token == token
