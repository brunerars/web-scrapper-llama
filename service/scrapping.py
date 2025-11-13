import os
from dotenv import load_dotenv
from firecrawl import Firecrawl

load_dotenv()

class ScrappingService:
    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("API Key do Firecrawl não encontrada. Verifique seu arquivo .env")
        
        self.app = Firecrawl(api_key=self.api_key)

    def scrape_website(self, url, collection_name):
        try:
            print(f"🚀 Iniciando crawl simplificado para: {url}")

            # ABORDAGEM SIMPLIFICADA: Confiando nos padrões do Firecrawl
            scraped_data = self.app.crawl(
                url=url,
                limit=15, # Ainda é bom ter um limite
                # Removendo include_paths e exclude_paths para o teste
                scrape_options={
                    "formats": ["markdown"],
                    "onlyMainContent": True
                }
            )       

            if not scraped_data or not hasattr(scraped_data, 'data') or not scraped_data.data:
                raise Exception("O processo de crawl não retornou nenhum dado. O site pode ser protegido ou incompatível com a extração automática.")

            collection_path = f"data/collections/{collection_name}"
            os.makedirs(collection_path, exist_ok=True)

            saved_count = 0
            for i, page in enumerate(scraped_data.data, start=1):
                if hasattr(page, 'markdown') and page.markdown:
                    file_name = f"page_{i}.md"
                    with open(os.path.join(collection_path, file_name), "w", encoding="utf-8") as f:
                        f.write(page.markdown)
                    saved_count += 1
                else:
                    source_url = page.metadata.get('sourceURL', 'desconhecida') if hasattr(page, 'metadata') else 'desconhecida'
                    print(f"⚠️ Página {source_url} ignorada (sem conteúdo markdown).")

            if saved_count == 0:
                 return {"success": False, "error": "Nenhum conteúdo markdown foi extraído das páginas encontradas."}

            return {"success": True, "files": saved_count}

        except Exception as e:
            print(f"❌ Erro durante o crawl: {str(e)}")
            return {"success": False, "error": str(e)}
