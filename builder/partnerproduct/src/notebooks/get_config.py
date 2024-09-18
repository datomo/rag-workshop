import json
import os
import yaml
import getpass

# == True shows a connection sting
check_system = False

chunk_size_web = 5000
chunk_overlap_web = 500

chunk_size_pdf = 6000
chunk_overlap_web = 600


directory_path = '../../../../data'  
_directory_path = '../../../data'

def get_connection_str():
    try:
        connection_string = getpass.getpass(prompt='Enter connection string from MongoDB')
    except Exception as error:
        print('ERROR', error)
    else:
        if connection_string.startswith('mongodb+srv:') and connection_string.endswith('.mongodb.net/'):
            print('Connection string entered correctly.')
            if check_system==True:
                print('Connection string entered:', connection_string)
        else: 
            print('Wrong connection string!')

    return connection_string

def find_pdf_files(directory_from, directory_to ):
    pdf_files = []
    for root, dirs, files in os.walk(directory_from):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(directory_to, file))
    return pdf_files
    
def main():
    connection_string = get_connection_str()
    
    with open('../faculty_of_science_links.json', 'r') as file:
        data_web = json.load(file)

    print("JSON file imported successfully.")

    pdf_files_list = find_pdf_files(directory_path, _directory_path)
    print(f"{len(pdf_files_list)} PDFs imported successfully.")

    data = {
    'ingest':  []
    }

    for rec in data_web['urls']:
        case =  {
            'source': 'web',
            'source_path': rec,
            'chunk_size': chunk_size_web,
            'chunk_overlap': chunk_overlap_web
        }
    
        data['ingest'].append(case)
    
    for rec in pdf_files_list:
        case =  {
            'source': 'pdf',
            'source_path': rec,
            'chunk_size': chunk_size_pdf,
            'chunk_overlap': chunk_overlap_web
        }
    
        data['ingest'].append(case)
    
    
    data_config = {
        "embedding": {
            "class_name": "AdaEmbeddings" # AdaEmbeddings is just a code name for openai embeddings;
            # to change the model go to rag-workshop/src/embeddings/ada-embeddings.ts 
            # now it is 'text-embedding-ada-002', but also can be 'text-embedding-3-small' (cheaper)
            # "class_name": "Nomic-v1.5"  # This line is commented out from the original config
        },
        "vector_store": {
            "connectionString": connection_string,
            "dbName": "chatter",
            "collectionName": "embedded_content",
            "embeddingKey": "embedding",
            "textKey": "text",
            "numCandidates": 150,
            "minScore": 0.4, # min score of vector search: bigger score -> less retrieved docs 
            "vectorSearchIndexName": "vector_index"
        },
        "llms": {
            "class_name": "OpenAI",  # "Fireworks" is commented out
            "model_name": "gpt-4o-mini" , # "'accounts/fireworks/models/mixtral-8x22b-instruct'" is commented out
            "temperature": "",
            "top_p": "",
            "top_k": ""
        }
    }
    
    data.update(data_config)

    with open('../config.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)

    print("YAML file created successfully.")

    return None 


if __name__ == "__main__":
    main()


    
    