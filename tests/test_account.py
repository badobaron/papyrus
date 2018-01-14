import mock
import pytest

from papyrus.account import (Account,
                             EthereumAccount,
                             BitcoinAccount,
                             )
from bitmerchant.network import BitcoinTestNet, BitcoinMainNet
from ecdsa import SECP256k1

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

class TestEthereumAccountGenerate(object):
    def setup_method(self):
        self.generate_patcher = mock.patch('papyrus.account.SigningKey.generate')
        self.mock_generate = self.generate_patcher.start()

    def teardown_method(self):
        self.generate_patcher.stop()

    def test_generate(self):
        ret_val = EthereumAccount.generate()

        assert ret_val._priv_key == self.mock_generate.return_value
        assert ret_val._pub_key == self.mock_generate.return_value.get_verifying_key.return_value
        self.mock_generate.assert_called_once_with(curve=SECP256k1)
        self.mock_generate.return_value.get_verifying_key.assert_called_once_with()

class TestEthereumAccountPubKey(object):
    def setup_method(self):
        self.deserialize_patcher = mock.patch('papyrus.account.Wallet.deserialize')
        self.mock_deserialize = self.deserialize_patcher.start()

        self.priv_key = mock.MagicMock()
        self.account = EthereumAccount(priv_key=self.priv_key)

    def teardown_method(self):
        self.deserialize_patcher.stop()

    def test_no_pub_key(self):
        expected = self.priv_key.get_verifying_key.return_value.to_string.return_value.hex.return_value
        actual = self.account.pub_key()

        assert expected == actual
        self.priv_key.get_verifying_key.assert_called_once_with()

    def test_pub_key(self):
        self.account._pub_key = mock.MagicMock()
        expected = self.account._pub_key.to_string.return_value.hex.return_value
        actual = self.account.pub_key()

        assert expected == actual
        assert not self.priv_key.get_verifying_key.called

class TestEthereumAccountPrivKey(object):
    def setup_method(self):
        self.priv_key = mock.MagicMock()
        self.pub_key = mock.MagicMock()

    def test_has_private_keys(self):
        account = EthereumAccount(priv_key=self.priv_key)

        expected = self.priv_key.to_string.return_value.hex.return_value
        actual = account.priv_key()

        assert expected == actual

    def test_no_private_keys(self):
        account = EthereumAccount(pub_key=self.pub_key)

        with pytest.raises(ValueError):
            account.priv_key()

class TestEthereumAccountAddress(object):
    def setup_method(self):
        self.keccak_patcher = mock.patch('papyrus.account.sha3.keccak_256')
        self.mock_keccak = self.keccak_patcher.start()
        self.mock_keccak.return_value.hexdigest.return_value = '012345678901234567890123456789'

        self.pub_key = mock.MagicMock()
        self.account = EthereumAccount(pub_key=self.pub_key)

    def teardown_method(self):
        self.keccak_patcher.stop()

    def test_address(self):
        expected = '0x456789'
        actual = self.account.address()

        assert expected == actual

class TestBitcoinAccountGenerate(object):
    def setup_method(self):
        self.new_random_wallet_patcher = mock.patch('papyrus.account.Wallet.new_random_wallet')
        self.mock_new_random_wallet = self.new_random_wallet_patcher.start()

    def teardown_method(self):
        self.new_random_wallet_patcher.stop()

    def test_generate(self):
        account = BitcoinAccount.generate()

        assert account._pub_key == self.mock_new_random_wallet.return_value.get_child.return_value.serialize_b58.return_value
        assert account._priv_key == self.mock_new_random_wallet.return_value.get_child.return_value.serialize_b58.return_value

        self.mock_new_random_wallet.return_value.get_child.return_value.serialize_b58.assert_has_calls([mock.call(private=False), mock.call(private=True)])

class TestBitcoinAccountPubKey(object):
    def setup_method(self):
        self.deserialize_patcher = mock.patch('papyrus.account.Wallet.deserialize')
        self.mock_deserialize = self.deserialize_patcher.start()

        self.priv_key = mock.MagicMock()
        self.account = BitcoinAccount(priv_key=self.priv_key, network=BitcoinTestNet)

    def teardown_method(self):
        self.deserialize_patcher.stop()

    def test_pub_key(self):
        expected = self.mock_deserialize.return_value.serialize_b58.return_value
        actual = self.account.pub_key()

        assert expected == actual
        self.mock_deserialize.assert_called_once_with(self.priv_key, network=BitcoinTestNet)
        self.mock_deserialize.return_value.serialize_b58.assert_called_once_with(private=False)

class TestBitcoinAccountPrivKey(object):
    def setup_method(self):
        self.priv_key = mock.MagicMock()
        self.pub_key = mock.MagicMock()

        self.deserialize_patcher = mock.patch('papyrus.account.Wallet.deserialize')
        self.mock_deserialize = self.deserialize_patcher.start()

    def teardown_method(self):
        self.deserialize_patcher.stop()

    def test_has_private_keys(self):
        account = BitcoinAccount(priv_key=self.priv_key, network=BitcoinTestNet)

        expected = self.mock_deserialize.return_value.export_to_wif.return_value
        actual = account.priv_key()

        assert expected == actual
        self.mock_deserialize.assert_called_once_with(self.priv_key, network=BitcoinTestNet)
        self.mock_deserialize.return_value.export_to_wif.assert_called_once_with()

    def test_no_private_keys(self):
        account = BitcoinAccount(pub_key=self.pub_key, network=BitcoinTestNet)

        with pytest.raises(ValueError):
            account.priv_key()

class TestBitcoinAccountAddress(object):
    def setup_method(self):
        self.deserialize_patcher = mock.patch('papyrus.account.Wallet.deserialize')
        self.mock_deserialize = self.deserialize_patcher.start()

        self.priv_key = mock.MagicMock()
        self.pub_key = mock.MagicMock()

    def teardown_method(self):
        self.deserialize_patcher.stop()

    def test_address_from_pub_key(self):
        account = BitcoinAccount(pub_key=self.pub_key, network=BitcoinTestNet)

        expected = self.mock_deserialize.return_value.to_address.return_value
        actual = account.address()

        assert expected == actual
        self.mock_deserialize.assert_called_once_with(self.pub_key, network=BitcoinTestNet)
        self.mock_deserialize.return_value.to_address.assert_called_once_with()

    def test_address_from_priv_key(self):
        account = BitcoinAccount(priv_key=self.priv_key, network=BitcoinTestNet)

        expected = self.mock_deserialize.return_value.to_address.return_value
        actual = account.address()

        assert expected == actual
        self.mock_deserialize.assert_called_once_with(self.priv_key, network=BitcoinTestNet)
        self.mock_deserialize.return_value.to_address.assert_called_once_with()
