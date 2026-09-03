import os
import re
import urllib.parse
from datetime import datetime, timedelta
import concurrent.futures

class INPEDownloader:
    def __init__(self, output_dir, logger_callback=print, progress_callback=None):
        self.output_dir = output_dir
        self.logger_callback = logger_callback
        self.progress_callback = progress_callback # function that takes (current, total)
        self._cancel_flag = False
        
        # Mapeamento dos formatos para extensões
        self.type_mapping = {
            'SAO': ['.SAO'],
            'RSF': ['.RSF'],
            'DFT': ['.DFT'],
            'SKY': ['.SKY'],
            'DVL': ['.DVL']
        }
        
    def log(self, msg):
        if self.logger_callback:
            self.logger_callback(msg)
            
    def cancel(self):
        self._cancel_flag = True
        
    def date_to_julian(self, date_obj):
        return date_obj.strftime('%j') # Retorna de 001 a 365/366

    def generate_date_range(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    def fetch_file_list(self, station, year, julian_day, allowed_extensions):
        """Faz a raspagem do Apache Directory Listing para encontrar arquivos válidos."""
        base_url = f"https://embracedata.inpe.br/ionosonde/{station}/{year}/{julian_day}/"
        try:
            import requests
            response = requests.get(base_url, timeout=15)
            if response.status_code != 200:
                self.log(f"[*] Sem dados em {station} para {julian_day}/{year}")
                return []
                
            # Extrai os links do HTML 
            links = re.findall(r'href=[\'"]?([^\'" >]+)', response.text)
            
            valid_urls = []
            for link in links:
                if link.startswith('?') or link.startswith('/') or link.startswith('http'):
                    continue 
                
                # Verifica se possui extensão desejada
                for ext in allowed_extensions:
                    if link.upper().endswith(ext.upper()):
                        valid_urls.append(urllib.parse.urljoin(base_url, link))
                        break
            
            return valid_urls
            
        except Exception as e:
            self.log(f"[!] Erro de conexão ao listar {base_url}: {str(e)}")
            return []

    def download_file(self, url, dest_path):
        """Realiza o download em disco com iter_content."""
        if self._cancel_flag:
            return False
            
        try:
            import requests
            response = requests.get(url, stream=True, timeout=20)
            if response.status_code == 200:
                with open(dest_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if self._cancel_flag:
                            return False
                        f.write(chunk)
                return True
            else:
                return False
        except Exception as e:
            self.log(f"[!] Erro de rede ao baixar {url}: {e}")
            return False

    def start_download(self, start_date, end_date, stations, file_types):
        """Orquestrador principal. Roda o crawling sequencial e os downloads em paralelo."""
        self._cancel_flag = False
        
        allowed_extensions = []
        for t in file_types:
            if t in self.type_mapping:
                allowed_extensions.extend(self.type_mapping[t])
                
        if not allowed_extensions:
            self.log("[!] Operação abortada: Nenhum formato selecionado.")
            return

        self.log("="*50)
        self.log("INICIANDO VARREDURA E CRAWLING")
        self.log(f"Estações: {', '.join(stations)}")
        self.log(f"Extensões requisitadas: {', '.join(allowed_extensions)}")
        self.log("="*50)
        
        all_urls_to_download = []
        
        # ETAPA 1: Raspagem rápida de URLs (Varredura)
        for station_code in stations:
            for current_date in self.generate_date_range(start_date, end_date):
                if self._cancel_flag:
                    self.log("[!] Operação cancelada!")
                    return
                    
                year = current_date.strftime('%Y')
                julian_day = self.date_to_julian(current_date)
                
                self.log(f"Checando índice: {station_code} -> Data {current_date.strftime('%d/%m/%Y')} (Dia {julian_day})")
                urls = self.fetch_file_list(station_code, year, julian_day, allowed_extensions)
                
                if urls:
                    for u in urls:
                        all_urls_to_download.append((u, station_code, year, julian_day))
                    
        total_files = len(all_urls_to_download)
        
        if total_files == 0:
            self.log(">> Nenhum arquivo correspondente foi encontrado no servidor para os parâmetros informados.")
            if self.progress_callback:
                self.progress_callback(1, 1)
            return
            
        # Usa um Pool baseado no número de núcleos físicos/lógicos do sistema (excelente para rede)
        cores = os.cpu_count() or 4
        workers = cores * 4
        self.log(f"==> Iniciando extração simultânea ({workers} threads dedicadas para rede)...")
        
        # ETAPA 2: Processamento Paralelo
        downloaded_count = 0
        error_count = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_url = {}
            for url_tuple in all_urls_to_download:
                url, station, year, julian_day = url_tuple
                
                filename = urllib.parse.unquote(url.split('/')[-1])
                day_dir = os.path.join(self.output_dir, station, year, julian_day)
                os.makedirs(day_dir, exist_ok=True)
                dest_path = os.path.join(day_dir, filename)
                
                if os.path.exists(dest_path):
                    self.log(f"[Ignorado - Já Existe] {filename}")
                    downloaded_count += 1
                    if self.progress_callback:
                        self.progress_callback(downloaded_count + error_count, total_files)
                    continue
                
                future = executor.submit(self.download_file, url, dest_path)
                future_to_url[future] = url
            
            # Aguardando resultados do Pool
            for future in concurrent.futures.as_completed(future_to_url):
                if self._cancel_flag:
                    break
                    
                url = future_to_url[future]
                filename = urllib.parse.unquote(url.split('/')[-1])
                try:
                    success = future.result()
                    if success:
                        self.log(f"[BAIXADO OK] {filename}")
                        downloaded_count += 1
                    else:
                        error_count += 1
                except Exception as exc:
                    self.log(f"[ERRO THREAD] Arquivo {filename}: {exc}")
                    error_count += 1
                    
                if self.progress_callback:
                    self.progress_callback(downloaded_count + error_count, total_files)
                    
        if self._cancel_flag:
            self.log("[!] Processo interrompido à força.")
        else:
            self.log("="*50)
            self.log(f"RESUMO: Baixados: {downloaded_count} | Erros: {error_count} | Total Encontrado: {total_files}")
            self.log("="*50)
