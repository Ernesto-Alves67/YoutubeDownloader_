import os
import unittest
from downloader.audio_downloader import AudioDownloader  # Substitua pelo nome do módulo onde AudioDownloader está


class TestAudioDownloaderRealNoUI(unittest.TestCase):
    def setUp(self):
        # Configurações para teste real
        self.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Vídeo curto (~3:30 min, Rick Astley)
        self.output_filename = "test_download.mp3"
        self.temp_dir = "./test_downloads"

        # Limpar diretório de teste se existir
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

        # Criar instância
        self.downloader = AudioDownloader(
            youtube_url=self.youtube_url,
            output_filename=self.output_filename,
            temp_dire=self.temp_dir
        )

    def tearDown(self):
        # Limpar arquivos após teste
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)

    def test_download_real_success(self):
        """Teste real de download - verifica se o arquivo MP3 é criado."""
        print("=== Iniciando teste de download real ===")
        print(f"URL: {self.youtube_url}")
        print(f"Diretório de saída: {self.temp_dir}")
        print(f"Arquivo esperado: {self.output_filename}")

        try:
            # Chamar o método de download
            result = self.downloader.download_and_convert_audio()
            print(f"Resultado retornado: {result}")

            # Verificar se o arquivo foi criado
            output_path = os.path.join(self.temp_dir, self.output_filename)
            self.assertTrue(os.path.exists(output_path), f"Arquivo {output_path} não foi criado!")
            file_size = os.path.getsize(output_path)
            self.assertGreater(file_size, 0, "Arquivo criado está vazio!")
            print(f"Arquivo criado com sucesso! Tamanho: {file_size} bytes")

        except Exception as e:
            print(f"Erro durante o download: {str(e)}")
            import traceback
            traceback.print_exc()
            self.fail(f"Download falhou: {str(e)}")

    def test_download_real_invalid_url(self):
        """Teste real com URL inválida para verificar tratamento de erro."""
        print("=== Iniciando teste com URL inválida ===")
        invalid_url = "https://www.youtube.com/watch?v=invalid_id"
        self.downloader.youtube_url = invalid_url

        try:
            result = self.downloader.download_and_convert_audio()
            print(f"Resultado: {result}")

            # Verificar que retornou erro
            self.assertIn("Erro", result, "Deveria retornar mensagem de erro para URL inválida")
            output_path = os.path.join(self.temp_dir, self.output_filename)
            self.assertFalse(os.path.exists(output_path), "Arquivo não deveria ter sido criado!")
            print("=== Teste de erro concluído! ===")

        except Exception as e:
            print(f"Erro inesperado no teste de falha: {str(e)}")
            self.fail(f"Teste de falha falhou inesperadamente: {str(e)}")


if __name__ == '__main__':
    unittest.main(verbosity=2)