import sys
from unittest import TestCase, mock

import boto3
from boto3 import Session
from moto import mock_aws
from mypy_boto3_s3.client import S3Client

from lambda_deploy.layer_manager import (
    create_temp_directory,
    setup_directory_structure,
    copy_directories_to_build,
    install_external_packages,
    zip_layer,
)


class TestLayerManagerMockIntegration(TestCase):
    """
    Lambda Layer Mock Integration
    """

    @property
    def aws_session(self) -> Session:
        return boto3.Session(region_name="us-east-1")

    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()

        self.s3_client: S3Client = self.aws_session.client("s3")
        self.bucket_name = "lambda-deploy-bucket"
        self.s3_client.create_bucket(Bucket=self.bucket_name)

    def tearDown(self):
        self.mock_aws.stop()

    def test_create_temp_directory(self):
        """Test that the temporary directory is created successfully."""
        with mock.patch("os.path.exists", return_value=False), mock.patch(
            "os.makedirs"
        ) as mock_makedirs:
            create_temp_directory("/tmp/test_layer")
            mock_makedirs.assert_called_once_with("/tmp/test_layer")

        # Test cleanup of existing directory
        with mock.patch("os.path.exists", return_value=True), mock.patch(
            "shutil.rmtree"
        ) as mock_rmtree, mock.patch("os.makedirs") as mock_makedirs:
            create_temp_directory("/tmp/test_layer")
            mock_rmtree.assert_called_once_with("/tmp/test_layer")
            mock_makedirs.assert_called_once_with("/tmp/test_layer")

    def test_setup_directory_structure(self):
        """Test directory structure setup within the layer."""
        with mock.patch("os.makedirs") as mock_makedirs:
            result = setup_directory_structure("/tmp/test_layer")
            expected_path = (
                "/tmp/test_layer/python/lib/python3.10/site-packages"
            )
            self.assertEqual(result, expected_path)
            mock_makedirs.assert_called_once_with(expected_path)

    def test_copy_directories_to_build(self):
        """Test copying directories to the build directory."""
        source_dirs = ["/source/dir1", "/source/dir2"]
        target_path = "/target"

        with mock.patch("os.path.exists", return_value=True), mock.patch(
            "shutil.copytree"
        ) as mock_copytree:
            copy_directories_to_build(source_dirs, target_path)
            expected_calls = [
                mock.call("/source/dir1", "/target/dir1"),
                mock.call("/source/dir2", "/target/dir2"),
            ]
            mock_copytree.assert_has_calls(expected_calls, any_order=True)

    def test_install_external_packages(self):
        """Test installation of external packages."""
        packages = ["numpy", "pandas"]
        lib_path = "/lib/path"

        with mock.patch("subprocess.run") as mock_run:
            install_external_packages(packages, lib_path)
            expected_calls = [
                mock.call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "numpy",
                        "-t",
                        lib_path,
                    ],
                    check=True,
                ),
                mock.call(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "pandas",
                        "-t",
                        lib_path,
                    ],
                    check=True,
                ),
            ]
            mock_run.assert_has_calls(expected_calls, any_order=True)

    def test_zip__layer(self):
        """Test zipping and uploading the layer."""
        base_path = "/tmp/lambda_layer"
        zip_path = "/tmp/lambda_layer.zip"

        # Mocking os and shutil functions
        with mock.patch("shutil.make_archive") as mock_make_archive:
            result = zip_layer(base_path, zip_path)
            self.assertEqual(result, zip_path + ".zip")
            mock_make_archive.assert_called_once_with(
                base_name=zip_path.replace(".zip", ""),
                format="zip",
                root_dir=base_path,
            )
