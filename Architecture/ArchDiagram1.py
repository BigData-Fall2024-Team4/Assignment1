from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.azure.storage import BlobStorage
from diagrams.azure.database import SQLDatabases

# Path to your custom icons
icon_path = "/Users/yuga/Downloads/Assignment1/Architecture/"

# Define graph attributes for better spacing between clusters
graph_attr = {
    "splines": "spline",  # Makes the lines between nodes smoother
    "nodesep": "1.0",     # Increase spacing between nodes
    "ranksep": "1.2"      # Increase spacing between ranks/clusters
}

with Diagram("GAIA Dataset Application", show=False, filename="gaia_architecture", direction="LR", graph_attr=graph_attr):
    
    # Load custom icons for missing components like Streamlit and OpenAI
    with Cluster("Streamlit App"):
        streamlit_app = Custom("Streamlit App", icon_path + "streamlit.png")
    
    with Cluster("Open Ai"):
        openai_api = Custom("OpenAI API", icon_path + "openai.png")  # Custom icon for OpenAI
    
    # Dataset Cluster
    with Cluster("Dataset"):
        gaia_node = Custom("GAIA Dataset", icon_path + "gaia.png")
        metadata_node = Custom("Metadata", icon_path + "json.png")

    # Databases Cluster
    with Cluster("Databases"):
        azure_blob_node = BlobStorage("Azure Blob Storage")
        azure_sql_node = SQLDatabases("Azure MSSQL")

    # Architecture Flow
    gaia_node >> azure_blob_node  # GAIA dataset stored in Azure Blob Storage
    metadata_node >> azure_sql_node  # Metadata stored in Azure SQL
    
    streamlit_app >> openai_api  # Streamlit app interacts with OpenAI API
    openai_api >> streamlit_app
    streamlit_app << azure_sql_node  # Streamlit retrieves metadata from Azure SQL

