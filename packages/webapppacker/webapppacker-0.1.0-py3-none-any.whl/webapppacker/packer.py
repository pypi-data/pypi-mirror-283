import os
import shutil
import subprocess
from .android_manifest import generate_manifest
from .utils import create_directory, zip_directory

class WebAppPacker:
    def __init__(self, app_name, package_name, version_code, version_name):
        self.app_name = app_name
        self.package_name = package_name
        self.version_code = version_code
        self.version_name = version_name
        self.build_dir = 'build'
        self.assets_dir = os.path.join(self.build_dir, 'assets')

    def pack(self, source_dir):
        # Limpar e criar diretórios de construção
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        create_directory(self.build_dir)
        create_directory(self.assets_dir)

        # Copiar arquivos web para assets
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(self.assets_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)

        # Gerar AndroidManifest.xml
        manifest_path = os.path.join(self.build_dir, 'AndroidManifest.xml')
        generate_manifest(manifest_path, self.package_name, self.app_name, self.version_code, self.version_name)

        # Criar APK não assinado
        apk_path = f"{self.app_name}.apk"
        zip_directory(self.build_dir, apk_path)

        print(f"APK não assinado criado: {apk_path}")
        return apk_path

    def sign_apk(self, apk_path, keystore_path, keystore_password, key_alias, key_password):
        # Esta função é um esboço e requer a ferramenta 'apksigner' do Android SDK
        signed_apk = f"{self.app_name}_signed.apk"
        subprocess.run([
            'apksigner', 'sign',
            '--ks', keystore_path,
            '--ks-pass', f'pass:{keystore_password}',
            '--ks-key-alias', key_alias,
            '--key-pass', f'pass:{key_password}',
            '--out', signed_apk,
            apk_path
        ])
        print(f"APK assinado criado: {signed_apk}")
        return signed_apk