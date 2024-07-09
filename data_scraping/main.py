from bs4 import BeautifulSoup
from tqdm import tqdm
import tqdm
import requests
import os

def download_pdfs_peraturan(
        base_url: str,
        query: str,
        save_dir: str
):
    # Raise error if dir does not exists
    if not os.path.exists(save_dir):
        raise Exception(f"Directory {save_dir} does not exists.")
    
    # Download all the pdfs based on the query
    response = requests.get(
        url=base_url,
        params={
            'PeraturanSearch[idglobal]': query
        }
    )
    
    # Raise error if failed to get the file
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve content: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Collect all the pdf links
    pdf_links = soup.find_all(
        'a', 
        href=lambda href: href and href.endswith('.pdf')
    )

    for link in tqdm(pdf_links, mininterval=3):
        try:
            pdf_url = link.get('url')
            if not pdf_url.startswith('http'):
                pdf_url = base_url + pdf_url
        except:
            print("Error: Link cannot be fetched")
            continue

        pdf_name = os.path.join(save_dir, pdf_url.split('/')[-1])
        pdf_response = requests.get(pdf_url)

        if pdf_response.status_code == 200:
            with open(pdf_name, 'wb') as pdf_file:
                try:
                    pdf_file.write(pdf_response.content)
                    print(f"Downloaded file: {pdf_name}")

                except Exception as e:
                    print(f"Unable to write file {pdf_name}: {e}")
                    continue
        else:
            print(f"Failed to download {pdf_url}: {pdf_response.status_code}")
            continue

def main() -> None:
    download_pdfs_peraturan(
        base_url='https://peraturan.go.id/',
        query='pertanian',
        save_dir='query_from_peraturan_go_id_pertanian'
    )

if __name__ == "__main__":
    main()