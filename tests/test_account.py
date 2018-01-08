import mock
import pytest

from papyrus.account import Account

class TestAccountInit(object):
    def setup_method(self):
        self.pub_key = mock.MagicMock()
        self.priv_key = mock.MagicMock()
        self.address = mock.MagicMock()

    def test_invalid(self):
        with pytest.raises(ValueError):
            Account()

    def test_valid(self):
        account = Account(pub_key=self.pub_key,
                          priv_key=self.priv_key,
                          address=self.address)

        assert self.pub_key == account._pub_key
        assert self.priv_key == account._priv_key
        assert self.address == account._address

class TestAccountHasPrivateKeys(object):
    def test_has_private_keys(self):
        account = Account(priv_key=mock.MagicMock())

        assert account.has_private_keys

    def test_has_no_private_keys(self):
        account = Account(pub_key=mock.MagicMock())

        assert not account.has_private_keys

class TestAccountParentMethodsRaise(object):
    def setup_method(self):
        self.account = Account(pub_key=mock.MagicMock(),
                               priv_key=mock.MagicMock(),
                               address=mock.MagicMock())

    def test_pub_key(self):
        with pytest.raises(NotImplementedError):
            self.account.pub_key()

    def test_priv_key(self):
        with pytest.raises(NotImplementedError):
            self.account.priv_key()

    def test_address(self):
        with pytest.raises(NotImplementedError):
            self.account.address()

    def test_generate(self):
        with pytest.raises(NotImplementedError):
            Account.generate()

class TestAccountEncryptedPrivKey(object):
    def setup_method(self):
        self.encrypt_patcher = mock.patch('papyrus.account.encrypt')
        self.mock_encrypt = self.encrypt_patcher.start()

        self.priv_key_patcher = mock.patch('papyrus.account.Account.priv_key')
        self.mock_priv_key = self.priv_key_patcher.start()

        self.account = Account(pub_key=mock.MagicMock(),
                               priv_key=mock.MagicMock(),
                               address=mock.MagicMock())

    def teardown_method(self):
        self.encrypt_patcher.stop()
        self.priv_key_patcher.stop()

    def test_encrypted_priv_key(self):
        expected = self.mock_encrypt.return_value
        actual = self.account.encrypted_priv_key('test_passphrase')

        assert expected == actual
        self.mock_encrypt.assert_called_once_with('test_passphrase',
                                                  self.mock_priv_key.return_value)

